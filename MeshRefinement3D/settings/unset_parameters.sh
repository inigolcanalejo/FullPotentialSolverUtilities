
source settings/unset_paths.sh

for path_variable_name in "${!Parameters[@]}"; do
    sed 's|'"$path_variable_name = ${Parameters[$path_variable_name]}"'|'"$path_variable_name = TBD"'|g' -i \
    /$Generate_Mesh_File_Path /$Salome_Converter_File_Path /$Potential_Flow_Analysis_File_Path
done