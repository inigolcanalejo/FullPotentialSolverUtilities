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
                "velocity_infinity": [1.0,0.0,0],
                "reference_area": 1,
                "create_output_file": false,
                "angle_of_attack": 0.0,
                "airfoil_meshsize": 1.0,
                "minimum_airfoil_meshsize": 1.0,
                "domain_size": 1.0
            }  """)

        settings.ValidateAndAssignDefaults(default_parameters)

        self.body_model_part = Model[settings["model_part_name"].GetString()]
        self.velocity_infinity = [0,0,0]
        self.velocity_infinity[0] = settings["velocity_infinity"][0].GetDouble()
        self.velocity_infinity[1] = settings["velocity_infinity"][1].GetDouble()
        self.velocity_infinity[2] = settings["velocity_infinity"][2].GetDouble()
        self.reference_area =  settings["reference_area"].GetDouble()
        self.create_output_file = settings["create_output_file"].GetBool()

        self.AOA = settings["angle_of_attack"].GetDouble()
        self.cl_reference = self.read_cl_reference(self.AOA)
        self.mesh_size = settings["airfoil_meshsize"].GetDouble()
        self.minimum_airfoil_meshsize = settings["minimum_airfoil_meshsize"].GetDouble()
        self.domain_size = settings["domain_size"].GetDouble()

        self.input_dir_path = 'TBD'

    def ExecuteFinalizeSolutionStep(self):
        super(ComputeLiftProcessRefinement, self).ExecuteFinalizeSolutionStep()

        cp_results_file_name = 'TBD'
        cp_file = open(cp_results_file_name,'w')

        number_of_conditions = self.body_model_part.NumberOfConditions()

        for cond in self.body_model_part.Conditions:
            cp = cond.GetValue(KratosMultiphysics.PRESSURE)

            x = 0.5*(cond.GetNodes()[1].X0+cond.GetNodes()[0].X0)

            if(number_of_conditions > 7000):
                if( condition_counter % factor == 0 ):
                    cp_file.write('{0:15f} {1:15f}\n'.format(x+0.5, cp))
            else:
                cp_file.write('{0:15f} {1:15f}\n'.format(x+0.5, cp))

        cp_file.flush()

        if(abs(self.cl_reference) < 1e-6):
            self.cl_relative_error = abs(self.Cl)*100.0
        else:
            self.cl_relative_error = abs(self.Cl - self.cl_reference)/abs(self.cl_reference)*100.0

        cl_error_results_h_file_name = 'TBD'
        with open(cl_error_results_h_file_name,'a') as cl_error_file:
            cl_error_file.write('{0:16.2e} {1:15f}\n'.format(self.mesh_size, self.cl_relative_error))
            cl_error_file.flush()

        cl_results_h_file_name = 'TBD'
        with open(cl_results_h_file_name,'a') as cl_file:
            cl_file.write('{0:16.2e} {1:15f}\n'.format(self.mesh_size, self.Cl))
            cl_file.flush()

        cl_reference_h_file_name = 'TBD'
        with open(cl_reference_h_file_name,'a') as cl_reference_file:
            cl_reference_file.write('{0:16.2e} {1:15f}\n'.format(self.mesh_size, self.cl_reference))
            cl_reference_file.flush()

        if(self.mesh_size < self.minimum_airfoil_meshsize + 1e-9):
            aoa_results_file_name = 'TBD'
            with open(aoa_results_file_name,'a') as cl_aoa_file:
                cl_aoa_file.write('{0:15f} {1:15f}\n'.format(self.AOA, self.Cl))
                cl_aoa_file.flush()

            cl_error_results_domain_directory_name = 'TBD'
            cl_error_results_domain_file_name = cl_error_results_domain_directory_name + '/AOA_'+ str(self.AOA) + '/cl_error_results_domain.dat'
            with open(cl_error_results_domain_file_name,'a') as cl_error_file:
                cl_error_file.write('{0:16.2e} {1:15f}\n'.format(self.domain_size, self.cl_relative_error))
                cl_error_file.flush()

        cp_tikz_file_name = 'TBD'
        with open(cp_tikz_file_name,'w') as cp_tikz_file:
            cp_tikz_file.write('\\begin{tikzpicture}\n' +
            '\\begin{axis}[\n' +
            '\t    title={ $c_l$ = ' + "{:.6f}".format(self.Cl) + ' $c_d$ = ' + "{:.6f}".format(self.Cd) + '},\n' +
            '\t    xlabel={$x/c$},\n' +
            '\t    ylabel={$c_p[\\unit{-}$]},\n' +
            '\t    xmin=-0.01, xmax=1.01,\n' +
            '\t    y dir=reverse,\n' +
            '\t    xtick={0,0.2,0.4,0.6,0.8,1},\n' +
            '\t    xticklabels={0,0.2,0.4,0.6,0.8,1},\n' +
            '\t    ymajorgrids=true,\n' +
            '\t    xmajorgrids=true,\n' +
            '\t    grid style=dashed,\n' +
            '\t    width=12cm\n' +
            ']\n\n' +
            '\\addplot[\n' +
            '\t    only marks,\n' +
            '\t    color=blue,\n' +
            '\t    mark=*,\n' +
            '\t    ]\n' +
            '\t    table {cp_results.dat};  \n' +
            '\t    \\addlegendentry{h = ' + "{:.1e}".format(self.mesh_size) + ' }\n\n' +
            '\t\end{axis}\n' +
            '\t\end{tikzpicture}')
            cp_tikz_file.flush()

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
