mode=dev
version=1.0
cur_dir=/home/biomind/Developer/IFS-Executor
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
tar -czvf $build_dir/environment/pm2.tgz $env_path/pm2
tar -czvf $build_dir/environment/python.tgz $env_path/python
tar -czvf $build_dir/environment/cuda.tgz $env_path/cuda
tar -czvf $build_dir/environment/triton.tgz $env_path/triton


# copy nvidia-driver
cp -r $cur_dir/nvidia-driver-installation $build_dir/


# # # build models
# tar -czvf $build_dir/models.tgz ./models

# # build PredictorMock
# tar -czvf $build_dir/PredictorMock.tgz ./PredictorMock


# cp scripts and instructions
cp $cur_dir/scripts/install_ifs.sh $build_dir/
cp $cur_dir/instructions.txt $build_dir/
cp $cur_dir/config.json $build_dir/


# build ifs modules
ifsmodule_dir=$build_dir/ifsmodule
mkdir -p $ifsmodule_dir
predictor_dir=$ifsmodule_dir/predictor/$version
mkdir -p $predictor_dir
scripts_dir=$ifsmodule_dir/scripts
mkdir -p $scripts_dir
annotation_dir=$ifsmodule_dir/annotation/$version
mkdir -p $annotation_dir
mlmodule_dir=$ifsmodule_dir/mlmodule/$version
mkdir -p $mlmodule_dir

new_ifsag=true
declare -A ifsag
ifsag=(
    [repo_name]="IFS-Angiography" 
    [repo_url]="git@github.com:WingsOfPanda/IFS-Angiography.git"
    [remote_name]="origin" 
    [branch]="main"   
)  
if [[ $new_ifsag == "true" ]]; then
    echo "Updating IFS-Angiography."
    cd $deps_dir/${ifsag[repo_name]}
    git remote add ${ifsag[remote_name]} ${ifsag[repo_url]}
    git fetch --all --prune
    git checkout -b ${ifsag[branch]}
    git checkout ${ifsag[branch]}
    git reset --hard ${ifsag[remote_name]}/${ifsag[branch]}
    git pull ${ifsag[remote_name]} ${ifsag[branch]}
    cp -rf *ag $mlmodule_dir/
    echo "--------------------------------"
fi

new_ifschest=false
declare -A ifschest
ifschest=(
    [repo_name]="IFS-Chest-CT" 
    [repo_url]="git@github.com:WingsOfPanda/IFS-Chest-CT.git"
    [remote_name]="origin" 
    [branch]="main"   
)  
if [[ $new_ifschest == "true" ]]; then
    echo "Updating IFS-Chest-CT."
    cd $deps_dir/${ifschest[repo_name]}
    git remote add ${ifschest[remote_name]} ${ifschest[repo_url]}
    git fetch --all --prune
    git checkout -b ${ifschest[branch]}
    git checkout ${ifschest[branch]}
    git reset --hard ${ifschest[remote_name]}/${ifschest[branch]}
    git pull ${ifschest[remote_name]} ${ifschest[branch]}
    cp -rf *cc $mlmodule_dir/
    echo "--------------------------------"
fi

new_ifsutils=true
declare -A ifsutils
ifsutils=(
    [repo_name]="IFS-Utils" 
    [repo_url]="git@github.com:WingsOfPanda/IFS-Utils.git"
    [remote_name]="origin" 
    [branch]="main"   
)  
if [[ $new_ifsutils == "true" ]]; then
    echo "Updating IFS-Utils."
    cd $deps_dir/${ifsutils[repo_name]}
    git remote add ${ifsutils[remote_name]} ${ifsutils[repo_url]}
    git fetch --all --prune
    git checkout -b ${ifsutils[branch]}
    git checkout ${ifsutils[branch]}
    git reset --hard ${ifsutils[remote_name]}/${ifsutils[branch]}
    git pull ${ifsutils[remote_name]} ${ifsutils[branch]}
    cp -rf ifsutils $mlmodule_dir/
    echo "--------------------------------"
fi

new_annotation=true
declare -A annotation
annotation=(
    [repo_name]="IFS-Annotation"
    [repo_url]="git@github.com:WingsOfPanda/IFS-Annotation.git"
    [remote_name]="origin" 
    [branch]="1.0"   
)  
if [[ $new_annotation == "true" ]]; then
    echo "Updating IFS-Annotation."
    cd $deps_dir/${annotation[repo_name]}
    git remote add ${annotation[remote_name]} ${annotation[repo_url]}
    git fetch --all --prune
    git checkout -b ${annotation[branch]}
    git checkout ${annotation[branch]}
    git reset --hard ${annotation[remote_name]}/${annotation[branch]}
    git pull ${annotation[remote_name]} ${annotation[branch]}
    cp -rf * $annotation_dir/
    echo "--------------------------------"
fi

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
# tar -czvf $build_dir/ifsmodule.tgz ./ifsmodule





