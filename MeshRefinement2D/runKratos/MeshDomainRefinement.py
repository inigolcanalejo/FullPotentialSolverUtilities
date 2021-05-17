#makes KratosMultiphysics backward compatible with python 2.6 and 2.7
from __future__ import print_function, absolute_import, division

import KratosMultiphysics
# Importing the base class
from potential_flow_analysis_refinement import PotentialFlowAnalysisRefinement
import time as time

"""
For user-scripting it is intended that a new class is derived
from PotentialFlowAnalysis to do modifications
"""

start_time = time.time()
if __name__ == "__main__":

    with open("ProjectParameters_new.json",'r') as parameter_file:
        parameters = KratosMultiphysics.Parameters(parameter_file.read())

    model = KratosMultiphysics.Model()
    simulation = PotentialFlowAnalysisRefinement(model,parameters)
    simulation.Run()

exe_time = time.time() - start_time

print('Kratos took ' + str(round(exe_time, 2)) + ' sec')