#Name of the directory where to save the mdpas
DATE=`date '+%Y%m%d_%H%M%S'`
MPDAS_DIRECTORY=$input_dir_path/mdpas_cosine_${DATE}_Domain_Size_${Initial_Domain_Size}\
_AOA_${Initial_AOA}_AMS_${Initial_Airfoil_MeshSize}_FMS_${Initial_FarField_MeshSize}

#Create the directory
mkdir -p ${MPDAS_DIRECTORY}

#Save the mdpas in a copy
cp -r $input_dir_path/mdpas/n* ${MPDAS_DIRECTORY}