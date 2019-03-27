# makes KratosMultiphysics backward compatible with python 2.6 and 2.7
from __future__ import print_function, absolute_import, division

# Importing Kratos
import KratosMultiphysics

# Importing the base class
from KratosMultiphysics.CompressiblePotentialFlowApplication.potential_flow_analysis import PotentialFlowAnalysis

class PotentialFlowAnalysisRefinement(PotentialFlowAnalysis):

    def __init__(self, Model, settings, AOA):
        super(PotentialFlowAnalysisRefinement,self).__init__(Model,settings)
        self.AOA = AOA

    def FinalizeSolutionStep(self):
        self._GetSolver().FinalizeSolutionStep()

        for process in self._GetListOfProcesses():
            process.ExecuteFinalizeSolutionStep()