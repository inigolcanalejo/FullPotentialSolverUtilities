#Removing plots
source scripts/removing_before_kratos_run.sh

cd runKratos/
#Run Kratos
unbuffer python3 MeshDomainRefinement.py 2>&1 | tee $FILEKRATOS
rm runKratos.post.lst
rm main_potential_jump*
rm main_cp*
cd ..

OUTPUTNAME=incompressible3D

