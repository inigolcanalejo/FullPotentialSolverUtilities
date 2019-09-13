#Resetting paths
export PYTHONPATH=""
export LD_LIBRARY_PATH=""

#Setting paths
source /home/inigo/Documents/paths/salomeConverter.sh
#source /home/inigo/Documents/paths/kratosMaster3.sh
#source /home/inigo/Documents/paths/kratosMaster.sh
source /home/inigo/Documents/paths/kratosMerge.sh
source /home/inigo/intel/mkl/bin/mklvars.sh intel64 lp64

echo "PYTHONPATH = $PYTHONPATH"
echo "LD_LIBRARY_PATH = $LD_LIBRARY_PATH"

GITBRANCH=$(git symbolic-ref HEAD | sed -e 's,.*/\(.*\),\1,')
#echo "GITBRANCH = $GITBRANCH"
input_dir_path=/home/inigo/simulations/naca0012/07_salome/05_MeshRefinement
salome_output_path=$input_dir_path/output_salome
mdpa_path=$input_dir_path/mdpas
#mdpa_path=$input_dir_path/mdpas_cosine_20190705_140938_Domain_Size_1e3_AOA_0.0_AMS_1e-6_FMS_1.0
#mdpa_path=/media/inigo/10740FB2740F9A1C/Results/COUPLED_PROBLEMS/05_MeshRefinement_20190503_201223_master_incompressible2D_all_aoa/mdpas
gid_output_path=/media/inigo/10740FB2740F9A1C/Outputs/05_MeshRefinement

DATE=`date '+%Y%m%d_%H%M%S'`
FILE=${input_dir_path}/plots/output_terminal.txt
NAME=${FILE%.*}
EXT=${FILE#*.}
NEWFILE=${NAME}_${DATE}_${GITBRANCH}.${EXT}