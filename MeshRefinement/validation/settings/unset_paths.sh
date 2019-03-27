
sed 's|'"salome_output_path = '$salome_output_path'"'|'"salome_output_path = 'TBD'"'|g' -i \
/$Salome_Converter_File_Path /$Generate_Mesh_Cosine_File_Path 

sed 's|'"mdpa_path = '$mdpa_path'"'|'"mdpa_path = 'TBD'"'|g' -i \
/$Salome_Converter_File_Path /$Mesh_Domain_Refinement_File_Path

sed 's|'"gid_output_path = '$gid_output_path'"'|'"gid_output_path = 'TBD'"'|g' -i \
/$Mesh_Domain_Refinement_File_Path

sed 's|'"input_dir_path = '$input_dir_path'"'|'"input_dir_path = 'TBD'"'|g' -i \
/$Compute_Lift_Process

