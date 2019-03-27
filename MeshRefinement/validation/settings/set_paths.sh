Compute_Lift_Process=$PWD/compute_lift_process_2d_refinement.py
cl_error_results_directory_name=$input_dir_path/plots/cl_error/data/cl
cl_error_results_h_file_name=$cl_error_results_directory_name/cl_error_results_h.dat

sed 's|'"salome_output_path = 'TBD'"'|'"salome_output_path = '$salome_output_path'"'|g' -i \
/$Salome_Converter_File_Path /$Generate_Mesh_Cosine_File_Path 

sed 's|'"mdpa_path = 'TBD'"'|'"mdpa_path = '$mdpa_path'"'|g' -i \
/$Salome_Converter_File_Path /$Potential_Flow_Analysis_File_Path

sed 's|'"gid_output_path = 'TBD'"'|'"gid_output_path = '$gid_output_path'"'|g' -i \
/$Potential_Flow_Analysis_File_Path

sed 's|'"input_dir_path = 'TBD'"'|'"input_dir_path = '$input_dir_path'"'|g' -i \
/$Compute_Lift_Process /$Potential_Flow_Analysis_File_Path

sed 's|'"cl_error_results_directory_name = 'TBD'"'|'"cl_error_results_directory_name = '$cl_error_results_directory_name'"'|g' -i \
/$Potential_Flow_Analysis_File_Path

sed 's|'"cl_error_results_h_file_name = 'TBD'"'|'"cl_error_results_h_file_name = '$cl_error_results_h_file_name'"'|g' -i \
/$Potential_Flow_Analysis_File_Path
