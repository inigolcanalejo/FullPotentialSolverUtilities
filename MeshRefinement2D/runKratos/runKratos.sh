# Removing plots
source scripts/removing_before_kratos_run.sh

cd runKratos/

GITBRANCH=$(git symbolic-ref HEAD | sed -e 's,.*/\(.*\),\1,')
DATE=`date '+%Y%m%d_%H%M%S'`
FILE=${input_dir_path}/plots/output_terminal.txt
NAME=${FILE%.*}
EXT=${FILE#*.}
NEWFILE=${NAME}_${DATE}_${GITBRANCH}.${EXT}

# Run Kratos
unbuffer python3 MeshDomainRefinement.py 2>&1 | tee $NEWFILE

# Removing files
rm cp*
rm runKratos.post.lst
cd ..

OUTPUTNAME=incompressible2D

