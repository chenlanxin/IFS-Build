import json
import SimpleITK as sitk
import pydicom
import numpy as np
import nibabel as nib
from showImg import show_npy, show_npy_3d
import time
from tqdm import tqdm
from stopwatch import stopwatch
import cv2


def get_series_files(folder):
    reader = sitk.ImageSeriesReader()
    series_uids = reader.GetGDCMSeriesIDs(folder)
    series_uid_to_files = {}
    for series_uid in series_uids:
        file_names = reader.GetGDCMSeriesFileNames(folder, series_uid)
        series_uid_to_files[series_uid] = file_names
    return series_uid_to_files


class SortSeriesFiles():
    '''
        对同一个series的dicom文件进行排序，可得到RAI方向的numpy文件及对应的SimpleITK image
        输入dicom文件的条件：
        1，只能有一个series，即所有dicom文件的SeriesInstanceUID相同
        2，只能有一个volume，即所有dicom文件的ImagePositionPatient不相同
        3，dicom文件必须要的tag值：ImagePositionPatient、ImageOrientationPatient、PixelSpacing
    '''

    def __init__(self, file_names):
        self.series_info = self.generate_series_info_sorted_by_z_postion_asc(
            file_names)
        self.rai_image_info = self.generate_rai_image_info(self.series_info)

    def generate_series_info_sorted_by_z_postion_asc(self, file_names):
        if len(file_names) <= 0:
            raise Exception("no file in the list")

        series_info = {}

        ds = pydicom.dcmread(
            file_names[0],
            force=True,
            stop_before_pixels=True
        )
        series_info["modality"] = str(ds.get('Modality', ''))
        series_info["patient_id"] = str(ds.get('PatientID', ''))
        series_info["patient_name"] = str(ds.get('PatientName', ''))
        series_info["patient_sex"] = str(ds.get('PatientSex', ''))
        series_info["study_instance_uid"] = str(ds.get('StudyInstanceUID', ''))
        series_info["study_date"] = str(ds.get('StudyDate', ''))
        series_info["study_description"] = str(ds.get('StudyDescription', ''))
        series_info["series_instance_uid"] = str(
            ds.get("SeriesInstanceUID", ''))
        series_info["series_description"] = str(
            ds.get('SeriesDescription', ''))
        series_info["series_number"] = str(ds.get('SeriesNumber', ''))
        series_info["columns"] = ds.get("Columns", 0)
        series_info["rows"] = ds.get('Rows', 0)
        window_center = ds.get('WindowCenter', '')
        if type(window_center) == pydicom.multival.MultiValue:
            series_info["window_center"] = list(window_center)
        else:
            series_info["window_center"] = float(window_center)
        window_width = ds.get('WindowWidth', '')
        if pydicom.multival.MultiValue == type(window_width):
            series_info["window_width"] = list(window_width)
        else:
            series_info["window_width"] = float(window_width)
        xy_pixel_spacing = ds.get("PixelSpacing", [1, 1])
        image_orientation_patient = ds.get(
            'ImageOrientationPatient', [1, 0, 0, 0, 1, 0])
        if len(image_orientation_patient) != 6:
            raise Exception("invalid tag ImageOrientationPatient[{0}]".format(
                image_orientation_patient))

        norm_direction = np.cross(
            image_orientation_patient[0:3], image_orientation_patient[3:6])
        if abs(np.dot(norm_direction, [0, 0, 1])) > 0.707:
            x_flipped = 0 if np.dot(image_orientation_patient[0:3], [
                                    1, 0, 0]) > 0.707 else 1  # < 45 degree
            y_flipped = 0 if np.dot(image_orientation_patient[3:6], [
                                    0, 1, 0]) > 0.707 else 1  # < 45 degree
            if np.dot(norm_direction, [0, 0, 1]) < 0:
                norm_direction = [-x for x in norm_direction]
        else:
            x_flipped = 0
            y_flipped = 0

        series_info["image_orientation_patient"] = list(
            image_orientation_patient)
        series_info["x_flipped"] = x_flipped
        series_info["y_flipped"] = y_flipped

        instance_infos = []
        for file_name in file_names:
            ds = pydicom.dcmread(
                file_name,
                force=True,
                stop_before_pixels=True
            )
            series_instance_uid = str(ds.get("SeriesInstanceUID", ''))
            if series_instance_uid != series_info["series_instance_uid"]:
                raise Exception("different SeriesInstanceUID in the list[{0}, {1}]".format(
                    series_instance_uid, series_info["series_instance_uid"]))

            sop_instance_uid = ds.get('SOPInstanceUID', '')
            image_position_patient = list(ds.get("ImagePositionPatient", []))
            if len(image_position_patient) != 3:
                print(
                    "no tag ImageOrientationPatient in file[{0}]".format(file_name))
                continue

            info = {
                "sop_instance_uid": sop_instance_uid,
                "image_position_patient": image_position_patient,
                "file_name": file_name
            }
            instance_infos.append(info)

        def func(f):
            return (np.dot(f.get("image_position_patient", [0, 0, 0]), norm_direction))

        sorted_instance_infos = sorted(instance_infos, key=func, reverse=False)

        z_pixel_spacing = 0
        for i in range(1, len(sorted_instance_infos)):
            z_pixel_spacing = np.linalg.norm(np.array(
                sorted_instance_infos[0]["image_position_patient"]) - np.array(sorted_instance_infos[i]["image_position_patient"]))
            if z_pixel_spacing > 0:
                break
        if z_pixel_spacing <= 0:
            raise Exception(
                "error z pixel spacing [{0}]".format(z_pixel_spacing))

        series_info["pixel_spacing"] = [
            xy_pixel_spacing[0], xy_pixel_spacing[1], z_pixel_spacing]
        series_info["sorted_file_names"] = [
            x.get("file_name", '') for x in sorted_instance_infos]
        series_info["sorted_instance_uids"] = [
            x.get("sop_instance_uid", '') for x in sorted_instance_infos]
        series_info["sorted_image_position_patients"] = [
            x.get("image_position_patient", '') for x in sorted_instance_infos]

        return series_info

    # R: right to left
    # A: anterior to posterior
    # I: inferior to superior
    def generate_rai_image_info(self, series_info):
        spacing = self.series_info.get("pixel_spacing", [1, 1, 1])
        origin_position = self.series_info.get(
            'sorted_image_position_patients', [[0, 0, 0]])[0]
        image_orientation_patient = self.series_info.get(
            "image_orientation_patient", [1, 0, 0, 0, 1, 0])
        cols_mm = self.series_info.get(
            "columns", 0) * self.series_info.get("pixel_spacing", [1, 1, 1])[0]
        rows_mm = self.series_info.get(
            "rows", 0) * self.series_info.get("pixel_spacing", [1, 1, 1])[1]
        if self.series_info.get("x_flipped", 0):
            origin_position = (np.array(
                origin_position) + np.array(image_orientation_patient[0:3]) * cols_mm).tolist()
            image_orientation_patient[0:3] = [-image_orientation_patient[0], -
                                              image_orientation_patient[1], -image_orientation_patient[2]]
        if self.series_info.get("y_flipped", 0):
            origin_position = (np.array(
                origin_position) + np.array(image_orientation_patient[3:6]) * rows_mm).tolist()
            image_orientation_patient[3:6] = [-image_orientation_patient[3], -
                                              image_orientation_patient[4], -image_orientation_patient[5]]
        image_orientation_patient = list(image_orientation_patient) + np.cross(
            image_orientation_patient[0:3], image_orientation_patient[3:6]).tolist()

        rai_image_info = {
            "spacing": spacing,
            "origin": origin_position,
            "direction": np.array(image_orientation_patient).reshape(3, 3).T.flatten().tolist()
        }
        return rai_image_info

    def get_sorted_series_info(self):
        return self.series_info

    def get_sorted_file_list(self):
        return self.series_info.get("sorted_file_names", [])

    def get_sorted_instance_uids(self):
        return self.series_info.get("sorted_instance_uids", [])

    def get_rai_image_info(self):
        return self.rai_image_info

    def get_numpy_data_rai(self):
        sorted_file_names = self.series_info.get("sorted_file_names", [])
        if len(sorted_file_names) <= 0:
            raise Exception('no sorted files')
        reader = sitk.ImageSeriesReader()
        reader.SetFileNames(sorted_file_names)
        img = reader.Execute()
        npd = sitk.GetArrayFromImage(img)
        if self.series_info.get("x_flipped", 0):
            npd = np.flip(npd, axis=2)
        if self.series_info.get("y_flipped", 0):
            npd = np.flip(npd, axis=1)
        # show_npy_3d(npd, 1)
        return npd

    def get_img_sitk(self):
        npd = self.get_numpy_data_rai()
        img = sitk.GetImageFromArray(npd)
        img.SetSpacing(self.rai_image_info.get("spacing", [1, 1, 1]))
        img.SetDirection(self.rai_image_info.get(
            "direction", [1, 0, 0, 0, 1, 0, 0, 0, 1]))
        img.SetOrigin(self.rai_image_info.get("origin", [0, 0, 0]))
        return img

    def save_nii(self, nii_path_name):
        img = self.get_img_sitk()
        sitk.WriteImage(img, nii_path_name)

    def save_json(self, json_path_name):
        with open(json_path_name, "w") as f:
            json.dump(self.series_info, f)
            f.close()


def itk_snap(file_names):
    ds = pydicom.dcmread(file_names[0], force=True, stop_before_pixels=True)
    orient = ds.ImageOrientationPatient
    orient = np.array([float(x) for x in orient]).reshape(2, 3)
    norm = np.cross(orient[0], orient[1])

    def func(f):
        pos = pydicom.dcmread(
            f, force=True, stop_before_pixels=True).ImagePositionPatient
        pos = np.array([float(x) for x in pos])
        return float(np.dot(pos, norm))

    sorted_files = sorted(file_names, key=func)
    reader = sitk.ImageSeriesReader()
    reader.SetFileNames(sorted_files)

    img = reader.Execute()
    # npd = sitk.GetArrayFromImage(img)
    # show_npy_3d(npd, 20)

    str_now = time.strftime("%Y%m%d%H%M%S", time.localtime())
    nii_pathname = '/Users/chenjiwen/temp/itk_{0}.nii.gz'.format(str_now)
    sitk.WriteImage(img, nii_pathname)
    print("itk-snap")


def check_nii_numpy(nii_path_name):
    sw = stopwatch('load nii')
    img = sitk.ReadImage(nii_path_name)
    npd = sitk.GetArrayFromImage(img)
    del sw
    show_npy_3d(npd, 20)


if __name__ == "__main__":

    dicom_folders = [
        '/home/biomind/Desktop/BDRM_CTA_001/CP'
    ]
    
    nii_cache_folder = '/home/biomind/Desktop/temp'

    for dicom_folder in tqdm(dicom_folders):
        series_uid_to_files = get_series_files(dicom_folder)

        for k, v in series_uid_to_files.items():
            if len(v) < 12:
                continue

            str_now = time.strftime("%Y%m%d%H%M%S", time.localtime())
            nii_pathname = f'{nii_cache_folder}/{str_now}.nii'
            json_pathname = f'{nii_cache_folder}/{str_now}.json'
            sw = stopwatch('load dicoms')
            ssf = SortSeriesFiles(v)
            npd = ssf.get_numpy_data_rai()
            del sw
            sw2 = stopwatch('save nii')
            ssf.save_nii(nii_pathname)
            del sw2
            ssf.save_json(json_pathname)
            check_nii_numpy(nii_pathname)

    print("end")
