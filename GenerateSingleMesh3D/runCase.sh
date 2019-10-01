#Run salome: generate geometry and mesh
rm salome_output/*
rm case/wake_stl.stl
python3 runSalome.py

#Convert salomes mesh into mdpa
source /home/inigo/Documents/paths/salomeConverter.sh
rm case/salome_wing.mdpa
python3 use_converter_wing.py

# #Run Kratos
# source /home/inigo/Documents/paths/kratosMaster.sh
# #source /home/inigo/Documents/paths/kratosMerge.sh
# cd case/
# #python3 MainKratos_withoutWake.py
# python3 MainKratos.py