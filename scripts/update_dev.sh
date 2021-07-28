cur_dir=/home/biomind/Developer/IFS-Build
home_dir=/home/biomind/.biomind/ifs
model_home=$home_dir/models/current
annotation_home=$home_dir/ifsmodule/annotation/current
mlmodule_home=$home_dir/ifsmodule/mlmodule/current
predictor_home=$home_dir/ifsmodule/predictor/current
scripts_home=$home_dir/ifsmodule/scripts
deps_dir=$cur_dir/deps


new_predictor=true
new_scripts=true

new_model=false
new_model_path=.

new_ifsag=false
declare -A ifsag
ifsag=(
    [repo_name]="IFS-Angiography" 
    [repo_url]="git@github.com:WingsOfPanda/IFS-Angiography.git"
    [remote_name]="origin" 
    [branch]="main"   
)  

new_ifsutils=false
declare -A ifsutils
ifsutils=(
    [repo_name]="IFS-Utils" 
    [repo_url]="git@github.com:WingsOfPanda/IFS-Utils.git"
    [remote_name]="origin" 
    [branch]="main"   
)  

new_annotation=false
declare -A annotation
annotation=(
    [repo_name]="IFS-Annotation"
    [repo_url]="git@github.com:WingsOfPanda/IFS-Annotation.git"
    [remote_name]="origin" 
    [branch]="1.0"   
)  


# git_modules=(${!ifsag[*]} ${!ifsutils[*]} ${!annotation[*]})
# git_values=(${ifsag[@]} ${ifsutils[@]} ${annotation[@]})

cd $cur_dir
mkdir -p ifsmodule/mlmodule
mkdir -p ifsmodule/annotation


# update ml models
if [[ $new_model == "true" ]]; then
    echo "Updating models."
    echo "--------------------------------"
    cp -rf $new_model_path/* $model_home
else
    echo "No new models updated."
    echo "--------------------------------"
fi

# update ml module

if [[ $new_ifsag == "true" ]]; then
    echo "Updating IFS-Angiography."
    cd $deps_dir/${ifsag[repo_name]}
    git remote add ${ifsag[remote_name]} ${ifsag[repo_url]}
    git fetch --all --prune
    git checkout -b ${ifsag[branch]}
    git checkout ${ifsag[branch]}
    git reset --hard ${ifsag[remote_name]}/${ifsag[branch]}
    git pull ${ifsag[remote_name]} ${ifsag[branch]}
    rm -rf $mlmodule_home/*ag
    cp -rf *ag $mlmodule_home/
    echo "--------------------------------"
fi

if [[ $new_ifsutils == "true" ]]; then
    echo "Updating IFS-Utils."
    cd $deps_dir/${ifsutils[repo_name]}
    git remote add ${ifsutils[remote_name]} ${ifsutils[repo_url]}
    git fetch --all --prune
    git checkout -b ${ifsutils[branch]}
    git checkout ${ifsutils[branch]}
    git reset --hard ${ifsutils[remote_name]}/${ifsutils[branch]}
    git pull ${ifsutils[remote_name]} ${ifsutils[branch]}
    rm -rf $mlmodule_home/ifsutils
    cp -rf ifsutils $mlmodule_home/
    echo "--------------------------------"
fi

if [[ $new_annotation == "true" ]]; then
    echo "Updating IFS-Annotation."
    cd $deps_dir/${annotation[repo_name]}
    git remote add ${annotation[remote_name]} ${annotation[repo_url]}
    git fetch --all --prune
    git checkout -b ${annotation[branch]}
    git checkout ${annotation[branch]}
    git reset --hard ${annotation[remote_name]}/${annotation[branch]}
    git pull ${annotation[remote_name]} ${annotation[branch]}
    rm -rf $annotation_home/*
    cp -rf * $annotation_home/
    echo "--------------------------------"
fi

if [[ $new_predictor == "true" ]]; then
    echo "Updating predictor."
    rm -rf $predictor_home/*
    cp -rf $cur_dir/ifsmodule/predictor/latest/* $predictor_home/
    echo "--------------------------------"
fi

if [[ $new_scripts == "true" ]]; then
    echo "Updating scripts."
    rm -rf $scripts_home
    cp -rf $cur_dir/ifsmodule/scripts $scripts_home/
    echo "--------------------------------"
fi





