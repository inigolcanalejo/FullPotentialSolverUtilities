# makes KratosMultiphysics backward compatible with python 2.6 and 2.7
from __future__ import print_function, absolute_import, division

# Importing Kratos
import KratosMultiphysics

# Importing the base class
from KratosMultiphysics.CompressiblePotentialFlowApplication.potential_flow_analysis import PotentialFlowAnalysis

import os
import loads_output
import shutil
import subprocess
from PyPDF2 import PdfFileReader, PdfFileMerger
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
        self.ExecuteAfterDomainLoop()

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

        self.case = 1
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
        self.cl_jump_error_results_h_file_name = 'TBD'
        self.cl_far_field_error_results_h_file_name = 'TBD'
        self.cl_results_directory_name = 'TBD'
        self.cl_results_h_file_name = 'TBD'
        self.cl_jump_results_h_file_name = 'TBD'
        self.cl_reference_h_file_name = 'TBD'

        self.aoa_results_directory_name = 'TBD'
        self.aoa_results_file_name = 'TBD'

        self.cl_error_results_domain_directory_name = 'TBD'

        self.cm_results_directory_name = 'TBD'
        self.cm_results_h_file_name = 'TBD'
        self.cm_reference_h_file_name = self.input_dir_path + '/plots/cm/data/cm/cm_reference_h.dat'
        self.cm_error_results_directory_name = 'TBD'
        self.cm_error_results_h_file_name = 'TBD'

    def ExecuteBeforeDomainLoop(self):
        self.reference_case_name = self.project_parameters["processes"]["boundary_conditions_process_list"][2]["Parameters"]["reference_case_name"].GetString()
        loads_output.create_plots_directory_tree(self.input_dir_path, self.reference_case_name)
        self.latex_output = open(self.input_dir_path + '/plots/latex_output.txt', 'w')
        self.latex_output.flush()
        self.AOA = self.Initial_AOA
        for _ in range(self.Number_Of_AOAS):
            shutil.rmtree(self.cl_error_results_domain_directory_name + '/AOA_'+ str(self.AOA), ignore_errors=True)
            shutil.copytree(self.cl_error_results_domain_directory_name + '/domain', self.cl_error_results_domain_directory_name + '/AOA_'+ str(self.AOA))
            loads_output.write_figures_domain_cl_error(self.cl_error_results_domain_directory_name + '/AOA_'+ str(self.AOA), self.AOA, self.input_dir_path)
            self.AOA += self.AOA_Increment

        self.merger_all_cp = PdfFileMerger()

    def ExecuteBeforeAOALoop(self):
        self.Domain_Length = int(self.Domain_Length)
        self.Domain_Width = int(self.Domain_Width)
        self.FarField_MeshSize = int(self.Domain_Length / 50.0)
        self.AOA = self.Initial_AOA
        if not os.path.exists(self.gid_output_path):
            os.makedirs(self.gid_output_path)
        if os.path.exists(self.gid_output_path + '/DS_' + str(self.Domain_Length)):
            shutil.rmtree(self.gid_output_path + '/DS_' + str(self.Domain_Length), ignore_errors=True)
        os.mkdir(self.gid_output_path + '/DS_' + str(self.Domain_Length))

        if os.path.exists(self.aoa_results_directory_name + '/DS_' + str(self.Domain_Length)):
            shutil.rmtree(self.aoa_results_directory_name + '/DS_' + str(self.Domain_Length))

        with open(self.aoa_results_file_name,'w') as cl_aoa_file:
            cl_aoa_file.flush()

        cp_data_directory_start_ds = self.input_dir_path + '/plots/cp/data/DS_' + str(self.Domain_Length)
        os.mkdir(cp_data_directory_start_ds)

    def ExecuteBeforeRefinementLoop(self):
        self.Airfoil_MeshSize = self.Initial_Airfoil_MeshSize
        os.mkdir(self.gid_output_path + '/DS_' + str(self.Domain_Length) + '/' + 'AOA_' + str(self.AOA))

        with open(self.cl_error_results_h_file_name,'w') as cl_error_file:
            cl_error_file.flush()
        with open(self.cl_jump_error_results_h_file_name,'w') as cl_error_file:
            cl_error_file.flush()
        with open(self.cl_far_field_error_results_h_file_name,'w') as cl_error_file:
            cl_error_file.flush()
        with open(self.cl_results_h_file_name,'w') as cl_file:
            cl_file.flush()
        with open(self.cl_jump_results_h_file_name,'w') as cl_file:
            cl_file.flush()
        with open(self.cl_reference_h_file_name,'w') as cl_file:
            cl_file.flush()

        self.cl_error_data_directory_name = 'data/cl_error_DS_' + str(self.Domain_Length) + '_AOA_' + str(self.AOA)
        self.cl_data_directory_name = 'data/cl_DS_' + str(self.Domain_Length) + '_AOA_' + str(self.AOA)
        self.cm_data_directory_name = 'data/cm_DS_' + str(self.Domain_Length) + '_AOA_' + str(self.AOA)
        self.cm_error_data_directory_name = 'data/cm_error_DS_' + str(self.Domain_Length) + '_AOA_' + str(self.AOA)

        self.cp_data_directory_start = self.input_dir_path + '/plots/cp/data/DS_' + str(self.Domain_Length) + '/' + 'AOA_' + str(self.AOA)
        os.mkdir(self.cp_data_directory_start)

        self.merger_refinement_cp = PdfFileMerger()

    def InitializeSolutionStep(self):
        super(PotentialFlowAnalysisRefinement, self).InitializeSolutionStep()
        self.cp_results_directory_name = self.input_dir_path + '/plots/cp/data/0_original'
        self.step = self._GetSolver().GetComputingModelPart().ProcessInfo[KratosMultiphysics.STEP]
        self.cp_data_directory_name = self.cp_data_directory_start + '/Case_' + str(self.case) + '_DS_' + str(self.Domain_Length) + '_AOA_' + str(
            self.AOA) + '_Far_Field_Mesh_Size_' + str(self.FarField_MeshSize) + '_Airfoil_Mesh_Size_' + str(self.Airfoil_MeshSize) + '_Step_' + str(self.step)

    def FinalizeSolutionStep(self):
        super(PotentialFlowAnalysisRefinement, self).FinalizeSolutionStep()
        loads_output.write_cp_figures(self.cp_data_directory_name, self.AOA, self.case, self.Airfoil_MeshSize, self.FarField_MeshSize, self.input_dir_path)
        shutil.copytree(self.cp_results_directory_name, self.cp_data_directory_name)

        latex = subprocess.Popen(['pdflatex', '-interaction=batchmode', self.input_dir_path + '/plots/cp/cp.tex'], stdout=self.latex_output)
        latex.communicate()

        self.step = self._GetSolver().GetComputingModelPart().ProcessInfo[KratosMultiphysics.STEP]

        cp_file_name = self.input_dir_path + '/plots/cp/plots/cp_Case_' + str(self.case) + '_DS_' + str(self.Domain_Length) + '_AOA_' + str(
                self.AOA) + '_Far_Field_Mesh_Size_' + str(self.FarField_MeshSize) + '_Airfoil_Mesh_Size_' + str(self.Airfoil_MeshSize) + '_Step_' + str(self.step) + '.pdf'
        shutil.copyfile('cp.pdf',cp_file_name)
        self.merger_refinement_cp.append(PdfFileReader(cp_file_name), 'case_' + str(self.case))
        self.merger_all_cp.append(PdfFileReader(cp_file_name), 'case_' + str(self.case))

    def SetParametersBeforeInitialize(self):
        loads_output.write_case(self.case, self.AOA, self.FarField_MeshSize, self.Airfoil_MeshSize, self.input_dir_path)
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
        loads_output.write_figures_cm(self.cm_data_directory_name, self.AOA, self.input_dir_path, self.Domain_Length)
        loads_output.write_figures_cm_error(self.cm_error_data_directory_name, self.AOA, self.input_dir_path, self.Domain_Length)

        shutil.copytree(self.cl_results_directory_name, self.input_dir_path + '/plots/cl/' + self.cl_data_directory_name)
        shutil.copytree(self.cl_error_results_directory_name, self.input_dir_path + '/plots/cl_error/' + self.cl_error_data_directory_name)
        shutil.copytree(self.cm_results_directory_name, self.input_dir_path + '/plots/cm/' + self.cm_data_directory_name)
        shutil.copytree(self.cm_error_results_directory_name, self.input_dir_path + '/plots/cm_error/' + self.cm_error_data_directory_name)

        os.remove(self.cl_error_results_h_file_name)
        os.remove(self.cl_jump_error_results_h_file_name)
        os.remove(self.cl_far_field_error_results_h_file_name)
        os.remove(self.cm_results_h_file_name)
        os.remove(self.cl_jump_results_h_file_name)
        os.remove(self.cm_reference_h_file_name)
        os.remove(self.cm_error_results_h_file_name)
        os.remove(self.cl_results_h_file_name)
        os.remove(self.cl_reference_h_file_name)

        cp_refienment_file_name = self.input_dir_path + '/plots/cp/cp_DS_' + str(self.Domain_Length) + '_AOA_' + str(self.AOA) + '.pdf'
        self.merger_refinement_cp.write(cp_refienment_file_name)
        self.AOA += self.AOA_Increment

    def ExecuteAfterAOALoop(self):
        latex_aoa = subprocess.Popen(['pdflatex', '-interaction=batchmode', '-output-directory', self.input_dir_path + '/plots/aoa/data', self.input_dir_path + '/plots/aoa/data/cl_aoa.tex'], stdout=self.latex_output)
        latex_aoa.communicate()
        shutil.copytree(self.aoa_results_directory_name + '/data', self.aoa_results_directory_name + '/DS_' + str(self.Domain_Length))

        self.Domain_Length *= self.Domain_Size_Factor
        self.Domain_Width *= self.Domain_Size_Factor

    def ExecuteAfterDomainLoop(self):
        cp_final_global_file_name = self.input_dir_path + '/plots/cp/cp_all.pdf'
        self.merger_all_cp.write(cp_final_global_file_name)

    def Finalize(self):
        super(PotentialFlowAnalysisRefinement,self).Finalize()
        self.project_parameters["solver_settings"].RemoveValue("element_replace_settings")
        #self.project_parameters["solver_settings"]["element_replace_settings"]["element_name"].SetString("IncompressiblePotentialFlowElement")
        #self.project_parameters["solver_settings"]["element_replace_settings"]["condition_name"].SetString("PotentialWallCondition")
        self.model.Reset()
