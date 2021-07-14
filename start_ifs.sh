#!/bin/bash
set -e

home_dir=/home/biomind
source $home_dir/.profile

# start mock server
# echo "### Start mock tasks queue"
# cd $home_dir/.ifs/PredictorMock
# python3 manage.py runserver &
# sleep 5

# start ifs
echo "### Start IFS server"
ifs-env start

pm2 log predictor

