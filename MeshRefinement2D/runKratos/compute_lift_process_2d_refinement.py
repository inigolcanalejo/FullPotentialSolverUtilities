import KratosMultiphysics
import KratosMultiphysics.FluidDynamicsApplication as KratosCFD
from KratosMultiphysics.CompressiblePotentialFlowApplication.compute_lift_process import ComputeLiftProcess
import KratosMultiphysics.CompressiblePotentialFlowApplication as CPFApp
import loads_output
import math

def Factory(settings, Model):
    if( not isinstance(settings,KratosMultiphysics.Parameters) ):
        raise Exception("expected input shall be a Parameters object, encapsulating a json string")
    return ComputeLiftProcessRefinement(Model, settings["Parameters"])

class ComputeLiftProcessRefinement(ComputeLiftProcess):
    def __init__(self, Model, settings):
        KratosMultiphysics.Process.__init__(self)

        default_parameters = KratosMultiphysics.Parameters("""
            {
                "model_part_name":"PLEASE_CHOOSE_MODEL_PART_NAME",
                "far_field_model_part_name" : "",
                "create_output_file": false,
                "angle_of_attack": 0.0,
                "airfoil_meshsize": 1.0,
                "minimum_airfoil_meshsize": 1.0,
                "domain_size": 1.0,
                "moment_reference_point" : [0.0,0.0,0.0],
                "reference_case_name": "",
                "is_infinite_wing": false
            }  """)

        settings.ValidateAndAssignDefaults(default_parameters)

        self.body_model_part = Model[settings["model_part_name"].GetString()]
        self.fluid_model_part = self.body_model_part.GetRootModelPart()
        far_field_model_part_name = settings["far_field_model_part_name"].GetString()
        if far_field_model_part_name != "":
            self.far_field_model_part = Model[far_field_model_part_name]
            self.compute_far_field_forces = True
        self.reference_area =  self.fluid_model_part.ProcessInfo.GetValue(CPFApp.REFERENCE_CHORD)
        self.create_output_file = settings["create_output_file"].GetBool()

        self.AOA = settings["angle_of_attack"].GetDouble()
        self.mesh_size = settings["airfoil_meshsize"].GetDouble()
        self.minimum_airfoil_meshsize = settings["minimum_airfoil_meshsize"].GetDouble()
        self.domain_size = settings["domain_size"].GetDouble()

        self.input_dir_path = 'TBD'
        self.moment_reference_point = settings["moment_reference_point"].GetVector()
        self.is_infinite_wing = settings["is_infinite_wing"].GetBool()

        aoa_rad = self.AOA * math.pi / 180.0
        x = self.moment_reference_point[0] * math.cos(aoa_rad) + self.moment_reference_point[1] * math.sin(aoa_rad)
        y = self.moment_reference_point[1] * math.cos(aoa_rad) - self.moment_reference_point[0] * math.sin(aoa_rad)
        self.moment_reference_point[0] = x
        self.moment_reference_point[1] = y
        self.reference_case_name = settings["reference_case_name"].GetString()
        if self.reference_case_name == "":
            raise Exception("Please enter a reference case name (XFOIL, AGARD, Lock or TAU)")

    def ExecuteFinalizeSolutionStep(self):
        self.free_stream_mach = self.fluid_model_part.ProcessInfo.GetValue(CPFApp.FREE_STREAM_MACH)
        self.hcr = self.fluid_model_part.ProcessInfo.GetValue(KratosCFD.HEAT_CAPACITY_RATIO)
        self.critical_cp = (math.pow((1+(self.hcr-1)*self.free_stream_mach**2/2)/(
            1+(self.hcr-1)/2), self.hcr/(self.hcr-1)) - 1) * 2 / (self.hcr * self.free_stream_mach**2)

        # This function finds and saves the trailing edge for further computations
        min_x_coordinate = 1e30
        max_x_coordinate = -1e30
        for node in self.body_model_part.Nodes:
            if(node.X < min_x_coordinate):
                min_x_coordinate = node.X
            if(node.X > max_x_coordinate):
                max_x_coordinate = node.X

        if self.reference_case_name == 'Lock':
            plot_reference_chord_projected = 1.0
        else:
            plot_reference_chord_projected = max_x_coordinate - min_x_coordinate
        print ('reference_area = ', self.reference_area)
        print ('plot_reference_chord_projected = ', plot_reference_chord_projected)

        super(ComputeLiftProcessRefinement, self).ExecuteFinalizeSolutionStep()

        cp_results_file_name = 'TBD'
        cp_file = open(cp_results_file_name,'w')

        number_of_conditions = self.body_model_part.NumberOfConditions()

        factor = math.floor(number_of_conditions / 7000+1)
        condition_counter = 0
        for cond in self.body_model_part.Conditions:
            condition_counter +=1
            cp = cond.GetValue(KratosMultiphysics.PRESSURE_COEFFICIENT)

            x = (0.5*(cond.GetNodes()[1].X0+cond.GetNodes()[0].X0) - min_x_coordinate) / plot_reference_chord_projected

            if(number_of_conditions > 7000):
                if( condition_counter % factor == 0 ):
                    cp_file.write('{0:15f} {1:15f}\n'.format(x, cp))
            else:
                cp_file.write('{0:15f} {1:15f}\n'.format(x, cp))

        cp_file.flush()


        if self.reference_case_name == 'TAU':
            self.cl_reference = self.read_cl_reference_membrane(self.AOA)
            self.cm_reference = 0.0
        elif self.reference_case_name == 'Lock':
            self.cl_reference = self.read_cl_reference_lock(self.AOA, self.free_stream_mach)
            self.cm_reference = 0.0
        elif self.reference_case_name == 'AGARD':
            self.cl_reference = self.read_cl_reference_agard(self.AOA, self.free_stream_mach)
            self.cm_reference = self.read_cm_reference_agard(self.AOA, self.free_stream_mach)
        elif self.reference_case_name == 'FLO36':
            self.cl_reference = self.read_cl_reference_flo36(self.AOA, self.free_stream_mach)
            self.cm_reference = self.read_cm_reference_flo36(self.AOA, self.free_stream_mach)
        else:
            self.cl_reference = self.read_cl_reference(self.AOA)
            self.cm_reference = self.read_cm_reference(self.AOA)

        if(abs(self.cl_reference) < 1e-6):
            self.cl_relative_error = abs(self.lift_coefficient)*100.0
        else:
            self.cl_relative_error = abs(self.lift_coefficient - self.cl_reference)/abs(self.cl_reference)*100.0

        cl_error_results_h_file_name = 'TBD'
        with open(cl_error_results_h_file_name,'a') as cl_error_file:
            cl_error_file.write('{0:16.2e} {1:15f}\n'.format(self.mesh_size, self.cl_relative_error))
            cl_error_file.flush()

        cl_results_h_file_name = 'TBD'
        with open(cl_results_h_file_name,'a') as cl_file:
            cl_file.write('{0:16.2e} {1:15f}\n'.format(self.mesh_size, self.lift_coefficient))
            cl_file.flush()

        cl_reference_h_file_name = 'TBD'
        with open(cl_reference_h_file_name,'a') as cl_reference_file:
            cl_reference_file.write('{0:16.2e} {1:15f}\n'.format(self.mesh_size, self.cl_reference))
            cl_reference_file.flush()

        if(self.mesh_size < self.minimum_airfoil_meshsize + 1e-9):
            aoa_results_file_name = 'TBD'
            with open(aoa_results_file_name,'a') as cl_aoa_file:
                cl_aoa_file.write('{0:15f} {1:15f}\n'.format(self.AOA, self.lift_coefficient))
                cl_aoa_file.flush()

            cl_error_results_domain_directory_name = 'TBD'
            cl_error_results_domain_file_name = cl_error_results_domain_directory_name + '/AOA_'+ str(self.AOA) + '/cl_error_results_domain.dat'
            with open(cl_error_results_domain_file_name,'a') as cl_error_file:
                cl_error_file.write('{0:16.2e} {1:15f}\n'.format(self.domain_size, self.cl_relative_error))
                cl_error_file.flush()

        cp_tikz_file_name = 'TBD'
        cp_critical_reference_file_name = 'default.dat'
        if self.reference_case_name == 'TAU':
            output_file_name = 'cp_tau_aoa_' + str(int(self.AOA)) + '.dat'
        elif self.reference_case_name == 'Lock':
            output_file_name = 'references/lock/cp_lock_aoa_' + str(int(self.AOA)) + '.dat'
            cp_critical_reference_file_name = 'references/lock/cp_critical_lock_mach_' + str(int(self.free_stream_mach*100)) + '.dat'
        elif self.reference_case_name == 'AGARD':
            output_file_name = 'references/agard/cp_agard_aoa_' + str(self.AOA) + '.dat'
        elif self.reference_case_name == 'FLO36':
            output_file_name = 'references/flo36/cp_flo36_aoa_' + str(int(self.AOA)) + '_mach_' + str(int(self.free_stream_mach*100)) + '.dat'
            cp_critical_reference_file_name = 'references/flo36/cp_critical_flo36_mach_' + str(int(self.free_stream_mach*100)) + '.dat'
            cp_crit_total_name = self.input_dir_path + '/plots/cp/data/0_original/' + cp_critical_reference_file_name
            with open(cp_crit_total_name,'w') as cp_crit_file:
                cp_crit_file.write('{0:16.2e} {1:15f}\n'.format(0, self.critical_cp))
                cp_crit_file.write('{0:16.2e} {1:15f}\n'.format(1.0, self.critical_cp))
                cp_crit_file.flush()
        else:
            output_file_name = 'references/xfoil/cp_xfoil_aoa_' + str(int(self.AOA)) + '.dat'
        with open(cp_tikz_file_name,'w') as cp_tikz_file:
            cp_tikz_file.write('\\begin{tikzpicture}\n' +
            '\\begin{axis}[\n' +
            '    title={ $M_\infty$ = ' + "{:.2f}".format(self.free_stream_mach) + ' $c_l$ = ' + "{:.6f}".format(self.lift_coefficient) + ' $c_d$ = ' + "{:.6f}".format(self.drag_coefficient) + '},\n' +
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
            '    color=blue,\n' +
            '    mark=+,\n' +
            '    mark size=1.5,\n' +
            '    ]\n' +
            '    table {cp_results.dat};  \n' +
            '    \\addlegendentry{Kratos}\n\n' +
            '\\addplot[\n' +
            '    only marks,\n' +
            '    color=red,\n' +
            '    mark=triangle*,\n' +
            '    mark size=1.5,\n' +
            '    mark options={solid},\n' +
            '    ]\n' +
            '    table {' + output_file_name + '};  \n' +
            '    \\addlegendentry{' + self.reference_case_name + '}\n\n' +
            '\\addplot[\n' +
            '    color=black,\n' +
            '    mark=none,\n' +
            '    mark options={dashed},\n' +
            '    dashed,\n' +
            '    ]\n' +
            '    table {' + cp_critical_reference_file_name + '};  \n' +
            '    \\addlegendentry{$c_p^*$ = ' + "{:.2f}".format(self.critical_cp) + '}\n\n' +
            '\end{axis}\n' +
            '\end{tikzpicture}')
            cp_tikz_file.flush()

        NumberOfNodes = self.fluid_model_part.NumberOfNodes()
        with open(self.input_dir_path + "/plots/results/all_cases.dat",'a') as aoa_file:
            aoa_file.write('{0:16.2e} {1:15f} {2:15f} {3:15f} {4:15f}\n'.format(NumberOfNodes, self.lift_coefficient, self.lift_coefficient_jump, self.cl_reference, self.drag_coefficient))
            aoa_file.flush()

        self.moment_coefficient *= -1
        cm_results_h_file_name = self.input_dir_path + '/plots/cm/data/cm/cm_results_h.dat'
        with open(cm_results_h_file_name,'a') as cm_file:
            cm_file.write('{0:16.2e} {1:15f}\n'.format(self.mesh_size, self.moment_coefficient[2]))
            cm_file.flush()

        cm_reference_h_file_name = self.input_dir_path + '/plots/cm/data/cm/cm_reference_h.dat'
        with open(cm_reference_h_file_name,'a') as cm_file:
            cm_file.write('{0:16.2e} {1:15f}\n'.format(self.mesh_size, self.cm_reference))
            cm_file.flush()

        if(abs(self.cm_reference) < 1e-6):
            self.cm_relative_error = abs(self.moment_coefficient[2] - self.cm_reference)
        else:
            self.cm_relative_error = abs(self.moment_coefficient[2] - self.cm_reference)/abs(self.cm_reference)*100.0

        cm_error_results_h_file_name = self.input_dir_path + '/plots/cm_error/data/cm_error/cm_error_results_h.dat'
        with open(cm_error_results_h_file_name,'a') as cm_file:
            cm_file.write('{0:16.2e} {1:15f}\n'.format(self.mesh_size, self.cm_relative_error))
            cm_file.flush()


    def read_cl_reference(self,AOA):
        #values computed with the panel method from xfoil
        if(abs(AOA - 0.0) < 1e-3):
            return 0.0
        elif(abs(AOA - 1.0) < 1e-3):
            return 0.1208
        elif(abs(AOA - 2.0) < 1e-3):
            return 0.2416
        elif(abs(AOA - 3.0) < 1e-3):
            return 0.3623
        elif(abs(AOA - 4.0) < 1e-3):
            return 0.4829
        elif(abs(AOA - 5.0) < 1e-3):
            return 0.6033
        elif(abs(AOA - 6.0) < 1e-3):
            return 0.7235
        elif(abs(AOA - 7.0) < 1e-3):
            return 0.8436
        elif(abs(AOA - 8.0) < 1e-3):
            return 0.9634
        elif(abs(AOA - 9.0) < 1e-3):
            return 1.0828
        elif(abs(AOA - 10.0) < 1e-3):
            return 1.202
        elif(abs(AOA - 11.0) < 1e-3):
            return 1.3208
        elif(abs(AOA - 12.0) < 1e-3):
            return 1.4392
        elif(abs(AOA - 13.0) < 1e-3):
            return 1.5572
        elif(abs(AOA - 14.0) < 1e-3):
            return 1.6746
        elif(abs(AOA - 15.0) < 1e-3):
            return 1.7916
        else:
            return 0.0

    def read_cl_reference_membrane(self,AOA):
        #values computed with the panel method from xfoil
        if(abs(AOA - 0.0) < 1e-3):
            return 0.391162386
        elif(abs(AOA - 2.0) < 1e-3):
            return 0.578745185
        elif(abs(AOA - 4.0) < 1e-3):
            return 0.76447573300
        elif(abs(AOA - 6.0) < 1e-3):
            return 0.942408097000
        elif(abs(AOA - 8.0) < 1e-3):
            return 1.107749899000
        elif(abs(AOA - 10.0) < 1e-3):
            return 1.258567592000
        elif(abs(AOA - 12.0) < 1e-3):
            return 1.370671228000
        elif(abs(AOA - 14.0) < 1e-3):
            return 1.062561017000
        elif(abs(AOA - 16.0) < 1e-3):
            return 1.062478416000
        elif(abs(AOA - 18.0) < 1e-3):
            return 1.062804501000
        elif(abs(AOA - 20.0) < 1e-3):
            return 1.089679153000
        else:
            print('There is no reference for this AOA')

    def read_cm_reference(self,AOA):
        #values computed with the panel method from xfoil
        if(abs(AOA - 0.0) < 1e-3):
            return 0.0
        elif(abs(AOA - 1.0) < 1e-3):
            return -0.0315
        elif(abs(AOA - 2.0) < 1e-3):
            return -0.0631
        elif(abs(AOA - 3.0) < 1e-3):
            return -0.0945
        elif(abs(AOA - 4.0) < 1e-3):
            return -0.1258
        elif(abs(AOA - 5.0) < 1e-3):
            return -0.1570
        elif(abs(AOA - 6.0) < 1e-3):
            return -0.1879
        elif(abs(AOA - 7.0) < 1e-3):
            return -0.2187
        elif(abs(AOA - 8.0) < 1e-3):
            return -0.2492
        elif(abs(AOA - 9.0) < 1e-3):
            return -0.2793
        elif(abs(AOA - 10.0) < 1e-3):
            return -0.3092
        elif(abs(AOA - 11.0) < 1e-3):
            return -0.3386
        elif(abs(AOA - 12.0) < 1e-3):
            return -0.3677
        elif(abs(AOA - 13.0) < 1e-3):
            return -0.3963
        elif(abs(AOA - 14.0) < 1e-3):
            return -0.4244
        elif(abs(AOA - 15.0) < 1e-3):
            return -0.4520
        else:
            return 0.0

    def read_cl_reference_lock(self,AOA, free_stream_mach):
        # Values from "Lock RC. Test cases for numerical methods in two dimensional transonic flows.
        # AGARD Report 575, 1970."
        if(abs(AOA - 0.0) < 1e-3):
            return 0.0
        elif( abs(AOA - 2.0) < 1e-3 and abs(free_stream_mach - 0.63) < 1e-3):
            return 0.335
        else:
            return 0.0

    def read_cl_reference_agard(self,AOA, free_stream_mach):
        # Values from "H. Viviand. Test cases for inviscid flow field methods.
        # NATO / Advisory Group for Aerospace Research and Development: AGARD advisory report ; 211
        # Neuilly-sur-Seine, France, 1985."
        if(abs(AOA - 1.25) < 1e-3 and abs(free_stream_mach - 0.8) < 1e-3):
            return 0.3632
        elif( abs(AOA - 1.0) < 1e-3 and abs(free_stream_mach - 0.85) < 1e-3):
            return 0.3584
        else:
            return 0.0

    def read_cl_reference_flo36(self,AOA, free_stream_mach):
        # Values from "Volpe, G., and Jameson, A., “Transonic Potential Flow Calculations
        # by Two Articial Density Methods,” AIAA Journal, Vol. 26, No. 4,
        # April 1988, pp. 425–429. doi:10.2514/3.9910"
        if(abs(AOA - 1.0) < 1e-3 and abs(free_stream_mach - 0.72) < 1e-3):
            return 0.2038
        elif( abs(AOA - 1.0) < 1e-3 and abs(free_stream_mach - 0.73) < 1e-3):
            return 0.2122
        elif( abs(AOA - 1.0) < 1e-3 and abs(free_stream_mach - 0.75) < 1e-3):
            return 0.2366
        elif( abs(AOA - 2.0) < 1e-3 and abs(free_stream_mach - 0.75) < 1e-3):
            return 0.5130
        else:
            return 0.0

    def read_cm_reference_agard(self,AOA, free_stream_mach):
        # Values from "H. Viviand. Test cases for inviscid flow field methods.
        # NATO / Advisory Group for Aerospace Research and Development: AGARD advisory report ; 211
        # Neuilly-sur-Seine, France, 1985."
        if(abs(AOA - 1.25) < 1e-3 and abs(free_stream_mach - 0.8) < 1e-3):
            return -0.0397
        elif( abs(AOA - 1.0) < 1e-3 and abs(free_stream_mach - 0.85) < 1e-3):
            return -0.1228
        else:
            return 0.0

    def read_cm_reference_flo36(self,AOA, free_stream_mach):
        # Values from "Volpe, G., and Jameson, A., “Transonic Potential Flow Calculations
        # by Two Articial Density Methods,” AIAA Journal, Vol. 26, No. 4,
        # April 1988, pp. 425–429. doi:10.2514/3.9910"
        if(abs(AOA - 1.0) < 1e-3 and abs(free_stream_mach - 0.72) < 1e-3):
            return -0.0001
        elif( abs(AOA - 1.0) < 1e-3 and abs(free_stream_mach - 0.73) < 1e-3):
            return 0.0003
        elif( abs(AOA - 1.0) < 1e-3 and abs(free_stream_mach - 0.75) < 1e-3):
            return -0.0007
        elif( abs(AOA - 2.0) < 1e-3 and abs(free_stream_mach - 0.75) < 1e-3):
            return -0.0166
        else:
            return 0.0
