import subprocess
import time as time

start_time = time.time()

salome_cmd = "salome -t python"
#salome_script_name = "generate_finite_wing.py"
#salome_script_name = "generate_finite_wing_middle.py"
#salome_script_name = "generate_finite_wing_wake_middle.py"
#salome_script_name = "generate_finite_wing_wake_sections.py"
#salome_script_name = "generate_finite_wing_wake_sections_no_wake.py"
salome_script_name = "generate_finite_wing_wake_sections_box.py"
# salome_script_name = "generate_onera_m6.py"
# salome_script_name = "generate_onera_m6_refinement_wake.py"

salome_exe = " ".join([salome_cmd, salome_script_name])

sp = subprocess.Popen(["/bin/bash", "-i", "-c", salome_exe])

sp.communicate()

exe_time = time.time() - start_time

print('Executing SALOME with "' + salome_script_name +
      '" took ' + str(round(exe_time, 2)) + ' sec')
