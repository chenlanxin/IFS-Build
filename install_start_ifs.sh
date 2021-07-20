#!/bin/bash
set -e

# update root_dir in triton setting
# update model_path in triton setting
# add ml_package in pythonpath
# start triton
# start predictor

home_dir=/home/biomind/.biomind
mkdir -p $home_dir
mode=$1

# cleanup() {
#     if [[ $TEMP_DIR && -d $TEMP_DIR ]]; then
#         echo "Removing  $TEMP_DIR..."
# 	rm -rf $TEMP_DIR
#     fi
# }

# trap cleanup EXIT

# TEMP_DIR=$(mktemp -d)

echo "### Checking OS..."
if [[ $(lsb_release -i | grep -o "Ubuntu") != "Ubuntu" ]]; then
    echo "This script is for Ubuntu os."
    exit 1
fi

if [[ $(lsb_release -d | grep -Eo "Ubuntu.+" | awk '{print $2}') != "20.04.2" ]]; then
    echo "Only support Ubuntu 20.04.2 LTS"
    exit 1
fi

# echo "Using temp $TEMP_DIR"
# echo ""

# pushd $TEMP_DIR

# echo "### Extracting IFS build packages..."
# cp -r $home_dir/ifs-release .
# echo ""

# sudo chown -R biomind:biomind .

# echo "### Check new apt..."
# dev_pkgs=$(cat $TEMP_DIR/ifs-release/apt/dev-pkgs)
# echo ""

# echo "### Check NVIDIA driver..."
# if [ "$(lspci | grep -i nvidia > /dev/null; echo $?)" -ne 0 ]; then
#     echo "No gpu found. Skip nvidia driver"
#     dev_pkgs=${dev_pkgs/nvidia-driver-465/}
# fi
# echo ""

# echo "### Installing dev apt packages..."
# sudo apt install -y \
#     -o dir::cache=$TEMP_DIR/ifs-release/apt/dev \
#     -o dir::state::lists=$TEMP_DIR/ifs-release/apt/lists \
#     -o dir::etc::sourcelist=$TEMP_DIR/ifs-release/apt/sources.list \
#     $dev_pkgs
# echo ""

# dev_pkgs=$(cat ./apt/dev-pkgs)
# sudo apt install -y -o dir::cache=./apt/dev -o dir::state::lists=./apt/lists -o dir::etc::sourcelist=./apt/sources.list $dev_pkgs


mkdir -p $home_dir/ifs

if [[ $mode == "prod" ]]; then
    if [ -d $home_dir/ifs/environment ]; then
        sudo rm -rf $home_dir/ifs/environment
        mkdir -p $home_dir/ifs/environment
    fi
    if [ -d $home_dir/ifs/ifsmodule ]; then
        sudo rm -rf $home_dir/ifs/ifsmodule
        mkdir -p $home_dir/ifs/ifsmodule
    fi
    if [ -d $home_dir/ifs/models ]; then
        sudo rm -rf $home_dir/ifs/models
        mkdir -p $home_dir/ifs/models
    fi

    if [ -f "./environment.tgz" ]; then
        echo "### Installing ifs environment..."
        tar -xzvf ./environment.tgz -C $home_dir/ifs > /dev/null
        echo ""
    else
        echo "No environment to update."
    fi

    if [ -f "./ifsmodule.tgz" ]; then
        echo "### Installing ifs ifsmodule..."
        tar -xzvf ./ifsmodule.tgz -C $home_dir/ifs > /dev/null
        echo ""
    else
        echo "No ifsmodule to update."
    fi

    if [ -f "./models.tgz" ]; then
        echo "### Installing ifs models..."
        tar -xzvf ./models.tgz -C $home_dir/ifs > /dev/null
        echo ""
    else
        echo "No models to update."
    fi

    cp -f ./config.json $home_dir/ifs > /dev/null
else
    echo "### Dev mode, installing..."
    if [ -d "./environment" ]; then
        echo "### Installing ifs environment..."
        cp -rf ./environment $home_dir/ifs
        echo ""
    else
        echo "No environment to update."
    fi

    if [ -d "./ifsmodule" ]; then
        echo "### Installing ifs ifsmodule..."
        cp -rf ./ifsmodule $home_dir/ifs
        echo ""
    else
        echo "No ifsmodule to update."
    fi

    if [ -d "./models" ]; then
        echo "### Installing ifs models..."
        cp -rf ./models $home_dir/ifs
        echo ""
    else
        echo "No models to update."
    fi

    cp -f ./config.json $home_dir/ifs > /dev/null
fi
echo ""


# ######################################################################################
# echo "### Installing ifs environment..."
# # if [ -d $home_dir/ifs/environment ]; then
# #     sudo rm -rf $home_dir/ifs/environment
# # fi
# # if [ -f "$home_dir/ifs-build/environment.tgz" ]; then
# #     echo "updating new environment..."
# # else
# #     echo "No environment to update."
# # fi

# mkdir -p $home_dir/ifs/environment
# if [[ $mode == "prod" ]]; then
#     tar -xzvf $home_dir/ifs-build/environment.tgz -C $home_dir/ifs > /dev/null
# else
#     echo "dev mode, copying environment..."
#     cp -rf ./environment/* $home_dir/ifs/environment
# fi
# echo ""
# ######################################################################################


# ######################################################################################
# echo "### Installing ifs modules..."
# mkdir -p $home_dir/ifs/ifsmodule
# if [[ $mode == "prod" ]]; then
#     tar -xzvf $home_dir/ifs-build/ifsmodule.tgz -C $home_dir/ifs > /dev/null
# else
#     echo "dev mode, copying ifs modules..."
#     cp -rf ./ifsmodule/* $home_dir/ifs/ifsmodule
# fi
# echo ""
# ######################################################################################


# ######################################################################################
# echo "### Check new models..."
# #dev_models=$(cat $TEMP_DIR/ifs-release/models.tgz)
# echo ""

# echo "### Copy models..."
# mkdir -p $home_dir/ifs/models
# if [[ $mode == "prod" ]]; then
#     tar -xzvf $home_dir/ifs-build/models.tgz -C $home_dir/ifs > /dev/null
# else
#     echo "dev mode, copying models..."
#     cp -rf ./models/* $home_dir/ifs/models
# fi
# echo ""
# ######################################################################################


######################################################################################
echo "### Inject environment profile script..."
if [ -f $home_dir/.profile ]; then
    echo ".profile existed..."
else
    sudo touch $home_dir/.profile
fi
source_profile_inject="source \"$home_dir/ifs/ifsmodule/scripts/profile.sh\""
if [[ $(cat /home/biomind/.profile | grep "$source_profile_inject" | wc -l) == "0" ]]; then
    echo "$source_profile_inject" >> /home/biomind/.profile
    echo "Injected environment script... Please re-login."
else
    echo "Environment script existed..."
fi
echo ""

if [ -f $home_dir/.zshrc ]; then
    echo "### Inject environment .zshrc script..."
    source_profile_inject="source \"$home_dir/ifs/ifsmodule/scripts/profile.sh\""
    if [[ $(cat /home/biomind/.zshrc | grep "$source_profile_inject" | wc -l) == "0" ]]; then
        echo "$source_profile_inject" >> /home/biomind/.zshrc
        echo "Injected environment to zshrc."
    else
        echo "Environment script zshrc existed..."
    fi
    echo ""
fi
######################################################################################

 
echo "### Setup ifs boot"
# $home_dir/ifs/environment/scripts/ifs-env setup-systemd
echo ""
# sudo systemctl start ifs-environment

mkdir -p $home_dir/ifs/cache
chmod a+w -R $home_dir/ifs/cache
mkdir -p $home_dir/ifs/cache/nii
chmod a+w -R $home_dir/ifs/cache/nii


source $home_dir/.profile

# # start mock server
echo "### Start mock tasks queue"
mkdir -p $home_dir/ifs/PredictorMock
if [[ $mode == "prod" ]]; then
    tar -xzvf ./PredictorMock.tgz -C $home_dir/ifs > /dev/null
else
    echo "dev mode, starting mock server..."
    cp -rf ./PredictorMock/* $home_dir/ifs/PredictorMock
fi

./start_ifs.sh 

# cd $home_dir/ifs/PredictorMock
# python3 manage.py runserver &

# sleep 5

# # start ifs
# echo "### Start IFS server"
# ifs-env start

# pm2 log predictor

