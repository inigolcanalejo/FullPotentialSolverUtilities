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
                    #self.Growth_Rate_Wing -= self.Growth_Rate_Wing_Refinement_Factor
                    self.Growth_Rate_Wing /= self.Growth_Rate_Wing_Refinement_Factor
                    self.Smallest_Airfoil_Mesh_Size /= 2.0
                    #self.FarField_MeshSize /= FarField_Refinement_Factor

                    self.case += 1
                self.ExecuteAfterWingRefinementLoop()
            self.ExecuteAfterDomainRefinementLoop()
        #self.ExecuteAfterAOALoop()

    def SetParameters(self):
        self.Wing_span = TBD
        self.Smallest_Airfoil_Mesh_Size = TBD
        self.Initial_Smallest_Airfoil_Mesh_Size = self.Smallest_Airfoil_Mesh_Size
        self.Biggest_Airfoil_Mesh_Size = TBD

        self.Number_Of_AOAS = TBD
        self.Number_Of_Domains_Refinements = TBD
        self.Number_Of_Wing_Refinements = TBD

        self.Initial_AOA = TBD
        self.AOA_Increment = TBD

        self.Initial_Growth_Rate_Wing = TBD
        self.Growth_Rate_Wing_Refinement_Factor = TBD

        self.Initial_Growth_Rate_Domain = TBD
        self.Growth_Rate_Domain_Refinement_Factor = TBD

        self.case = 0
        self.Domain_Length = 100
        self.Domain_Width = self.Domain_Length
        self.FarField_MeshSize = int(self.Domain_Length / 10.0)

        minimum_mesh_growth_rate_wing = self.Initial_Growth_Rate_Wing / \
            self.Growth_Rate_Wing_Refinement_Factor**(self.Number_Of_Wing_Refinements-1)

        minimum_mesh_growth_rate_domain = self.Initial_Growth_Rate_Domain / \
            self.Growth_Rate_Domain_Refinement_Factor**(self.Number_Of_Domains_Refinements-1)

        self.minimum_mesh_growth_rate = minimum_mesh_growth_rate_wing * minimum_mesh_growth_rate_domain

        self.SetFilePaths()

    def SetFilePaths(self):
        self.input_dir_path = 'TBD'
        self.mdpa_path = 'TBD'
        self.gid_output_path = 'TBD'

        self.cl_results_directory_name = 'TBD'
        self.cd_results_directory_name = 'TBD'
        self.cm_results_directory_name = 'TBD'
        self.cl_error_results_directory_name = 'TBD'
        self.cd_error_results_directory_name = 'TBD'
        self.cm_error_results_directory_name = 'TBD'
        self.cl_aoa_results_directory_name = 'TBD'
        self.cd_aoa_results_directory_name = 'TBD'
        self.cm_aoa_results_directory_name = 'TBD'
        self.potential_jump_results_directory_name = self.input_dir_path + '/plots/potential_jump/data/potential_jump'
        self.cp_results_directory_name = self.input_dir_path + '/plots/cp/data/cp'
        self.cp_100_results_directory_name = self.input_dir_path + '/plots/cp_section_100/data/cp'
        self.cp_150_results_directory_name = self.input_dir_path + '/plots/cp_section_150/data/cp'
        self.cp_180_results_directory_name = self.input_dir_path + '/plots/cp_section_180/data/cp'
        self.newton_convergence_directory_name = self.input_dir_path + '/plots/newton_convergence/data/convergence'

    def ExecuteBeforeAOALoop(self):
        loads_output.create_cd_plots_directory_tree(self.input_dir_path)
        self.latex_output = open(self.input_dir_path + '/plots/latex_output.txt', 'w')
        self.latex_output.flush()
        self.AOA = self.Initial_AOA
        shutil.copytree(self.cl_aoa_results_directory_name, self.cl_aoa_results_directory_name + 'oa')
        shutil.copytree(self.cd_aoa_results_directory_name, self.cd_aoa_results_directory_name + 'oa')
        shutil.copytree(self.cm_aoa_results_directory_name, self.cm_aoa_results_directory_name + 'oa')

    def ExecuteBeforeDomainRefinementLoop(self):
        self.AOA = round(self.AOA, 1)
        self.Growth_Rate_Domain = self.Initial_Growth_Rate_Domain
        shutil.rmtree(self.gid_output_path + '/AOA_' + str(self.AOA), ignore_errors=True)
        if not os.path.exists(self.gid_output_path + '/AOA_' + str(self.AOA)):
            os.makedirs(self.gid_output_path + '/AOA_' + str(self.AOA))

        self.cl_data_directory_name = 'data/cl_AOA_' + str(self.AOA)
        self.cd_data_directory_name = 'data/cd_AOA_' + str(self.AOA)
        self.cm_data_directory_name = 'data/cm_AOA_' + str(self.AOA)
        self.cl_error_data_directory_name = 'data/cl_error_AOA_' + str(self.AOA)
        self.cd_error_data_directory_name = 'data/cd_error_AOA_' + str(self.AOA)
        self.cm_error_data_directory_name = 'data/cm_error_AOA_' + str(self.AOA)

        shutil.copytree(self.cl_results_directory_name, self.input_dir_path + '/plots/cl/' + self.cl_data_directory_name)
        shutil.copytree(self.cd_results_directory_name, self.input_dir_path + '/plots/cd/' + self.cd_data_directory_name)
        shutil.copytree(self.cm_results_directory_name, self.input_dir_path + '/plots/cm/' + self.cm_data_directory_name)
        shutil.copytree(self.cl_error_results_directory_name, self.input_dir_path + '/plots/cl_error/' + self.cl_error_data_directory_name)
        shutil.copytree(self.cd_error_results_directory_name, self.input_dir_path + '/plots/cd_error/' + self.cd_error_data_directory_name)
        shutil.copytree(self.cm_error_results_directory_name, self.input_dir_path + '/plots/cm_error/' + self.cm_error_data_directory_name)

        self.Growth_Rate_Domain_Counter = 0

        self.merger_local_jump = PdfFileMerger()
        self.merger_local_cp = PdfFileMerger()
        self.merger_local_cp_100 = PdfFileMerger()
        self.merger_local_cp_150 = PdfFileMerger()
        self.merger_local_cp_180 = PdfFileMerger()

        # shutil.rmtree(self.aoa_results_directory_name + '/DS_' + str(self.Domain_Length), ignore_errors=True)

        # with open(self.aoa_results_file_name,'w') as cl_aoa_file:
        #     cl_aoa_file.flush()

        # cp_data_directory_start_ds = self.input_dir_path + '/plots/cp/data/DS_' + str(self.Domain_Length)
        # os.mkdir(cp_data_directory_start_ds)

    def ExecuteBeforeWingRefinementLoop(self):
        self.Growth_Rate_Domain = round(self.Growth_Rate_Domain, 2)
        self.Growth_Rate_Wing = self.Initial_Growth_Rate_Wing
        self.Smallest_Airfoil_Mesh_Size = self.Initial_Smallest_Airfoil_Mesh_Size
        os.mkdir(self.gid_output_path + '/AOA_' + str(self.AOA) + '/DR_' + str(self.Growth_Rate_Domain))

        # with open(self.cl_error_results_h_file_name,'w') as cl_error_file:
        #     cl_error_file.flush()
        # with open(self.cl_results_h_file_name,'w') as cl_file:
        #     cl_file.flush()
        # with open(self.cl_reference_h_file_name,'w') as cl_file:
        #     cl_file.flush()

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
        self.Growth_Rate_Wing = round(self.Growth_Rate_Wing, 2)
        #loads_output.write_case(self.case, self.AOA, self.FarField_MeshSize, self.Airfoil_MeshSize, self.input_dir_path)
        #self.Smallest_Airfoil_Mesh_Size = round_to_1(self.Smallest_Airfoil_Mesh_Size)
        self.Smallest_Airfoil_Mesh_Size = round(self.Smallest_Airfoil_Mesh_Size, 3)
        print("\n\tCase ", self.case, ' AOA = ', self.AOA, ' Growth_Rate_Domain = ', self.Growth_Rate_Domain, ' Growth_Rate_Wing = ', self.Growth_Rate_Wing, "\n")
        print("Smallest_Airfoil_Mesh_Size = ", self.Smallest_Airfoil_Mesh_Size)

        potential_jump_dir_name = self.input_dir_path + '/plots/potential_jump/data/AOA_' + str(self.AOA) + '/Growth_Rate_Domain_' + str(
            self.Growth_Rate_Domain) + '/Growth_Rate_Wing_' + str(self.Growth_Rate_Wing)
        shutil.copytree(self.potential_jump_results_directory_name, potential_jump_dir_name)
        loads_output.write_jump_figures(potential_jump_dir_name, self.AOA, self.case, self.Growth_Rate_Domain, self.Growth_Rate_Wing, self.input_dir_path)

        cp_dir_name = self.input_dir_path + '/plots/cp/data/AOA_' + str(self.AOA) + '/Growth_Rate_Domain_' + str(
            self.Growth_Rate_Domain) + '/Growth_Rate_Wing_' + str(self.Growth_Rate_Wing)
        shutil.copytree(self.cp_results_directory_name, cp_dir_name)

        loads_output.write_cp_figures(cp_dir_name, self.AOA, self.case, self.Growth_Rate_Domain, self.Growth_Rate_Wing, self.input_dir_path,'cp')

        cp_100_dir_name = self.input_dir_path + '/plots/cp_section_100/data/AOA_' + str(self.AOA) + '/Growth_Rate_Domain_' + str(
            self.Growth_Rate_Domain) + '/Growth_Rate_Wing_' + str(self.Growth_Rate_Wing)
        shutil.copytree(self.cp_100_results_directory_name, cp_100_dir_name)

        loads_output.write_cp_figures(cp_100_dir_name, self.AOA, self.case, self.Growth_Rate_Domain, self.Growth_Rate_Wing, self.input_dir_path,'cp_section_100')

        cp_150_dir_name = self.input_dir_path + '/plots/cp_section_150/data/AOA_' + str(self.AOA) + '/Growth_Rate_Domain_' + str(
            self.Growth_Rate_Domain) + '/Growth_Rate_Wing_' + str(self.Growth_Rate_Wing)
        shutil.copytree(self.cp_150_results_directory_name, cp_150_dir_name)

        loads_output.write_cp_figures(cp_150_dir_name, self.AOA, self.case, self.Growth_Rate_Domain, self.Growth_Rate_Wing, self.input_dir_path,'cp_section_150')

        cp_180_dir_name = self.input_dir_path + '/plots/cp_section_180/data/AOA_' + str(self.AOA) + '/Growth_Rate_Domain_' + str(
            self.Growth_Rate_Domain) + '/Growth_Rate_Wing_' + str(self.Growth_Rate_Wing)
        shutil.copytree(self.cp_180_results_directory_name, cp_180_dir_name)

        loads_output.write_cp_figures(cp_180_dir_name, self.AOA, self.case, self.Growth_Rate_Domain, self.Growth_Rate_Wing, self.input_dir_path,'cp_section_180')

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

        wake_file_name = self.mdpa_path + '/wake_Case_' + str(self.case) + '_AOA_' + str(self.AOA) + '_Wing_Span_' + str(
              self.Wing_span) + '_Airfoil_Mesh_Size_' + str(self.Smallest_Airfoil_Mesh_Size) + '_Growth_Rate_Wing_' + str(
                self.Growth_Rate_Wing) + '_Growth_Rate_Domain_' + str(self.Growth_Rate_Domain) + '.stl'

        self.project_parameters["processes"]["boundary_conditions_process_list"][1]["Parameters"]["wake_stl_file_name"].SetString(
            wake_file_name)

        self.project_parameters["processes"]["boundary_conditions_process_list"][2]["Parameters"]["growth_rate_domain"].SetDouble(
            self.Growth_Rate_Domain)
        self.project_parameters["processes"]["boundary_conditions_process_list"][2]["Parameters"]["growth_rate_wing"].SetDouble(
            self.Growth_Rate_Wing)
        self.project_parameters["processes"]["boundary_conditions_process_list"][2]["Parameters"]["angle_of_attack"].SetDouble(
            self.AOA)
        self.project_parameters["processes"]["boundary_conditions_process_list"][2]["Parameters"]["minimum_mesh_growth_rate"].SetDouble(
            self.minimum_mesh_growth_rate)

        # self.project_parameters["processes"]["boundary_conditions_process_list"][2]["Parameters"]["airfoil_meshsize"].SetDouble(
        #     self.Airfoil_MeshSize)
        # self.project_parameters["processes"]["boundary_conditions_process_list"][2]["Parameters"]["minimum_airfoil_meshsize"].SetDouble(
        #     self.Minimum_Airfoil_MeshSize)
        # self.project_parameters["processes"]["boundary_conditions_process_list"][2]["Parameters"]["domain_size"].SetDouble(
        #     self.Domain_Length)

        self._solver = self._CreateSolver()
        self._GetSolver().AddVariables()

    def ExecuteAfterWingRefinementLoop(self):
        # cp_refienment_file_name = self.input_dir_path + '/plots/cp/cp_DS_' + str(self.Domain_Length) + '_AOA_' + str(self.AOA) + '.pdf'
        # self.merger_refinement_cp.write(cp_refienment_file_name)
        loads_output.add_cl_to_tikz(self.input_dir_path, self.cl_data_directory_name, self.Growth_Rate_Domain, self.Growth_Rate_Domain_Counter)
        loads_output.add_cd_to_tikz(self.input_dir_path, self.cd_data_directory_name, self.Growth_Rate_Domain, self.Growth_Rate_Domain_Counter)
        loads_output.add_cm_to_tikz(self.input_dir_path, self.cm_data_directory_name, self.Growth_Rate_Domain, self.Growth_Rate_Domain_Counter)
        loads_output.add_cl_error_to_tikz(self.input_dir_path, self.cl_error_data_directory_name, self.Growth_Rate_Domain, self.Growth_Rate_Domain_Counter)
        loads_output.add_cd_error_to_tikz(self.input_dir_path, self.cd_error_data_directory_name, self.Growth_Rate_Domain, self.Growth_Rate_Domain_Counter)
        loads_output.add_cm_error_to_tikz(self.input_dir_path, self.cm_error_data_directory_name, self.Growth_Rate_Domain, self.Growth_Rate_Domain_Counter)
        self.Growth_Rate_Domain /= self.Growth_Rate_Domain_Refinement_Factor
        self.Growth_Rate_Domain_Counter += 1

    def ExecuteAfterDomainRefinementLoop(self):
        # latex_aoa = subprocess.Popen(['pdflatex', '-interaction=batchmode', '-output-directory', self.input_dir_path + '/plots/aoa/data', self.input_dir_path + '/plots/aoa/data/cl_aoa.tex'], stdout=self.latex_output)
        # latex_aoa.communicate()
        # shutil.copytree(self.aoa_results_directory_name + '/data', self.aoa_results_directory_name + '/DS_' + str(self.Domain_Length))

        # loads_output.write_figures_cl_error(self.cl_error_data_directory_name, self.AOA, self.input_dir_path, self.Domain_Length)
        loads_output.write_figures_cl(self.cl_data_directory_name, self.AOA, self.input_dir_path, self.Domain_Length, self.Wing_span, self.Smallest_Airfoil_Mesh_Size)
        loads_output.write_figures_cd(self.cd_data_directory_name, self.AOA, self.input_dir_path, self.Domain_Length, self.Wing_span, self.Smallest_Airfoil_Mesh_Size)
        loads_output.write_figures_cm(self.cm_data_directory_name, self.AOA, self.input_dir_path, self.Domain_Length, self.Wing_span, self.Smallest_Airfoil_Mesh_Size)
        loads_output.write_figures_cl_error(self.cl_error_data_directory_name, self.AOA, self.input_dir_path, self.Domain_Length, self.Wing_span, self.Smallest_Airfoil_Mesh_Size)
        loads_output.write_figures_cd_error(self.cd_error_data_directory_name, self.AOA, self.input_dir_path, self.Domain_Length, self.Wing_span, self.Smallest_Airfoil_Mesh_Size)
        loads_output.write_figures_cm_error(self.cm_error_data_directory_name, self.AOA, self.input_dir_path, self.Domain_Length, self.Wing_span, self.Smallest_Airfoil_Mesh_Size)
        loads_output.add_cl_reference_to_tikz(self.input_dir_path, self.cl_data_directory_name)
        loads_output.add_cd_reference_to_tikz(self.input_dir_path, self.cd_data_directory_name)
        loads_output.add_cm_reference_to_tikz(self.input_dir_path, self.cm_data_directory_name)
        loads_output.close_cl_tikz(self.input_dir_path, self.cl_data_directory_name)
        loads_output.close_cd_tikz(self.input_dir_path, self.cd_data_directory_name)
        loads_output.close_cm_tikz(self.input_dir_path, self.cm_data_directory_name)
        loads_output.close_cl_error_tikz(self.input_dir_path, self.cl_error_data_directory_name)
        loads_output.close_cd_error_tikz(self.input_dir_path, self.cd_error_data_directory_name)
        loads_output.close_cm_error_tikz(self.input_dir_path, self.cm_error_data_directory_name)

        jump_final_file_name = self.input_dir_path + '/plots/potential_jump/AOA_' + str(self.AOA) + '.pdf'
        self.merger_local_jump.write(jump_final_file_name)

        cp_final_file_name = self.input_dir_path + '/plots/cp/AOA_' + str(self.AOA) + '.pdf'
        self.merger_local_cp.write(cp_final_file_name)

        cp_100_final_file_name = self.input_dir_path + '/plots/cp_section_100/AOA_' + str(self.AOA) + '.pdf'
        self.merger_local_cp_100.write(cp_100_final_file_name)

        cp_150_final_file_name = self.input_dir_path + '/plots/cp_section_150/AOA_' + str(self.AOA) + '.pdf'
        self.merger_local_cp_150.write(cp_150_final_file_name)

        cp_180_final_file_name = self.input_dir_path + '/plots/cp_section_180/AOA_' + str(self.AOA) + '.pdf'
        self.merger_local_cp_180.write(cp_180_final_file_name)

        #shutil.copytree(self.cl_results_directory_name, self.input_dir_path + '/plots/cl/' + self.cl_error_data_directory_name)

        # os.remove(self.cl_error_results_h_file_name)
        # os.remove(self.cl_results_h_file_name)
        # os.remove(self.cl_reference_h_file_name)
        #os.remove(self.cl_p_results_file_name)

        self.AOA += self.AOA_Increment

    # def ExecuteAfterAOALoop(self):
    #     cp_final_global_file_name = self.input_dir_path + '/plots/cp/cp_all.pdf'
    #     self.merger_all_cp.write(cp_final_global_file_name)

    def Finalize(self):
        latex = subprocess.Popen(['pdflatex', '-interaction=batchmode', self.input_dir_path + '/plots/potential_jump/main_potential_jump.tex'], stdout=self.latex_output)
        latex.communicate()
        jump_file_name = self.input_dir_path + '/plots/potential_jump/plots/Case_' + str(self.case) + '_AOA_' + str(self.AOA) + '_Growth_Rate_Domain_' + str(
            self.Growth_Rate_Domain) + '_Growth_Rate_Wing_' + str(self.Growth_Rate_Wing)
        shutil.copyfile('main_potential_jump.pdf',jump_file_name)
        self.merger_local_jump.append(PdfFileReader(jump_file_name), 'case_' + str(self.case))

        latex = subprocess.Popen(['pdflatex', '-interaction=batchmode', self.input_dir_path + '/plots/cp/main_cp.tex'], stdout=self.latex_output)
        latex.communicate()
        cp_file_name = self.input_dir_path + '/plots/cp/plots/Case_' + str(self.case) + '_AOA_' + str(self.AOA) + '_Growth_Rate_Domain_' + str(
            self.Growth_Rate_Domain) + '_Growth_Rate_Wing_' + str(self.Growth_Rate_Wing)
        shutil.copyfile('main_cp.pdf',cp_file_name)
        self.merger_local_cp.append(PdfFileReader(cp_file_name), 'case_' + str(self.case))

        latex = subprocess.Popen(['pdflatex', '-interaction=batchmode', self.input_dir_path + '/plots/cp_section_100/main_cp_100.tex'], stdout=self.latex_output)
        latex.communicate()
        cp_100_file_name = self.input_dir_path + '/plots/cp_section_100/plots/Case_' + str(self.case) + '_AOA_' + str(self.AOA) + '_Growth_Rate_Domain_' + str(
            self.Growth_Rate_Domain) + '_Growth_Rate_Wing_' + str(self.Growth_Rate_Wing)
        shutil.copyfile('main_cp_100.pdf',cp_100_file_name)
        self.merger_local_cp_100.append(PdfFileReader(cp_100_file_name), 'case_' + str(self.case))

        latex = subprocess.Popen(['pdflatex', '-interaction=batchmode', self.input_dir_path + '/plots/cp_section_150/main_cp_150.tex'], stdout=self.latex_output)
        latex.communicate()
        cp_150_file_name = self.input_dir_path + '/plots/cp_section_150/plots/Case_' + str(self.case) + '_AOA_' + str(self.AOA) + '_Growth_Rate_Domain_' + str(
            self.Growth_Rate_Domain) + '_Growth_Rate_Wing_' + str(self.Growth_Rate_Wing)
        shutil.copyfile('main_cp_150.pdf',cp_150_file_name)
        self.merger_local_cp_150.append(PdfFileReader(cp_150_file_name), 'case_' + str(self.case))

        latex = subprocess.Popen(['pdflatex', '-interaction=batchmode', self.input_dir_path + '/plots/cp_section_180/main_cp_180.tex'], stdout=self.latex_output)
        latex.communicate()
        cp_180_file_name = self.input_dir_path + '/plots/cp_section_180/plots/Case_' + str(self.case) + '_AOA_' + str(self.AOA) + '_Growth_Rate_Domain_' + str(
            self.Growth_Rate_Domain) + '_Growth_Rate_Wing_' + str(self.Growth_Rate_Wing)
        shutil.copyfile('main_cp_180.pdf',cp_180_file_name)
        self.merger_local_cp_180.append(PdfFileReader(cp_180_file_name), 'case_' + str(self.case))

        self.newton_convergence_data_directory_name = 'data/AOA_' + str(self.AOA) + '_Growth_Rate_Domain_' + str(
            self.Growth_Rate_Domain) + '_Growth_Rate_Wing_' + str(self.Growth_Rate_Wing)
        shutil.copytree(self.newton_convergence_directory_name, self.input_dir_path + '/plots/newton_convergence/' + self.newton_convergence_data_directory_name)
        loads_output.write_figures_newton_convergence(self.newton_convergence_data_directory_name, self.AOA, self.input_dir_path, self.Domain_Length, self.Wing_span, self.Smallest_Airfoil_Mesh_Size)

        super(PotentialFlowAnalysisRefinement,self).Finalize()
        self.project_parameters["solver_settings"].RemoveValue("element_replace_settings")
        #self.project_parameters["solver_settings"]["element_replace_settings"]["element_name"].SetString("IncompressiblePotentialFlowElement")
        #self.project_parameters["solver_settings"]["element_replace_settings"]["condition_name"].SetString("PotentialWallCondition")
        self.model.Reset()
