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

        # if self.step > 1:
        #     self.upwind_factor_constant -= 0.1
        if self.step > 160:
            self.upwind_factor_constant -= 0.1
        elif self.step > 17:
            self.upwind_factor_constant -= 0.1
            # self.critical_mach += 0.01
        elif self.step > 8:
            # self.free_stream_mach += 0.0095
            self.upwind_factor_constant -= 0.1
        elif self.step > 3:
            self.free_stream_mach += 0.01
        elif self.step > 1:
            self.free_stream_mach += 0.1

        self.u_inf = round(self.free_stream_mach,2) * self.free_stream_speed_of_sound
        self.free_stream_velocity = KratosMultiphysics.Vector(3)

        self.domain_size = self.fluid_model_part.ProcessInfo.GetValue(KratosMultiphysics.DOMAIN_SIZE)
        if self.domain_size == 2:
            # By convention 2D airfoils are in the xy plane
            self.free_stream_velocity[0] = round(self.u_inf*math.cos(self.angle_of_attack),8)
            self.free_stream_velocity[1] = round(self.u_inf*math.sin(self.angle_of_attack),8)
            self.free_stream_velocity[2] = 0.0
        else: # self.domain_size == 3
            # By convention 3D wings and aircrafts:
            # y axis along the span
            # z axis pointing upwards
            # TODO: Add sideslip angle beta
            self.free_stream_velocity[0] = round(self.u_inf*math.cos(self.angle_of_attack),8)
            self.free_stream_velocity[1] = 0.0
            self.free_stream_velocity[2] = round(self.u_inf*math.sin(self.angle_of_attack),8)

        KratosMultiphysics.Logger.PrintInfo('ApplyFarFieldProcess',' step = ', self.step)
        KratosMultiphysics.Logger.PrintInfo('ApplyFarFieldProcess',' free_stream_mach = ', round(self.free_stream_mach,4))
        KratosMultiphysics.Logger.PrintInfo('ApplyFarFieldProcess',' upwinding_factor_constant = ', round(self.upwind_factor_constant,3))
        KratosMultiphysics.Logger.PrintInfo('ApplyFarFieldProcess',' critical_mach = ', round(self.critical_mach,3))
        KratosMultiphysics.Logger.PrintInfo('ApplyFarFieldProcess',' free_stream_velocity = ', self.free_stream_velocity)
        self.fluid_model_part.ProcessInfo.SetValue(CPFApp.FREE_STREAM_MACH, round(self.free_stream_mach,4))
        self.fluid_model_part.ProcessInfo.SetValue(CPFApp.FREE_STREAM_VELOCITY, self.free_stream_velocity)
        self.fluid_model_part.ProcessInfo.SetValue(CPFApp.CRITICAL_MACH, round(self.critical_mach,3))
        self.fluid_model_part.ProcessInfo.SetValue(CPFApp.UPWIND_FACTOR_CONSTANT, round(self.upwind_factor_constant,3))
        super(ApplyFarFieldProcessRefinement, self).ExecuteInitializeSolutionStep()
