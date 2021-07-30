# == IFSEnv Begin

export IFS_HOME=/home/biomind/.biomind/ifs
export IFS_ENV_PATH=$IFS_HOME/environment
export IFS_MODULE_PATH=$IFS_HOME/ifsmodule
export IFS_VAR_PATH=$IFS_HOME/var
export IFS_LOG_PATH=$IFS_HOME/logs
#PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin

echo ""
echo "Setup inference server environment DEV package..."

dependent=on
if [[ $dependent == "on" ]]; then
    # Pm2
    IFS_PM2_VER=current
    export IFS_PM2_PATH="$IFS_ENV_PATH/pm2/$IFS_PM2_VER"
    export PM2_HOME=$IFS_VAR_PATH/pm2
    if [ -d "$IFS_PM2_PATH" ]; then
        PATH="$IFS_PM2_PATH:$PATH"
        echo "Added $IFS_ENV_PATH/pm2/$IFS_PM2_VER to PATH"
    else
        echo "Missing $IFS_ENV_PATH/pm2/$IFS_PM2_VER"
    fi

    # Python
    IFS_PYTHON_VER=current
    export IFS_PYTHON_PATH="$IFS_ENV_PATH/python/$IFS_PYTHON_VER"
    if [ -d "$IFS_PYTHON_PATH" ]; then
        PATH="$IFS_PYTHON_PATH/bin:$PATH"
        echo "Added $IFS_ENV_PATH/python/$IFS_PYTHON_VER to PATH"
    else
        echo "Missing $IFS_ENV_PATH/python/$IFS_PYTHON_VER"
    fi
fi

# Triton

# pip packages
IFS_PIP_VER=current
export IFS_PIP_PATH="$IFS_ENV_PATH/pip/$IFS_PIP_VER"
if [ -d "$IFS_PIP_PATH" ]; then
    PYTHONPATH="$IFS_PIP_PATH:$PYTHONPATH"
    echo "Added $IFS_ENV_PATH/pip/$IFS_PIP_VER to PATH"
else
    echo "Missing $IFS_ENV_PATH/pip/$IFS_PIP_VER path"
fi

# cuda
IFS_CUDA_VER=current
export IFS_CUDA_PATH="$IFS_ENV_PATH/cuda/$IFS_CUDA_VER"
if [ -d "$IFS_CUDA_PATH" ]; then
    PATH="$IFS_CUDA_PATH/bin:$PATH"
    LD_LIBRARY_PATH="$IFS_CUDA_PATH/lib64:$PATH"
    echo "Added $IFS_ENV_PATH/cuda/$IFS_CUDA_VER to PATH"
else
    echo "Missing $IFS_ENV_PATH/cuda/$IFS_CUDA_VER"
fi

# ml module
IFS_ML_VER=current
export IFS_ML_PATH="$IFS_MODULE_PATH/mlmodule/$IFS_ML_VER"
if [ -d "$IFS_ML_PATH" ]; then
    PYTHONPATH="$IFS_ML_PATH:$PYTHONPATH"
    echo "Added $IFS_MODULE_PATH/mlmodule/$IFS_ML_VER to PATH"
else
    echo "Missing $IFS_MODULE_PATH/mlmodule/$IFS_ML_VER path"
fi

# ml predictor

# Scripts path
export IFS_SCRIPTS_PATH="$IFS_MODULE_PATH/scripts"
if [ -d "$IFS_SCRIPTS_PATH" ]; then
    PATH="$IFS_SCRIPTS_PATH:$PATH"
    echo "Added scripts to PATH"
else
    echo "Missing scripts"
fi

export PATH=$PATH
export PYTHONPATH=$PYTHONPATH
#export LD_LIBRARY_PATH=

export CUDA_DEVICE_ORDER=PCI_BUS_ID 
export CUDA_VISIBLE_DEVICES=0

# export PATH=/home/biomind/lanxin/ifs-build/cuda-11.1/bin:$PATH
# export LD_LIBRARY_PATH=/home/biomind/lanxin/ifs-build/cuda-11.1/lib64:$LD_LIBRARY_PATH
# export C_INCLUDE_PATH=/home/biomind/lanxin/ifs-build/cuda-11.1/include:$C_INCLUDE_PATH
# export CPLUS_INCLUDE_PATH=/home/biomind/lanxin/ifs-build/cuda-11.1/include:$CPLUS_INCLUDE_PATH

echo ""

# == IFSEnv End
