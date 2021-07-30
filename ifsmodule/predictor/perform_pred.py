import time
import os
import SimpleITK as sitk
import numpy as np
import requests
import json 
import base64
import zlib
import json 
from pprint import pprint

with open('/home/biomind/.biomind/ifs/config.json') as j:
    cfg = json.load(j)
pprint(cfg)

queue_hosts = cfg['queue_host']
annotation_host = cfg['annotation_host']
task_num = cfg['task_num']
get_task_endpoint = cfg['get_task_endpoint']
update_task_endpoint = cfg['update_task_endpoint']
get_task_sleep_time = cfg['get_task_sleep_time']
mode = cfg['mode']

pred_map = {
    'braincta_predictor':    'pred_headcta',
    'headneckcta_predictor': 'pred_hdnkcta',
    'archcta_predictor':     'pred_archcta',
    'corocta_predictor':     'pred_corocta',
    'lungct_v2_predictor':      'pred_lungct',
    'cta_predictor':         'pred_generalcta'
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

def pred_generalcta(img_path, job_id, cache_path):
    from pltag.gnelcta.pilt import MainApi
    main_api = MainApi(mode=mode, pkg=pkg)
    print(f'inference server initialted')

    ts = time.time()
    img_arr, sitk_ = nii_img_reader(img_path)
    load_duration = time.time() - ts
    print(f'loaded data shape: {img_arr.shape}')
    print(f'loaded data in {load_duration}s')

    for i in range(1):
        ts = time.time()
        cta_results = main_api.pilt(sitk_, img_arr, cache_path)
        pred_duration = time.time() - ts            
        print('-' * 100)
        print(f'{i}th operation done in {pred_duration}s')
        print('-' * 100)

    return cta_results, pred_duration

def pred_hdnkcta(img_path, job_id, cache_path):
    from pltag.hdnkcta.pilt import MainApi
    main_api = MainApi(mode=mode, pkg=pkg)
    print(f'inference server initialted')

    ts = time.time()
    img_arr, sitk_ = nii_img_reader(img_path)
    load_duration = time.time() - ts
    print(f'loaded data shape: {img_arr.shape}')
    print(f'loaded data in {load_duration}s')

    for i in range(1):
        ts = time.time()
        cta_results = main_api.pilt(sitk_, img_arr, cache_path)
        pred_duration = time.time() - ts            
        print('-' * 100)
        print(f'{i}th operation done in {pred_duration}s')
        print('-' * 100)

    return cta_results, pred_duration

def pred_corocta(img_path, job_id, cache_path):
    from pltag.corocta.pilt import MainApi
    main_api = MainApi(mode=mode, pkg=pkg)
    print(f'inference server initialted')

    ts = time.time()
    img_arr, sitk_ = nii_img_reader(img_path)
    load_duration = time.time() - ts
    print(f'loaded data shape: {img_arr.shape}')
    print(f'loaded data in {load_duration}s')

    for i in range(1):
        ts = time.time()
        cta_results = main_api.pilt(sitk_, img_arr, cache_path)
        pred_duration = time.time() - ts            
        print('-' * 100)
        print(f'{i}th operation done in {pred_duration}s')
        print('-' * 100)

    return cta_results, pred_duration

def pred_headcta(img_path, job_id, cache_path):
    from pltag.headcta.pilt import MainApi
    main_api = MainApi(mode=mode, pkg=pkg)
    print(f'inference server initialted')

    ts = time.time()
    img_arr, sitk_ = nii_img_reader(img_path)
    load_duration = time.time() - ts
    print(f'loaded data shape: {img_arr.shape}')
    print(f'loaded data in {load_duration}s')

    for i in range(1):
        ts = time.time()
        cta_results = main_api.pilt(sitk_, img_arr, cache_path)
        pred_duration = time.time() - ts            
        print('-' * 100)
        print(f'{i}th operation done in {pred_duration}s')
        print('-' * 100)

    return cta_results, pred_duration

def pred_archcta(img_path, job_id, cache_path):
    from pltag.archcta.pilt import MainApi
    main_api = MainApi(mode=mode, pkg=pkg)
    print(f'inference server initialted')

    ts = time.time()
    img_arr, sitk_ = nii_img_reader(img_path)
    load_duration = time.time() - ts
    print(f'loaded data shape: {img_arr.shape}')
    print(f'loaded data in {load_duration}s')

    for i in range(1):
        ts = time.time()
        cta_results = main_api.pilt(sitk_, img_arr, cache_path)
        pred_duration = time.time() - ts            
        print('-' * 100)
        print(f'{i}th operation done in {pred_duration}s')
        print('-' * 100)

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
        lung_results = main_api.ifsr(sitk_, img_arr, cache_path, "")
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


def download_inputdata(url, task_uid, cache_path):
    if url.startswith("http"):
        ts = time.time()
        if not os.path.exists(cache_path):
            os.makedirs(cache_path)
        tmp_file = os.path.join(cache_path, f'{task_uid}.nrrd')
        cmd = f"curl '{url}' -o {tmp_file} -k"
        os.system(cmd)
        print(f"Downloading data takes {time.time() - ts} seconds.")
        return tmp_file
    else:
        return url

def update_task(update_task_url, input):
    try:
        resp = requests.post(update_task_url, json=input, verify=False)
        print(resp.status_code)
        if resp.status_code == 200:
            status = input['status']
            print(f'update task status to {status}.')
        else:
            print(f"failed to POST {update_task_url}: {resp.status_code}")
    except Exception as e:
        print(f"failed to POST {update_task_url}: {e}")

def request_annotation(input_data):
    '''
    input_data = {
        "job_uid": job_uid,
        'task_uid': task_uid,
        'vol_id': vol_id,
        'predictor': predictor,
        "cache_path": cache_path,
        "payload": result
    }
    '''
    anno_url = f"{annotation_host}/annotation/predict/"
    res = requests.post(anno_url, data=input_data)
    print(res.status_code)
    if res.status_code == 201:
        print(f"Check {input_data['cache_path']} for result protocols.")
    else:
        print(f'failed to post annotation. errorcode {res.status_code}')
    return res.json()

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


while 1:
    for queue_host in queue_hosts:
        get_tasks_url = f"{queue_host}{get_task_endpoint}{task_num}"
        update_task_url = f"{queue_host}{update_task_endpoint}"
        print(f'Getting tasks from {get_tasks_url}...')
        tasks = get_tasks(get_tasks_url)
        if len(tasks) == 0:
            #print('No task found.')
            time.sleep(get_task_sleep_time)
            # tasks = get_tasks(get_tasks_url)
            continue
        for task in tasks:
            print('Processing tasks')
            try:
                predictor = task['predictor']
                # get if is mock mode
                mock_flg = 0
                if isinstance(task, dict):
                    if 'status' in list(task.keys()):
                        if task['status'] == 999:
                            mock_flg = 1

                # update task status
                task['status'] = 10
                print(task)
                update_task(update_task_url, task)

                # ['auto', 'config', 'status', 'job_uid', 'task_uid', 'predictor', 'study_uid', 'cache_path', 'status_code', 'classifier_series']
                payload = task['payload']
                ts = time.time()
                job_uid = payload['job_uid']
                task_uid = payload['task_uid']
                classifier_series = payload['classifier_series']
                for k, v in classifier_series.items():
                    if v['type'] == "CTA":
                        vol_id = k
                        vol_file = v['vol_url']
                        break
                    elif v['type'] == "CT_Lung":
                        vol_id = k
                        vol_file = v['vol_url']
                        break
                new_vol_id = vol_id.split('.vol')[0]
                cache_path = f'/home/biomind/.biomind/ifs/cache/{predictor}/{new_vol_id}' 
                if not os.path.exists(cache_path):
                    os.makedirs(cache_path)
                print(f'Predicting {predictor}...')

                tmp_file = download_inputdata(vol_file, task_uid, cache_path)
                print(tmp_file)
                if not os.path.exists(tmp_file):
                    task['status'] = 30
                    error_dict = {
                        "code": "model_vessel_0010",
                        "info": "failed to get nii file",
                        "module": predictor
                    }
                    task['payload']['status_code'].append(error_dict)
                    print(task['payload']['status_code'])
                    update_task(update_task_url, task)
                    continue
                
                # start predicting
                try:
                    result, pred_duration = eval(pred_map[predictor])(tmp_file, task_uid, cache_path)
                except:
                    task['status'] = 30
                    error_dict = {
                        "code": "model_vessel_0011",
                        "info": "failed to predict",
                        "module": predictor
                    }
                    task['payload']['status_code'].append(error_dict)
                    print(task['payload']['status_code'])
                    update_task(update_task_url, task)
                    continue

                # # catch statuscode 
                # if isinstance(result, str):
                #     # update task: error
                #     task['status'] = 30
                #     error_dict = {
                #         "code": result,
                #         "info": "error during prediction",
                #         "module": predictor
                #     }
                #     task['payload']['status_code'].append(error_dict)
                #     print(task['payload']['status_code'])
                #     update_task(update_task_url, task)
                #     continue

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

                # update task: finished
                task['status'] = 20
                task['payload'].update(result[0])
                result_path = os.path.join(cache_path, f'{predictor}_payload_output.json')
                with open(result_path, 'w') as f:
                    json.dump(task, f)
                update_task(update_task_url, task)
                
                # delete nii file if not in mock mode
                if not mock_flg:
                    os.system(f'rm -f {tmp_file}')
                

                # post duration to dashboard
                if mode == 'dev':
                    try:
                        post_duration_prom('duration_job', predictor, task_duration)
                        post_duration_prom('duration_pred', predictor, pred_duration)
                    except:
                        print('No prometheus service found.')
                
                try:
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
                            'vol_file'
                        ]
                        write_res2csv(csv_path, head_row)
                    row_list = [predictor, task_uid, job_uid, task_duration, pred_duration, vol_file]
                    write_res2csv(csv_path, row_list)
                except Exception as e:
                    print(f'failed to write csv file, {e}')

            
            except Exception as e:
                print(f'Error {e}')
                task['status'] = 30
                error_dict = {
                    "code": "model_vessel_0009",
                    "info": "error occurs before prediction",
                    "module": predictor
                }
                task['payload']['status_code'].append(error_dict)
                print(task['payload']['status_code'])
                update_task(update_task_url, task)
    

