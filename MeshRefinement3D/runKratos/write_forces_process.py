import KratosMultiphysics
from KratosMultiphysics.CompressiblePotentialFlowApplication.compute_lift_process import ComputeLiftProcess
import KratosMultiphysics.CompressiblePotentialFlowApplication as CPFApp
import math

def _DotProduct(A,B):
    return sum(i[0]*i[1] for i in zip(A, B))

def Factory(settings, Model):
    if( not isinstance(settings,KratosMultiphysics.Parameters) ):
        raise Exception("expected input shall be a Parameters object, encapsulating a json string")
    return WriteForcesProcess(Model, settings["Parameters"])

class WriteForcesProcess(ComputeLiftProcess):
    def __init__(self, Model, settings ):
        KratosMultiphysics.Process.__init__(self)

        default_parameters = KratosMultiphysics.Parameters(r'''{
            "model_part_name": "",
            "far_field_model_part_name": "",
            "middle_airfoil_model_part_name": "",
            "moment_reference_point" : [0.0,0.0,0.0],
            "trailing_edge_model_part_name": "",
            "trefft_plane_cut_model_part_name": "",
            "is_infinite_wing": false,
            "growth_rate_domain": 0.0,
            "growth_rate_wing": 0.0,
            "angle_of_attack": 0.0,
            "minimum_mesh_growth_rate": 0.0,
            "section_100_model_part_name": "",
            "section_150_model_part_name": "",
            "section_180_model_part_name": ""
        }''')

        settings.ValidateAndAssignDefaults(default_parameters)

        self.body_model_part = Model[settings["model_part_name"].GetString()]
        far_field_model_part_name = settings["far_field_model_part_name"].GetString()
        if far_field_model_part_name != "":
            self.far_field_model_part = Model[far_field_model_part_name]
            self.compute_far_field_forces = True
        self.compute_lift_from_jump_3d = False
        trailing_edge_model_part_name = settings["trailing_edge_model_part_name"].GetString()
        if(trailing_edge_model_part_name != ""):
            self.trailing_edge_model_part = Model[trailing_edge_model_part_name]
            self.compute_lift_from_jump_3d = True
        self.fluid_model_part = self.body_model_part.GetRootModelPart()
        self.reference_area =  self.fluid_model_part.ProcessInfo.GetValue(CPFApp.REFERENCE_CHORD)
        self.moment_reference_point = settings["moment_reference_point"].GetVector()
        self.is_infinite_wing = settings["is_infinite_wing"].GetBool()

        trefft_plane_cut_model_part_name = settings["trefft_plane_cut_model_part_name"].GetString()
        if trefft_plane_cut_model_part_name != "":
            self.compute_trefft_plane_forces = True
            if not self.fluid_model_part.HasSubModelPart(trefft_plane_cut_model_part_name):
                trefft_plane_cut_model_part_name = 'Trefft_Plane_Cut'
                self.trefft_plane_cut_model_part = self.fluid_model_part.CreateSubModelPart(trefft_plane_cut_model_part_name)
            else: self.trefft_plane_cut_model_part = self.fluid_model_part.GetSubModelPart(trefft_plane_cut_model_part_name)

        if not self.reference_area > 0.0:
            raise Exception('The reference area should be larger than 0.')

        self.Growth_Rate_Domain = settings["growth_rate_domain"].GetDouble()
        self.Growth_Rate_Wing = settings["growth_rate_wing"].GetDouble()
        self.AOA = settings["angle_of_attack"].GetDouble()
        self.minimum_mesh_growth_rate = settings["minimum_mesh_growth_rate"].GetDouble()
        self.input_dir_path = 'TBD'

        middle_airfoil_model_part_name = settings["middle_airfoil_model_part_name"].GetString()
        if middle_airfoil_model_part_name != "":
            if not self.fluid_model_part.HasSubModelPart(middle_airfoil_model_part_name):
                middle_airfoil_model_part_name = 'Middle_Airfoil'
                self.middle_airfoil_model_part = self.fluid_model_part.CreateSubModelPart(middle_airfoil_model_part_name)
            else: self.middle_airfoil_model_part = self.fluid_model_part.GetSubModelPart(middle_airfoil_model_part_name)

        section_100_model_part_name = settings["section_100_model_part_name"].GetString()
        if section_100_model_part_name != "":
            if not self.fluid_model_part.HasSubModelPart(section_100_model_part_name):
                section_100_model_part_name = 'Section_100'
                self.section_100_model_part = self.fluid_model_part.CreateSubModelPart(section_100_model_part_name)
            else: self.section_100_model_part = self.fluid_model_part.GetSubModelPart(section_100_model_part_name)

        section_150_model_part_name = settings["section_150_model_part_name"].GetString()
        if section_150_model_part_name != "":
            if not self.fluid_model_part.HasSubModelPart(section_150_model_part_name):
                section_150_model_part_name = 'section_150'
                self.section_150_model_part = self.fluid_model_part.CreateSubModelPart(section_150_model_part_name)
            else: self.section_150_model_part = self.fluid_model_part.GetSubModelPart(section_150_model_part_name)

        section_180_model_part_name = settings["section_180_model_part_name"].GetString()
        if section_180_model_part_name != "":
            if not self.fluid_model_part.HasSubModelPart(section_180_model_part_name):
                section_180_model_part_name = 'section_180'
                self.section_180_model_part = self.fluid_model_part.CreateSubModelPart(section_180_model_part_name)
            else: self.section_180_model_part = self.fluid_model_part.GetSubModelPart(section_180_model_part_name)

        self.moment_coefficient = KratosMultiphysics.Vector(3, 0.0)

    def ExecuteFinalizeSolutionStep(self):
        super(WriteForcesProcess, self).ExecuteFinalizeSolutionStep()

        nodal_value_process = CPFApp.ComputeNodalValueProcess(self.fluid_model_part, ["PRESSURE_COEFFICIENT"])
        nodal_value_process.Execute()

        if self.compute_trefft_plane_forces:
            potential_integral = 0.0
            drag_integral = 0.0
            for cond in self.trefft_plane_cut_model_part.Conditions:
                length = cond.GetGeometry().Area()
                for node in cond.GetNodes():
                    potential = node.GetSolutionStepValue(CPFApp.VELOCITY_POTENTIAL)
                    auxiliary_potential = node.GetSolutionStepValue(CPFApp.AUXILIARY_VELOCITY_POTENTIAL)
                    velocity = node.GetValue(KratosMultiphysics.VELOCITY)
                    velocity_normal_component = _DotProduct(self.wake_normal,velocity)
                    potential_jump = auxiliary_potential - potential
                    potential_integral += 0.5 * length * potential_jump
                    drag_integral -= 0.5 * length * potential_jump * velocity_normal_component

            self.lift_coefficient_jump_trefft = 2*potential_integral/(self.free_stream_velocity_norm*self.reference_area)

            free_stream_velocity = self.fluid_model_part.ProcessInfo.GetValue(CPFApp.FREE_STREAM_VELOCITY)
            free_stream_velocity_norm2 = _DotProduct(free_stream_velocity,free_stream_velocity)
            self.drag_coefficient_jump_trefft = drag_integral/(free_stream_velocity_norm2*self.reference_area)
            KratosMultiphysics.Logger.PrintInfo('ComputeLiftProcess',' Cl = ', self.lift_coefficient_jump_trefft, 'Potential Jump Trefft Plane')
            KratosMultiphysics.Logger.PrintInfo('ComputeLiftProcess',' Cd = ', self.drag_coefficient_jump_trefft, 'Potential Jump Trefft Plane')


        # with open('results_3d_finite_wing.dat', 'a') as file:
        #     file.write('{0:12.4f} {1:12.4f} {2:12.4f} {3:12.2e} {4:12.2e} {4:12.2e} {6:12.4e}'.format(
        #         self.lift_coefficient, # 0
        #         self.lift_coefficient_far_field, #  1
        #         self.lift_coefficient_jump, # 2
        #         self.drag_coefficient, # 3
        #         self.drag_coefficient_far_field, # 4
        #         self.lateral_force_coefficient, # 5
        #         self.lateral_force_coefficient_far_field)) # 6
        #     file.flush()

        NumberOfNodes = self.fluid_model_part.NumberOfNodes()
        self.cl_reference = self.read_cl_reference(self.AOA)
        self.cd_reference = self.read_cd_reference(self.AOA)
        self.cm_reference = self.read_cm_reference(self.AOA)

        if(abs(self.cl_reference) < 1e-6):
            self.cl_p_relative_error = abs(self.lift_coefficient - self.cl_reference)
        else:
            self.cl_p_relative_error = abs(self.lift_coefficient - self.cl_reference)/abs(self.cl_reference)*100.0

        if(abs(self.cd_reference) < 1e-6):
            self.cd_p_relative_error = abs(self.drag_coefficient - self.cd_reference)
        else:
            self.cd_p_relative_error = abs(self.drag_coefficient - self.cd_reference)/abs(self.cd_reference)*100.0

        if(abs(self.cm_reference) < 1e-6):
            self.cm_p_relative_error = abs(self.moment_coefficient[1] - self.cm_reference)
        else:
            self.cm_p_relative_error = abs(self.moment_coefficient[1] - self.cm_reference)/abs(self.cm_reference)*100.0

        cl_data_directory_name = self.input_dir_path + '/plots/cl/' + 'data/cl_AOA_' + str(self.AOA)
        cl_p_results_file_name = cl_data_directory_name + '/cl_p_results_GRD_' +  str(self.Growth_Rate_Domain) + '.dat'
        with open(cl_p_results_file_name,'a') as cl_file:
            cl_file.write('{0:16.2e} {1:15f}\n'.format(NumberOfNodes, self.lift_coefficient))
            cl_file.flush()

        cl_f_results_file_name = cl_data_directory_name + '/cl_f_results_GRD_' +  str(self.Growth_Rate_Domain) + '.dat'
        with open(cl_f_results_file_name,'a') as cl_file:
            cl_file.write('{0:16.2e} {1:15f}\n'.format(NumberOfNodes, self.lift_coefficient_far_field))
            cl_file.flush()

        cl_j_results_file_name = cl_data_directory_name + '/cl_j_results_GRD_' +  str(self.Growth_Rate_Domain) + '.dat'
        with open(cl_j_results_file_name,'a') as cl_file:
            cl_file.write('{0:16.2e} {1:15f}\n'.format(NumberOfNodes, self.lift_coefficient_jump))
            cl_file.flush()

        cl_reference_results_file_name = cl_data_directory_name + '/cl_ref.dat'
        with open(cl_reference_results_file_name,'a') as cl_file:
            cl_file.write('{0:16.2e} {1:15f}\n'.format(NumberOfNodes, self.cl_reference))
            cl_file.flush()

        cd_data_directory_name = self.input_dir_path + '/plots/cd/' + 'data/cd_AOA_' + str(self.AOA)
        cd_p_results_file_name = cd_data_directory_name + '/cd_p_results_GRD_' +  str(self.Growth_Rate_Domain) + '.dat'
        with open(cd_p_results_file_name,'a') as cl_file:
            cl_file.write('{0:16.2e} {1:15f}\n'.format(NumberOfNodes, self.drag_coefficient))
            cl_file.flush()

        cd_results_file_name = cd_data_directory_name + '/cd_f_results_GRD_' +  str(self.Growth_Rate_Domain) + '.dat'
        with open(cd_results_file_name,'a') as cl_file:
            cl_file.write('{0:16.2e} {1:15f}\n'.format(NumberOfNodes, self.drag_coefficient_far_field))
            cl_file.flush()

        cd_reference_results_file_name = cd_data_directory_name + '/cd_ref.dat'
        with open(cd_reference_results_file_name,'a') as cl_file:
            cl_file.write('{0:16.2e} {1:15f}\n'.format(NumberOfNodes, self.cd_reference))
            cl_file.flush()

        cm_data_directory_name = self.input_dir_path + '/plots/cm/' + 'data/cm_AOA_' + str(self.AOA)
        cm_results_file_name = cm_data_directory_name + '/cm_p_results_GRD_' +  str(self.Growth_Rate_Domain) + '.dat'
        with open(cm_results_file_name,'a') as cl_file:
            cl_file.write('{0:16.2e} {1:15f}\n'.format(NumberOfNodes, self.moment_coefficient[1]))
            cl_file.flush()

        cm_reference_results_file_name = cm_data_directory_name + '/cm_ref.dat'
        with open(cm_reference_results_file_name,'a') as cl_file:
            cl_file.write('{0:16.2e} {1:15f}\n'.format(NumberOfNodes, self.cm_reference))
            cl_file.flush()

        cl_error_data_directory_name = self.input_dir_path + '/plots/cl_error/' + 'data/cl_error_AOA_' + str(self.AOA)
        cl_error_p_results_file_name = cl_error_data_directory_name + '/cl_error_p_results_GRD_' +  str(self.Growth_Rate_Domain) + '.dat'
        with open(cl_error_p_results_file_name,'a') as cl_file:
            cl_file.write('{0:16.2e} {1:15f}\n'.format(NumberOfNodes, self.cl_p_relative_error))
            cl_file.flush()

        cd_error_data_directory_name = self.input_dir_path + '/plots/cd_error/' + 'data/cd_error_AOA_' + str(self.AOA)
        cd_error_p_results_file_name = cd_error_data_directory_name + '/cd_error_p_results_GRD_' +  str(self.Growth_Rate_Domain) + '.dat'
        with open(cd_error_p_results_file_name,'a') as cd_file:
            cd_file.write('{0:16.2e} {1:15f}\n'.format(NumberOfNodes, self.cd_p_relative_error))
            cd_file.flush()

        cm_error_data_directory_name = self.input_dir_path + '/plots/cm_error/' + 'data/cm_error_AOA_' + str(self.AOA)
        cm_error_p_results_file_name = cm_error_data_directory_name + '/cm_error_p_results_GRD_' +  str(self.Growth_Rate_Domain) + '.dat'
        with open(cm_error_p_results_file_name,'a') as cm_file:
            cm_file.write('{0:16.2e} {1:15f}\n'.format(NumberOfNodes, self.cm_p_relative_error))
            cm_file.flush()

        mesh_size = self.Growth_Rate_Wing * self.Growth_Rate_Domain
        if mesh_size < self.minimum_mesh_growth_rate + 1e-9:
            cl_aoa_results_file_name = self.input_dir_path + '/plots/cl_aoa/' + 'data/cl_aoa/cl_aoa.dat'
            with open(cl_aoa_results_file_name,'a') as cl_aoa_file:
                cl_aoa_file.write('{0:15f} {1:15f}\n'.format(self.AOA, self.lift_coefficient))
                cl_aoa_file.flush()

            cl_aoa_ref_results_file_name = self.input_dir_path + '/plots/cl_aoa/' + 'data/cl_aoa/cl_aoa_ref.dat'
            with open(cl_aoa_ref_results_file_name,'a') as cl_aoa_file:
                cl_aoa_file.write('{0:15f} {1:15f}\n'.format(self.AOA, self.cl_reference))
                cl_aoa_file.flush()

            cd_aoa_results_file_name = self.input_dir_path + '/plots/cd_aoa/' + 'data/cd_aoa/cd_aoa.dat'
            with open(cd_aoa_results_file_name,'a') as cd_aoa_file:
                cd_aoa_file.write('{0:15f} {1:15f}\n'.format(self.AOA, self.drag_coefficient))
                cd_aoa_file.flush()

            cd_aoa_ref_results_file_name = self.input_dir_path + '/plots/cd_aoa/' + 'data/cd_aoa/cd_aoa_ref.dat'
            with open(cd_aoa_ref_results_file_name,'a') as cd_aoa_file:
                cd_aoa_file.write('{0:15f} {1:15f}\n'.format(self.AOA, self.cd_reference))
                cd_aoa_file.flush()

            cm_aoa_results_file_name = self.input_dir_path + '/plots/cm_aoa/' + 'data/cm_aoa/cm_aoa.dat'
            with open(cm_aoa_results_file_name,'a') as cm_aoa_file:
                cm_aoa_file.write('{0:15f} {1:15f}\n'.format(self.AOA, self.moment_coefficient[1]))
                cm_aoa_file.flush()

            cm_aoa_ref_results_file_name = self.input_dir_path + '/plots/cm_aoa/' + 'data/cm_aoa/cm_aoa_ref.dat'
            with open(cm_aoa_ref_results_file_name,'a') as cm_aoa_file:
                cm_aoa_file.write('{0:15f} {1:15f}\n'.format(self.AOA, self.cm_reference))
                cm_aoa_file.flush()

        potential_jump_dir_name = self.input_dir_path + '/plots/potential_jump/data/AOA_' + str(self.AOA) + '/Growth_Rate_Domain_' + str(
        self.Growth_Rate_Domain) + '/Growth_Rate_Wing_' + str(self.Growth_Rate_Wing)

        potential_jump_file_name = potential_jump_dir_name + '/potential_jump_results.dat'

        with open(potential_jump_file_name, 'w') as jump_file:
            for node in self.trailing_edge_model_part.Nodes:
                potential = node.GetSolutionStepValue(CPFApp.VELOCITY_POTENTIAL)
                auxiliary_potential = node.GetSolutionStepValue(CPFApp.AUXILIARY_VELOCITY_POTENTIAL)
                potential_jump = potential - auxiliary_potential

                jump_file.write('{0:15f} {1:15f}\n'.format(node.Y, potential_jump))

        potential_jump_file_name = potential_jump_dir_name + '/potential_jump_trefftz_results.dat'

        with open(potential_jump_file_name, 'w') as jump_file:
            for node in self.trefft_plane_cut_model_part.Nodes:
                potential = node.GetSolutionStepValue(CPFApp.VELOCITY_POTENTIAL)
                auxiliary_potential = node.GetSolutionStepValue(CPFApp.AUXILIARY_VELOCITY_POTENTIAL)
                potential_jump = auxiliary_potential - potential

                jump_file.write('{0:15f} {1:15f}\n'.format(node.Y, potential_jump))

        cp_dir_name = self.input_dir_path + '/plots/cp/data/AOA_' + str(self.AOA) + '/Growth_Rate_Domain_' + str(
        self.Growth_Rate_Domain) + '/Growth_Rate_Wing_' + str(self.Growth_Rate_Wing)

        cp_file_name = cp_dir_name + '/cp_results.dat'

        aoa_rad = self.AOA * math.pi / 180.0
        with open(cp_file_name, 'w') as cp_file:
            for node in self.middle_airfoil_model_part.Nodes:
                pressure_coeffient = node.GetValue(KratosMultiphysics.PRESSURE_COEFFICIENT)
                x = node.X * math.cos(aoa_rad) - node.Z * math.sin(aoa_rad) + 0.5
                #x = node.X + 0.5
                #if node.GetValue(CPFApp.UPPER_SURFACE):
                cp_file.write('{0:15f} {1:15f}\n'.format(x, pressure_coeffient))

        cp_tikz_file_name = cp_dir_name + '/cp.tikz'
        output_file_name = cp_dir_name + '/aoa' + str(int(self.AOA)) + '.dat'
        with open(cp_tikz_file_name,'w') as cp_tikz_file:
            cp_tikz_file.write('\\begin{tikzpicture}\n' +
            '\\begin{axis}[\n' +
            '    title={ $c_l$ = ' + "{:.6f}".format(self.lift_coefficient) + ' $c_d$ = ' + "{:.6f}".format(self.drag_coefficient) + '},\n' +
            '    xlabel={$x/c$},\n' +
            '    ylabel={$c_p[\\unit{-}$]},\n' +
            '    %xmin=-0.01, xmax=1.01,\n' +
            '    y dir=reverse,\n' +
            '    %xtick={0,0.2,0.4,0.6,0.8,1},\n' +
            '    %xticklabels={0,0.2,0.4,0.6,0.8,1},\n' +
            '    ymajorgrids=true,\n' +
            '    xmajorgrids=true,\n' +
            '    grid style=dashed,\n' +
            '    legend style={at={(0.5,-0.2)},anchor=north},\n' +
            '    width=12cm\n' +
            ']\n\n' +
            '\\addplot[\n' +
            '    only marks,\n' +
            '    color=red,\n' +
            #'    mark=square,\n' +
            '    mark=*,\n' +
            '    mark size=1pt,\n' +
            '    ]\n' +
            '    table {cp_results.dat};  \n' +
            '    \\addlegendentry{Kratos}\n\n' +
            '\\addplot[\n' +
            '    color=black,\n' +
            '    mark=none,\n' +
            '    mark options={solid},\n' +
            '    ]\n' +
            '    table {' + output_file_name + '};  \n' +
            '    \\addlegendentry{XFLR5}\n\n' +
            '\end{axis}\n' +
            '\end{tikzpicture}')
            cp_tikz_file.flush()

        cp_100_dir_name = self.input_dir_path + '/plots/cp_section_100/data/AOA_' + str(self.AOA) + '/Growth_Rate_Domain_' + str(
        self.Growth_Rate_Domain) + '/Growth_Rate_Wing_' + str(self.Growth_Rate_Wing)

        cp_100_file_name = cp_100_dir_name + '/cp_results.dat'

        aoa_rad = self.AOA * math.pi / 180.0
        with open(cp_100_file_name, 'w') as cp_file:
            for node in self.section_100_model_part.Nodes:
                pressure_coeffient = node.GetValue(KratosMultiphysics.PRESSURE_COEFFICIENT)
                x = node.X * math.cos(aoa_rad) - node.Z * math.sin(aoa_rad) + 0.5
                #x = node.X + 0.5
                #if node.GetValue(CPFApp.UPPER_SURFACE):
                cp_file.write('{0:15f} {1:15f}\n'.format(x, pressure_coeffient))

        cp_tikz_file_name = cp_100_dir_name + '/cp.tikz'
        output_file_name = cp_100_dir_name + '/aoa' + str(int(self.AOA)) + '.dat'
        with open(cp_tikz_file_name,'w') as cp_tikz_file:
            cp_tikz_file.write('\\begin{tikzpicture}\n' +
            '\\begin{axis}[\n' +
            '    title={ Section 100, $c_l$ = ' + "{:.6f}".format(self.lift_coefficient) + ' $c_d$ = ' + "{:.6f}".format(self.drag_coefficient) + '},\n' +
            '    xlabel={$x/c$},\n' +
            '    ylabel={$c_p[\\unit{-}$]},\n' +
            '    %xmin=-0.01, xmax=1.01,\n' +
            '    y dir=reverse,\n' +
            '    %xtick={0,0.2,0.4,0.6,0.8,1},\n' +
            '    %xticklabels={0,0.2,0.4,0.6,0.8,1},\n' +
            '    ymajorgrids=true,\n' +
            '    xmajorgrids=true,\n' +
            '    grid style=dashed,\n' +
            '    legend style={at={(0.5,-0.2)},anchor=north},\n' +
            '    width=12cm\n' +
            ']\n\n' +
            '\\addplot[\n' +
            '    only marks,\n' +
            '    color=red,\n' +
            #'    mark=square,\n' +
            '    mark=*,\n' +
            '    mark size=1pt,\n' +
            '    ]\n' +
            '    table {cp_results.dat};  \n' +
            '    \\addlegendentry{Kratos}\n\n' +
            '\\addplot[\n' +
            '    color=black,\n' +
            '    mark=none,\n' +
            '    mark options={solid},\n' +
            '    ]\n' +
            '    table {' + output_file_name + '};  \n' +
            '    \\addlegendentry{XFLR5}\n\n' +
            '\end{axis}\n' +
            '\end{tikzpicture}')
            cp_tikz_file.flush()

        cp_150_dir_name = self.input_dir_path + '/plots/cp_section_150/data/AOA_' + str(self.AOA) + '/Growth_Rate_Domain_' + str(
        self.Growth_Rate_Domain) + '/Growth_Rate_Wing_' + str(self.Growth_Rate_Wing)

        cp_150_file_name = cp_150_dir_name + '/cp_results.dat'

        aoa_rad = self.AOA * math.pi / 180.0
        with open(cp_150_file_name, 'w') as cp_file:
            for node in self.section_150_model_part.Nodes:
                pressure_coeffient = node.GetValue(KratosMultiphysics.PRESSURE_COEFFICIENT)
                x = node.X * math.cos(aoa_rad) - node.Z * math.sin(aoa_rad) + 0.5
                #x = node.X + 0.5
                #if node.GetValue(CPFApp.UPPER_SURFACE):
                cp_file.write('{0:15f} {1:15f}\n'.format(x, pressure_coeffient))

        cp_tikz_file_name = cp_150_dir_name + '/cp.tikz'
        output_file_name = cp_150_dir_name + '/aoa' + str(int(self.AOA)) + '.dat'
        with open(cp_tikz_file_name,'w') as cp_tikz_file:
            cp_tikz_file.write('\\begin{tikzpicture}\n' +
            '\\begin{axis}[\n' +
            '    title={ Section 150, $c_l$ = ' + "{:.6f}".format(self.lift_coefficient) + ' $c_d$ = ' + "{:.6f}".format(self.drag_coefficient) + '},\n' +
            '    xlabel={$x/c$},\n' +
            '    ylabel={$c_p[\\unit{-}$]},\n' +
            '    %xmin=-0.01, xmax=1.01,\n' +
            '    y dir=reverse,\n' +
            '    %xtick={0,0.2,0.4,0.6,0.8,1},\n' +
            '    %xticklabels={0,0.2,0.4,0.6,0.8,1},\n' +
            '    ymajorgrids=true,\n' +
            '    xmajorgrids=true,\n' +
            '    grid style=dashed,\n' +
            '    legend style={at={(0.5,-0.2)},anchor=north},\n' +
            '    width=12cm\n' +
            ']\n\n' +
            '\\addplot[\n' +
            '    only marks,\n' +
            '    color=red,\n' +
            #'    mark=square,\n' +
            '    mark=*,\n' +
            '    mark size=1pt,\n' +
            '    ]\n' +
            '    table {cp_results.dat};  \n' +
            '    \\addlegendentry{Kratos}\n\n' +
            '\\addplot[\n' +
            '    color=black,\n' +
            '    mark=none,\n' +
            '    mark options={solid},\n' +
            '    ]\n' +
            '    table {' + output_file_name + '};  \n' +
            '    \\addlegendentry{XFLR5}\n\n' +
            '\end{axis}\n' +
            '\end{tikzpicture}')
            cp_tikz_file.flush()

        cp_180_dir_name = self.input_dir_path + '/plots/cp_section_180/data/AOA_' + str(self.AOA) + '/Growth_Rate_Domain_' + str(
        self.Growth_Rate_Domain) + '/Growth_Rate_Wing_' + str(self.Growth_Rate_Wing)

        cp_180_file_name = cp_180_dir_name + '/cp_results.dat'

        aoa_rad = self.AOA * math.pi / 180.0
        with open(cp_180_file_name, 'w') as cp_file:
            for node in self.section_180_model_part.Nodes:
                pressure_coeffient = node.GetValue(KratosMultiphysics.PRESSURE_COEFFICIENT)
                x = node.X * math.cos(aoa_rad) - node.Z * math.sin(aoa_rad) + 0.5
                #x = node.X + 0.5
                #if node.GetValue(CPFApp.UPPER_SURFACE):
                cp_file.write('{0:15f} {1:15f}\n'.format(x, pressure_coeffient))

        cp_tikz_file_name = cp_180_dir_name + '/cp.tikz'
        output_file_name = cp_180_dir_name + '/aoa' + str(int(self.AOA)) + '.dat'
        with open(cp_tikz_file_name,'w') as cp_tikz_file:
            cp_tikz_file.write('\\begin{tikzpicture}\n' +
            '\\begin{axis}[\n' +
            '    title={ Section 180, $c_l$ = ' + "{:.6f}".format(self.lift_coefficient) + ' $c_d$ = ' + "{:.6f}".format(self.drag_coefficient) + '},\n' +
            '    xlabel={$x/c$},\n' +
            '    ylabel={$c_p[\\unit{-}$]},\n' +
            '    %xmin=-0.01, xmax=1.01,\n' +
            '    y dir=reverse,\n' +
            '    %xtick={0,0.2,0.4,0.6,0.8,1},\n' +
            '    %xticklabels={0,0.2,0.4,0.6,0.8,1},\n' +
            '    ymajorgrids=true,\n' +
            '    xmajorgrids=true,\n' +
            '    grid style=dashed,\n' +
            '    legend style={at={(0.5,-0.2)},anchor=north},\n' +
            '    width=12cm\n' +
            ']\n\n' +
            '\\addplot[\n' +
            '    only marks,\n' +
            '    color=red,\n' +
            #'    mark=square,\n' +
            '    mark=*,\n' +
            '    mark size=1pt,\n' +
            '    ]\n' +
            '    table {cp_results.dat};  \n' +
            '    \\addlegendentry{Kratos}\n\n' +
            '\\addplot[\n' +
            '    color=black,\n' +
            '    mark=none,\n' +
            '    mark options={solid},\n' +
            '    ]\n' +
            '    table {' + output_file_name + '};  \n' +
            '    \\addlegendentry{XFLR5}\n\n' +
            '\end{axis}\n' +
            '\end{tikzpicture}')
            cp_tikz_file.flush()

        velocity_nodal_value_process = CPFApp.ComputeNodalValueProcess(self.fluid_model_part, ["VELOCITY"])
        velocity_nodal_value_process.Execute()



    def read_cl_reference(self,AOA):
        # Values computed with XFLR5 using the 3D inviscid panel method
        # with 40 panels in the chord direction and 40 in the span direction
        if(abs(AOA - 0.0) < 1e-3):
            return 0.0
        elif(abs(AOA - 1.0) < 1e-3):
            return 0.067343
        elif(abs(AOA - 2.0) < 1e-3):
            return 0.134628
        elif(abs(AOA - 3.0) < 1e-3):
            return 0.201797
        elif(abs(AOA - 4.0) < 1e-3):
            return 0.268793
        elif(abs(AOA - 5.0) < 1e-3):
            return 0.335557
        elif(abs(AOA - 6.0) < 1e-3):
            return 0.402033
        elif(abs(AOA - 7.0) < 1e-3):
            return 0.468165
        elif(abs(AOA - 8.0) < 1e-3):
            return 0.533897
        elif(abs(AOA - 9.0) < 1e-3):
            return 0.599175
        elif(abs(AOA - 10.0) < 1e-3):
            return 0.663944
        # elif(abs(AOA - 11.0) < 1e-3):
        #     return 1.3208
        # elif(abs(AOA - 12.0) < 1e-3):
        #     return 1.4392
        # elif(abs(AOA - 13.0) < 1e-3):
        #     return 1.5572
        # elif(abs(AOA - 14.0) < 1e-3):
        #     return 1.6746
        # elif(abs(AOA - 15.0) < 1e-3):
        #     return 1.7916
        else:
            return 0.0

    def read_cd_reference(self,AOA):
        # Values computed with XFLR5 using the 3D inviscid panel method
        # with 40 panels in the chord direction and 40 in the span direction
        if(abs(AOA - 0.0) < 1e-3):
            return 0.0
        elif(abs(AOA - 1.0) < 1e-3):
            return 0.000359
        elif(abs(AOA - 2.0) < 1e-3):
            return 0.001435
        elif(abs(AOA - 3.0) < 1e-3):
            return 0.003224
        elif(abs(AOA - 4.0) < 1e-3):
            return 0.005721
        elif(abs(AOA - 5.0) < 1e-3):
            return 0.008919
        elif(abs(AOA - 6.0) < 1e-3):
            return 0.012807
        elif(abs(AOA - 7.0) < 1e-3):
            return 0.017374
        elif(abs(AOA - 8.0) < 1e-3):
            return 0.022606
        elif(abs(AOA - 9.0) < 1e-3):
            return 0.028487
        elif(abs(AOA - 10.0) < 1e-3):
            return 0.034999
        # elif(abs(AOA - 11.0) < 1e-3):
        #     return 1.3208
        # elif(abs(AOA - 12.0) < 1e-3):
        #     return 1.4392
        # elif(abs(AOA - 13.0) < 1e-3):
        #     return 1.5572
        # elif(abs(AOA - 14.0) < 1e-3):
        #     return 1.6746
        # elif(abs(AOA - 15.0) < 1e-3):
        #     return 1.7916
        else:
            return 0.0

    def read_cm_reference(self,AOA):
        # Values computed with XFLR5 using the 3D inviscid panel method
        # with 40 panels in the chord direction and 40 in the span direction
        if(abs(AOA - 0.0) < 1e-3):
            return 0.0
        elif(abs(AOA - 1.0) < 1e-3):
            return -0.015634
        elif(abs(AOA - 2.0) < 1e-3):
            return -0.031218
        elif(abs(AOA - 3.0) < 1e-3):
            return -0.046734
        elif(abs(AOA - 4.0) < 1e-3):
            return -0.062163
        elif(abs(AOA - 5.0) < 1e-3):
            return -0.077485
        elif(abs(AOA - 6.0) < 1e-3):
            return -0.092683
        elif(abs(AOA - 7.0) < 1e-3):
            return -0.107738
        elif(abs(AOA - 8.0) < 1e-3):
            return -0.122632
        elif(abs(AOA - 9.0) < 1e-3):
            return -0.137345
        elif(abs(AOA - 10.0) < 1e-3):
            return -0.151861
        # elif(abs(AOA - 11.0) < 1e-3):
        #     return 1.3208
        # elif(abs(AOA - 12.0) < 1e-3):
        #     return 1.4392
        # elif(abs(AOA - 13.0) < 1e-3):
        #     return 1.5572
        # elif(abs(AOA - 14.0) < 1e-3):
        #     return 1.6746
        # elif(abs(AOA - 15.0) < 1e-3):
        #     return 1.7916
        else:
            return 0.0