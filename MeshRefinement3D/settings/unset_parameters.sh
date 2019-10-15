
source settings/unset_paths.sh

for path_variable_name in "${!Parameters[@]}"; do
    for path_file_name in "${!PathNames[@]}"; do
        sed 's|'"$path_variable_name = ${Parameters[$path_variable_name]}"'|'"$path_variable_name = TBD"'|g' -i \
        /${PathNames[$path_file_name]}
    done
done