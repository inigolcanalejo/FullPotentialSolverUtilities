# makes KratosMultiphysics backward compatible with python 2.6 and 2.7
from __future__ import print_function, absolute_import, division

# Importing Kratos
import KratosMultiphysics

# Importing the base class
from KratosMultiphysics.CompressiblePotentialFlowApplication.potential_flow_analysis import PotentialFlowAnalysis

import os
import shutil
from math import log10, floor

def round_to_1(x):
    return round(x, -int(floor(log10(abs(x)))))

class PotentialFlowAnalysisRefinement(PotentialFlowAnalysis):

    def Run(self):
        mdpa_path = 'TBD'
        gid_output_path = 'TBD'

        Number_Of_Refinements = TBD
        Number_Of_AOAS = TBD
        Number_Of_Domains_Size = TBD

        Initial_AOA = TBD
        AOA_Increment = TBD

        Initial_Airfoil_MeshSize = TBD
        Airfoil_Refinement_Factor = TBD

        Initial_Domain_Size = TBD
        Domain_Size_Factor = TBD

        case = 0
        Domain_Length = Initial_Domain_Size
        Domain_Width = Initial_Domain_Size

        # Loop over domains
        for k in range(Number_Of_Domains_Size):
            Domain_Length = int(Domain_Length)
            Domain_Width = int(Domain_Width)
            FarField_MeshSize = int(Domain_Length / 50.0)
            AOA = Initial_AOA
            shutil.rmtree(gid_output_path + '/DS_' +
                          str(Domain_Length), ignore_errors=True)
            os.mkdir(gid_output_path + '/DS_' + str(Domain_Length))

            # Loop over AOAs
            for j in range(Number_Of_AOAS):
                Airfoil_MeshSize = Initial_Airfoil_MeshSize

                os.mkdir(gid_output_path + '/DS_' + str(Domain_Length) + '/' + 'AOA_' + str(AOA))

                # Loop over Refinements
                for i in range(Number_Of_Refinements):
                    Airfoil_MeshSize = round_to_1(Airfoil_MeshSize)
                    print("\n\tCase ", case, "\n")

                    mdpa_file_name = mdpa_path + '/naca0012_Case_' + str(case) + '_DS_' + str(Domain_Length) + '_AOA_' + str(
                        AOA) + '_Far_Field_Mesh_Size_' + str(FarField_MeshSize) + '_Airfoil_Mesh_Size_' + str(Airfoil_MeshSize)

                    self.project_parameters["solver_settings"]["model_import_settings"]["input_filename"].SetString(
                        mdpa_file_name)

                    gid_output_file_name = gid_output_path + '/DS_' + str(Domain_Length) + '/' + 'AOA_' + str(
                        AOA) + '/' + self.project_parameters["problem_data"]["problem_name"].GetString() + '_Case_' + str(
                        case) + '_DS_' + str(Domain_Length) + '_AOA_' + str(AOA) + '_Far_Field_Mesh_Size_' + str(
                        FarField_MeshSize) + '_Airfoil_Mesh_Size_' + str(Airfoil_MeshSize)

                    self.project_parameters["output_processes"]["gid_output"][0]["Parameters"]["output_name"].SetString(
                        gid_output_file_name)

                    self.project_parameters["processes"]["boundary_conditions_process_list"][2]["Parameters"]["angle_of_attack"].SetDouble(
                        AOA)
                    self.project_parameters["processes"]["boundary_conditions_process_list"][2]["Parameters"]["airfoil_meshsize"].SetDouble(
                        Airfoil_MeshSize)

                    self._solver = self._CreateSolver()
                    self._GetSolver().AddVariables()
                    
                    self.Initialize()
                    self.RunSolutionLoop()
                    self.Finalize()

                    Airfoil_MeshSize *= Airfoil_Refinement_Factor
                    #FarField_MeshSize /= FarField_Refinement_Factor

                    case += 1
                AOA += AOA_Increment
            Domain_Length /= Domain_Size_Factor
            Domain_Width /= Domain_Size_Factor

    def Finalize(self):
        super(PotentialFlowAnalysisRefinement,self).Finalize()
        self.model.Reset()