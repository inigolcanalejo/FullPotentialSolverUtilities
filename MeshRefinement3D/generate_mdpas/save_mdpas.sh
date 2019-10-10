echo " Saving mdpas"
#Name of the directory where to save the mdpas
DATE=`date '+%Y%m%d_%H%M%S'`
MPDAS_DIRECTORY=$input_dir_path/saved_mdpas/mdpas_wing_${DATE}_AOA_${Initial_AOA}\
_Initial_Growth_Rate_Domain_${Initial_Growth_Rate_Domain}_Initial_Growth_Rate_Wing_${Initial_Growth_Rate_Wing}

#Create the directory
mkdir -p ${MPDAS_DIRECTORY}

#Save the mdpas in a copy
cp -r $input_dir_path/mdpas/* ${MPDAS_DIRECTORY}