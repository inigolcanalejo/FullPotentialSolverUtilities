
sed 's|'"salome_output_path = '$salome_output_path'"'|'"salome_output_path = 'TBD'"'|g' -i \
/$Salome_Converter_File_Path /$Generate_Mesh_Cosine_File_Path 

sed 's|'"mdpa_path = '$mdpa_path'"'|'"mdpa_path = 'TBD'"'|g' -i \
/$Salome_Converter_File_Path /$Potential_Flow_Analysis_File_Path

sed 's|'"gid_output_path = '$gid_output_path'"'|'"gid_output_path = 'TBD'"'|g' -i \
/$Potential_Flow_Analysis_File_Path

sed 's|'"input_dir_path = '$input_dir_path'"'|'"input_dir_path = 'TBD'"'|g' -i \
/$Compute_Lift_Process /$Potential_Flow_Analysis_File_Path

sed 's|'"cl_error_results_directory_name = '$cl_error_results_directory_name'"'|'"cl_error_results_directory_name = 'TBD'"'|g' -i \
/$Potential_Flow_Analysis_File_Path

sed 's|'"cl_error_results_h_file_name = '$cl_error_results_h_file_name'"'|'"cl_error_results_h_file_name = 'TBD'"'|g' -i \
/$Potential_Flow_Analysis_File_Path

