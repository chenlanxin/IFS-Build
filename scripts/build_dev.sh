mode=dev
version=1.0
cur_dir=/home/biomind/Developer/IFS-Build
build_dir=/home/biomind/euler-latest
mkdir -p $build_dir

# build environment
mkdir -p $build_dir/environment
env_path=$cur_dir/environment
# cp -rf $env_path/pip $build_dir/environment
# cp -rf $env_path/pm2 $build_dir/environment
# cp -rf $env_path/python $build_dir/environment
# cp -rf $env_path/cuda $build_dir/environment
# cp -rf $env_path/triton $build_dir/environment
tar -czvf $build_dir/environment/pip.tgz $env_path/pip
tar -czvf $build_dir/environment/pm2.tgz $env_path/pip
tar -czvf $build_dir/environment/python.tgz $env_path/pip
tar -czvf $build_dir/environment/cuda.tgz $env_path/pip
tar -czvf $build_dir/environment/triton.tgz $env_path/pip


# copy nvidia-driver
cp -r $cur_dir/nvidia-driver-installation $build_dir/


# # # build models
# tar -czvf $build_dir/models.tgz ./models

# # build PredictorMock
# tar -czvf $build_dir/PredictorMock.tgz ./PredictorMock


# cp scripts and instructions
cp ./install_start_ifs.sh $build_dir/
cp ./start_ifs.sh $build_dir/
cp ./stop_ifs.sh $build_dir/
cp ./instructions.txt $build_dir/
cp ./config.json $build_dir/

# build ifs modules
# # build ml module
# cd $cur_dir/deps/IFS-Angiography
# git pull origin main
# cd $cur_dir/deps/IFS-Utils
# git pull origin main
# cd $cur_dir
# python3 -m pip install ./deps/IFS-Angiography --target=./ifsmodule/mlmodule/1.1/
# python3 -m pip install ./deps/IFS-Utils --target=./ifsmodule/mlmodule/1.1/
# # build annotation server
# cd $cur_dir/deps/IFS-Utils-annotation/annotation_server
# python3 setup.py
# mkdir -p $cur_dir/ifsmodule/annotation
# cp -rf ../build/* $cur_dir/ifsmodule/annotation/
# build predictor
# build scripts
# cd $cur_dir
tar -czvf $build_dir/ifsmodule.tgz ./ifsmodule





