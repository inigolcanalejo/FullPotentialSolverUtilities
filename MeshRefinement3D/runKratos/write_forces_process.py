import KratosMultiphysics
from KratosMultiphysics.CompressiblePotentialFlowApplication.compute_lift_process import ComputeLiftProcess
import KratosMultiphysics.CompressiblePotentialFlowApplication as CPFApp

def Factory(settings, Model):
    if( not isinstance(settings,KratosMultiphysics.Parameters) ):
        raise Exception("expected input shall be a Parameters object, encapsulating a json string")
    return WriteForcesProcess(Model, settings["Parameters"])

class WriteForcesProcess(ComputeLiftProcess):
    def __init__(self, Model, settings ):
        KratosMultiphysics.Process.__init__(self)

        default_parameters = KratosMultiphysics.Parameters(r'''{
            "model_part_name": "please specify the model part that contains the surface nodes",
            "far_field_model_part_name": "please specify the model part that contains the surface nodes",
            "moment_reference_point" : [0.0,0.0,0.0],
            "trailing_edge_model_part_name": "",
            "is_infinite_wing": false,
            "growth_rate_domain": 0.0,
            "angle_of_attack": 0.0
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

        if not self.reference_area > 0.0:
            raise Exception('The reference area should be larger than 0.')

        self.Growth_Rate_Domain = settings["growth_rate_domain"].GetDouble()
        self.AOA = settings["angle_of_attack"].GetDouble()
        self.input_dir_path = 'TBD'

    def ExecuteFinalizeSolutionStep(self):
        super(WriteForcesProcess, self).ExecuteFinalizeSolutionStep()

        nodal_value_process = CPFApp.ComputeNodalValueProcess(self.fluid_model_part, ["PRESSURE_COEFFICIENT"])
        nodal_value_process.Execute()

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
            cl_file.write('{0:16.2e} {1:15f}\n'.format(NumberOfNodes, 0.33))
            cl_file.flush()



    def read_cl_reference(self,AOA):
        # Values computed with XFLR5 using the 3D inviscid panel method
        # with 40 panels in the chord direction and 40 in the span direction
        if(abs(AOA - 0.0) < 1e-3):
            return 0.0
        elif(abs(AOA - 1.0) < 1e-3):
            return 0.068439
        elif(abs(AOA - 2.0) < 1e-3):
            return 0.136047
        elif(abs(AOA - 3.0) < 1e-3):
            return 0.203540
        elif(abs(AOA - 4.0) < 1e-3):
            return 0.270858
        elif(abs(AOA - 5.0) < 1e-3):
            return 0.337945
        elif(abs(AOA - 6.0) < 1e-3):
            return 0.404744
        elif(abs(AOA - 7.0) < 1e-3):
            return 0.471199
        elif(abs(AOA - 8.0) < 1e-3):
            return 0.537254
        elif(abs(AOA - 9.0) < 1e-3):
            return 0.602854
        elif(abs(AOA - 10.0) < 1e-3):
            return 0.667947
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
            return 0.000365
        elif(abs(AOA - 2.0) < 1e-3):
            return 0.001444
        elif(abs(AOA - 3.0) < 1e-3):
            return 0.003232
        elif(abs(AOA - 4.0) < 1e-3):
            return 0.005725
        elif(abs(AOA - 5.0) < 1e-3):
            return 0.008915
        elif(abs(AOA - 6.0) < 1e-3):
            return 0.012791
        elif(abs(AOA - 7.0) < 1e-3):
            return 0.017343
        elif(abs(AOA - 8.0) < 1e-3):
            return 0.022557
        elif(abs(AOA - 9.0) < 1e-3):
            return 0.028416
        elif(abs(AOA - 10.0) < 1e-3):
            return 0.034903
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
            return -0.016078
        elif(abs(AOA - 2.0) < 1e-3):
            return -0.031858
        elif(abs(AOA - 3.0) < 1e-3):
            return -0.047599
        elif(abs(AOA - 4.0) < 1e-3):
            return -0.063282
        elif(abs(AOA - 5.0) < 1e-3):
            return -0.078888
        elif(abs(AOA - 6.0) < 1e-3):
            return -0.094398
        elif(abs(AOA - 7.0) < 1e-3):
            return -0.109794
        elif(abs(AOA - 8.0) < 1e-3):
            return -0.125056
        elif(abs(AOA - 9.0) < 1e-3):
            return -0.140165
        elif(abs(AOA - 10.0) < 1e-3):
            return -0.155104
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