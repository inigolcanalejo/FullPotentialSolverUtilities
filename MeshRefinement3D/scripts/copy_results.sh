##Copying results
DIRECTORY=/media/inigo/10740FB2740F9A1C/Results/06_wing_mesh_refinement/
DATE=`date '+%Y%m%d_%H%M%S'`
mkdir -p ${DIRECTORY}${DATE}_AOA_${Initial_AOA}_Wing_Span_${Wing_span}_Airfoil_Mesh_Size_${Smallest_Airfoil_Mesh_Size}\
_Biggest_Airfoil_Mesh_Size_${Biggest_Airfoil_Mesh_Size}_Initial_Growth_Rate_Domain_${Initial_Growth_Rate_Domain}\
_Initial_Growth_Rate_Wing_${Initial_Growth_Rate_Wing}

cp -r $input_dir_path/* ${DIRECTORY}${DATE}_AOA_${Initial_AOA}_Wing_Span_${Wing_span}_Airfoil_Mesh_Size_${Smallest_Airfoil_Mesh_Size}\
_Biggest_Airfoil_Mesh_Size_${Biggest_Airfoil_Mesh_Size}_Initial_Growth_Rate_Domain_${Initial_Growth_Rate_Domain}\
_Initial_Growth_Rate_Wing_${Initial_Growth_Rate_Wing}

cp $PWD/settings/parameters.sh ${DIRECTORY}${DATE}_AOA_${Initial_AOA}_Wing_Span_${Wing_span}_Airfoil_Mesh_Size_${Smallest_Airfoil_Mesh_Size}\
_Biggest_Airfoil_Mesh_Size_${Biggest_Airfoil_Mesh_Size}_Initial_Growth_Rate_Domain_${Initial_Growth_Rate_Domain}\
_Initial_Growth_Rate_Wing_${Initial_Growth_Rate_Wing}