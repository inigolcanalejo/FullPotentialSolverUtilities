#Resetting paths
export PYTHONPATH=""
export LD_LIBRARY_PATH=""

#Setting paths
source /home/inigo/Documents/paths/salomeConverter.sh
#source /home/inigo/Documents/paths/kratosMaster3.sh
source /home/inigo/Documents/paths/kratosMaster.sh
#source /home/inigo/Documents/paths/kratosMerge.sh
#source /home/inigo/intel/mkl/bin/mklvars.sh intel64 lp64

echo "PYTHONPATH = $PYTHONPATH"
echo "LD_LIBRARY_PATH = $LD_LIBRARY_PATH"

GITBRANCH=$(git symbolic-ref HEAD | sed -e 's,.*/\(.*\),\1,')
#echo "GITBRANCH = $GITBRANCH"
input_dir_path=/media/inigo/10740FB2740F9A1C/3d_results
#input_dir_path=/media/inigo/10740FB2740F9A1C/Results/06_wing_mesh_refinement/20191011_101705_AOA_0.0_Wing_Span_4.0_Airfoil_Mesh_Size_0.01_Biggest_Airfoil_Mesh_Size_0.05_Initial_Growth_Rate_Domain_0.7_Initial_Growth_Rate_Wing_0.7
salome_output_path=$input_dir_path/output_salome
mdpa_path=$input_dir_path/mdpas
#mdpa_path=/media/inigo/10740FB2740F9A1C/Results/06_wing_mesh_refinement/20191014_112855_AOA_0.0_Wing_Span_4.0_Airfoil_Mesh_Size_0.01_Biggest_Airfoil_Mesh_Size_0.05_Initial_Growth_Rate_Domain_0.7_Initial_Growth_Rate_Wing_0.7/mdpas
gid_output_path=$input_dir_path/output_gid
#gid_output_path=/media/inigo/10740FB2740F9A1C/Results/06_wing_mesh_refinement/20191014_112855_AOA_0.0_Wing_Span_4.0_Airfoil_Mesh_Size_0.01_Biggest_Airfoil_Mesh_Size_0.05_Initial_Growth_Rate_Domain_0.7_Initial_Growth_Rate_Wing_0.7/output_salome

DATE=`date '+%Y%m%d_%H%M%S'`
FILE=${input_dir_path}/plots/output_terminal.txt
NAME=${FILE%.*}
EXT=${FILE#*.}
NEWFILE=${NAME}_${DATE}_${GITBRANCH}.${EXT}