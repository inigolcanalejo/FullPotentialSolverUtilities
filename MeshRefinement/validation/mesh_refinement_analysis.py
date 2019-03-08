# makes KratosMultiphysics backward compatible with python 2.6 and 2.7
from __future__ import print_function, absolute_import, division

# Importing Kratos
import KratosMultiphysics

# Importing the solvers
import KratosMultiphysics.ExternalSolversApplication

# Importing the base class
from KratosMultiphysics.CompressiblePotentialFlowApplication.potential_flow_analysis import PotentialFlowAnalysis

class MeshRefinementAnalysis(PotentialFlowAnalysis):

    def RunSolutionLoop(self):
        print('entering RunSolutionLoop MeshRefinementAnalysis')
        super(MeshRefinementAnalysis,self).RunSolutionLoop()