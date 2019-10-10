import KratosMultiphysics
from KratosMultiphysics.CompressiblePotentialFlowApplication.compute_lift_process import ComputeLiftProcess
import KratosMultiphysics.CompressiblePotentialFlowApplication as CPFApp

def Factory(settings, Model):
    if( not isinstance(settings,KratosMultiphysics.Parameters) ):
        raise Exception("expected input shall be a Parameters object, encapsulating a json string")
    return WriteForcesProcess(Model, settings["Parameters"])

class WriteForcesProcess(ComputeLiftProcess):
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