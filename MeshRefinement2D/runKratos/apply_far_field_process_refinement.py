import KratosMultiphysics
import KratosMultiphysics.FluidDynamicsApplication as KratosCFD
import KratosMultiphysics.CompressiblePotentialFlowApplication as CPFApp
from KratosMultiphysics.CompressiblePotentialFlowApplication.apply_far_field_process import ApplyFarFieldProcess
import math

def Factory(settings, Model):
    if( not isinstance(settings,KratosMultiphysics.Parameters) ):
        raise Exception("expected input shall be a Parameters object, encapsulating a json string")
    return ApplyFarFieldProcessRefinement(Model, settings["Parameters"])

class ApplyFarFieldProcessRefinement(ApplyFarFieldProcess):
    def ExecuteInitializeSolutionStep(self):
        self.step = self.fluid_model_part.ProcessInfo[KratosMultiphysics.STEP]

        # For M > 0.75 we need to increase and decrease the viscosity
        if self.free_stream_mach > 0.759:
            if not self.increase_viscotiy:
                # Decreasing viscosity
                self.critical_mach += 0.01
                self.upwind_factor_constant -= 0.1
            elif abs(self.critical_mach - 0.75) < 1e-4:
                # When reached, increase the mach number and then decrease the viscosity
                self.free_stream_mach += 0.005
                self.increase_viscotiy = False
            elif self.increase_viscotiy:
                # Increasing viscosity
                self.critical_mach -= 0.01
                self.upwind_factor_constant += 0.1

            if abs(self.critical_mach - 0.90) < 1e-4:
                # When reaching, start increasing the viscosity again
                self.increase_viscotiy = True

        elif self.step > 10:
            self.increase_viscotiy = True
            self.free_stream_mach += 0.005
        elif self.step > 7:
            self.increase_viscotiy = True
            self.free_stream_mach += 0.01
        elif self.step > 1:
            self.increase_viscotiy = True
            self.free_stream_mach += 0.10

        self.u_inf = round(self.free_stream_mach,2) * self.free_stream_speed_of_sound
        self.free_stream_velocity = KratosMultiphysics.Vector(3)
        self.free_stream_velocity[0] = round(self.u_inf*math.cos(self.angle_of_attack),8)
        self.free_stream_velocity[1] = round(self.u_inf*math.sin(self.angle_of_attack),8)
        self.free_stream_velocity[2] = 0.0
        KratosMultiphysics.Logger.PrintInfo('ApplyFarFieldProcess',' step = ', self.step)
        KratosMultiphysics.Logger.PrintInfo('ApplyFarFieldProcess',' free_stream_mach = ', round(self.free_stream_mach,3))
        KratosMultiphysics.Logger.PrintInfo('ApplyFarFieldProcess',' upwinding_factor_constant = ', round(self.upwind_factor_constant,3))
        KratosMultiphysics.Logger.PrintInfo('ApplyFarFieldProcess',' critical_mach = ', round(self.critical_mach,3))
        self.fluid_model_part.ProcessInfo.SetValue(CPFApp.FREE_STREAM_MACH, round(self.free_stream_mach,3))
        self.fluid_model_part.ProcessInfo.SetValue(CPFApp.FREE_STREAM_VELOCITY, self.free_stream_velocity)
        self.fluid_model_part.ProcessInfo.SetValue(CPFApp.CRITICAL_MACH, round(self.critical_mach,3))
        self.fluid_model_part.ProcessInfo.SetValue(CPFApp.UPWIND_FACTOR_CONSTANT, round(self.upwind_factor_constant,3))
        super(ApplyFarFieldProcessRefinement, self).ExecuteInitializeSolutionStep()
