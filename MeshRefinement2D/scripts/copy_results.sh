##Copying results
DIRECTORY=/media/inigo/10740FB2740F9A1C/Results/COUPLED_PROBLEMS/05_MeshRefinement
DATE=`date '+%Y%m%d_%H%M%S'`
mkdir -p ${DIRECTORY}_${DATE}_${GITBRANCH}_${OUTPUTNAME}
mkdir -p ${DIRECTORY}_${DATE}_${GITBRANCH}_${OUTPUTNAME}/output_gid
mkdir -p ${DIRECTORY}_${DATE}_${GITBRANCH}_${OUTPUTNAME}/mdpas

cp -r $input_dir_path/plots/ ${DIRECTORY}_${DATE}_${GITBRANCH}_${OUTPUTNAME}
cp -r /media/inigo/10740FB2740F9A1C/Outputs/05_MeshRefinement/* ${DIRECTORY}_${DATE}_${GITBRANCH}_${OUTPUTNAME}/output_gid

#Save the mdpas in a copy
cp -r $input_dir_path/mdpas/n* ${DIRECTORY}_${DATE}_${GITBRANCH}_${OUTPUTNAME}/mdpas

cp $PWD/settings/parameters.sh ${DIRECTORY}_${DATE}_${GITBRANCH}_${OUTPUTNAME}