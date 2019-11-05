Generate_Mesh_File_Path=$PWD/generate_mdpas/generate_finite_wing.py
Generate_Mesh_Middle_File_Path=$PWD/generate_mdpas/generate_finite_wing_middle.py
Generate_Mesh_Wake_Middle_File_Path=$PWD/generate_mdpas/generate_finite_wing_wake_middle.py
Generate_Mesh_Wake_Sections_File_Path=$PWD/generate_mdpas/generate_finite_wing_wake_sections.py
Salome_Converter_File_Path=$PWD/generate_mdpas/use_converter.py
Potential_Flow_Analysis_File_Path=$PWD/runKratos/potential_flow_analysis_refinement.py

Generate_Mesh_Cosine_File_Path=$PWD/generate_mdpas/generateMeshRefinementCosine.py
Generate_Mesh_Cosine_Wake_File_Path=$PWD/generate_mdpas/generateMeshRefinementCosineWake.py
Generate_Mesh_Membrane_File_Path=$PWD/generate_mdpas/membraneAirfoil_separating4.py
Salome_Converter_Membrane_File_Path=$PWD/generate_mdpas/use_converter_membrane.py

declare -A PathNames

PathNames[Generate_Mesh_File_Path]=$PWD/generate_mdpas/generate_finite_wing.py
PathNames[Generate_Mesh_Middle_File_Path]=$PWD/generate_mdpas/generate_finite_wing_middle.py
PathNames[Generate_Mesh_Wake_Middle_File_Path]=$PWD/generate_mdpas/generate_finite_wing_wake_middle.py
PathNames[Generate_Mesh_Wake_Sections_File_Path]=$PWD/generate_mdpas/generate_finite_wing_wake_sections.py
PathNames[Salome_Converter_File_Path]=$PWD/generate_mdpas/use_converter.py
PathNames[Potential_Flow_Analysis_File_Path]=$PWD/runKratos/potential_flow_analysis_refinement.py


source settings/set_paths.sh

declare -A Parameters

Parameters[Number_Of_AOAS]=$Number_Of_AOAS
Parameters[Number_Of_Domains_Refinements]=$Number_Of_Domains_Refinements
Parameters[Number_Of_Wing_Refinements]=$Number_Of_Wing_Refinements

Parameters[Initial_AOA]=$Initial_AOA
Parameters[AOA_Increment]=$AOA_Increment

Parameters[Initial_Growth_Rate_Domain]=$Initial_Growth_Rate_Domain
Parameters[Growth_Rate_Domain_Refinement_Factor]=$Growth_Rate_Domain_Refinement_Factor

Parameters[Initial_Growth_Rate_Wing]=$Initial_Growth_Rate_Wing
Parameters[Growth_Rate_Wing_Refinement_Factor]=$Growth_Rate_Wing_Refinement_Factor

Parameters[Smallest_Airfoil_Mesh_Size]=$Smallest_Airfoil_Mesh_Size
Parameters[Biggest_Airfoil_Mesh_Size]=$Biggest_Airfoil_Mesh_Size
Parameters[Wing_span]=$Wing_span

#echo 'Parameters:'
for path_variable_name in "${!Parameters[@]}"; do
    #echo ' '$path_variable_name '=' ${Parameters[$path_variable_name]}
    for path_file_name in "${!PathNames[@]}"; do
        sed 's|'"$path_variable_name = TBD"'|'"$path_variable_name = ${Parameters[$path_variable_name]}"'|g' -i \
        /${PathNames[$path_file_name]}
    done
done