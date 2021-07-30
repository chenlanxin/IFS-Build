#!/bin/bash
set -e

# update root_dir in triton setting
# update model_path in triton setting
# add ml_package in pythonpath
# start triton
# start predictor


home_dir=/home/ifsr/.ifsr
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

######################################################################################
echo "### Checking OS..."
if [[ $(lsb_release -i | grep -o "Ubuntu") != "Ubuntu" ]]; then
    echo "This script is for Ubuntu os."
    exit 1
fi

if [[ $(lsb_release -d | grep -Eo "Ubuntu.+" | awk '{print $2}') != "20.04.2" ]]; then
    echo "Only support Ubuntu 20.04.2 LTS"
    exit 1
fi
######################################################################################


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


# mkdir -p $home_dir/ifs


######################################################################################
# copy config.json
cp -f ./config.json $home_dir/ > /dev/null
######################################################################################


######################################################################################
# install the environment
echo "### Installing ifs environment..."
env_home=$home_dir/environment
if [ -d $env_home ]; then
    sudo rm -rf $env_home
fi
mkdir -p $env_home
tar -xzvf ./environment/cuda.tgz -C $env_home > /dev/null
tar -xzvf ./environment/pip.tgz -C $env_home > /dev/null
tar -xzvf ./environment/pm2.tgz -C $env_home > /dev/null
tar -xzvf ./environment/python.tgz -C $env_home > /dev/null
tar -xzvf ./environment/triton.tgz -C $env_home > /dev/null
######################################################################################


######################################################################################
# install the models
echo "### Installing ifs models..."
model_home=$home_dir/models
if [ -d $model_home ]; then
    sudo rm -rf $model_home
fi
mkdir -p $model_home
tar -xzvf ./models.tgz -C $model_home > /dev/null
######################################################################################


######################################################################################
ifsmodule_home=$home_dir/ifsmodule
if [ -d $ifsmodule_home ]; then
    sudo rm -rf $ifsmodule_home
fi
mkdir -p $ifsmodule_home
if [[ $mode == "prod" ]]; then
    if [ -f "./ifsmodule.tgz" ]; then
        echo "### Installing ifs ifsmodule..."
        tar -xzvf ./ifsmodule.tgz -C $ifsmodule_home > /dev/null
        echo ""
    else
        echo "No ifsmodule to update."
    fi

    cp -f ./config.json $home_dir/ifs > /dev/null
else
    if [ -d "./ifsmodule" ]; then
        echo "### Installing ifs ifsmodule in dev mode..."
        cp -rf ./ifsmodule $ifsmodule_home
        echo ""
    else
        echo "No ifsmodule to update."
    fi

fi
echo ""
######################################################################################


######################################################################################
# create symlink 

######################################################################################


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


source $home_dir/.profile


# # # start mock server
# echo "### Start mock tasks queue"
# mkdir -p $home_dir/ifs/PredictorMock
# if [[ $mode == "prod" ]]; then
#     tar -xzvf ./PredictorMock.tgz -C $home_dir/ifs > /dev/null
# else
#     echo "dev mode, starting mock server..."
#     cp -rf ./PredictorMock/* $home_dir/ifs/PredictorMock
# fi



