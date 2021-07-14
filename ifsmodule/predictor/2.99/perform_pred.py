import time
import os
import SimpleITK as sitk
import numpy as np
import requests
import json 
import base64
import zlib

mock_mode = 'off'
queue_host = "https://192.168.2.46"
# queue_host = "http://127.0.0.1:8000"
# queue_host = "http://192.168.2.137:8001"
task_num = 1
get_tasks_url = f"{queue_host}/euler/get_task/{task_num}"
#TODO
post_callback_url = f"{queue_host}/tasks/"

pred_map = {
    'braincta_predictor': 'pred_headcta',
    'headneckcta_predictor': 'pred_hdnkcta',
    'archcta_predictor':     'pred_archcta',
    'corocta_predictor':     'pred_corocta',
    'headcta_predictor':     'pred_headcta',
    'lungct':      'pred_lungct'
}
mode = 'ifstime'
pkg = ''

def nii_img_reader(img_dir, is_normalize=False):
    """

    :param img_dir:
    :param is_normalize:
    :return:5
    """
    img_itk = sitk.ReadImage(img_dir)
    img_np = sitk.GetArrayFromImage(img_itk)
    if is_normalize:
        img_np[img_np > 0] = 1
        img_np[img_np != 1] = 0
    return img_np.astype(np.int16), img_itk

def npy2str(ndarr):
    return base64.b64encode(zlib.compress(ndarr.dumps(), 9)).decode()

def pred_hdnkcta(img_path, job_id, cache_path):
    from ifsag.hdnkcta.ifsr import MainApi
    main_api = MainApi(mode=mode, pkg=pkg)
    print(f'inference server initialted')

    ts = time.time()
    img_arr, sitk_ = nii_img_reader(img_path)
    load_duration = time.time() - ts
    print(f'loaded data shape: {img_arr.shape}')
    print(f'loaded data in {load_duration}s')

    for i in range(1):
        ts = time.time()
        cta_results = main_api.ifsr(cache_path, sitk_, img_arr)
        pred_duration = time.time() - ts            
        print('-' * 100)
        print(f'{i}th operation done in {pred_duration}s')
        print('-' * 100)
    
    # ts = time.time()
    # res_json = {
    #     'mask1': npy2str(cta_results[0]),
    #     'mask2': npy2str(cta_results[1])
    # }
    # if not os.path.exists(cache_path):
    #     os.mkdir(cache_path)
    # res_json_path = os.path.join(cache_path, 'protocol.json')
    # with open(res_json_path, 'w') as f:
    #         json.dump(res_json, f)
    # save_duration = time.time() - ts
    # print(f'save results in {save_duration}s')

    return cta_results, pred_duration

def pred_corocta(img_path, job_id, cache_path):
    from ifsag.corocta.ifsr import MainApi
    main_api = MainApi(mode=mode, pkg=pkg)
    print(f'inference server initialted')

    ts = time.time()
    img_arr, sitk_ = nii_img_reader(img_path)
    load_duration = time.time() - ts
    print(f'loaded data shape: {img_arr.shape}')
    print(f'loaded data in {load_duration}s')

    for i in range(1):
        ts = time.time()
        cta_results = main_api.ifsr(cache_path, sitk_, img_arr)
        pred_duration = time.time() - ts            
        print('-' * 100)
        print(f'{i}th operation done in {pred_duration}s')
        print('-' * 100)

    return cta_results, pred_duration

def pred_headcta(img_path, job_id, cache_path):
    from ifsag.headcta.ifsr import MainApi
    main_api = MainApi(mode=mode, pkg=pkg)
    print(f'inference server initialted')

    ts = time.time()
    img_arr, sitk_ = nii_img_reader(img_path)
    load_duration = time.time() - ts
    print(f'loaded data shape: {img_arr.shape}')
    print(f'loaded data in {load_duration}s')

    for i in range(1):
        ts = time.time()
        cta_results = main_api.ifsr(cache_path, sitk_, img_arr)
        pred_duration = time.time() - ts            
        print('-' * 100)
        print(f'{i}th operation done in {pred_duration}s')
        print('-' * 100)

    return cta_results, pred_duration

def pred_archcta(img_path, job_id, cache_path):
    from ifsag.archcta.ifsr import MainApi
    main_api = MainApi(mode=mode, pkg=pkg)
    print(f'inference server initialted')

    ts = time.time()
    img_arr, sitk_ = nii_img_reader(img_path)
    load_duration = time.time() - ts
    print(f'loaded data shape: {img_arr.shape}')
    print(f'loaded data in {load_duration}s')

    for i in range(1):
        ts = time.time()
        cta_results = main_api.ifsr(cache_path, sitk_, img_arr)
        pred_duration = time.time() - ts            
        print('-' * 100)
        print(f'{i}th operation done in {pred_duration}s')
        print('-' * 100)
    print(f"task jobid[{job_id}] done, check cache path [{cache_path}]")

    return cta_results, pred_duration

def pred_lungct(img_path, job_id, cache_path):
    from ifscc.lung.ifsr import MainApi
    main_api = MainApi(mode=mode, pkg=pkg)
    print(f'inference server initialted')

    ts = time.time()
    img_arr, sitk_ = nii_img_reader(img_path)
    load_duration = time.time() - ts
    print(f'loaded data shape: {img_arr.shape}')
    print(f'loaded data in {load_duration}s')

    for i in range(1):
        ts = time.time()
        lung_results = main_api.ifsr(sitk_, img_arr, "")
        pred_duration = time.time() - ts            
        print('-' * 100)
        print(f'{i}th operation done in {pred_duration}s')
        print('-' * 100)

    return lung_results, pred_duration

def get_tasks(get_tasks_url):
    try:
        # import urllib3
        # urllib3.disable_warnings()
        resp = requests.get(get_tasks_url, verify=False)
        if resp.status_code == 200:
            res = resp.json()
            tasks = res['data']
            return tasks
        else:
            print(f"failed to GET {get_tasks_url}: {resp.status_code}")
            return []
    except Exception as e:
        print(f"failed to GET {get_tasks_url}: {e}")
        return []

def get_mock_tasks():
    try:
        get_tasks_url = f"{queue_host}/tasks/get?num={task_num}"
        resp = requests.get(get_tasks_url)
        if resp.status_code == 200:
            res = resp.json()
            return res
        else:
            print(f"failed to GET {get_tasks_url}: {resp.status_code}")
            return []
    except Exception as e:
        print(f"failed to GET {get_tasks_url}: {e}")
        return []

def download_inputdata(url, task_uid):
    tmp_file = f'/home/biomind/.biomind/ifs/cache/nii/{task_uid}.nii.gz'
    cmd = f'curl {url} -o {tmp_file} -k'
    os.system(cmd)
    return tmp_file

#TODO
def post_callback(post_callback_url):
    pass

def request_annotation(input_data):
    anno_url = "http://localhost:9999/annotation/predict/"
    # res_protocol_path = os.path.join(cache_path, "payload_output.json")
    # input_data = {
    #     "job_uid": job_uid,
    #     'task_uid': task_uid,
    #     'predictor': predictor,
    #     "cache_path": cache_path,
    # }
    res = requests.post(anno_url, data=input_data)
    print(res.status_code)
    print(f"Check {input_data['cache_path']} for result protocols.")

def post_duration_prom(duration_name, task_name, duration):
    prom_url = "http://localhost:9091/metrics/job/predict/instance/machine"
    '''
    duration_job{task_name="archcta"} 65
    duration_pred{task_name="archcta"} 60
    duration_anno{task_name="archcta"} 3
    '''
    duration_record = '''
        %s{task_name="%s"} %s
    ''' %(duration_name, task_name, duration)
    res = requests.post(prom_url, data=duration_record)   
    print(res)

def write_res2csv(csv_path, row_list):
    import csv
    with open(csv_path, 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, dialect='excel')
        writer.writerow(row_list)
  

while mock_mode == 'off':
    tasks = get_tasks(get_tasks_url)
    while len(tasks) == 0:
        time.sleep(1)
        print('No task found.')
        tasks = get_tasks(get_tasks_url)
    for task in tasks:
        try:
            # ['auto', 'config', 'status', 'job_uid', 'task_uid', 'predictor', 'study_uid', 'cache_path', 'status_code', 'classifier_series']
            payload = task['payload']
            ts = time.time()
            predictor = task['predictor']
            job_uid = payload['job_uid']
            task_uid = payload['task_uid']
            cache_path = '/home/biomind/.biomind/ifs/cache/headcta' #payload['cache_path']
            classifier_series = payload['classifier_series']
            vol_files = []
            for k, v in classifier_series.items():
                vol_file = v['vol_url']
                break
            if not os.path.exists(cache_path):
                os.makedirs(cache_path)
            tmp_file = download_inputdata(vol_file, task_uid)
            result, pred_duration = eval(pred_map[predictor])(tmp_file, task_uid, cache_path)
            task_duration = time.time() - ts 
            call_back = {
                'job_uid': job_uid,
                'task_uid': task_uid,
                'predictor': predictor,
                'task_status': 'done',
                'task_duration': task_duration,
                'pred_duration': pred_duration
            }
            print(call_back)
            os.system(f'rm -f {tmp_file}')

            # do annotation
            if 1: # predictor == 'archcta' or predictor == 'headneckcta':
                input_data = {
                    "job_uid": job_uid,
                    'task_uid': task_uid,
                    'predictor': predictor,
                    "cache_path": cache_path,
                }
                ts = time.time()
                request_annotation(input_data)
                anno_duration = time.time() - ts
            else:
                anno_duration = 0

            # post duration to dashboard
            try:
                post_duration_prom('duration_job', predictor, task_duration)
                post_duration_prom('duration_pred', predictor, pred_duration)
                post_duration_prom('duration_anno', predictor, anno_duration)
            except:
                print('No prometheus service found.')
            
            # write duration to csv file
            csv_path = '/home/biomind/.biomind/ifs/cache/durations.csv'
            # from datetime import datetime
            # datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if not os.path.exists(csv_path):
                head_row = [
                    'predictor',
                    'task_uid',
                    'job_uid',
                    'task_duration',
                    'pred_duration',
                    'anno_duration'
                    'vol_file'
                ]
                write_res2csv(csv_path, head_row)
            row_list = [predictor, task_uid, job_uid, task_duration, pred_duration, anno_duration, vol_file]
            write_res2csv(csv_path, row_list)

            #TODO
            # post callback to backend server
        except Exception as e:
            print(f'Error {e}')


while mock_mode == 'on':
    tasks = get_tasks(get_tasks_url)
    while len(tasks) == 0:
        time.sleep(1)
        tasks = get_tasks(get_tasks_url)
    for task in tasks:
        try:
            ts = time.time()
            task_name = task['task_name']
            job_uid = task['job_id']
            cache_path = task['cache_path']
            vol_file = task['vol_file']
            if not os.path.exists(cache_path):
                os.mkdir(cache_path)
                
            result, pred_duration = eval(pred_map[task_name])(vol_file, job_uid, cache_path)
            task_duration = time.time() - ts
            call_back = {
                'jobid': job_uid,
                'job_status': 'done',
                'job_duration': task_duration,
                'pred_duration': pred_duration
            }
            print(call_back)

            # do annotation
            if predictor == 'archcta' or predictor == 'headneckcta':
                input_data = {
                    "job_uid": job_uid,
                    'task_uid': vol_file,
                    'predictor': task_name,
                    "cache_path": cache_path,
                }
                ts = time.time()
                request_annotation(input_data)
                anno_duration = time.time() - ts
            else:
                anno_duration = 0

            # post duration to dashboard
            try:
                post_duration_prom('duration_job', task_name, task_duration)
                post_duration_prom('duration_pred', task_name, pred_duration)
                post_duration_prom('duration_anno', task_name, anno_duration)
            except:
                print('No prometheus service found.')
            
            # write duration to csv file
            csv_path = '/home/biomind/.biomind/ifs/cache/durations_mock.csv'
            # from datetime import datetime
            # datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if not os.path.exists(csv_path):
                head_row = [
                    'predictor',
                    'vol_file',
                    'job_uid',
                    'task_duration',
                    'pred_duration',
                    'anno_duration'
                    'vol_file'
                ]
                write_res2csv(csv_path, head_row)
            row_list = [task_name, vol_file, job_uid, task_duration, pred_duration, anno_duration, vol_file]
            write_res2csv(csv_path, row_list)
            #TODO
            # post callback to backend server
        except Exception as e:
            print(f'Error {e}')