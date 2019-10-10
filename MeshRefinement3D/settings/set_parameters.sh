Generate_Mesh_File_Path=$PWD/generate_mdpas/generate_finite_wing.py
Generate_Mesh_Cosine_File_Path=$PWD/generate_mdpas/generateMeshRefinementCosine.py
Generate_Mesh_Cosine_Wake_File_Path=$PWD/generate_mdpas/generateMeshRefinementCosineWake.py
Generate_Mesh_Membrane_File_Path=$PWD/generate_mdpas/membraneAirfoil_separating4.py
Salome_Converter_File_Path=$PWD/generate_mdpas/use_converter.py
Salome_Converter_Membrane_File_Path=$PWD/generate_mdpas/use_converter_membrane.py
Mesh_Refinement_File_Path=$PWD/MeshRefinement.py
Mesh_Domain_Refinement_File_Path=$PWD/MeshDomainRefinement.py
Potential_Flow_Analysis_File_Path=$PWD/potential_flow_analysis_refinement.py

source settings/set_paths.sh

sed 's|'"Number_Of_Wing_Refinements = TBD"'|'"Number_Of_Wing_Refinements = $Number_Of_Wing_Refinements"'|g' -i /$Generate_Mesh_File_Path \
                                /$Salome_Converter_File_Path /$Mesh_Refinement_File_Path /$Generate_Mesh_Cosine_File_Path /$Generate_Mesh_Cosine_Wake_File_Path \
                                /$Potential_Flow_Analysis_File_Path /$Generate_Mesh_Membrane_File_Path /$Salome_Converter_Membrane_File_Path

sed 's|'"Number_Of_AOAS = TBD"'|'"Number_Of_AOAS = $Number_Of_AOAS"'|g' -i /$Generate_Mesh_File_Path \
                                /$Salome_Converter_File_Path /$Mesh_Refinement_File_Path /$Generate_Mesh_Cosine_File_Path /$Generate_Mesh_Cosine_Wake_File_Path \
                                /$Potential_Flow_Analysis_File_Path /$Generate_Mesh_Membrane_File_Path /$Salome_Converter_Membrane_File_Path

sed 's|'"Number_Of_Domains_Refinements = TBD"'|'"Number_Of_Domains_Refinements = $Number_Of_Domains_Refinements"'|g' -i /$Generate_Mesh_File_Path \
                                /$Salome_Converter_File_Path /$Mesh_Refinement_File_Path /$Generate_Mesh_Cosine_File_Path /$Generate_Mesh_Cosine_Wake_File_Path \
                                /$Potential_Flow_Analysis_File_Path /$Generate_Mesh_Membrane_File_Path /$Salome_Converter_Membrane_File_Path


sed 's|'"Initial_AOA = TBD"'|'"Initial_AOA = $Initial_AOA"'|g' -i /$Generate_Mesh_File_Path \
                                /$Salome_Converter_File_Path /$Mesh_Refinement_File_Path /$Generate_Mesh_Cosine_File_Path /$Generate_Mesh_Cosine_Wake_File_Path \
                                /$Potential_Flow_Analysis_File_Path /$Generate_Mesh_Membrane_File_Path /$Salome_Converter_Membrane_File_Path

sed 's|'"AOA_Increment = TBD"'|'"AOA_Increment = $AOA_Increment"'|g' -i /$Generate_Mesh_File_Path \
                                /$Salome_Converter_File_Path /$Mesh_Refinement_File_Path /$Generate_Mesh_Cosine_File_Path /$Generate_Mesh_Cosine_Wake_File_Path \
                                /$Potential_Flow_Analysis_File_Path /$Generate_Mesh_Membrane_File_Path /$Salome_Converter_Membrane_File_Path



sed 's|'"Initial_Growth_Rate_Wing = TBD"'|'"Initial_Growth_Rate_Wing = $Initial_Growth_Rate_Wing"'|g' -i /$Generate_Mesh_File_Path \
                                /$Salome_Converter_File_Path /$Mesh_Refinement_File_Path /$Generate_Mesh_Cosine_File_Path /$Generate_Mesh_Cosine_Wake_File_Path \
                                /$Potential_Flow_Analysis_File_Path /$Generate_Mesh_Membrane_File_Path /$Salome_Converter_Membrane_File_Path

sed 's|'"Growth_Rate_Wing_Refinement_Factor = TBD"'|'"Growth_Rate_Wing_Refinement_Factor = $Growth_Rate_Wing_Refinement_Factor"'|g' -i /$Generate_Mesh_File_Path \
                                /$Salome_Converter_File_Path /$Mesh_Refinement_File_Path /$Generate_Mesh_Cosine_File_Path /$Generate_Mesh_Cosine_Wake_File_Path \
                                /$Potential_Flow_Analysis_File_Path /$Generate_Mesh_Membrane_File_Path /$Salome_Converter_Membrane_File_Path



sed 's|'"Smallest_Airfoil_Mesh_Size = TBD"'|'"Smallest_Airfoil_Mesh_Size = $Smallest_Airfoil_Mesh_Size"'|g' -i /$Generate_Mesh_File_Path \
                                /$Salome_Converter_File_Path /$Mesh_Refinement_File_Path /$Generate_Mesh_Cosine_File_Path /$Generate_Mesh_Cosine_Wake_File_Path \
                                /$Potential_Flow_Analysis_File_Path /$Generate_Mesh_Membrane_File_Path /$Salome_Converter_Membrane_File_Path

sed 's|'"Biggest_Airfoil_Mesh_Size = TBD"'|'"Biggest_Airfoil_Mesh_Size = $Biggest_Airfoil_Mesh_Size"'|g' -i /$Generate_Mesh_File_Path \
                                /$Salome_Converter_File_Path /$Mesh_Refinement_File_Path /$Generate_Mesh_Cosine_File_Path /$Generate_Mesh_Cosine_Wake_File_Path \
                                /$Potential_Flow_Analysis_File_Path /$Generate_Mesh_Membrane_File_Path /$Salome_Converter_Membrane_File_Path

sed 's|'"Wing_span = TBD"'|'"Wing_span = $Wing_span"'|g' -i /$Generate_Mesh_File_Path \
                                /$Salome_Converter_File_Path /$Mesh_Refinement_File_Path /$Generate_Mesh_Cosine_File_Path /$Generate_Mesh_Cosine_Wake_File_Path \
                                /$Potential_Flow_Analysis_File_Path /$Generate_Mesh_Membrane_File_Path /$Salome_Converter_Membrane_File_Path


sed 's|'"Initial_Growth_Rate_Domain = TBD"'|'"Initial_Growth_Rate_Domain = $Initial_Growth_Rate_Domain"'|g' -i /$Generate_Mesh_File_Path \
                                /$Salome_Converter_File_Path /$Mesh_Refinement_File_Path /$Generate_Mesh_Cosine_File_Path /$Generate_Mesh_Cosine_Wake_File_Path \
                                /$Potential_Flow_Analysis_File_Path /$Generate_Mesh_Membrane_File_Path /$Salome_Converter_Membrane_File_Path

sed 's|'"Growth_Rate_Domain_Refinement_Factor = TBD"'|'"Growth_Rate_Domain_Refinement_Factor = $Growth_Rate_Domain_Refinement_Factor"'|g' -i /$Generate_Mesh_File_Path \
                                /$Salome_Converter_File_Path /$Mesh_Refinement_File_Path /$Generate_Mesh_Cosine_File_Path /$Generate_Mesh_Cosine_Wake_File_Path \
                                /$Potential_Flow_Analysis_File_Path /$Generate_Mesh_Membrane_File_Path /$Salome_Converter_Membrane_File_Path

