# Removing plots
source scripts/removing_before_kratos_run.sh

cd runKratos/

# Run Kratos
unbuffer python3 MeshDomainRefinement.py 2>&1 | tee $NEWFILE

# Removing files
rm cp*
rm runKratos.post.lst
cd ..

OUTPUTNAME=incompressible2D

