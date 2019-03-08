
ProjectParameters_File_Path=$PWD/ProjectParameters.json

sed 's|'"ELEMENT TBD"'|'"$Element"'|g' -i /$ProjectParameters_File_Path

sed 's|'"WAKE PROCESS TBD"'|'"$WakeProcess"'|g' -i /$ProjectParameters_File_Path