# Copying results
DATE=`date '+%Y%m%d_%H%M%S'`
output_dir_complete_path=${output_dir_path}_${DATE}_${GITBRANCH}_${OUTPUTNAME}
mkdir -p $output_dir_complete_path

cp -r $input_dir_path/mdpas $output_dir_complete_path/mdpas
cp -r $input_dir_path/output_gid $output_dir_complete_path/output_gid
cp -r $input_dir_path/output_salome $output_dir_complete_path/output_salome
cp -r $input_dir_path/plots $output_dir_complete_path/plots

cp $PWD/settings/parameters.sh $output_dir_complete_path