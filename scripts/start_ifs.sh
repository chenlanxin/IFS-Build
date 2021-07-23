#!/bin/bash
set -e

home_dir=/home/biomind
source $home_dir/.profile

# if [ "$(getcap /home/biomind/.biomind/ifs/environment/triton/current/opt/tritonserver/bin/tritonserver | wc -l)" = "0" ]; then
#     sudo setcap cap_ipc_owner=eip /home/biomind/.biomind/ifs/environment/triton/current/opt/tritonserver/bin/tritonserver
# fi

# sudo ldconfig 

# start mock server
echo "### Start mock tasks queue"
cd $home_dir/.biomind/ifs/PredictorMock
python3 manage.py runserver &
sleep 5

# start ifs
echo "### Start IFS server"
ifs-env start

pm2 log predictor --timestamp

