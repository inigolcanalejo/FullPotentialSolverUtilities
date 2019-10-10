# makes KratosMultiphysics backward compatible with python 2.6 and 2.7
from __future__ import print_function, absolute_import, division

# Importing Kratos
import KratosMultiphysics

# Importing the base class
from KratosMultiphysics.CompressiblePotentialFlowApplication.potential_flow_analysis import PotentialFlowAnalysis

import os
#import loads_output
import shutil
import subprocess
from PyPDF2 import PdfFileReader, PdfFileMerger
from math import log10, floor

def round_to_1(x):
    return round(x, -int(floor(log10(abs(x)))))

class PotentialFlowAnalysisRefinement(PotentialFlowAnalysis):

    def Run(self):
        self.SetParameters()
        self.ExecuteBeforeAOALoop()
        # Loop over domains
        for _ in range(self.Number_Of_AOAS):
            self.ExecuteBeforeDomainRefinementLoop()
            # Loop over AOAs
            for _ in range(self.Number_Of_Domains_Refinements):
                self.ExecuteBeforeWingRefinementLoop()
                # Loop over Refinements
                for _ in range(self.Number_Of_Wing_Refinements):
                    #self.MakeCpDir()
                    self.SetParametersBeforeInitialize()

                    self.Initialize()
                    self.RunSolutionLoop()
                    self.Finalize()

                    #self.OutputCp()
                    self.Growth_Rate_Wing -= self.Growth_Rate_Wing_Refinement_Factor
                    #self.FarField_MeshSize /= FarField_Refinement_Factor

                    self.case += 1
                self.ExecuteAfterWingRefinementLoop()
            self.ExecuteAfterDomainRefinementLoop()
        #self.ExecuteAfterAOALoop()

    def SetParameters(self):
        self.Wing_span = 4.0
        self.Smallest_Airfoil_Mesh_Size = 0.01
        self.Biggest_Airfoil_Mesh_Size = 0.05

        self.Number_Of_AOAS = 1
        self.Number_Of_Domains_Refinements = 1
        self.Number_Of_Wing_Refinements = 1

        self.Initial_AOA = 5.0
        self.AOA_Increment = 2.0

        self.Initial_Growth_Rate_Wing = 0.7
        self.Growth_Rate_Wing_Refinement_Factor = 0.1

        self.Initial_Growth_Rate_Domain = 0.7
        self.Growth_Rate_Domain_Refinement_Factor = 0.1

        self.case = 0
        self.Domain_Length = 100
        self.Domain_Width = self.Domain_Length
        self.FarField_MeshSize = int(self.Domain_Length / 10.0)

        # self.Minimum_Airfoil_MeshSize = self.Initial_Airfoil_MeshSize * \
        #     (self.Airfoil_Refinement_Factor**(self.Number_Of_Refinements-1))

        self.SetFilePaths()

    def SetFilePaths(self):
        self.input_dir_path = '/media/inigo/10740FB2740F9A1C/3d_results'
        self.mdpa_path = '/media/inigo/10740FB2740F9A1C/3d_results/mdpas'
        self.gid_output_path = '/media/inigo/10740FB2740F9A1C/3d_results/output_gid'

        # self.cl_error_results_directory_name = '/media/inigo/10740FB2740F9A1C/3d_results/plots/cl_error/data/cl'
        # self.cl_error_results_h_file_name = '/media/inigo/10740FB2740F9A1C/3d_results/plots/cl_error/data/cl/cl_error_results_h.dat'
        # self.cl_results_directory_name = '/media/inigo/10740FB2740F9A1C/3d_results/plots/cl/data/cl'
        # self.cl_results_h_file_name = '/media/inigo/10740FB2740F9A1C/3d_results/plots/cl/data/cl/cl_results_h.dat'
        # self.cl_reference_h_file_name = '/media/inigo/10740FB2740F9A1C/3d_results/plots/cl/data/cl/cl_reference_h.dat'

        # self.aoa_results_directory_name = '/media/inigo/10740FB2740F9A1C/3d_results/plots/aoa'
        # self.aoa_results_file_name = '/media/inigo/10740FB2740F9A1C/3d_results/plots/aoa/data/cl_aoa.dat'

        # self.cl_error_results_domain_directory_name = '/media/inigo/10740FB2740F9A1C/3d_results/plots/cl_error_domain_size/data'

    def ExecuteBeforeAOALoop(self):
        # self.latex_output = open(self.input_dir_path + '/plots/latex_output.txt', 'w')
        # self.latex_output.flush()
        self.AOA = self.Initial_AOA

        # for _ in range(self.Number_Of_AOAS):
        #     shutil.rmtree(self.cl_error_results_domain_directory_name + '/AOA_'+ str(self.AOA), ignore_errors=True)
        #     shutil.copytree(self.cl_error_results_domain_directory_name + '/domain', self.cl_error_results_domain_directory_name + '/AOA_'+ str(self.AOA))
        #     loads_output.write_figures_domain_cl_error(self.cl_error_results_domain_directory_name + '/AOA_'+ str(self.AOA), self.AOA, self.input_dir_path)
        #     self.AOA += self.AOA_Increment

        # self.merger_all_cp = PdfFileMerger()
        # loads_output.write_header_all_cases(self.input_dir_path)

    def ExecuteBeforeDomainRefinementLoop(self):
        self.Growth_Rate_Domain = self.Initial_Growth_Rate_Domain
        shutil.rmtree(self.gid_output_path + '/AOA_' + str(self.AOA), ignore_errors=True)
        os.mkdir(self.gid_output_path + '/AOA_' + str(self.AOA))

        # shutil.rmtree(self.aoa_results_directory_name + '/DS_' + str(self.Domain_Length), ignore_errors=True)

        # with open(self.aoa_results_file_name,'w') as cl_aoa_file:
        #     cl_aoa_file.flush()

        # cp_data_directory_start_ds = self.input_dir_path + '/plots/cp/data/DS_' + str(self.Domain_Length)
        # os.mkdir(cp_data_directory_start_ds)

    def ExecuteBeforeWingRefinementLoop(self):
        self.Growth_Rate_Wing = self.Initial_Growth_Rate_Wing
        os.mkdir(self.gid_output_path + '/AOA_' + str(self.AOA) + '/DR_' + str(self.Growth_Rate_Domain))

        # with open(self.cl_error_results_h_file_name,'w') as cl_error_file:
        #     cl_error_file.flush()
        # with open(self.cl_results_h_file_name,'w') as cl_file:
        #     cl_file.flush()
        # with open(self.cl_reference_h_file_name,'w') as cl_file:
        #     cl_file.flush()

        # self.cl_error_data_directory_name = 'data/cl_error_DS_' + str(self.Domain_Length) + '_AOA_' + str(self.AOA)
        # self.cl_data_directory_name = 'data/cl_DS_' + str(self.Domain_Length) + '_AOA_' + str(self.AOA)

        # self.cp_data_directory_start = self.input_dir_path + '/plots/cp/data/DS_' + str(self.Domain_Length) + '/' + 'AOA_' + str(self.AOA)
        # os.mkdir(self.cp_data_directory_start)

        # self.merger_refinement_cp = PdfFileMerger()

    #def MakeCpDir(self):
    #     self.cp_results_directory_name = self.input_dir_path + '/plots/cp/data/0_original'
    #     self.cp_data_directory_name = self.cp_data_directory_start + '/Case_' + str(self.case) + '_DS_' + str(self.Domain_Length) + '_AOA_' + str(
    #             self.AOA) + '_Far_Field_Mesh_Size_' + str(self.FarField_MeshSize) + '_Airfoil_Mesh_Size_' + str(self.Airfoil_MeshSize)

    #def OutputCp(self):
    #     loads_output.write_cp_figures(self.cp_data_directory_name, self.AOA, self.case, self.Airfoil_MeshSize, self.FarField_MeshSize, self.input_dir_path)
    #     shutil.copytree(self.cp_results_directory_name, self.cp_data_directory_name)

    #     latex = subprocess.Popen(['pdflatex', '-interaction=batchmode', self.input_dir_path + '/plots/cp/cp.tex'], stdout=self.latex_output)
    #     latex.communicate()

    #     cp_file_name = self.input_dir_path + '/plots/cp/plots/cp_Case_' + str(self.case) + '_DS_' + str(self.Domain_Length) + '_AOA_' + str(
    #                 self.AOA) + '_Far_Field_Mesh_Size_' + str(self.FarField_MeshSize) + '_Airfoil_Mesh_Size_' + str(self.Airfoil_MeshSize) + '.pdf'
    #     shutil.copyfile('cp.pdf',cp_file_name)
    #     self.merger_refinement_cp.append(PdfFileReader(cp_file_name), 'case_' + str(self.case))
    #     self.merger_all_cp.append(PdfFileReader(cp_file_name), 'case_' + str(self.case))

    def SetParametersBeforeInitialize(self):
        #loads_output.write_case(self.case, self.AOA, self.FarField_MeshSize, self.Airfoil_MeshSize, self.input_dir_path)
        self.Smallest_Airfoil_Mesh_Size = round_to_1(self.Smallest_Airfoil_Mesh_Size)
        print("\n\tCase ", self.case, "\n")

        mdpa_file_name = self.mdpa_path + '/wing_Case_' + str(self.case) + '_AOA_' + str(self.AOA) + '_Wing_Span_' + str(
              self.Wing_span) + '_Airfoil_Mesh_Size_' + str(self.Smallest_Airfoil_Mesh_Size) + '_Growth_Rate_Wing_' + str(
                self.Growth_Rate_Wing) + '_Growth_Rate_Domain_' + str(self.Growth_Rate_Domain)

        self.project_parameters["solver_settings"]["model_import_settings"]["input_filename"].SetString(
            mdpa_file_name)

        gid_output_file_name = self.gid_output_path + '/AOA_' + str(self.AOA) + '/DR_' + str(
            self.Growth_Rate_Domain) + '/' + self.project_parameters["problem_data"]["problem_name"].GetString() + '_Case_' + str(
            self.case) + '_AOA_' + str(self.AOA) + '_Wing_Span_' + str(
              self.Wing_span) + '_Airfoil_Mesh_Size_' + str(self.Smallest_Airfoil_Mesh_Size) + '_Growth_Rate_Wing_' + str(
                self.Growth_Rate_Wing) + '_Growth_Rate_Domain_' + str(self.Growth_Rate_Domain)

        self.project_parameters["output_processes"]["gid_output"][0]["Parameters"]["output_name"].SetString(
            gid_output_file_name)

        wake_file_name = self.input_dir_path + '/output_salome' + '/wake_Case_' + str(self.case) + '_AOA_' + str(self.AOA) + '_Wing_Span_' + str(
              self.Wing_span) + '_Airfoil_Mesh_Size_' + str(self.Smallest_Airfoil_Mesh_Size) + '_Growth_Rate_Wing_' + str(
                self.Growth_Rate_Wing) + '_Growth_Rate_Domain_' + str(self.Growth_Rate_Domain) + '.stl'

        self.project_parameters["processes"]["boundary_conditions_process_list"][1]["Parameters"]["wake_stl_file_name"].SetString(
            wake_file_name)

        # self.project_parameters["processes"]["boundary_conditions_process_list"][2]["Parameters"]["angle_of_attack"].SetDouble(
        #     self.AOA)
        # self.project_parameters["processes"]["boundary_conditions_process_list"][2]["Parameters"]["airfoil_meshsize"].SetDouble(
        #     self.Airfoil_MeshSize)
        # self.project_parameters["processes"]["boundary_conditions_process_list"][2]["Parameters"]["minimum_airfoil_meshsize"].SetDouble(
        #     self.Minimum_Airfoil_MeshSize)
        # self.project_parameters["processes"]["boundary_conditions_process_list"][2]["Parameters"]["domain_size"].SetDouble(
        #     self.Domain_Length)

        self._solver = self._CreateSolver()
        self._GetSolver().AddVariables()

    def ExecuteAfterWingRefinementLoop(self):
        # loads_output.write_figures_cl_error(self.cl_error_data_directory_name, self.AOA, self.input_dir_path, self.Domain_Length)
        # loads_output.write_figures_cl(self.cl_data_directory_name, self.AOA, self.input_dir_path, self.Domain_Length)

        # shutil.copytree(self.cl_results_directory_name, self.input_dir_path + '/plots/cl/' + self.cl_data_directory_name)
        # shutil.copytree(self.cl_error_results_directory_name, self.input_dir_path + '/plots/cl_error/' + self.cl_error_data_directory_name)

        # os.remove(self.cl_error_results_h_file_name)
        # os.remove(self.cl_results_h_file_name)
        # os.remove(self.cl_reference_h_file_name)

        # cp_refienment_file_name = self.input_dir_path + '/plots/cp/cp_DS_' + str(self.Domain_Length) + '_AOA_' + str(self.AOA) + '.pdf'
        # self.merger_refinement_cp.write(cp_refienment_file_name)
        self.Growth_Rate_Domain -= self.Growth_Rate_Domain_Refinement_Factor

    def ExecuteAfterDomainRefinementLoop(self):
        # latex_aoa = subprocess.Popen(['pdflatex', '-interaction=batchmode', '-output-directory', self.input_dir_path + '/plots/aoa/data', self.input_dir_path + '/plots/aoa/data/cl_aoa.tex'], stdout=self.latex_output)
        # latex_aoa.communicate()
        # shutil.copytree(self.aoa_results_directory_name + '/data', self.aoa_results_directory_name + '/DS_' + str(self.Domain_Length))

        self.AOA += self.AOA_Increment

    # def ExecuteAfterAOALoop(self):
    #     cp_final_global_file_name = self.input_dir_path + '/plots/cp/cp_all.pdf'
    #     self.merger_all_cp.write(cp_final_global_file_name)

    def Finalize(self):
        super(PotentialFlowAnalysisRefinement,self).Finalize()
        self.project_parameters["solver_settings"].RemoveValue("element_replace_settings")
        #self.project_parameters["solver_settings"]["element_replace_settings"]["element_name"].SetString("IncompressiblePotentialFlowElement")
        #self.project_parameters["solver_settings"]["element_replace_settings"]["condition_name"].SetString("PotentialWallCondition")
        self.model.Reset()
