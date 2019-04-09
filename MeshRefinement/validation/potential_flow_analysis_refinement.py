# makes KratosMultiphysics backward compatible with python 2.6 and 2.7
from __future__ import print_function, absolute_import, division

# Importing Kratos
import KratosMultiphysics

# Importing the base class
from KratosMultiphysics.CompressiblePotentialFlowApplication.potential_flow_analysis import PotentialFlowAnalysis

import os
import loads_output
import shutil
from math import log10, floor

def round_to_1(x):
    return round(x, -int(floor(log10(abs(x)))))

class PotentialFlowAnalysisRefinement(PotentialFlowAnalysis):

    def Run(self):
        self.SetParameters()
        self.ExecuteBeforeDomainLoop()
        # Loop over domains
        for _ in range(self.Number_Of_Domains_Size):
            self.ExecuteBeforeAOALoop()
            # Loop over AOAs
            for _ in range(self.Number_Of_AOAS):
                self.ExecuteBeforeRefinementLoop()
                # Loop over Refinements
                for _ in range(self.Number_Of_Refinements):
                    self.SetParametersBeforeInitialize()

                    self.Initialize()
                    self.RunSolutionLoop()
                    self.Finalize()

                    self.Airfoil_MeshSize *= self.Airfoil_Refinement_Factor
                    #self.FarField_MeshSize /= FarField_Refinement_Factor

                    self.case += 1
                self.ExecuteAfterRefinementLoop()
            self.ExecuteAfterAOALoop()

    def SetParameters(self):
        self.Number_Of_Refinements = TBD
        self.Number_Of_AOAS = TBD
        self.Number_Of_Domains_Size = TBD

        self.Initial_AOA = TBD
        self.AOA_Increment = TBD

        self.Initial_Airfoil_MeshSize = TBD
        self.Airfoil_Refinement_Factor = TBD

        self.Initial_Domain_Size = TBD
        self.Domain_Size_Factor = TBD

        self.case = 0
        self.Domain_Length = self.Initial_Domain_Size
        self.Domain_Width = self.Initial_Domain_Size

        self.Minimum_Airfoil_MeshSize = self.Initial_Airfoil_MeshSize * \
            (self.Airfoil_Refinement_Factor**(self.Number_Of_Refinements-1))

        self.SetFilePaths()

    def SetFilePaths(self):
        self.input_dir_path = 'TBD'
        self.mdpa_path = 'TBD'
        self.gid_output_path = 'TBD'

        self.cl_error_results_directory_name = 'TBD'
        self.cl_error_results_h_file_name = 'TBD'
        self.cl_results_directory_name = 'TBD'
        self.cl_results_h_file_name = 'TBD'
        self.cl_reference_h_file_name = 'TBD'

        self.aoa_results_directory_name = 'TBD'
        self.aoa_results_file_name = 'TBD'

        self.cl_error_results_domain_directory_name = 'TBD'

    def ExecuteBeforeDomainLoop(self):
        self.AOA = self.Initial_AOA
        for _ in range(self.Number_Of_AOAS):
            shutil.rmtree(self.cl_error_results_domain_directory_name + '/AOA_'+ str(self.AOA), ignore_errors=True)
            shutil.copytree(self.cl_error_results_domain_directory_name + '/domain', self.cl_error_results_domain_directory_name + '/AOA_'+ str(self.AOA))
            loads_output.write_figures_domain_cl_error(self.cl_error_results_domain_directory_name + '/AOA_'+ str(self.AOA), self.AOA, self.input_dir_path)
            self.AOA += self.AOA_Increment

    def ExecuteBeforeAOALoop(self):
        self.Domain_Length = int(self.Domain_Length)
        self.Domain_Width = int(self.Domain_Width)
        self.FarField_MeshSize = int(self.Domain_Length / 50.0)
        self.AOA = self.Initial_AOA
        shutil.rmtree(self.gid_output_path + '/DS_' + str(self.Domain_Length), ignore_errors=True)
        os.mkdir(self.gid_output_path + '/DS_' + str(self.Domain_Length))

        shutil.rmtree(self.aoa_results_directory_name + '/DS_' + str(self.Domain_Length), ignore_errors=True)

        with open(self.aoa_results_file_name,'w') as cl_aoa_file:
            cl_aoa_file.flush()



    def ExecuteBeforeRefinementLoop(self):
        self.Airfoil_MeshSize = self.Initial_Airfoil_MeshSize
        os.mkdir(self.gid_output_path + '/DS_' + str(self.Domain_Length) + '/' + 'AOA_' + str(self.AOA))

        with open(self.cl_error_results_h_file_name,'w') as cl_error_file:
            cl_error_file.flush()
        with open(self.cl_results_h_file_name,'w') as cl_file:
            cl_file.flush()
        with open(self.cl_reference_h_file_name,'w') as cl_file:
            cl_file.flush()

        self.cl_error_data_directory_name = 'data/cl_error_DS_' + str(self.Domain_Length) + '_AOA_' + str(self.AOA)
        self.cl_data_directory_name = 'data/cl_DS_' + str(self.Domain_Length) + '_AOA_' + str(self.AOA)

    def SetParametersBeforeInitialize(self):
        self.Airfoil_MeshSize = round_to_1(self.Airfoil_MeshSize)
        print("\n\tCase ", self.case, "\n")

        mdpa_file_name = self.mdpa_path + '/naca0012_Case_' + str(self.case) + '_DS_' + str(self.Domain_Length) + '_AOA_' + str(
            self.AOA) + '_Far_Field_Mesh_Size_' + str(self.FarField_MeshSize) + '_Airfoil_Mesh_Size_' + str(self.Airfoil_MeshSize)

        self.project_parameters["solver_settings"]["model_import_settings"]["input_filename"].SetString(
            mdpa_file_name)

        gid_output_file_name = self.gid_output_path + '/DS_' + str(self.Domain_Length) + '/' + 'AOA_' + str(
            self.AOA) + '/' + self.project_parameters["problem_data"]["problem_name"].GetString() + '_Case_' + str(
            self.case) + '_DS_' + str(self.Domain_Length) + '_AOA_' + str(self.AOA) + '_Far_Field_Mesh_Size_' + str(
            self.FarField_MeshSize) + '_Airfoil_Mesh_Size_' + str(self.Airfoil_MeshSize)

        self.project_parameters["output_processes"]["gid_output"][0]["Parameters"]["output_name"].SetString(
            gid_output_file_name)

        self.project_parameters["processes"]["boundary_conditions_process_list"][2]["Parameters"]["angle_of_attack"].SetDouble(
            self.AOA)
        self.project_parameters["processes"]["boundary_conditions_process_list"][2]["Parameters"]["airfoil_meshsize"].SetDouble(
            self.Airfoil_MeshSize)
        self.project_parameters["processes"]["boundary_conditions_process_list"][2]["Parameters"]["minimum_airfoil_meshsize"].SetDouble(
            self.Minimum_Airfoil_MeshSize)
        self.project_parameters["processes"]["boundary_conditions_process_list"][2]["Parameters"]["domain_size"].SetDouble(
            self.Domain_Length)

        self._solver = self._CreateSolver()
        self._GetSolver().AddVariables()

    def ExecuteAfterRefinementLoop(self):
        loads_output.write_figures_cl_error(self.cl_error_data_directory_name, self.AOA, self.input_dir_path, self.Domain_Length)
        loads_output.write_figures_cl(self.cl_data_directory_name, self.AOA, self.input_dir_path, self.Domain_Length)

        shutil.copytree(self.cl_results_directory_name, self.input_dir_path + '/plots/cl/' + self.cl_data_directory_name)
        shutil.copytree(self.cl_error_results_directory_name, self.input_dir_path + '/plots/cl_error/' + self.cl_error_data_directory_name)

        os.remove(self.cl_error_results_h_file_name)
        os.remove(self.cl_results_h_file_name)
        os.remove(self.cl_reference_h_file_name)
        self.AOA += self.AOA_Increment

    def ExecuteAfterAOALoop(self):
        shutil.copytree(self.aoa_results_directory_name + '/data', self.aoa_results_directory_name + '/DS_' + str(self.Domain_Length))

        self.Domain_Length *= self.Domain_Size_Factor
        self.Domain_Width *= self.Domain_Size_Factor

    def Finalize(self):
        super(PotentialFlowAnalysisRefinement,self).Finalize()
        self.project_parameters["solver_settings"].RemoveValue("element_replace_settings")
        #self.project_parameters["solver_settings"]["element_replace_settings"]["element_name"].SetString("IncompressiblePotentialFlowElement")
        #self.project_parameters["solver_settings"]["element_replace_settings"]["condition_name"].SetString("PotentialWallCondition")
        self.model.Reset()
