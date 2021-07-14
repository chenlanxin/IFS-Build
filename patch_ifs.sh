#!/bin/bash
set -e

./stop_ifs.sh

mode=$1
home_dir=/home/biomind

if [[ $mode == "prod" ]]; then
    if [ -f "./cuda.tgz" ]; then
        echo "### Updating cuda environment..."
        tar -xzvf ./cuda.tgz -C $home_dir/.ifs > /dev/null
        echo ""
    else
        echo "No new cuda to update."
    fi

    if [ -f "./scripts.tgz" ]; then
        echo "### Updating scripts environment..."
        tar -xzvf ./scripts.tgz -C $home_dir/.ifs > /dev/null
        echo ""
    else
        echo "No new scripts to update."
    fi
    if [ -f "./ifsmodule.tgz" ]; then
        echo "### Updating ifsmodule environment..."
        tar -xzvf ./ifsmodule.tgz -C $home_dir/.ifs > /dev/null
        echo ""
    else
        echo "No new ifsmodule to update."
    fi
else
    echo "### Dev mode, updating..."
    if [ -d "./cuda" ]; then
        echo "### Updating cuda environment..."
        cp -rf ./cuda $home_dir/.ifs
        echo ""
    else
        echo "No cuda environment to update."
    fi
    if [ -d "./scripts" ]; then
        echo "### Updating scripts environment..."
        cp -rf ./scripts $home_dir/.ifs
        echo ""
    else
        echo "No scripts environment to update."
    fi
    if [ -d "./ifsmodule" ]; then
        echo "### Updating ifsmodule environment..."
        cp -rf ./ifsmodule $home_dir/.ifs
        echo ""
    else
        echo "No ifsmodule environment to update."
    fi
fi
echo ""


source $home_dir/.profile

# start mock server
echo "### Start mock tasks queue"
cd $home_dir/.ifs/PredictorMock
python3 manage.py runserver &

sleep 5

# start ifs
echo "### Start IFS server"
ifs-env start

pm2 log predictor