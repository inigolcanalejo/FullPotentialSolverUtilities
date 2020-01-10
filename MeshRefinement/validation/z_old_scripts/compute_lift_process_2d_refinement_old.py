from KratosMultiphysics import *
import KratosMultiphysics
import KratosMultiphysics.CompressiblePotentialFlowApplication as CompressiblePotentialFlowApplication
from numpy import *
import itertools
import loads_output
import math

def Factory(settings, Model):
    if( not isinstance(settings,KratosMultiphysics.Parameters) ):
        raise Exception("expected input shall be a Parameters object, encapsulating a json string")
    return ComputeLiftProcess(Model, settings["Parameters"])

##all the processes python processes should be derived from "python_process"
class ComputeLiftProcess(KratosMultiphysics.Process):
    def __init__(self, Model, settings ):
        KratosMultiphysics.Process.__init__(self)

        default_parameters = KratosMultiphysics.Parameters("""
            {
                "model_part_name":"PLEASE_CHOOSE_MODEL_PART_NAME",
                "upper_surface_model_part_name" : "please specify the model part that contains the upper surface nodes",
                "lower_surface_model_part_name" : "please specify the model part that contains the lower surface nodes",
                "far_field_model_part_name"   : "PotentialWallCondition2D_Far_field_Auto1",
                "mesh_id": 0,
                "velocity_infinity": [1.0,0.0,0],
                "angle_of_attack": 0.0,
                "airfoil_meshsize": 1.0,
                "energy_reference": 1.0,
                "potential_energy_reference": 1.0,
                "cl_ok_reference": 1.0,
                "domain_size": 1.0,
                "reference_area": 1
            }  """)

        settings.ValidateAndAssignDefaults(default_parameters)

        self.fluid_model_part = Model[settings["model_part_name"].GetString()]
        self.upper_surface_model_part = Model[settings["upper_surface_model_part_name"].GetString()]
        self.lower_surface_model_part = Model[settings["lower_surface_model_part_name"].GetString()]
        self.far_field_model_part = Model[settings["far_field_model_part_name"].GetString()]

        self.velocity_infinity = [0,0,0]
        self.velocity_infinity[0] = settings["velocity_infinity"][0].GetDouble()
        self.velocity_infinity[1] = settings["velocity_infinity"][1].GetDouble()
        self.velocity_infinity[2] = settings["velocity_infinity"][2].GetDouble()

        self.reference_area =  settings["reference_area"].GetDouble()
        self.aoa = settings["angle_of_attack"].GetDouble()
        self.cl_reference = loads_output.read_cl_reference(self.aoa)
        self.mesh_size = settings["airfoil_meshsize"].GetDouble()
        print('mesh size =', self.mesh_size)

        self.energy_reference = settings["energy_reference"].GetDouble()
        print('self.energy_reference = ', self.energy_reference)

        self.total_potential_energy_reference = settings["potential_energy_reference"].GetDouble()
        print('self.total_potential_energy_reference = ', self.total_potential_energy_reference)

        self.cl_ok_reference = settings["cl_ok_reference"].GetDouble()
        print('self.cl_ok_reference = ', self.cl_ok_reference)

        self.domain_size = settings["domain_size"].GetDouble()
        print('self.domain_size = ', self.domain_size)

    def ExecuteFinalizeSolutionStep(self):
        print('COMPUTE LIFT')

        rx = 0.0
        ry = 0.0
        rz = 0.0
        
        rx_low = 0.0
        ry_low = 0.0
        rz_low = 0.0

        self.work_dir = '/home/inigo/simulations/naca0012/07_salome/05_MeshRefinement/'
        cp_results_file_name = self.work_dir + 'plots/cp/data/0_original/cp_results.dat'
        cp_file = open(cp_results_file_name,'w')

        #cp_coordinates_file_name = 'plots/cp/data/0_original/coordinates.dat'
        #coordinates_file = open(cp_coordinates_file_name,'a')
        number_of_conditions = 0
        for cond in itertools.chain(self.upper_surface_model_part.Conditions, self.lower_surface_model_part.Conditions):
            number_of_conditions += 1

        factor = math.floor(number_of_conditions / 7000+1)
        
        condition_counter = 0
        for cond in itertools.chain(self.upper_surface_model_part.Conditions, self.lower_surface_model_part.Conditions):
          condition_counter +=1
          n = cond.GetValue(NORMAL)
          cp_up = cond.GetValue(PRESSURE)

          x = 0.5*(cond.GetNodes()[1].X0+cond.GetNodes()[0].X0)
          y = 0.5*(cond.GetNodes()[1].Y0+cond.GetNodes()[0].Y0)

          if(number_of_conditions > 7000):
              if( condition_counter % factor == 0 ):
                  cp_file.write('{0:15f} {1:15f}\n'.format(x+0.5, cp_up))
          else:
              cp_file.write('{0:15f} {1:15f}\n'.format(x+0.5, cp_up))
          
          #cp_file.write('{0:15f} {1:15f}\n'.format(x+0.5, cp_up))
          #coordinates_file.write('{0:15f} {1:15f}\n'.format(x+0.5, -y))
          


          rx += n[0]*cp_up
          ry += n[1]*cp_up
          rz += n[2]*cp_up
          
        
        cp_file.flush()

        print('number of conditions = ', number_of_conditions)
        
        RX = rx/self.reference_area
        RY = ry/self.reference_area
        RZ = rz/self.reference_area

        Cl = RY
        Cd = RX

        self.Cl = Cl

        if(abs(self.cl_reference) < 1e-6):
            self.cl_relative_error = abs(Cl)*100.0
        else:
            self.cl_relative_error = abs(Cl - self.cl_reference)/abs(self.cl_reference)*100.0

        if(abs(self.cl_ok_reference - 1.0) < 1e-7):
            self.cl_relative_error_ok = 0.0
            self.fluid_model_part.ProcessInfo.SetValue(K0,Cl)
        else:
            self.cl_relative_error_ok = abs(Cl - self.cl_ok_reference)/abs(self.cl_ok_reference)



        print('Cl = ', Cl)
        print('Cd = ', Cd)
        print('RZ = ', RZ)

        
        far_field_lift = 0.0
        for node in self.far_field_model_part.Nodes:
            jump = node.GetSolutionStepValue(KratosMultiphysics.CompressiblePotentialFlowApplication.POTENTIAL_JUMP)
            if(abs(jump - 1e-8) > 1e-7):
                far_field_lift = jump
                print('Far field computed lift = ', far_field_lift)
                break

        if(Cl*far_field_lift < 0):
            far_field_lift *= -1.0

        if(abs(self.cl_reference) < 1e-6):
            self.cl_relative_error_jump = abs(far_field_lift)*100.0
        else:
            self.cl_relative_error_jump = abs(far_field_lift - self.cl_reference)/abs(self.cl_reference)*100.0

        #compute the internal energy norm and relative error
        internal_energy_sum = 0.0
        for element in self.fluid_model_part.Elements:
            internal_energy_sum += element.GetValue(KratosMultiphysics.INTERNAL_ENERGY)

        if(abs(self.energy_reference - 1.0) < 1e-7):
            relative_error_energy_norm = 0.0
            self.fluid_model_part.ProcessInfo.SetValue(CompressiblePotentialFlowApplication.ENERGY_NORM_REFERENCE,internal_energy_sum)
        else:
            relative_error_energy_norm = math.sqrt(abs(internal_energy_sum - self.energy_reference)/abs(self.energy_reference))

        external_energy_sum = 0.0
        for cond in self.far_field_model_part.Conditions:
            external_energy_sum += cond.GetValue(EXTERNAL_ENERGY)

        total_potential_energy = internal_energy_sum - external_energy_sum

        if(abs(self.total_potential_energy_reference - 1.0) < 1e-7):
            relative_error_energy_norm_variant = 0.0
            self.fluid_model_part.ProcessInfo.SetValue(CompressiblePotentialFlowApplication.POTENTIAL_ENERGY_REFERENCE,total_potential_energy)
        else:
            relative_error_energy_norm_variant = math.sqrt(abs(total_potential_energy - self.total_potential_energy_reference)/abs(self.energy_reference))
        
        NumberOfNodes = self.fluid_model_part.NumberOfNodes()
    
        with open (self.work_dir + "mesh_refinement_loads.dat",'a') as loads_file:
            loads_file.write('{0:16.2e} {1:15f} {2:15f} {3:15f} {4:15f}\n'.format(NumberOfNodes, Cl, far_field_lift, self.cl_reference, Cd, RZ))
            loads_file.flush()

        with open(self.work_dir + "plots/results/all_cases.dat",'a') as aoa_file:
            aoa_file.write('{0:16.2e} {1:15f} {2:15f} {3:15f} {4:15f}\n'.format(NumberOfNodes, Cl, far_field_lift, self.cl_reference, Cd, RZ))
            aoa_file.flush()

        cl_results_file_name = self.work_dir + "plots/cl/data/cl/cl_results.dat"
        with open(cl_results_file_name,'a') as cl_file:
            cl_file.write('{0:16.2e} {1:15f}\n'.format(NumberOfNodes, Cl))
            cl_file.flush()

        cl_results_h_file_name = self.work_dir + "plots/cl/data/cl/cl_results_h.dat"
        with open(cl_results_h_file_name,'a') as cl_file:
            cl_file.write('{0:16.2e} {1:15f}\n'.format(self.mesh_size, Cl))
            cl_file.flush()

        cl_reference_file_name = self.work_dir + "plots/cl/data/cl/cl_reference.dat"
        with open(cl_reference_file_name,'a') as cl_reference_file:
            cl_reference_file.write('{0:16.2e} {1:15f}\n'.format(NumberOfNodes, self.cl_reference))
            cl_reference_file.flush()

        cl_reference_h_file_name = self.work_dir + "plots/cl/data/cl/cl_reference_h.dat"
        with open(cl_reference_h_file_name,'a') as cl_reference_file:
            cl_reference_file.write('{0:16.2e} {1:15f}\n'.format(self.mesh_size, self.cl_reference))
            cl_reference_file.flush()

        cl_error_results_file_name = self.work_dir + "plots/cl_error/data/cl/cl_error_results.dat"
        with open(cl_error_results_file_name,'a') as cl_error_file:
            cl_error_file.write('{0:16.2e} {1:15f}\n'.format(NumberOfNodes, self.cl_relative_error))
            cl_error_file.flush()

        cl_error_results_h_file_name = self.work_dir + "plots/cl_error/data/cl/cl_error_results_h.dat"
        with open(cl_error_results_h_file_name,'a') as cl_error_file:
            cl_error_file.write('{0:16.2e} {1:15f}\n'.format(self.mesh_size, self.cl_relative_error))
            cl_error_file.flush()

        cl_error_results_h_log_file_name = self.work_dir + "plots/cl_error/data/cl/cl_error_results_h_log.dat"
        with open(cl_error_results_h_log_file_name,'a') as cl_error_file:
            cl_error_file.write('{0:16.2e} {1:15f}\n'.format(self.mesh_size, self.cl_relative_error/100.0))
            cl_error_file.flush()

        if(self.mesh_size > 1e-7 and self.mesh_size < 1e-5 and self.domain_size < 1e6):
            cl_error_results_domain_file_name = self.work_dir + "plots/cl_error_domain_size/cl_error_results_domain.dat"
            with open(cl_error_results_domain_file_name,'a') as cl_error_file:
                cl_error_file.write('{0:16.2e} {1:15f}\n'.format(self.domain_size, self.cl_relative_error))
                cl_error_file.flush()

        if(abs(self.cl_ok_reference - 1.0) > 1e-7):
            cl_error_results_h_log_file_name = self.work_dir + "plots/cl_error/data/cl/cl_error_results_h_log_ok.dat"
            with open(cl_error_results_h_log_file_name,'a') as cl_error_file:
                cl_error_file.write('{0:16.2e} {1:15f}\n'.format(self.mesh_size, self.cl_relative_error_ok))
                cl_error_file.flush()


        if(abs(self.energy_reference - 1.0) > 1e-7):
            energy_h_results_file_name = self.work_dir + "plots/relative_error_energy_norm/data/energy/energy_h_results.dat"
            with open(energy_h_results_file_name,'a') as energy_h_file:
                energy_h_file.write('{0:16.6e} {1:16.6e}\n'.format(self.mesh_size, relative_error_energy_norm))
                energy_h_file.flush()

            energy_n_results_file_name = self.work_dir + "plots/relative_error_energy_norm/data/energy/energy_n_results.dat"
            with open(energy_n_results_file_name,'a') as energy_n_file:
                energy_n_file.write('{0:16.6e} {1:16.6e}\n'.format(NumberOfNodes, relative_error_energy_norm))
                energy_n_file.flush()

            energy_variant_h_file_name = self.work_dir + "plots/relative_error_energy_norm/data/energy/energy_variant_h_results.dat"
            with open(energy_variant_h_file_name,'a') as energy_variant_h_file:
                energy_variant_h_file.write('{0:16.6e} {1:16.6e}\n'.format(self.mesh_size, relative_error_energy_norm_variant))
                energy_variant_h_file.flush()

            energy_variant_n_file_name = self.work_dir + "plots/relative_error_energy_norm/data/energy/energy_variant_n_results.dat"
            with open(energy_variant_n_file_name,'a') as energy_variant_n_file:
                energy_variant_n_file.write('{0:16.6e} {1:16.6e}\n'.format(NumberOfNodes, relative_error_energy_norm_variant))
                energy_variant_n_file.flush()

        cl_far_field_results_file_name = self.work_dir + "plots/cl/data/cl/cl_jump_results.dat"
        with open(cl_far_field_results_file_name,'a') as cl_jump_file:
            cl_jump_file.write('{0:16.2e} {1:15f}\n'.format(NumberOfNodes, far_field_lift))
            cl_jump_file.flush()

        cl_far_field_results_h_file_name = self.work_dir + "plots/cl/data/cl/cl_jump_results_h.dat"
        with open(cl_far_field_results_h_file_name,'a') as cl_jump_file:
            cl_jump_file.write('{0:16.2e} {1:15f}\n'.format(self.mesh_size, far_field_lift))
            cl_jump_file.flush()

        cl_far_field_error_results_file_name = self.work_dir + "plots/cl_error/data/cl/cl_jump_error_results.dat"
        with open(cl_far_field_error_results_file_name,'a') as cl_jump_error_file:
            cl_jump_error_file.write('{0:16.2e} {1:15f}\n'.format(NumberOfNodes, self.cl_relative_error_jump))
            cl_jump_error_file.flush()

        cl_far_field_error_results_h_file_name = self.work_dir + "plots/cl_error/data/cl/cl_jump_error_results_h.dat"
        with open(cl_far_field_error_results_h_file_name,'a') as cl_jump_error_file:
            cl_jump_error_file.write('{0:16.2e} {1:15f}\n'.format(self.mesh_size, self.cl_relative_error_jump))
            cl_jump_error_file.flush()

        cl_far_field_error_results_h_log_file_name = self.work_dir + "plots/cl_error/data/cl/cl_jump_error_results_h_log.dat"
        with open(cl_far_field_error_results_h_log_file_name,'a') as cl_jump_error_file:
            cl_jump_error_file.write('{0:16.2e} {1:15f}\n'.format(self.mesh_size, self.cl_relative_error_jump/100.0))
            cl_jump_error_file.flush()
        
        cd_results_file_name = self.work_dir + "plots/cd/data/cd/cd_results.dat"
        with open(cd_results_file_name,'a') as cd_file:
            cd_file.write('{0:16.2e} {1:15f}\n'.format(NumberOfNodes, Cd))
            cd_file.flush()

        cp_tikz_file_name = self.work_dir + "plots/cp/data/0_original/cp.tikz"
        with open(cp_tikz_file_name,'w') as cp_tikz_file:
            cp_tikz_file.write('\\begin{tikzpicture}\n' +
            '\\begin{axis}[\n' +
            '\t    title={ $c_l$ = ' + "{:.6f}".format(Cl) + ' $c_d$ = ' + "{:.6f}".format(Cd) + '},\n' +
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
            '\t    \\addlegendentry{ndof = ' + "{:.2e}".format(NumberOfNodes) + ' }\n\n' +
            '\t\end{axis}\n' +
            '\t\end{tikzpicture}')
            cp_tikz_file.flush()

        #loads_output.write_cl(Cl)

    def ExecuteFinalize(self):
        with open(self.work_dir + 'plots/aoa/cl_aoa.dat','a') as cl_aoa_file:
            cl_aoa_file.write('{0:15f}\n'.format(self.Cl))
            cl_aoa_file.flush()

        
