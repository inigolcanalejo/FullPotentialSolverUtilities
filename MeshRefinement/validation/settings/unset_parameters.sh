
source settings/unset_paths.sh

sed 's|'"Number_Of_Refinements = $Number_Of_Refinements"'|'"Number_Of_Refinements = TBD"'|g' -i /$Generate_Mesh_File_Path \
                                /$Salome_Converter_File_Path /$Mesh_Refinement_File_Path /$Generate_Mesh_Cosine_File_Path \
                                /$Potential_Flow_Analysis_File_Path /$Generate_Mesh_Membrane_File_Path /$Salome_Converter_Membrane_File_Path

sed 's|'"Number_Of_AOAS = $Number_Of_AOAS"'|'"Number_Of_AOAS = TBD"'|g' -i /$Generate_Mesh_File_Path \
                                /$Salome_Converter_File_Path /$Mesh_Refinement_File_Path /$Generate_Mesh_Cosine_File_Path \
                                /$Potential_Flow_Analysis_File_Path /$Generate_Mesh_Membrane_File_Path /$Salome_Converter_Membrane_File_Path

sed 's|'"Number_Of_Domains_Size = $Number_Of_Domains_Size"'|'"Number_Of_Domains_Size = TBD"'|g' -i /$Generate_Mesh_File_Path \
                                /$Salome_Converter_File_Path /$Mesh_Refinement_File_Path /$Generate_Mesh_Cosine_File_Path \
                                /$Potential_Flow_Analysis_File_Path /$Generate_Mesh_Membrane_File_Path /$Salome_Converter_Membrane_File_Path


sed 's|'"Initial_AOA = $Initial_AOA"'|'"Initial_AOA = TBD"'|g' -i /$Generate_Mesh_File_Path \
                                /$Salome_Converter_File_Path /$Mesh_Refinement_File_Path /$Generate_Mesh_Cosine_File_Path \
                                /$Potential_Flow_Analysis_File_Path /$Generate_Mesh_Membrane_File_Path /$Salome_Converter_Membrane_File_Path

sed 's|'"AOA_Increment = $AOA_Increment"'|'"AOA_Increment = TBD"'|g' -i /$Generate_Mesh_File_Path \
                                /$Salome_Converter_File_Path /$Mesh_Refinement_File_Path /$Generate_Mesh_Cosine_File_Path \
                                /$Potential_Flow_Analysis_File_Path /$Generate_Mesh_Membrane_File_Path /$Salome_Converter_Membrane_File_Path



sed 's|'"Initial_Airfoil_MeshSize = $Initial_Airfoil_MeshSize"'|'"Initial_Airfoil_MeshSize = TBD"'|g' -i /$Generate_Mesh_File_Path \
                                /$Salome_Converter_File_Path /$Mesh_Refinement_File_Path /$Generate_Mesh_Cosine_File_Path \
                                /$Potential_Flow_Analysis_File_Path /$Generate_Mesh_Membrane_File_Path /$Salome_Converter_Membrane_File_Path

sed 's|'"Airfoil_Refinement_Factor = $Airfoil_Refinement_Factor"'|'"Airfoil_Refinement_Factor = TBD"'|g' -i /$Generate_Mesh_File_Path \
                                /$Salome_Converter_File_Path /$Mesh_Refinement_File_Path /$Generate_Mesh_Cosine_File_Path \
                                /$Potential_Flow_Analysis_File_Path /$Generate_Mesh_Membrane_File_Path /$Salome_Converter_Membrane_File_Path



sed 's|'"Initial_FarField_MeshSize = $Initial_FarField_MeshSize"'|'"Initial_FarField_MeshSize = TBD"'|g' -i /$Generate_Mesh_File_Path \
                                /$Salome_Converter_File_Path /$Mesh_Refinement_File_Path /$Generate_Mesh_Cosine_File_Path \
                                /$Potential_Flow_Analysis_File_Path /$Generate_Mesh_Membrane_File_Path /$Salome_Converter_Membrane_File_Path

sed 's|'"FarField_Refinement_Factor = $FarField_Refinement_Factor"'|'"FarField_Refinement_Factor = TBD"'|g' -i /$Generate_Mesh_File_Path \
                                /$Salome_Converter_File_Path /$Mesh_Refinement_File_Path /$Generate_Mesh_Cosine_File_Path \
                                /$Potential_Flow_Analysis_File_Path /$Generate_Mesh_Membrane_File_Path /$Salome_Converter_Membrane_File_Path

sed 's|'"Initial_Domain_Size = $Initial_Domain_Size"'|'"Initial_Domain_Size = TBD"'|g' -i /$Generate_Mesh_File_Path \
                                /$Salome_Converter_File_Path /$Mesh_Refinement_File_Path /$Generate_Mesh_Cosine_File_Path \
                                /$Potential_Flow_Analysis_File_Path /$Generate_Mesh_Membrane_File_Path /$Salome_Converter_Membrane_File_Path

sed 's|'"Domain_Size_Factor = $Domain_Size_Factor"'|'"Domain_Size_Factor = TBD"'|g' -i /$Generate_Mesh_File_Path \
                                /$Salome_Converter_File_Path /$Mesh_Refinement_File_Path /$Generate_Mesh_Cosine_File_Path \
                                /$Potential_Flow_Analysis_File_Path /$Generate_Mesh_Membrane_File_Path /$Salome_Converter_Membrane_File_Path