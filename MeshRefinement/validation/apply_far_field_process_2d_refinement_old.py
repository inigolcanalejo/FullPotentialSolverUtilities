import KratosMultiphysics
import KratosMultiphysics.CompressiblePotentialFlowApplication as CompressiblePotentialFlowApplication
import numpy as np
#from CompressiblePotentialFlowApplication import*

def Factory(settings, Model):
    if( not isinstance(settings,KratosMultiphysics.Parameters) ):
        raise Exception("expected input shall be a Parameters object, encapsulating a json string")
    return ApplyFarFieldProcess(Model, settings["Parameters"])

## All the processes python should be derived from "Process"
class ApplyFarFieldProcess(KratosMultiphysics.Process):
    def __init__(self, Model, settings ):
        KratosMultiphysics.Process.__init__(self)
        
        default_parameters = KratosMultiphysics.Parameters( """
            {
                "model_part_name":"PLEASE_CHOOSE_MODEL_PART_NAME",
                "mesh_id": 0,
                "inlet_phi": 1.0,
                "velocity_infinity": [1.0,0.0,0]
            }  """ );
        
            
        settings.ValidateAndAssignDefaults(default_parameters);
        
        self.model_part = Model[settings["model_part_name"].GetString()]
        self.velocity_infinity = KratosMultiphysics.Vector(3)#array('d', [1.0, 2.0, 3.14])#np.array([0,0,0])#np.zeros(3)#vector(3)
        self.velocity_infinity[0] = settings["velocity_infinity"][0].GetDouble()
        self.velocity_infinity[1] = settings["velocity_infinity"][1].GetDouble()
        self.velocity_infinity[2] = settings["velocity_infinity"][2].GetDouble()
        #self.density_infinity = settings["density_infinity"].GetDouble() #TODO: must read this from the properties
        self.inlet_phi = settings["inlet_phi"].GetDouble()

        self.penalty = 0e0
        self.peso = 1e0
        self.penalty2 = 1
        
        self.model_part.ProcessInfo.SetValue(CompressiblePotentialFlowApplication.VELOCITY_INFINITY,self.velocity_infinity)
        self.model_part.ProcessInfo.SetValue(KratosMultiphysics.INITIAL_PENALTY,self.penalty)
        self.model_part.ProcessInfo.SetValue(KratosMultiphysics.WATER_PRESSURE,self.peso)
        self.model_part.ProcessInfo.SetValue(KratosMultiphysics.MIU,self.penalty2)
        
        
        
    def Execute(self):
        #KratosMultiphysics.VariableUtils().SetVectorVar(CompressiblePotentialFlowApplication.VELOCITY_INFINITY, self.velocity_infinity, self.model_part.Conditions)
        for cond in self.model_part.Conditions:
            cond.SetValue(CompressiblePotentialFlowApplication.VELOCITY_INFINITY, self.velocity_infinity)

        #select the first node
        for node in self.model_part.Nodes:
            node1 = node
            break
        
        #find the node with the minimal x
        x0 = node1.X
        y0 = node1.X
        z0 = node1.X

        pos = 1e30
        for node in self.model_part.Nodes:
            dx = node.X - x0
            dy = node.Y - y0
            dz = node.Z - z0
            
            tmp = dx*self.velocity_infinity[0] + dy*self.velocity_infinity[1] + dz*self.velocity_infinity[2]
            
            if(tmp < pos):
                pos = tmp

        for node in self.model_part.Nodes:
            dx = node.X - x0
            dy = node.Y - y0
            dz = node.Z - z0
            
            tmp = dx*self.velocity_infinity[0] + dy*self.velocity_infinity[1] + dz*self.velocity_infinity[2]
            
            if(tmp < pos+1e-9):
                node.Fix(KratosMultiphysics.POTENTIAL)
                node.SetSolutionStepValue(KratosMultiphysics.POTENTIAL,0,self.inlet_phi)
                node.Set(KratosMultiphysics.INLET, True)
        
    def ExecuteInitializeSolutionStep(self):
        self.Execute()
        
    def ExecuteFinalizeSolutionStep(self):

        self.work_dir = '/home/inigo/simulations/naca0012/07_salome/05_MeshRefinement/'

        velocity_norm_x_results_file_name = self.work_dir + 'plots/far_field/data/0_original/velocity_norm_x_results.dat'
        velocity_norm_x_file = open(velocity_norm_x_results_file_name,'w')

        velocity_u_x_results_file_name = self.work_dir + 'plots/far_field/data/0_original/velocity_u_x_results.dat'
        velocity_u_x_file = open(velocity_u_x_results_file_name,'w')

        velocity_v_x_results_file_name = self.work_dir + 'plots/far_field/data/0_original/velocity_v_x_results.dat'
        velocity_v_x_file = open(velocity_v_x_results_file_name,'w')


        velocity_norm_y_results_file_name = self.work_dir + 'plots/far_field/data/0_original/velocity_norm_y_results.dat'
        velocity_norm_y_file = open(velocity_norm_y_results_file_name,'w')

        velocity_u_y_results_file_name = self.work_dir + 'plots/far_field/data/0_original/velocity_u_y_results.dat'
        velocity_u_y_file = open(velocity_u_y_results_file_name,'w')

        velocity_v_y_results_file_name = self.work_dir + 'plots/far_field/data/0_original/velocity_v_y_results.dat'
        velocity_v_y_file = open(velocity_v_y_results_file_name,'w')

        velocity_far_field = KratosMultiphysics.Vector(3)

        for cond in self.model_part.Conditions:
            velocity_far_field = cond.GetValue(KratosMultiphysics.VELOCITY)
            velocity_norm = np.linalg.norm(velocity_far_field)
            
            x = 0.5*(cond.GetNodes()[1].X0+cond.GetNodes()[0].X0)
            y = 0.5*(cond.GetNodes()[1].Y0+cond.GetNodes()[0].Y0)
            
            velocity_norm_x_file.write('{0:15f} {1:15f}\n'.format(x, velocity_norm))
            velocity_u_x_file.write('{0:15f} {1:15f}\n'.format(x, velocity_far_field[0]))
            velocity_v_x_file.write('{0:15f} {1:15f}\n'.format(x, velocity_far_field[1]))

            velocity_norm_y_file.write('{0:15f} {1:15f}\n'.format(y, velocity_norm))
            velocity_u_y_file.write('{0:15f} {1:15f}\n'.format(y, velocity_far_field[0]))
            velocity_v_y_file.write('{0:15f} {1:15f}\n'.format(y, velocity_far_field[1]))
            

        velocity_norm_x_file.flush()
        velocity_norm_x_file.close()
        
        velocity_u_x_file.flush()
        velocity_u_x_file.close()

        velocity_v_x_file.flush()
        velocity_v_x_file.close()

        velocity_norm_y_file.flush()
        velocity_norm_y_file.close()
        
        velocity_u_y_file.flush()
        velocity_u_y_file.close()

        velocity_v_y_file.flush()
        velocity_v_y_file.close()

        velocity_norm_x_tikz_file_name = self.work_dir + "plots/far_field/data/0_original/velocity_norm_x.tikz"
        with open(velocity_norm_x_tikz_file_name,'w') as velocity_norm_x_tikz_file:
            velocity_norm_x_tikz_file.write('\\begin{tikzpicture}\n' +
            '\\begin{axis}[\n' +
            '\t    title={Far field velocity norm(x)},\n' +
            '\t    xlabel={$x$},\n' +
            '\t    ylabel={velocity norm(x)},\n' +
            '\t    ymajorgrids=true,\n' +
            '\t    xmajorgrids=true,\n' +
            '\t    y tick label style={ \n' +
            '\t        /pgf/number format/.cd, \n' + 
            '\t            fixed,\n' + 
            '\t            fixed zerofill,\n' + 
            '\t            precision=5,\n' + 
            '\t        /tikz/.cd \n' + 
            '\t    },\n' + 
            '\t    grid style=dashed,\n' +
            '\t    width=12cm\n' +
            ']\n\n' +
            '\\addplot[\n' +
            '\t    only marks,\n' +
            '\t    color=black,\n' +
            '\t    mark=*,\n' +
            '\t    ]\n' +
            '\t    table {velocity_norm_x_results.dat};  \n' +
            '\t\end{axis}\n' +
            '\t\end{tikzpicture}')
            velocity_norm_x_tikz_file.flush()

        velocity_u_x_tikz_file_name = self.work_dir + "plots/far_field/data/0_original/velocity_u_x.tikz"
        with open(velocity_u_x_tikz_file_name,'w') as velocity_u_x_tikz_file:
            velocity_u_x_tikz_file.write('\\begin{tikzpicture}\n' +
            '\\begin{axis}[\n' +
            '\t    title={Far field velocity u(x)},\n' +
            '\t    xlabel={$x$},\n' +
            '\t    ylabel={u(x)},\n' +
            '\t    ymajorgrids=true,\n' +
            '\t    xmajorgrids=true,\n' +
            '\t    y tick label style={ \n' +
            '\t        /pgf/number format/.cd, \n' + 
            '\t            fixed,\n' + 
            '\t            fixed zerofill,\n' + 
            '\t            precision=5,\n' + 
            '\t        /tikz/.cd \n' + 
            '\t    },\n' +
            '\t    grid style=dashed,\n' +
            '\t    width=12cm\n' +
            ']\n\n' +
            '\\addplot[\n' +
            '\t    only marks,\n' +
            '\t    color=blue,\n' +
            '\t    mark=*,\n' +
            '\t    ]\n' +
            '\t    table {velocity_u_x_results.dat};  \n' +
            '\t\end{axis}\n' +
            '\t\end{tikzpicture}')
            velocity_u_x_tikz_file.flush()

        velocity_v_x_tikz_file_name = self.work_dir + "plots/far_field/data/0_original/velocity_v_x.tikz"
        with open(velocity_v_x_tikz_file_name,'w') as velocity_v_x_tikz_file:
            velocity_v_x_tikz_file.write('\\begin{tikzpicture}\n' +
            '\\begin{axis}[\n' +
            '\t    title={Far field velocity v(x)},\n' +
            '\t    xlabel={$x$},\n' +
            '\t    ylabel={v(x)},\n' +
            '\t    ymajorgrids=true,\n' +
            '\t    xmajorgrids=true,\n' +
            '\t    y tick label style={ \n' +
            '\t        /pgf/number format/.cd, \n' + 
            '\t            fixed,\n' + 
            '\t            fixed zerofill,\n' + 
            '\t            precision=5,\n' + 
            '\t        /tikz/.cd \n' + 
            '\t    },\n' +
            '\t    grid style=dashed,\n' +
            '\t    width=12cm\n' +
            ']\n\n' +
            '\\addplot[\n' +
            '\t    only marks,\n' +
            '\t    color=red,\n' +
            '\t    mark=*,\n' +
            '\t    ]\n' +
            '\t    table {velocity_v_x_results.dat};  \n' +
            '\t\end{axis}\n' +
            '\t\end{tikzpicture}')
            velocity_v_x_tikz_file.flush()

        velocity_norm_y_tikz_file_name = self.work_dir + "plots/far_field/data/0_original/velocity_norm_y.tikz"
        with open(velocity_norm_y_tikz_file_name,'w') as velocity_norm_y_tikz_file:
            velocity_norm_y_tikz_file.write('\\begin{tikzpicture}\n' +
            '\\begin{axis}[\n' +
            '\t    title={Far field velocity norm(y)},\n' +
            '\t    xlabel={$y$},\n' +
            '\t    ylabel={velocity norm(y)},\n' +
            '\t    ymajorgrids=true,\n' +
            '\t    xmajorgrids=true,\n' +
            '\t    y tick label style={ \n' +
            '\t        /pgf/number format/.cd, \n' + 
            '\t            fixed,\n' + 
            '\t            fixed zerofill,\n' + 
            '\t            precision=5,\n' + 
            '\t        /tikz/.cd \n' + 
            '\t    },\n' +
            '\t    grid style=dashed,\n' +
            '\t    width=12cm\n' +
            ']\n\n' +
            '\\addplot[\n' +
            '\t    only marks,\n' +
            '\t    color=black,\n' +
            '\t    mark=*,\n' +
            '\t    ]\n' +
            '\t    table {velocity_norm_y_results.dat};  \n' +
            '\t\end{axis}\n' +
            '\t\end{tikzpicture}')
            velocity_norm_y_tikz_file.flush()

        velocity_u_y_tikz_file_name = self.work_dir + "plots/far_field/data/0_original/velocity_u_y.tikz"
        with open(velocity_u_y_tikz_file_name,'w') as velocity_u_y_tikz_file:
            velocity_u_y_tikz_file.write('\\begin{tikzpicture}\n' +
            '\\begin{axis}[\n' +
            '\t    title={Far field velocity u(y)},\n' +
            '\t    xlabel={$y$},\n' +
            '\t    ylabel={u(y)},\n' +
            '\t    ymajorgrids=true,\n' +
            '\t    xmajorgrids=true,\n' +
            '\t    y tick label style={ \n' +
            '\t        /pgf/number format/.cd, \n' + 
            '\t            fixed,\n' + 
            '\t            fixed zerofill,\n' + 
            '\t            precision=5,\n' + 
            '\t        /tikz/.cd \n' + 
            '\t    },\n' +
            '\t    grid style=dashed,\n' +
            '\t    width=12cm\n' +
            ']\n\n' +
            '\\addplot[\n' +
            '\t    only marks,\n' +
            '\t    color=blue,\n' +
            '\t    mark=*,\n' +
            '\t    ]\n' +
            '\t    table {velocity_u_y_results.dat};  \n' +
            '\t\end{axis}\n' +
            '\t\end{tikzpicture}')
            velocity_u_y_tikz_file.flush()

        velocity_v_y_tikz_file_name = self.work_dir + "plots/far_field/data/0_original/velocity_v_y.tikz"
        with open(velocity_v_y_tikz_file_name,'w') as velocity_v_y_tikz_file:
            velocity_v_y_tikz_file.write('\\begin{tikzpicture}\n' +
            '\\begin{axis}[\n' +
            '\t    title={Far field velocity v(y)},\n' +
            '\t    xlabel={$y$},\n' +
            '\t    ylabel={v(y)},\n' +
            '\t    ymajorgrids=true,\n' +
            '\t    xmajorgrids=true,\n' +
            '\t    y tick label style={ \n' +
            '\t        /pgf/number format/.cd, \n' + 
            '\t            fixed,\n' + 
            '\t            fixed zerofill,\n' + 
            '\t            precision=5,\n' + 
            '\t        /tikz/.cd \n' + 
            '\t    },\n' +
            '\t    grid style=dashed,\n' +
            '\t    width=12cm\n' +
            ']\n\n' +
            '\\addplot[\n' +
            '\t    only marks,\n' +
            '\t    color=red,\n' +
            '\t    mark=*,\n' +
            '\t    ]\n' +
            '\t    table {velocity_v_y_results.dat};  \n' +
            '\t\end{axis}\n' +
            '\t\end{tikzpicture}')
            velocity_v_y_tikz_file.flush()
