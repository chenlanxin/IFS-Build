mode=dev
cur_dir=/home/biomind/Developer/IFS-Build
build_dir=/home/biomind/euler-0.0.0
mkdir -p $build_dir

# # # copy nvidia-driver
# cp -r ./nvidia-driver-installation $build_dir/

# # # build environment
# tar -czvf $build_dir/environment.tgz ./environment

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





