Compute_Lift_Process=$PWD/compute_lift_process_2d_refinement.py

sed 's|'"salome_output_path = 'TBD'"'|'"salome_output_path = '$salome_output_path'"'|g' -i \
/$Salome_Converter_File_Path /$Generate_Mesh_Cosine_File_Path 

sed 's|'"mdpa_path = 'TBD'"'|'"mdpa_path = '$mdpa_path'"'|g' -i \
/$Salome_Converter_File_Path /$Mesh_Domain_Refinement_File_Path

sed 's|'"gid_output_path = 'TBD'"'|'"gid_output_path = '$gid_output_path'"'|g' -i \
/$Mesh_Domain_Refinement_File_Path

sed 's|'"input_dir_path = 'TBD'"'|'"input_dir_path = '$input_dir_path'"'|g' -i \
/$Compute_Lift_Process
