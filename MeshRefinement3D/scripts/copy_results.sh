# Copying results
DATE=`date '+%Y%m%d_%H%M%S'`
output_dir_complete_path=${output_dir_path}${DATE}_AOA_${Initial_AOA}_Wing_Span_${Wing_span}_Airfoil_Mesh_Size_${Smallest_Airfoil_Mesh_Size}\
_Biggest_Airfoil_Mesh_Size_${Biggest_Airfoil_Mesh_Size}_Initial_Growth_Rate_Domain_${Initial_Growth_Rate_Domain}\
_Initial_Growth_Rate_Wing_${Initial_Growth_Rate_Wing}

mkdir -p $output_dir_complete_path

cp -r $input_dir_path/mdpas $output_dir_complete_path/mdpas
cp -r $input_dir_path/output_gid $output_dir_complete_path/output_gid
cp -r $input_dir_path/plots $output_dir_complete_path/plots

cp $PWD/settings/parameters.sh $output_dir_complete_path