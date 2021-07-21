import django
print(django.__file__)
import rest_framework
print(rest_framework.__file__)
from django.shortcuts import render
from django.http import request, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

PREDICTOR_TASKS = [
    {
        "status": 999,
        "predictor": "archcta_predictor",
        "payload": {
            "task_uid": "1",
            "job_uid": "1",
            "status_code": [],
            "classifier_series": {
                "1": {
                    "type": "CTA",
                    "vol_url": "/home/biomind/.biomind/ifs/PredictorMock/data/arch/Neck_1981785777491291/CP.nii.gz"
                },
            }
        }
    },
    {
        "status": 999,
        "predictor": "headneckcta_predictor",
        "payload": {
            "task_uid": "2",
            "job_uid": "2",
            "status_code": [],
            "classifier_series": {
                "2": {
                    "type": "CTA",
                    "vol_url": "/home/biomind/.biomind/ifs/PredictorMock/data/headneck/R100510321--/CP.nii.gz"
                },
            }
        }
    },
    {
        "status": 999,
        "predictor": "braincta_predictor",
        "payload": {
            "task_uid": "3",
            "job_uid": "3",
            "status_code": [],
            "classifier_series": {
                "3": {
                    "type": "CTA",
                    "vol_url": "/home/biomind/.biomind/ifs/PredictorMock/data/braincta/R100943475--/CP.nii.gz"
                },
            }
        }
    },
    {
        "status": 999,
        "predictor": "corocta_predictor",
        "payload": {
            "task_uid": "4",
            "job_uid": "4",
            "status_code": [],
            "classifier_series": {
                "4": {
                    "type": "CTA",
                    "vol_url": "/home/biomind/.biomind/ifs/PredictorMock/data/corocta/CORONARYARTERY/CP.nii.gz"
                },
            }
        }
    },

    {
        "task_name": "lungct_predictor",
        "job_id": "1",
        "cache_path": "/home/biomind/.ifs/cache/lungct/02f91c98aa6b47cc60a937e477888fcc",
        "vol_file": "/home/liupan/IFS/Data-Repository/lung/02f91c98aa6b47cc60a937e477888fcc/02f91c98aa6b47cc60a937e477888fcc.nii.gz"
    },
    {
        "task_name": "lungct_predictor",
        "job_id": "2",
        "cache_path": "/home/biomind/.ifs/cache/lungct/c1b74d69a42cfd607f4b73567f6674a6",
        "vol_file": "/home/liupan/IFS/Data-Repository/lung/c1b74d69a42cfd607f4b73567f6674a6/c1b74d69a42cfd607f4b73567f6674a6.nii.gz"
    },
    {
        "task_name": "lungct_predictor",
        "job_id": "3",
        "cache_path": "/home/biomind/.ifs/cache/lungct/d358010d3048636768039e0a6c4a2fe2",
        "vol_file": "/home/liupan/IFS/Data-Repository/lung/d358010d3048636768039e0a6c4a2fe2/d358010d3048636768039e0a6c4a2fe2.nii.gz"
    },
    {
        "task_name": "lungct_predictor",
        "job_id": "4",
        "cache_path": "/home/biomind/.ifs/cache/lungct/e2572612383618d794452ada590f4b1a",
        "vol_file": "/home/liupan/IFS/Data-Repository/lung/e2572612383618d794452ada590f4b1a/e2572612383618d794452ada590f4b1a.nii.gz"
    },
    {
        "task_name": "corocta_predictor",
        "job_id": "5",
        "cache_path": "/home/biomind/.ifs/cache/corocta/Neck_1981785777491291",
        "vol_file": "/home/liupan/IFS/Data-Repository/vessel/coronary/CORONARYARTERY/CP.nii.gz"
    },
    {
        "task_name": "headneckcta_predictor",
        "job_id": "6",
        "cache_path": "/home/biomind/.ifs/cache/archcta/Neck_1981785777491291",
        "vol_file": "/home/liupan/IFS/Data-Repository/vessel/headneck/R100510321--/CP.nii.gz"
    },
    {
        "task_name": "headneckcta_predictor",
        "job_id": "7",
        "cache_path": "/home/biomind/.ifs/cache/archcta/Neck_1981785777491291",
        "vol_file": "/home/liupan/IFS/Data-Repository/vessel/headneck/R100943475--/CP.nii.gz"
    },
    {
        "task_name": "headneckcta_predictor",
        "job_id": "8",
        "cache_path": "/home/biomind/.ifs/cache/archcta/Neck_1981785777491291",
        "vol_file": "/home/liupan/IFS/Data-Repository/vessel/headneck/R100976192--/CP.nii.gz"
    },
    {
        "task_name": "headcta_predictor",
        "job_id": "9",
        "cache_path": "/home/biomind/.ifs/cache/archcta/Neck_1981785777491291",
        "vol_file": "/home/liupan/IFS/Data-Repository/vessel/head/R100510321--/CP.nii.gz"
    },
    {
        "task_name": "headcta_predictor",
        "job_id": "10",
        "cache_path": "/home/biomind/.ifs/cache/archcta/Neck_1981785777491291",
        "vol_file": "/home/liupan/IFS/Data-Repository/vessel/head/R100943475--/CP.nii.gz"
    },
    {
        "task_name": "headcta_predictor",
        "job_id": "11",
        "cache_path": "/home/biomind/.ifs/cache/archcta/Neck_1981785777491291",
        "vol_file": "/home/liupan/IFS/Data-Repository/vessel/head/R100976192--/CP.nii.gz"
    },
    {
        "task_name": "archcta_predictor",
        "job_id": "12",
        "cache_path": "/home/biomind/.ifs/cache/archcta/Neck_1981785777491291",
        "vol_file": "/home/liupan/IFS/Data-Repository/vessel/arch/Neck_1981785777491291/CP.nii.gz"
    },

    {
        "task_name": "archcta_predictor",
        "job_id": "13",
        "cache_path": "/home/biomind/.ifs/cache/archcta/R100510321--",
        "vol_file": "/home/liupan/IFS/Data-Repository/vessel/arch/R100510321--/CP.nii.gz"
    },

    {
        "task_name": "archcta_predictor",
        "job_id": "14",
        "cache_path": "/home/biomind/.ifs/cache/archcta/R100943475--",
        "vol_file": "/home/liupan/IFS/Data-Repository/vessel/arch/R100943475--/CP.nii.gz"
    },

    {
        "task_name": "archcta_predictor",
        "job_id": "15",
        "cache_path": "/home/biomind/.ifs/cache/archcta/R100976192--",
        "vol_file": "/home/liupan/IFS/Data-Repository/vessel/arch/R100976192--/CP.nii.gz"
    },

    {
        "task_name": "archcta_predictor",
        "job_id": "64784",
        "cache_path": "Users/chenjiwen/temp/study_uid",
        "t2_vol_file": "/home/biomind/.ifs/PredictorMock/data/arch/Neck_1981785777491291/CP.nii.gz",
        "tc_vol_file": "Users/chenjiwen/temp/study_uid/xxxxx.nii.gz",
        "dwi_vol_file": "Users/chenjiwen/temp/study_uid/xxxxx.nii.gz"
    },
]


@api_view(['GET'])
def get_tasks(request):
    try:
        num = int(request.query_params.get("top", 0))
        if num <= 0:
            num = int(request.data.get("top", 0))

        if num <= 0:
            return Response(data=[], status=status.HTTP_200_OK)

        # return HttpResponse("hello")
        tasks_data = {
            "data": PREDICTOR_TASKS[0:num]
        }
        return Response(data=tasks_data, status=status.HTTP_200_OK)
    except Exception as e:
        print(f"failed to get tasks: {e}")
        return Response(data=None, status=status.HTTP_400_BAD_REQUEST)
