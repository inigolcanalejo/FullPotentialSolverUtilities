#Run salome: generate geometry and mesh
rm salome_output/*
python3 runSalome.py

#Convert salomes mesh into mdpa
source /home/inigo/Documents/paths/salomeConverter.sh
rm case/salome_wing.mdpa
python3 use_converter_wing.py

#Run Kratos
source /home/inigo/Documents/paths/kratosMaster3.sh
cd case/
#python3 MainKratos_withoutWake.py
python3 MainKratos.py