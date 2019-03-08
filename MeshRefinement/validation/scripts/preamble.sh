#Resetting paths
export PYTHONPATH=""
export LD_LIBRARY_PATH=""

#Setting paths
source /home/inigo/Documents/paths/salomeConverter.sh
source /home/inigo/Documents/paths/kratosMaster3.sh
source /home/inigo/intel/mkl/bin/mklvars.sh intel64 lp64

echo "PYTHONPATH = $PYTHONPATH"
echo "LD_LIBRARY_PATH = $LD_LIBRARY_PATH"

GITBRANCH=$(git symbolic-ref HEAD | sed -e 's,.*/\(.*\),\1,')
Input_Dir=/home/inigo/simulations/naca0012/07_salome/05_MeshRefinement
Salome_Output=/home/inigo/simulations/naca0012/07_salome/05_MeshRefinement/output_salome

DATE=`date '+%Y%m%d_%H%M%S'`
FILE=${Input_Dir}/plots/output_terminal.txt
NAME=${FILE%.*}
EXT=${FILE#*.}
NEWFILE=${NAME}_${DATE}_${GITBRANCH}.${EXT}