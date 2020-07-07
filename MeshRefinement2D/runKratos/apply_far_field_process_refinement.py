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

        if self.step > 1:
            # self.free_stream_mach += 0.01
            self.critical_mach += 0.01
            # self.upwind_factor_constant -= 0.1

        self.u_inf = self.free_stream_mach * self.free_stream_speed_of_sound
        self.free_stream_velocity = KratosMultiphysics.Vector(3)
        self.free_stream_velocity[0] = round(self.u_inf*math.cos(self.angle_of_attack),8)
        self.free_stream_velocity[1] = round(self.u_inf*math.sin(self.angle_of_attack),8)
        self.free_stream_velocity[2] = 0.0
        KratosMultiphysics.Logger.PrintInfo('ApplyFarFieldProcess',' step = ', self.step)
        KratosMultiphysics.Logger.PrintInfo('ApplyFarFieldProcess',' free_stream_mach = ', round(self.free_stream_mach,2))
        KratosMultiphysics.Logger.PrintInfo('ApplyFarFieldProcess',' upwinding_factor_constant = ', self.upwind_factor_constant)
        KratosMultiphysics.Logger.PrintInfo('ApplyFarFieldProcess',' critical_mach = ', self.critical_mach)
        self.fluid_model_part.ProcessInfo.SetValue(CPFApp.FREE_STREAM_MACH,self.free_stream_mach)
        self.fluid_model_part.ProcessInfo.SetValue(CPFApp.FREE_STREAM_VELOCITY,self.free_stream_velocity)
        self.fluid_model_part.ProcessInfo.SetValue(CPFApp.CRITICAL_MACH,self.critical_mach)
        self.fluid_model_part.ProcessInfo.SetValue(CPFApp.UPWIND_FACTOR_CONSTANT,self.upwind_factor_constant)
        super(ApplyFarFieldProcessRefinement, self).ExecuteInitializeSolutionStep()
