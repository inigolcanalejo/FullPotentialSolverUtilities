# Resetting paths
export PYTHONPATH=""
export LD_LIBRARY_PATH=""

# Setting paths
source /home/inigo/Documents/paths/salomeConverter.sh
source /home/inigo/Documents/paths/kratosMaster4.sh
#source /home/inigo/intel/mkl/bin/mklvars.sh intel64 lp64

echo "PYTHONPATH = $PYTHONPATH"
echo "LD_LIBRARY_PATH = $LD_LIBRARY_PATH"

# Path where mdpas and outputs are created
input_dir_path=/media/inigo/10740FB2740F9A1C/2d_results_test

# Path where mdpas and output are saved
output_dir_path=/media/inigo/10740FB2740F9A1C/Results/07_naca0012_incompressible/MeshRefinement

# Further paths
salome_output_path=$input_dir_path/output_salome
mdpa_path=$input_dir_path/mdpas
gid_output_path=$input_dir_path/output_gid

