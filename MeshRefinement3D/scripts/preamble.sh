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
