import KratosMultiphysics
from KratosMultiphysics.CompressiblePotentialFlowApplication.compute_lift_process import ComputeLiftProcess

def Factory(settings, Model):
    if( not isinstance(settings,KratosMultiphysics.Parameters) ):
        raise Exception("expected input shall be a Parameters object, encapsulating a json string")
    return WriteForcesProcess(Model, settings["Parameters"])

class WriteForcesProcess(ComputeLiftProcess):
    def ExecuteFinalizeSolutionStep(self):
        super(WriteForcesProcess, self).ExecuteFinalizeSolutionStep()

        with open('results_3d.dat', 'a') as file:
            file.write('{0:12.4f} {1:12.2e} {2:12.4f} {3:12.2e}'.format(
                self.lift_coefficient, self.drag_coefficient, self.lift_coefficient_far_field, self.drag_coefficient_far_field))
            file.flush()