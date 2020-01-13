#makes KratosMultiphysics backward compatible with python 2.6 and 2.7
from __future__ import print_function, absolute_import, division

import KratosMultiphysics
# Importing the base class
from potential_flow_analysis_refinement import PotentialFlowAnalysisRefinement

"""
For user-scripting it is intended that a new class is derived
from PotentialFlowAnalysis to do modifications
"""

if __name__ == "__main__":

    with open("ProjectParameters.json",'r') as parameter_file:
        parameters = KratosMultiphysics.Parameters(parameter_file.read())

    model = KratosMultiphysics.Model()
    simulation = PotentialFlowAnalysisRefinement(model,parameters)
    simulation.Run()