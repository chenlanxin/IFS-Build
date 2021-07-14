patch_dir=/home/biomind/ifs-patch
mkdir -p $patch_dir

# build environment
# tar -czvf $patch_dir/cuda.tgz ./environment/cuda
# tar -czvf $patch_dir/ifsmodule.tgz ./ifsmodule
tar -czvf $patch_dir/scripts.tgz ./ifsmodule/scripts

# cp scripts and instructions
cp ./patch_ifs.sh $patch_dir/
cp ./start_ifs.sh $build_dir/
cp ./stop_ifs.sh $patch_dir/
cp ./instructions.txt $patch_dir/

