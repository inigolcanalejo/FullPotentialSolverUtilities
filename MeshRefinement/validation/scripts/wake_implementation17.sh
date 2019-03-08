#Removing plots
source scripts/removing_before_kratos_run.sh

#Set element and wake process
Element=IncompressiblePotentialFlowElement2D3N
WakeProcess=define_wake_process_2d_refinement_wake_implementation_17_no_corner_one_structure_te_up
source scripts/set_element_and_wake_script.sh

#Run Kratos
unbuffer python3 MeshRefinement.py 2>&1 | tee $NEWFILE

#Unset element and wake process
sed 's|'"$Element"'|'"ELEMENT TBD"'|g' -i /$ProjectParameters_File_Path
sed 's|'"$WakeProcess"'|'"WAKE PROCESS TBD"'|g' -i /$ProjectParameters_File_Path

OUTPUTNAME=wake_implementation_99_17_no_corner_one_structure_TE_up
#Remove plots after run, run latex and copy results
source scripts/run_latex.sh

cd /home/inigo/software/kratosMaster/Kratos/applications/CompressiblePotentialFlowApplication/validation