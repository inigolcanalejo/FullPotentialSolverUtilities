
sed 's|'"salome_output_path = '$salome_output_path'"'|'"salome_output_path = 'TBD'"'|g' -i \
/$Salome_Converter_File_Path /$Generate_Mesh_File_Path /$Generate_Mesh_Middle_File_Path /$Generate_Mesh_Wake_Middle_File_Path /$Generate_Mesh_Wake_Sections_File_Path /$Generate_Mesh_Wake_Sections_No_Wake_File_Path /$Generate_Mesh_Wake_Sections_Box_File_Path

sed 's|'"mdpa_path = '$mdpa_path'"'|'"mdpa_path = 'TBD'"'|g' -i \
/$Salome_Converter_File_Path /$Potential_Flow_Analysis_File_Path /$Generate_Mesh_File_Path /$Generate_Mesh_Middle_File_Path /$Generate_Mesh_Wake_Middle_File_Path /$Generate_Mesh_Wake_Sections_File_Path /$Generate_Mesh_Wake_Sections_No_Wake_File_Path /$Generate_Mesh_Wake_Sections_Box_File_Path

sed 's|'"gid_output_path = '$gid_output_path'"'|'"gid_output_path = 'TBD'"'|g' -i \
/$Potential_Flow_Analysis_File_Path

sed 's|'"input_dir_path = '$input_dir_path'"'|'"input_dir_path = 'TBD'"'|g' -i \
/$Compute_Lift_Process /$Potential_Flow_Analysis_File_Path

for path_variable_name in "${!paths[@]}"; do
    sed 's|'"$path_variable_name = '${paths[$path_variable_name]}'"'|'"$path_variable_name = 'TBD'"'|g' -i \
    /$Compute_Lift_Process /$Potential_Flow_Analysis_File_Path
done


