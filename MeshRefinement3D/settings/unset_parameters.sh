
source settings/unset_paths.sh

sed 's|'"Number_Of_Wing_Refinements = $Number_Of_Wing_Refinements"'|'"Number_Of_Wing_Refinements = TBD"'|g' -i /$Generate_Mesh_File_Path \
                                /$Salome_Converter_File_Path /$Mesh_Refinement_File_Path /$Generate_Mesh_Cosine_File_Path /$Generate_Mesh_Cosine_Wake_File_Path \
                                /$Potential_Flow_Analysis_File_Path /$Generate_Mesh_Membrane_File_Path /$Salome_Converter_Membrane_File_Path

sed 's|'"Number_Of_AOAS = $Number_Of_AOAS"'|'"Number_Of_AOAS = TBD"'|g' -i /$Generate_Mesh_File_Path \
                                /$Salome_Converter_File_Path /$Mesh_Refinement_File_Path /$Generate_Mesh_Cosine_File_Path /$Generate_Mesh_Cosine_Wake_File_Path \
                                /$Potential_Flow_Analysis_File_Path /$Generate_Mesh_Membrane_File_Path /$Salome_Converter_Membrane_File_Path

sed 's|'"Number_Of_Domains_Refinements = $Number_Of_Domains_Refinements"'|'"Number_Of_Domains_Refinements = TBD"'|g' -i /$Generate_Mesh_File_Path \
                                /$Salome_Converter_File_Path /$Mesh_Refinement_File_Path /$Generate_Mesh_Cosine_File_Path /$Generate_Mesh_Cosine_Wake_File_Path \
                                /$Potential_Flow_Analysis_File_Path /$Generate_Mesh_Membrane_File_Path /$Salome_Converter_Membrane_File_Path


sed 's|'"Initial_AOA = $Initial_AOA"'|'"Initial_AOA = TBD"'|g' -i /$Generate_Mesh_File_Path \
                                /$Salome_Converter_File_Path /$Mesh_Refinement_File_Path /$Generate_Mesh_Cosine_File_Path /$Generate_Mesh_Cosine_Wake_File_Path \
                                /$Potential_Flow_Analysis_File_Path /$Generate_Mesh_Membrane_File_Path /$Salome_Converter_Membrane_File_Path

sed 's|'"AOA_Increment = $AOA_Increment"'|'"AOA_Increment = TBD"'|g' -i /$Generate_Mesh_File_Path \
                                /$Salome_Converter_File_Path /$Mesh_Refinement_File_Path /$Generate_Mesh_Cosine_File_Path /$Generate_Mesh_Cosine_Wake_File_Path \
                                /$Potential_Flow_Analysis_File_Path /$Generate_Mesh_Membrane_File_Path /$Salome_Converter_Membrane_File_Path



sed 's|'"Initial_Growth_Rate_Wing = $Initial_Growth_Rate_Wing"'|'"Initial_Growth_Rate_Wing = TBD"'|g' -i /$Generate_Mesh_File_Path \
                                /$Salome_Converter_File_Path /$Mesh_Refinement_File_Path /$Generate_Mesh_Cosine_File_Path /$Generate_Mesh_Cosine_Wake_File_Path \
                                /$Potential_Flow_Analysis_File_Path /$Generate_Mesh_Membrane_File_Path /$Salome_Converter_Membrane_File_Path

sed 's|'"Growth_Rate_Wing_Refinement_Factor = $Growth_Rate_Wing_Refinement_Factor"'|'"Growth_Rate_Wing_Refinement_Factor = TBD"'|g' -i /$Generate_Mesh_File_Path \
                                /$Salome_Converter_File_Path /$Mesh_Refinement_File_Path /$Generate_Mesh_Cosine_File_Path /$Generate_Mesh_Cosine_Wake_File_Path \
                                /$Potential_Flow_Analysis_File_Path /$Generate_Mesh_Membrane_File_Path /$Salome_Converter_Membrane_File_Path

sed 's|'"Smallest_Airfoil_Mesh_Size = $Smallest_Airfoil_Mesh_Size"'|'"Smallest_Airfoil_Mesh_Size = TBD"'|g' -i /$Generate_Mesh_File_Path \
                                /$Salome_Converter_File_Path /$Mesh_Refinement_File_Path /$Generate_Mesh_Cosine_File_Path /$Generate_Mesh_Cosine_Wake_File_Path \
                                /$Potential_Flow_Analysis_File_Path /$Generate_Mesh_Membrane_File_Path /$Salome_Converter_Membrane_File_Path

sed 's|'"Biggest_Airfoil_Mesh_Size = $Biggest_Airfoil_Mesh_Size"'|'"Biggest_Airfoil_Mesh_Size = TBD"'|g' -i /$Generate_Mesh_File_Path \
                                /$Salome_Converter_File_Path /$Mesh_Refinement_File_Path /$Generate_Mesh_Cosine_File_Path /$Generate_Mesh_Cosine_Wake_File_Path \
                                /$Potential_Flow_Analysis_File_Path /$Generate_Mesh_Membrane_File_Path /$Salome_Converter_Membrane_File_Path

sed 's|'"Wing_span = $Wing_span"'|'"Wing_span = TBD"'|g' -i /$Generate_Mesh_File_Path \
                                /$Salome_Converter_File_Path /$Mesh_Refinement_File_Path /$Generate_Mesh_Cosine_File_Path /$Generate_Mesh_Cosine_Wake_File_Path \
                                /$Potential_Flow_Analysis_File_Path /$Generate_Mesh_Membrane_File_Path /$Salome_Converter_Membrane_File_Path

sed 's|'"Initial_Growth_Rate_Domain = $Initial_Growth_Rate_Domain"'|'"Initial_Growth_Rate_Domain = TBD"'|g' -i /$Generate_Mesh_File_Path \
                                /$Salome_Converter_File_Path /$Mesh_Refinement_File_Path /$Generate_Mesh_Cosine_File_Path /$Generate_Mesh_Cosine_Wake_File_Path \
                                /$Potential_Flow_Analysis_File_Path /$Generate_Mesh_Membrane_File_Path /$Salome_Converter_Membrane_File_Path

sed 's|'"Growth_Rate_Domain_Refinement_Factor = $Growth_Rate_Domain_Refinement_Factor"'|'"Growth_Rate_Domain_Refinement_Factor = TBD"'|g' -i /$Generate_Mesh_File_Path \
                                /$Salome_Converter_File_Path /$Mesh_Refinement_File_Path /$Generate_Mesh_Cosine_File_Path /$Generate_Mesh_Cosine_Wake_File_Path \
                                /$Potential_Flow_Analysis_File_Path /$Generate_Mesh_Membrane_File_Path /$Salome_Converter_Membrane_File_Path