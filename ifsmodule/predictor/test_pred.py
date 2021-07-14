import requests
import os
import time

def post_duration(job_id, task_name, job_duration, pred_duration):
    prom_url = "http://localhost:9091/metrics/job/predict/instance/machine"
    '''
    duration_job{task_name="archcta"} 65
    duration_pred{task_name="archcta"} 60
    '''
    prom_record = {
        'jobid': job_id,
        'task_name': task_name,
        'job_status': 'done',
        'job_duration': job_duration,
        'pred_duration': pred_duration
    }

    job_duration_record = '''
        duration_job{task_name="%s"} %s
    ''' %(task_name, job_duration)
    res = requests.post(prom_url, data=job_duration_record)

    pred_duration_record = '''
        duration_pred{task_name="%s"} %s
    ''' %(task_name, pred_duration)
    res = requests.post(prom_url, data=pred_duration_record)

# post_duration('1', 'archcta', 100, 90)

def write_res2csv(csv_path, row_list):
    import csv
    with open(csv_path, 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, dialect='excel')
        writer.writerow(row_list)
 
csv_path = '/home/biomind/.ifs/cache/durations.csv'
if not os.path.exists(csv_path):
    head_row = [
        'task_name',
        'job_id',
        'job_duration',
        'pred_duration',
        'anno_duration'
        'vol_file'
    ]
    write_res2csv(csv_path, head_row)
row_list = ['archcta', 1, 50, 40, 3, 'test.nii.gz']
write_res2csv(csv_path, row_list)
