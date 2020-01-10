from __future__ import print_function, absolute_import, division #makes KratosMultiphysics backward compatible with python 2.6 and 2.7

from KratosMultiphysics import *
import KratosMultiphysics
#from KratosMultiphysics.FluidDynamicsApplication import *
from KratosMultiphysics.ExternalSolversApplication import *
#from KratosMultiphysics.MeshingApplication import *
from KratosMultiphysics.CompressiblePotentialFlowApplication import *
import potential_flow_solver
import os
import loads_output
import shutil
#import compute_lift_process_new
import subprocess
from PyPDF2 import PdfFileReader, PdfFileMerger
from math import *
from math import log10, floor

def round_to_1(x):
    return round(x, -int(floor(log10(abs(x)))))
######################################################################################
######################################################################################
######################################################################################
Number_Of_Refinements = TBD
Number_Of_AOAS = TBD

Initial_AOA = TBD
AOA_Increment = TBD

Initial_Airfoil_MeshSize = TBD
Airfoil_Refinement_Factor = TBD

Initial_FarField_MeshSize = TBD
FarField_Refinement_Factor = TBD

work_dir = '/home/inigo/simulations/naca0012/07_salome/05_MeshRefinement/'
input_mdpa_path = '/home/inigo/simulations/naca0012/07_salome/05_MeshRefinement/mdpas/'
output_gid_path = '/media/inigo/10740FB2740F9A1C/Outputs/05_MeshRefinement/'
latex_output = open(work_dir + '/plots/latex_output.txt', 'w')
latex_output.flush()

cl_results_file_name = work_dir + 'plots/cl/data/cl/cl_results.dat'
cl_results_h_file_name = work_dir + 'plots/cl/data/cl/cl_results_h.dat'
cl_reference_file_name = work_dir + 'plots/cl/data/cl/cl_reference.dat'
cl_reference_h_file_name = work_dir + 'plots/cl/data/cl/cl_reference_h.dat'
cl_far_field_results_file_name = work_dir + 'plots/cl/data/cl/cl_jump_results.dat'
cl_far_field_results_h_file_name = work_dir + 'plots/cl/data/cl/cl_jump_results_h.dat'
cl_results_directory_name = work_dir + 'plots/cl/data/cl'

cl_error_results_file_name = work_dir + 'plots/cl_error/data/cl/cl_error_results.dat'
cl_error_results_h_file_name = work_dir + 'plots/cl_error/data/cl/cl_error_results_h.dat'
cl_error_results_h_log_file_name = work_dir + 'plots/cl_error/data/cl/cl_error_results_h_log.dat'
cl_error_results_h_log_ok_file_name = work_dir + 'plots/cl_error/data/cl/cl_error_results_h_log_ok.dat'
cl_far_field_error_results_file_name = work_dir + 'plots/cl_error/data/cl/cl_jump_error_results.dat'
cl_far_field_error_results_h_file_name = work_dir + 'plots/cl_error/data/cl/cl_jump_error_results_h.dat'
cl_far_field_error_results_h_log_file_name = work_dir + 'plots/cl_error/data/cl/cl_jump_error_results_h_log.dat'
cl_error_results_directory_name = work_dir + 'plots/cl_error/data/cl'

energy_h_results_file_name = work_dir + 'plots/relative_error_energy_norm/data/energy/energy_h_results.dat'
energy_n_results_file_name = work_dir + 'plots/relative_error_energy_norm/data/energy/energy_n_results.dat'
energy_variant_h_results_file_name = work_dir + 'plots/relative_error_energy_norm/data/energy/energy_variant_h_results.dat'
energy_variant_n_results_file_name = work_dir + 'plots/relative_error_energy_norm/data/energy/energy_variant_n_results.dat'
energy_results_directory_name = work_dir + 'plots/relative_error_energy_norm/data/energy'

cd_results_file_name = work_dir + 'plots/cd/data/cd/cd_results.dat'
cd_results_directory_name = work_dir + 'plots/cd/data/cd'

condition_results_file_name = work_dir + 'plots/condition_number/data/condition/condition_results.dat'
condition_results_directory_name = work_dir + 'plots/condition_number/data/condition'

aoa_results_file_name = work_dir + 'plots/aoa/cl_aoa.dat'
with open(aoa_results_file_name,'w') as cl_aoa_file:
    cl_aoa_file.flush()

loads_output.write_header_all_cases(work_dir)

merger_global = PdfFileMerger()
merger_global_far_field_x = PdfFileMerger()
merger_global_far_field_y = PdfFileMerger()
merger_global_jump = PdfFileMerger()

case = 0
AOA = Initial_AOA
for j in range(Number_Of_AOAS):
    Airfoil_MeshSize = Initial_Airfoil_MeshSize
    FarField_MeshSize = Initial_FarField_MeshSize

    merger = PdfFileMerger()
    merger_local_far_field_x = PdfFileMerger()
    merger_local_far_field_y = PdfFileMerger()
    merger_local_jump = PdfFileMerger()

    with open(cl_results_file_name,'w') as cl_file:
        cl_file.flush()

    with open(cl_results_h_file_name,'w') as cl_file:
        cl_file.flush()

    with open(cl_reference_file_name,'w') as cl_reference_file:
        cl_reference_file.flush()

    with open(cl_reference_h_file_name,'w') as cl_reference_file:
        cl_reference_file.flush()

    with open(cl_error_results_file_name,'w') as cl_error_file:
        cl_error_file.flush()

    with open(cl_error_results_h_file_name,'w') as cl_error_file:
        cl_error_file.flush()

    with open(cl_error_results_h_log_ok_file_name,'w') as cl_error_file:
        cl_error_file.flush()

    with open(energy_h_results_file_name,'w') as energy_file:
        energy_file.flush()

    with open(energy_n_results_file_name,'w') as energy_file:
        energy_file.flush()

    with open(energy_variant_h_results_file_name,'w') as energy_file:
        energy_file.flush()

    with open(energy_variant_n_results_file_name,'w') as energy_file:
        energy_file.flush()

    with open(cl_far_field_results_file_name,'w') as cl_jump_file:
        cl_jump_file.flush()

    with open(cl_far_field_results_h_file_name,'w') as cl_jump_file:
        cl_jump_file.flush()

    with open(cd_results_file_name, 'w') as cd_file:
        cd_file.flush()

    with open(condition_results_file_name, 'w') as condition_file:
        condition_file.flush()

    mesh_refinement_file_name = work_dir + 'plots/results/mesh_refinement_AOA_' + str(AOA)
    cl_data_directory_name = 'data/cl_AOA_' + str(AOA)
    cl_error_data_directory_name = 'data/cl_error_AOA_' + str(AOA)
    energy_data_directory_name = 'data/energy_AOA_' + str(AOA)
    cd_data_directory_name = 'data/cd_AOA_' + str(AOA)
    condition_data_directory_name = 'data/condition_AOA_' + str(AOA)
    loads_output.write_header(work_dir)

    cp_data_directory_start = work_dir + 'plots/cp/data/AOA_' + str(AOA)
    os.mkdir(cp_data_directory_start)

    far_field_data_directory_start = work_dir + 'plots/far_field/data/AOA_' + str(AOA)
    os.mkdir(far_field_data_directory_start)

    jump_data_directory_start = work_dir + 'plots/potential_jump/data/AOA_' + str(AOA)
    os.mkdir(jump_data_directory_start)

    cl_aoa_file = open(aoa_results_file_name,'a')
    cl_aoa_file.write('{0:15f}'.format(AOA))
    cl_aoa_file.flush()

    os.mkdir(output_gid_path + 'AOA_' + str(AOA))

    energy_reference = 1.0
    potential_energy_reference = 1.0
    cl_ok_reference = 1.0
    counter = 0.0

    for i in range(Number_Of_Refinements):
        Airfoil_MeshSize = round_to_1(Airfoil_MeshSize)
        print("\n\tCase ", case, "\n")
        loads_output.write_case(case, AOA, FarField_MeshSize, Airfoil_MeshSize, work_dir)

        cp_results_directory_name = work_dir + 'plots/cp/data/0_original'
        cp_data_directory_name = cp_data_directory_start + '/Case_' + str(case) + '_AOA_' + str(
                AOA) + '_Far_Field_Mesh_Size_' + str(FarField_MeshSize) + '_Airfoil_Mesh_Size_' + str(Airfoil_MeshSize)

        far_field_results_directory_name = work_dir + 'plots/far_field/data/0_original'
        far_field_data_directory_name = far_field_data_directory_start + '/Case_' + str(case) + '_AOA_' + str(
                AOA) + '_Far_Field_Mesh_Size_' + str(FarField_MeshSize) + '_Airfoil_Mesh_Size_' + str(Airfoil_MeshSize)

        jump_results_directory_name = work_dir + 'plots/potential_jump/data/jump'
        jump_data_directory_name = jump_data_directory_start + '/Case_' + str(case) + '_AOA_' + str(
                AOA) + '_Far_Field_Mesh_Size_' + str(FarField_MeshSize) + '_Airfoil_Mesh_Size_' + str(Airfoil_MeshSize)

        ## Parse the ProjectParameters
        #parameter_file = open("ProjectParameters_compressibility.json",'r')
        parameter_file = open("ProjectParameters.json",'r')
        ProjectParameters = Parameters( parameter_file.read())

        ## Get echo level and parallel type
        verbosity = ProjectParameters["problem_data"]["echo_level"].GetInt()
        parallel_type = ProjectParameters["problem_data"]["parallel_type"].GetString()

        ## Fluid model part definition
        model = KratosMultiphysics.Model()
        #main_model_part = ModelPart(ProjectParameters["problem_data"]["model_part_name"].GetString())
        main_model_part = model(ProjectParameters["problem_data"]["model_part_name"].GetString())
        main_model_part.ProcessInfo.SetValue(DOMAIN_SIZE, ProjectParameters["problem_data"]["domain_size"].GetInt())

        alpharad = AOA*pi/180.0
        chord_normal_X = sin(alpharad)
        chord_normal_Y = cos(alpharad)
        
        main_model_part.ProcessInfo.SetValue(Y1, chord_normal_X)
        main_model_part.ProcessInfo.SetValue(Y2, chord_normal_Y)

        ###TODO replace this "model" for real one once available
        #Model = {ProjectParameters["problem_data"]["model_part_name"].GetString() : main_model_part}
        #model = KratosMultiphysics.Model()

        #Set Mesh input_filename
        #mdpa_file_name = input_mdpa_path + "naca0012Mesh" +str(case)
        mdpa_file_name = input_mdpa_path + 'naca0012_Case_' + str(case) + '_AOA_' + str(
                AOA) + '_Far_Field_Mesh_Size_' + str(FarField_MeshSize) + '_Airfoil_Mesh_Size_' + str(Airfoil_MeshSize)

        ProjectParameters["solver_settings"]["model_import_settings"]["input_filename"].SetString(mdpa_file_name)
        ProjectParameters["boundary_conditions_process_list"][2]["Parameters"]["angle_of_attack"].SetDouble(AOA)
        ProjectParameters["boundary_conditions_process_list"][2]["Parameters"]["airfoil_meshsize"].SetDouble(Airfoil_MeshSize)
        ProjectParameters["boundary_conditions_process_list"][2]["Parameters"]["energy_reference"].SetDouble(energy_reference)
        ProjectParameters["boundary_conditions_process_list"][2]["Parameters"]["potential_energy_reference"].SetDouble(potential_energy_reference)
        ProjectParameters["boundary_conditions_process_list"][2]["Parameters"]["cl_ok_reference"].SetDouble(cl_ok_reference)
        
        ## Solver construction    
        solver = potential_flow_solver.CreateSolver(main_model_part, ProjectParameters["solver_settings"])

        solver.AddVariables()

        ## Read the model - note that SetBufferSize is done here
        solver.ImportModelPart()

        ## Add AddDofs
        solver.AddDofs()

        
        ## Set output name
        #problem_name = output_gid_path + 'AOA_' + str(AOA) + '/' + ProjectParameters["problem_data"]["problem_name"].GetString()+ "Mesh" + str(case)
        problem_name = output_gid_path + 'AOA_' + str(AOA) + '/' + ProjectParameters["problem_data"]["problem_name"].GetString()+ '_Case_' + str(case) + '_AOA_' + str(
                AOA) + '_Far_Field_Mesh_Size_' + str(FarField_MeshSize) + '_Airfoil_Mesh_Size_' + str(Airfoil_MeshSize)

        ## Initialize GiD  I/O
        if (parallel_type == "OpenMP"):
            from gid_output_process import GiDOutputProcess
            gid_output = GiDOutputProcess(solver.GetComputingModelPart(),
                                        problem_name ,
                                        ProjectParameters["output_configuration"])

        gid_output.ExecuteInitialize()

        ##TODO: replace MODEL for the Kratos one ASAP
        ## Get the list of the skin submodel parts in the object Model
        for i in range(ProjectParameters["solver_settings"]["skin_parts"].size()):
            skin_part_name = ProjectParameters["solver_settings"]["skin_parts"][i].GetString()
            #Model.update({skin_part_name: main_model_part.GetSubModelPart(skin_part_name)})
            model.update({skin_part_name: main_model_part.GetSubModelPart(skin_part_name)})

        ## Get the list of the no-skin submodel parts in the object Model (results processes and no-skin conditions)
        for i in range(ProjectParameters["solver_settings"]["no_skin_parts"].size()):
            no_skin_part_name = ProjectParameters["solver_settings"]["no_skin_parts"][i].GetString()
            #Model.update({no_skin_part_name: main_model_part.GetSubModelPart(no_skin_part_name)})
            model.update({no_skin_part_name: main_model_part.GetSubModelPart(no_skin_part_name)})

        ## Print model_part and properties
        if(verbosity > 1):
            print("")
            print(main_model_part)
            for properties in main_model_part.Properties:
                print(properties)

        ## Processes construction
        import process_factory
        # "list_of_processes" contains all the processes already constructed (boundary conditions, initial conditions and gravity)
        # Note 1: gravity is firstly constructed. Outlet process might need its information.
        # Note 2: conditions are constructed before BCs. Otherwise, they may overwrite the BCs information.
        #ProjectParameters["boundary_conditions_process_list"]["model_import_settings"]["input_filename"].SetString(mdpa_file_name)
        #ProjectParameters["boundary_conditions_process_list"][2]["Parameters"]["mesh_refinement_file_name"].SetString(mesh_refinement_file_name)
        #list_of_processes = process_factory.KratosProcessFactory(Model).ConstructListOfProcesses( ProjectParameters["boundary_conditions_process_list"] )
        list_of_processes = process_factory.KratosProcessFactory(model).ConstructListOfProcesses( ProjectParameters["boundary_conditions_process_list"] )
        if(verbosity > 1):
            for process in list_of_processes:
                print(process)

        ## Processes initialization
        for process in list_of_processes:
            process.ExecuteInitialize()

        ## Solver initialization
        solver.Initialize()

        #TODO: think if there is a better way to do this
        fluid_model_part = solver.GetComputingModelPart()

        ## Stepping and time settings
        # Dt = ProjectParameters["problem_data"]["time_step"].GetDouble()
        start_time = ProjectParameters["problem_data"]["start_time"].GetDouble()
        end_time = ProjectParameters["problem_data"]["end_time"].GetDouble()

        time = start_time
        step = 0
        out = 0.0

        gid_output.ExecuteBeforeSolutionLoop()

        for process in list_of_processes:
            process.ExecuteBeforeSolutionLoop()

        ## Writing the full ProjectParameters file before solving
        if ((parallel_type == "OpenMP") or (KratosMPI.mpi.rank == 0)) and (verbosity > 0):
            f = open("ProjectParametersOutput.json", 'w')
            f.write(ProjectParameters.PrettyPrintJsonString())
            f.close()

        Dt = 0.01
        step += 1
        time = time + Dt
        main_model_part.CloneTimeStep(time)

        if (parallel_type == "OpenMP") or (KratosMPI.mpi.rank == 0):
            print("")
            print("STEP = ", step)
            print("TIME = ", time)

        for process in list_of_processes:
            process.ExecuteInitializeSolutionStep()

        gid_output.ExecuteInitializeSolutionStep()

        solver.Solve()

        for process in list_of_processes:
            process.ExecuteFinalizeSolutionStep()

        gid_output.ExecuteFinalizeSolutionStep()

        #TODO: decide if it shall be done only when output is processed or not
        for process in list_of_processes:
            process.ExecuteBeforeOutputStep()

        if gid_output.IsOutputStep():
            gid_output.PrintOutput()

        for process in list_of_processes:
            process.ExecuteAfterOutputStep()

        out = out + Dt

        gid_output.ExecuteFinalize()

        #output cp
        loads_output.write_cp_figures(cp_data_directory_name, AOA, case, Airfoil_MeshSize, FarField_MeshSize, work_dir)
        shutil.copytree(cp_results_directory_name, cp_data_directory_name)

        latex = subprocess.Popen(['pdflatex', '-interaction=batchmode', work_dir + 'plots/cp/cp.tex'], stdout=latex_output)
        latex.communicate()

        cp_file_name = work_dir + 'plots/cp/plots/cp_Case_' + str(case) + '_AOA_' + str(
                AOA) + '_Far_Field_Mesh_Size_' + str(FarField_MeshSize) + '_Airfoil_Mesh_Size_' + str(Airfoil_MeshSize) + '.pdf'
        shutil.copyfile('cp.pdf',cp_file_name)
        merger.append(PdfFileReader(cp_file_name), 'case_' + str(case))
        merger_global.append(PdfFileReader(cp_file_name), 'case_' + str(case))

        #output far field
        loads_output.write_figures_far_field(far_field_data_directory_name, AOA, case, Airfoil_MeshSize,  FarField_MeshSize, work_dir)
        shutil.copytree(far_field_results_directory_name, far_field_data_directory_name)

        latex_far_field = subprocess.Popen(['pdflatex', '-interaction=batchmode',work_dir + 'plots/far_field/main_far_field_x.tex'], stdout=latex_output)
        latex_far_field.communicate()

        latex_far_field = subprocess.Popen(['pdflatex', '-interaction=batchmode',work_dir + 'plots/far_field/main_far_field_y.tex'], stdout=latex_output)
        latex_far_field.communicate()

        far_field_x_file_name = work_dir + 'plots/far_field/plots/velocity_x_Case_' + str(case) + '_AOA_' + str(
                AOA) + '_Far_Field_Mesh_Size_' + str(FarField_MeshSize) + '_Airfoil_Mesh_Size_' + str(Airfoil_MeshSize) + '.pdf'
        shutil.copyfile('main_far_field_x.pdf',far_field_x_file_name)
        merger_local_far_field_x.append(PdfFileReader(far_field_x_file_name), 'case_' + str(case))
        merger_global_far_field_x.append(PdfFileReader(far_field_x_file_name), 'case_' + str(case))

        far_field_y_file_name = work_dir + 'plots/far_field/plots/velocity_y_Case_' + str(case) + '_AOA_' + str(
                AOA) + '_Far_Field_Mesh_Size_' + str(FarField_MeshSize) + '_Airfoil_Mesh_Size_' + str(Airfoil_MeshSize) + '.pdf'
        shutil.copyfile('main_far_field_y.pdf',far_field_y_file_name)
        merger_local_far_field_y.append(PdfFileReader(far_field_y_file_name), 'case_' + str(case))
        merger_global_far_field_y.append(PdfFileReader(far_field_y_file_name), 'case_' + str(case))

        #output jump
        loads_output.write_jump_figures(jump_data_directory_name, AOA, case, Airfoil_MeshSize, FarField_MeshSize, work_dir)
        shutil.copytree(jump_results_directory_name, jump_data_directory_name)

        latex = subprocess.Popen(['pdflatex', '-interaction=batchmode', work_dir + 'plots/potential_jump/main_jump.tex'], stdout=latex_output)
        latex.communicate()

        jump_file_name = work_dir + 'plots/potential_jump/plots/jump_Case_' + str(case) + '_AOA_' + str(
                AOA) + '_Far_Field_Mesh_Size_' + str(FarField_MeshSize) + '_Airfoil_Mesh_Size_' + str(Airfoil_MeshSize) + '.pdf'
        shutil.copyfile('main_jump.pdf',jump_file_name)
        merger_local_jump.append(PdfFileReader(jump_file_name), 'case_' + str(case))
        merger_global_jump.append(PdfFileReader(jump_file_name), 'case_' + str(case))

        if(counter < 1):
            energy_reference = main_model_part.ProcessInfo[ENERGY_NORM_REFERENCE]
            potential_energy_reference = main_model_part.ProcessInfo[POTENTIAL_ENERGY_REFERENCE]
            cl_ok_reference = main_model_part.ProcessInfo[K0]
            for process in list_of_processes:
                process.ExecuteFinalize()

        '''
        if(case % 2 == 0):
            Airfoil_Refinement_Factor_Effective = 2
        else:
            Airfoil_Refinement_Factor_Effective = 5
        '''
        Airfoil_MeshSize *= Airfoil_Refinement_Factor
        FarField_MeshSize /= FarField_Refinement_Factor
        
        case +=1
        counter +=1.0
    
    
    
    os.rename(work_dir + "mesh_refinement_loads.dat", mesh_refinement_file_name)
    
    loads_output.write_figures_cl(cl_data_directory_name, AOA, work_dir)
    loads_output.write_figures_cl_error(cl_error_data_directory_name, AOA, work_dir)
    loads_output.write_figures_cd(cd_data_directory_name, AOA, work_dir)
    loads_output.write_figures_condition(condition_data_directory_name, AOA, work_dir)
    loads_output.write_figures_energy(energy_data_directory_name, AOA, work_dir)
    
    shutil.copytree(cl_results_directory_name, work_dir + 'plots/cl/' + cl_data_directory_name)
    os.remove(cl_results_file_name)
    os.remove(cl_reference_file_name)
    os.remove(cl_far_field_results_file_name)

    shutil.copytree(cl_error_results_directory_name, work_dir + 'plots/cl_error/' + cl_error_data_directory_name)
    os.remove(cl_error_results_file_name)
    os.remove(cl_error_results_h_file_name)
    os.remove(cl_error_results_h_log_file_name)
    os.remove(cl_error_results_h_log_ok_file_name)
    os.remove(cl_far_field_error_results_file_name)
    os.remove(cl_far_field_error_results_h_file_name)
    os.remove(cl_far_field_error_results_h_log_file_name)

    shutil.copytree(energy_results_directory_name, work_dir + 'plots/relative_error_energy_norm/' + energy_data_directory_name)
    os.remove(energy_h_results_file_name)
    os.remove(energy_n_results_file_name)
    os.remove(energy_variant_h_results_file_name)
    os.remove(energy_variant_n_results_file_name)

    shutil.copytree(cd_results_directory_name, work_dir + 'plots/cd/' + cd_data_directory_name)
    os.remove(cd_results_file_name)

    shutil.copytree(condition_results_directory_name, work_dir + 'plots/condition_number/' + condition_data_directory_name)
    os.remove(condition_results_file_name)

    cp_final_file_name = work_dir + 'plots/cp/cp_AOA_' + str(AOA) + '.pdf'
    merger.write(cp_final_file_name)

    far_field_x_final_file_name = work_dir + 'plots/far_field/far_field_x_AOA_' + str(AOA) + '.pdf'
    merger_local_far_field_x.write(far_field_x_final_file_name)

    far_field_y_final_file_name = work_dir + 'plots/far_field/far_field_y_AOA_' + str(AOA) + '.pdf'
    merger_local_far_field_y.write(far_field_y_final_file_name)

    jump_final_file_name = work_dir + 'plots/potential_jump/jump_AOA_' + str(AOA) + '.pdf'
    merger_local_jump.write(jump_final_file_name)

    AOA += AOA_Increment

cp_final_global_file_name = work_dir + 'plots/cp/cp_all.pdf'
merger_global.write(cp_final_global_file_name)

far_field_x_global_file_name = work_dir + 'plots/far_field/far_field_x_all.pdf'
merger_global_far_field_x.write(far_field_x_global_file_name)

far_field_y_global_file_name = work_dir + 'plots/far_field/far_field_y_all.pdf'
merger_global_far_field_y.write(far_field_y_global_file_name)

jump_final_global_file_name = work_dir + 'plots/potential_jump/jump_all.pdf'
merger_global_jump.write(jump_final_global_file_name)
