#Resetting paths
export PYTHONPATH=""
export LD_LIBRARY_PATH=""

#Setting paths
source /home/inigo/Documents/paths/salomeConverter.sh
#source /home/inigo/Documents/paths/kratosMaster3.sh
source /home/inigo/Documents/paths/kratosMaster.sh
#source /home/inigo/Documents/paths/kratosMaster4.sh
#source /home/inigo/Documents/paths/kratosMerge.sh
#source /home/inigo/intel/mkl/bin/mklvars.sh intel64 lp64

echo "PYTHONPATH = $PYTHONPATH"
echo "LD_LIBRARY_PATH = $LD_LIBRARY_PATH"

GITBRANCH=$(git symbolic-ref HEAD | sed -e 's,.*/\(.*\),\1,')
#echo "GITBRANCH = $GITBRANCH"
input_dir_path=/media/inigo/10740FB2740F9A1C/3d_results_test
#input_dir_path=/media/inigo/10740FB2740F9A1C/Results/06_wing_mesh_refinement/20191011_101705_AOA_0.0_Wing_Span_4.0_Airfoil_Mesh_Size_0.01_Biggest_Airfoil_Mesh_Size_0.05_Initial_Growth_Rate_Domain_0.7_Initial_Growth_Rate_Wing_0.7
salome_output_path=$input_dir_path/output_salome
mdpa_path=$input_dir_path/mdpas
#mdpa_path=/media/inigo/10740FB2740F9A1C/Results/06_wing_mesh_refinement/20191022_122442_AOA_5.0_Wing_Span_4.0_Airfoil_Mesh_Size_0.011_Biggest_Airfoil_Mesh_Size_0.06_Initial_Growth_Rate_Domain_0.6_Initial_Growth_Rate_Wing_0.6/mdpas
#mdpa_path=/media/inigo/10740FB2740F9A1C/Results/06_wing_mesh_refinement/20191021_170337_AOA_5.0_Wing_Span_4.0_Airfoil_Mesh_Size_0.001_Biggest_Airfoil_Mesh_Size_0.05_Initial_Growth_Rate_Domain_0.7_Initial_Growth_Rate_Wing_0.7/mdpas
#mdpa_path=/media/inigo/10740FB2740F9A1C/Results/06_wing_mesh_refinement/20191017_201158_AOA_0.0_Wing_Span_4.0_Airfoil_Mesh_Size_0.01_Biggest_Airfoil_Mesh_Size_0.05_Initial_Growth_Rate_Domain_0.7_Initial_Growth_Rate_Wing_0.7/mdpas
#mdpa_path=/media/inigo/10740FB2740F9A1C/Results/06_wing_mesh_refinement/20191021_102917_AOA_5.0_Wing_Span_4.0_Airfoil_Mesh_Size_0.001_Biggest_Airfoil_Mesh_Size_0.05_Initial_Growth_Rate_Domain_0.7_Initial_Growth_Rate_Wing_0.7/mdpas
gid_output_path=$input_dir_path/output_gid
#gid_output_path=/media/inigo/10740FB2740F9A1C/Results/06_wing_mesh_refinement/20191014_112855_AOA_0.0_Wing_Span_4.0_Airfoil_Mesh_Size_0.01_Biggest_Airfoil_Mesh_Size_0.05_Initial_Growth_Rate_Domain_0.7_Initial_Growth_Rate_Wing_0.7/output_salome

DATE=`date '+%Y%m%d_%H%M%S'`
FILEK=${input_dir_path}/plots/output_terminal_kratos.txt
FILES=${input_dir_path}/plots/output_terminal_salome.txt
FILEC=${input_dir_path}/plots/output_terminal_converter.txt
NAMEK=${FILEK%.*}
NAMES=${FILES%.*}
NAMEC=${FILEC%.*}
EXT=${FILEK#*.}
FILEKRATOS=${NAMEK}_${DATE}_${GITBRANCH}.${EXT}
FILESALOME=${NAMES}_${DATE}_${GITBRANCH}.${EXT}
FILECONVERTER=${NAMEC}_${DATE}_${GITBRANCH}.${EXT}
mkdir -p ${input_dir_path}/plots