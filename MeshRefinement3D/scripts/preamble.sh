# Resetting paths
export PYTHONPATH=""
export LD_LIBRARY_PATH=""

# Setting paths
source /home/inigo/Documents/paths/salomeConverter.sh
# source /home/inigo/Documents/paths/kratosMaster5.sh
#source /home/inigo/Documents/paths/kratosMaster5FullDebug.sh
source /home/inigo/Documents/paths/kratosMaster6.sh
# source /home/inigo/Documents/paths/kratosMaster6FullDebug.sh
#source /home/inigo/intel/mkl/bin/mklvars.sh intel64 lp64

echo "PYTHONPATH = $PYTHONPATH"
echo "LD_LIBRARY_PATH = $LD_LIBRARY_PATH"

# Path where mdpas and outputs are created
input_dir_path=/media/inigo/10740FB2740F9A1C/3d_results_test2

# Path where mdpas and output are saved
output_dir_path=/media/inigo/10740FB2740F9A1C/Results/11_onera/

# Further paths
salome_output_path=$input_dir_path/output_salome
# mdpa_path=$input_dir_path/mdpas
# mdpa_path=$input_dir_path/mdpas_naca_wake_ref
# mdpa_path=$input_dir_path/mdpas_naca_no_refinement_box
# mdpa_path=$input_dir_path/mdpas_onera_wake_ref
# mdpa_path=$input_dir_path/mdpas_onera_mesh_refinement
# mdpa_path=$input_dir_path/mdpas_naca_blunt_te_coarse_wake_0_deg/wake_size_01
# mdpa_path=$input_dir_path/mdpas_naca_blunt_te_coarse_wake_0_deg
mdpa_path=$input_dir_path/mdpas_nasa_crm_salome
gid_output_path=$input_dir_path/output_gid

DATE=`date '+%Y%m%d_%H%M%S'`
GITBRANCH=$(git symbolic-ref HEAD | sed -e 's,.*/\(.*\),\1,')
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