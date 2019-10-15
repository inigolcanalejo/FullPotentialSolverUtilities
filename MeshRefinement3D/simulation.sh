#!/bin/bash
#
#run this file using the command:
# bash simulation.sh

#Going to the current directory
echo "The previous current working directory: $PWD"

SCRIPT=`realpath $0`
SCRIPTPATH=`dirname $SCRIPT`
cd $SCRIPTPATH

echo "The current working directory:          $PWD"

#Setting paths
source scripts/preamble.sh

#Setting the parameters
source settings/parameters.sh
source settings/set_parameters.sh
cd generate_mdpas/

# Run salome: generate geometry and mesh
rm $input_dir_path/output_salome/*
rm $input_dir_path/mdpas/wa*
python3 runSalome.py

# Convert salomes mesh into mdpa
rm $input_dir_path/mdpas/M*
rm $input_dir_path/mdpas/S*
python3 use_converter.py
rm $input_dir_path/output_salome/*

# # Save mdpas file in a copy
# source save_mdpas.sh

cd ..
# Run Kratos
source runKratos/runKratos.sh
# Run Latex
source scripts/run_latex.sh
# Copy results
source scripts/copy_results.sh

source settings/unset_parameters.sh



