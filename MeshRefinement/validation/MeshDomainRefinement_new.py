from __future__ import print_function, absolute_import, division #makes KratosMultiphysics backward compatible with python 2.6 and 2.7

import KratosMultiphysics
from mesh_refinement_analysis import MeshRefinementAnalysis
import os
from math import log10, floor

"""
For user-scripting it is intended that a new class is derived
from PotentialFlowAnalysis to do modifications
"""

def round_to_1(x):
    return round(x, -int(floor(log10(abs(x)))))

if __name__ == "__main__":

    with open("ProjectParameters_new.json",'r') as parameter_file:
        parameters = KratosMultiphysics.Parameters(parameter_file.read())

    work_dir = 'TBD'

    input_mdpa_path = work_dir + '/mdpas/'
    output_gid_path = '/media/inigo/10740FB2740F9A1C/Outputs/05_MeshRefinement/'

    Number_Of_Refinements = TBD
    Number_Of_AOAS = TBD
    Number_Of_Domains_Size = TBD

    Initial_AOA = TBD
    AOA_Increment = TBD

    Initial_Airfoil_MeshSize = TBD
    Airfoil_Refinement_Factor = TBD

    Initial_FarField_MeshSize = TBD
    FarField_Refinement_Factor = TBD

    Initial_Domain_Size = TBD
    Domain_Size_Factor = TBD

    case = 0
    Domain_Length = Initial_Domain_Size
    Domain_Width = Initial_Domain_Size

    for k in range(Number_Of_Domains_Size):
        Domain_Length = int(Domain_Length)
        Domain_Width = int(Domain_Width)
        FarField_MeshSize = int(Domain_Length / 50.0)
        AOA = Initial_AOA
        os.mkdir(output_gid_path + 'DS_' + str(Domain_Length))

        for j in range(Number_Of_AOAS):
            Airfoil_MeshSize = Initial_Airfoil_MeshSize

            os.mkdir(output_gid_path + 'DS_' + str(Domain_Length) + '/' + 'AOA_' + str(AOA))

            for i in range(Number_Of_Refinements):
                Airfoil_MeshSize = round_to_1(Airfoil_MeshSize)
                print("\n\tCase ", case, "\n")

                mdpa_file_name = input_mdpa_path + 'naca0012_Case_' + str(case) + '_DS_' + str(Domain_Length) + '_AOA_' + str(
                    AOA) + '_Far_Field_Mesh_Size_' + str(FarField_MeshSize) + '_Airfoil_Mesh_Size_' + str(Airfoil_MeshSize)

                parameters["solver_settings"]["model_import_settings"]["input_filename"].SetString(mdpa_file_name)

                gid_output_file_name = output_gid_path + 'DS_' + str(Domain_Length) + '/' + 'AOA_' + str(
                    AOA) + '/' + parameters["problem_data"]["problem_name"].GetString()+ '_Case_' + str(
                    case) + '_DS_' + str(Domain_Length) + '_AOA_' + str(AOA) + '_Far_Field_Mesh_Size_' + str(
                    FarField_MeshSize) + '_Airfoil_Mesh_Size_' + str(Airfoil_MeshSize)

                parameters["output_processes"]["gid_output"][0]["Parameters"]["output_name"].SetString(gid_output_file_name)

                model = KratosMultiphysics.Model()
                simulation = MeshRefinementAnalysis(model,parameters)
                simulation.Run()

                Airfoil_MeshSize *= Airfoil_Refinement_Factor
                #FarField_MeshSize /= FarField_Refinement_Factor

                case +=1
            AOA += AOA_Increment
        Domain_Length /= Domain_Size_Factor
        Domain_Width /= Domain_Size_Factor
