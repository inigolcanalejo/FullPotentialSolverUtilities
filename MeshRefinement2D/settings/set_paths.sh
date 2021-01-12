Compute_Lift_Process=$PWD/runKratos/compute_lift_process_2d_refinement.py

declare -A paths

paths[cl_error_results_directory_name]=$input_dir_path/plots/cl_error/data/cl
paths[cl_error_results_h_file_name]=${paths[cl_error_results_directory_name]}/cl_error_results_h.dat
paths[cl_jump_error_results_h_file_name]=${paths[cl_error_results_directory_name]}/cl_jump_error_results_h.dat
paths[cl_far_field_error_results_h_file_name]=${paths[cl_error_results_directory_name]}/cl_far_field_error_results_h.dat
paths[cl_results_directory_name]=$input_dir_path/plots/cl/data/cl
paths[cl_results_h_file_name]=${paths[cl_results_directory_name]}/cl_results_h.dat
paths[cl_jump_results_h_file_name]=${paths[cl_results_directory_name]}/cl_jump_results_h.dat
paths[cl_reference_h_file_name]=${paths[cl_results_directory_name]}/cl_reference_h.dat
paths[cm_results_directory_name]=$input_dir_path/plots/cm/data/cm
paths[cm_results_h_file_name]=${paths[cm_results_directory_name]}/cm_results_h.dat
paths[cm_reference_h_file_name]=${paths[cm_results_directory_name]}/cm_reference_h.dat
paths[cm_error_results_directory_name]=$input_dir_path/plots/cm_error/data/cm_error
paths[cm_error_results_h_file_name]=${paths[cm_error_results_directory_name]}/cm_error_results_h.dat
paths[aoa_results_directory_name]=$input_dir_path/plots/aoa
paths[aoa_results_file_name]=$input_dir_path/plots/aoa/data/cl_aoa.dat
paths[cl_error_results_domain_directory_name]=$input_dir_path/plots/cl_error_domain_size/data
paths[cp_results_file_name]=$input_dir_path/plots/cp/data/0_original/cp_results.dat
paths[cp_tikz_file_name]=$input_dir_path/plots/cp/data/0_original/cp.tikz

for path_variable_name in "${!paths[@]}"; do
    sed 's|'"$path_variable_name = 'TBD'"'|'"$path_variable_name = '${paths[$path_variable_name]}'"'|g' -i \
    /$Compute_Lift_Process /$Potential_Flow_Analysis_File_Path
done


sed 's|'"salome_output_path = 'TBD'"'|'"salome_output_path = '$salome_output_path'"'|g' -i \
/$Salome_Converter_File_Path /$Generate_Mesh_Cosine_File_Path /$Generate_Mesh_Cosine_Wake_File_Path \
/$Generate_Mesh_Membrane_File_Path /$Salome_Converter_Membrane_File_Path /$Generate_Mesh_File_Path

sed 's|'"mdpa_path = 'TBD'"'|'"mdpa_path = '$mdpa_path'"'|g' -i \
/$Salome_Converter_File_Path /$Potential_Flow_Analysis_File_Path /$Salome_Converter_Membrane_File_Path

sed 's|'"gid_output_path = 'TBD'"'|'"gid_output_path = '$gid_output_path'"'|g' -i \
/$Potential_Flow_Analysis_File_Path

sed 's|'"input_dir_path = 'TBD'"'|'"input_dir_path = '$input_dir_path'"'|g' -i \
/$Compute_Lift_Process /$Potential_Flow_Analysis_File_Path
