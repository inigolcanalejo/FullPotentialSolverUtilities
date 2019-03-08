# makes KratosMultiphysics backward compatible with python 2.6 and 2.7
from __future__ import print_function, absolute_import, division

# Importing Kratos
import KratosMultiphysics

# Importing the solvers
import KratosMultiphysics.ExternalSolversApplication

# Importing the base class
from KratosMultiphysics.CompressiblePotentialFlowApplication.potential_flow_analysis import PotentialFlowAnalysis

class MeshRefinementAnalysis(PotentialFlowAnalysis):

    def __init__(self,model,project_parameters,case,Domain_Length,AOA,FarField_MeshSize,Airfoil_MeshSize):

        mdpa_path = 'TBD'
        gid_output_path = 'TBD'

        mdpa_file_name = mdpa_path + '/naca0012_Case_' + str(case) + '_DS_' + str(Domain_Length) + '_AOA_' + str(
                    AOA) + '_Far_Field_Mesh_Size_' + str(FarField_MeshSize) + '_Airfoil_Mesh_Size_' + str(Airfoil_MeshSize)

        project_parameters["solver_settings"]["model_import_settings"]["input_filename"].SetString(mdpa_file_name)

        gid_output_file_name = gid_output_path + '/DS_' + str(Domain_Length) + '/' + 'AOA_' + str(
                    AOA) + '/' + project_parameters["problem_data"]["problem_name"].GetString()+ '_Case_' + str(
                    case) + '_DS_' + str(Domain_Length) + '_AOA_' + str(AOA) + '_Far_Field_Mesh_Size_' + str(
                    FarField_MeshSize) + '_Airfoil_Mesh_Size_' + str(Airfoil_MeshSize)

        project_parameters["output_processes"]["gid_output"][0]["Parameters"]["output_name"].SetString(gid_output_file_name)

        super(MeshRefinementAnalysis,self).__init__(model,project_parameters)

    def RunSolutionLoop(self):
        print('entering RunSolutionLoop MeshRefinementAnalysis')
        super(MeshRefinementAnalysis,self).RunSolutionLoop()