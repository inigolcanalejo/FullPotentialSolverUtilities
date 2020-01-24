# Resetting paths
export PYTHONPATH=""
export LD_LIBRARY_PATH=""

# Setting paths
source /path/to/salomeConverter.sh
source /path/to/kratosMaster.sh
#source /path/to/intel/mkl/bin/mklvars.sh intel64 lp64

echo "PYTHONPATH = $PYTHONPATH"
echo "LD_LIBRARY_PATH = $LD_LIBRARY_PATH"

# Path where mdpas and outputs are created
input_dir_path=/path/to/desired/directory

# Path where mdpas and output are saved
output_dir_path=/path/to/desired/directory

# Further paths
salome_output_path=$input_dir_path/output_salome
mdpa_path=$input_dir_path/mdpas
gid_output_path=$input_dir_path/output_gid

