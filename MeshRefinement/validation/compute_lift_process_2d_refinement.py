import KratosMultiphysics
from KratosMultiphysics.CompressiblePotentialFlowApplication.compute_lift_process import ComputeLiftProcess
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
                "reference_area": 1,
                "create_output_file": false,
                "angle_of_attack": 0.0,
                "airfoil_meshsize": 1.0,
                "minimum_airfoil_meshsize": 1.0,
                "domain_size": 1.0,
                "moment_reference_point" : [0.0,0.0,0.0],
                "is_infinite_wing": false
            }  """)

        settings.ValidateAndAssignDefaults(default_parameters)

        self.body_model_part = Model[settings["model_part_name"].GetString()]
        self.fluid_model_part = self.body_model_part.GetRootModelPart()
        far_field_model_part_name = settings["far_field_model_part_name"].GetString()
        if far_field_model_part_name != "":
            self.far_field_model_part = Model[far_field_model_part_name]
            self.compute_far_field_forces = True
        self.reference_area =  settings["reference_area"].GetDouble()
        self.create_output_file = settings["create_output_file"].GetBool()

        self.AOA = settings["angle_of_attack"].GetDouble()
        self.cl_reference = self.read_cl_reference(self.AOA)
        #self.cl_reference = self.read_cl_reference_membrane(self.AOA)
        self.mesh_size = settings["airfoil_meshsize"].GetDouble()
        self.minimum_airfoil_meshsize = settings["minimum_airfoil_meshsize"].GetDouble()
        self.domain_size = settings["domain_size"].GetDouble()

        self.input_dir_path = 'TBD'
        self.moment_reference_point = settings["moment_reference_point"].GetVector()
        self.is_infinite_wing = settings["is_infinite_wing"].GetBool()

    def ExecuteFinalizeSolutionStep(self):

        # This function finds and saves the trailing edge for further computations
        min_x_coordinate = 1e30
        max_x_coordinate = -1e30
        for node in self.body_model_part.Nodes:
            if(node.X < min_x_coordinate):
                min_x_coordinate = node.X
            if(node.X > max_x_coordinate):
                max_x_coordinate = node.X

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
        output_file_name = 'cp_tau_aoa_' + str(int(self.AOA)) + '.dat'
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
            '    color=blue,\n' +
            '    mark=*,\n' +
            '    ]\n' +
            '    table {cp_results.dat};  \n' +
            '    \\addlegendentry{Kratos}\n\n' +
            '\\addplot[\n' +
            '    only marks,\n' +
            '    color=red,\n' +
            '    mark=square*,\n' +
            '    mark options={solid},\n' +
            '    ]\n' +
            '    table {' + output_file_name + '};  \n' +
            '    \\addlegendentry{TAU}\n\n' +
            '\end{axis}\n' +
            '\end{tikzpicture}')
            cp_tikz_file.flush()

        NumberOfNodes = self.fluid_model_part.NumberOfNodes()
        with open(self.input_dir_path + "/plots/results/all_cases.dat",'a') as aoa_file:
            aoa_file.write('{0:16.2e} {1:15f} {2:15f} {3:15f} {4:15f}\n'.format(NumberOfNodes, self.lift_coefficient, self.lift_coefficient_jump, self.cl_reference, self.drag_coefficient))
            aoa_file.flush()

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
