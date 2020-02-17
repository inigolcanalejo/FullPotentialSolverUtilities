# Removing plots
source scripts/removing_before_kratos_run.sh

cd runKratos/

GITBRANCH=$(git symbolic-ref HEAD | sed -e 's,.*/\(.*\),\1,')
DATE=`date '+%Y%m%d_%H%M%S'`
FILE=${input_dir_path}/plots/output_terminal.txt
NAME=${FILE%.*}
EXT=${FILE#*.}
NEWFILE=${NAME}_${DATE}_${GITBRANCH}.${EXT}
mkdir -p ${input_dir_path}/plots

# Run Kratos
unbuffer python3 MeshDomainRefinement.py 2>&1 | tee $NEWFILE

cp $PWD/ProjectParameters_new.json $input_dir_path
cp ../settings/parameters.sh $input_dir_path

# Removing files
rm cp*
rm runKratos.post.lst
cd ..

OUTPUTNAME=incompressible2D

