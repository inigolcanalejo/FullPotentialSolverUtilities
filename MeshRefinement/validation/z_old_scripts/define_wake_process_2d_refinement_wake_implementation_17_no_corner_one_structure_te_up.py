import KratosMultiphysics
import KratosMultiphysics.CompressiblePotentialFlowApplication
import math

def Factory(settings, Model):
    if( not isinstance(settings,KratosMultiphysics.Parameters) ):
        raise Exception("expected input shall be a Parameters object, encapsulating a json string")

    return DefineWakeProcess(Model, settings["Parameters"])


class DefineWakeProcess(KratosMultiphysics.Process):
    def __init__(self, Model, settings ):
        KratosMultiphysics.Process.__init__(self)

        default_settings = KratosMultiphysics.Parameters("""
            {
                "mesh_id"                   : 0,
                "model_part_name"           : "please specify the model part that contains the kutta nodes",
                "upper_surface_model_part_name" : "please specify the model part that contains the upper surface nodes",
                "lower_surface_model_part_name" : "please specify the model part that contains the lower surface nodes",
                "fluid_part_name"           : "MainModelPart",
                "direction"                 : [1.0,0.0,0.0],
                "stl_filename"              : "please specify name of stl file",
                "epsilon"    : 1e-9
            }
            """)

        settings.ValidateAndAssignDefaults(default_settings)

        self.direction = KratosMultiphysics.Vector(3)
        self.direction[0] = settings["direction"][0].GetDouble()
        self.direction[1] = settings["direction"][1].GetDouble()
        self.direction[2] = settings["direction"][2].GetDouble()
        dnorm = math.sqrt(self.direction[0]**2 + self.direction[1]**2 + self.direction[2]**2)
        self.direction[0] /= dnorm
        self.direction[1] /= dnorm
        self.direction[2] /= dnorm
        print(self.direction)

        self.epsilon = settings["epsilon"].GetDouble()

        self.upper_surface_model_part = Model[settings["upper_surface_model_part_name"].GetString()]
        self.lower_surface_model_part = Model[settings["lower_surface_model_part_name"].GetString()]
        self.fluid_model_part = Model[settings["fluid_part_name"].GetString()]
        self.wake_model_part = self.fluid_model_part.CreateSubModelPart("wake_modelpart")
        self.kutta_model_part = self.fluid_model_part.CreateSubModelPart("kutta_model_part")
        self.trailing_edge_model_part = self.fluid_model_part.CreateSubModelPart("trailing_edge_model_part")
        self.penalty_model_part = self.fluid_model_part.CreateSubModelPart("penalty_model_part")

        KratosMultiphysics.NormalCalculationUtils().CalculateOnSimplex(self.fluid_model_part,
                                                                       self.fluid_model_part.ProcessInfo[KratosMultiphysics.DOMAIN_SIZE])

        # Neigbour search tool instance
        AvgElemNum = 10
        AvgNodeNum = 10
        nodal_neighbour_search = KratosMultiphysics.FindNodalNeighboursProcess(self.fluid_model_part, AvgElemNum, AvgNodeNum)
        # Find neighbours
        nodal_neighbour_search.Execute()

        self.stl_filename = settings["stl_filename"].GetString()
        
    def Execute(self):
        #find the trailing edge node
        pos = -1e30
        
        print('...Finding the trailing edge...')
        for unode in self.upper_surface_model_part.Nodes:
            if(unode.X > pos):
                pos = unode.X
                te_node = unode
        
        for unode in self.upper_surface_model_part.Nodes:
            if(unode.X > pos - 1e-10):
                unode.SetSolutionStepValue(KratosMultiphysics.CompressiblePotentialFlowApplication.TRAILING_EDGE, True)

        self.kutta_model_part.Nodes.append(te_node)

        print('...Finding the trailing edge finished...')

        #mark as STRUCTURE and deactivate the elements that touch the kutta node
        for node in self.kutta_model_part.Nodes:
            node.Set(KratosMultiphysics.STRUCTURE)
            x1 = node.X
            y1 = node.Y
            z1 = node.Z

        #Selecting upper and lower surface nodes
        for node in self.upper_surface_model_part.Nodes:
            node.SetSolutionStepValue(KratosMultiphysics.CompressiblePotentialFlowApplication.UPPER_SURFACE, True)
            node.SetSolutionStepValue(KratosMultiphysics.CompressiblePotentialFlowApplication.AIRFOIL, True)
        for node in self.lower_surface_model_part.Nodes:
            node.SetSolutionStepValue(KratosMultiphysics.CompressiblePotentialFlowApplication.LOWER_SURFACE, True)
            node.SetSolutionStepValue(KratosMultiphysics.CompressiblePotentialFlowApplication.AIRFOIL, True)

        #compute the distances of the elements of the wake, and decide which ones are wake
        xn = KratosMultiphysics.Vector(3)

        self.n = KratosMultiphysics.Vector(3)
        self.n[0] = -self.direction[1]
        self.n[1] = self.direction[0]
        self.n[2] = 0.0

        print('...Selecting wake elements...')
        for node in self.kutta_model_part.Nodes:
            x0 = node.X
            y0 = node.Y
            for elem in self.fluid_model_part.Elements:
                #check in the potentially active portion
                potentially_active_portion = False
                for elnode in elem.GetNodes():
                    #all nodes that touch the kutta nodes are potentiallyactive
                    if(elnode.Is(KratosMultiphysics.STRUCTURE)):
                        potentially_active_portion = True
                        break
                for elnode in elem.GetNodes():
                    #compute x distance
                    xn[0] = elnode.X - x0
                    xn[1] = elnode.Y - y0
                    xn[2] = 0.0
                    dx = xn[0]*self.direction[0] + xn[1]*self.direction[1]
                    if(dx > 0):
                        potentially_active_portion = True
                        break

                if(potentially_active_portion):
                    distances = KratosMultiphysics.Vector(len(elem.GetNodes()))

                    counter = 0
                    for elnode in elem.GetNodes():
                        xn[0] = elnode.X - x0
                        xn[1] = elnode.Y - y0
                        xn[2] = 0.0
                        d = xn[0]*self.n[0] + xn[1]*self.n[1]
                        if(abs(d) < self.epsilon):
                            d = self.epsilon
                        if(d<0 and
                            elnode.IsNot(KratosMultiphysics.STRUCTURE) and
                            elnode.GetSolutionStepValue(KratosMultiphysics.CompressiblePotentialFlowApplication.UPPER_SURFACE) == True):
                            d = self.epsilon
                            print('\ndetected upper surface node')
                        if( xn[0] < 0 and 
                            d > 0 and #for high angles of attack (selecting nodes in the lower surface)
                            elnode.IsNot(KratosMultiphysics.STRUCTURE) and
                            elnode.GetSolutionStepValue(KratosMultiphysics.CompressiblePotentialFlowApplication.LOWER_SURFACE) == True):
                            d = -self.epsilon
                            print('\ndetected lower surface node!')
                        distances[counter] = d
                        counter += 1

                    npos = 0
                    nneg = 0
                    for d in distances:
                        if(d < 0):
                            nneg += 1
                        else:
                            npos += 1

                    if(nneg > 0 and npos > 0):
                        elem.Set(KratosMultiphysics.MARKER, True)
                        self.wake_model_part.Elements.append(elem)
                        counter = 0
                        for elnode in elem.GetNodes():
                            elnode.SetSolutionStepValue(KratosMultiphysics.DISTANCE, 0, distances[counter])
                            self.wake_model_part.Nodes.append(elnode)
                            counter += 1
                            #In this implementation 15 trailing edge elements elements are selected
                            if(elnode.Is(KratosMultiphysics.STRUCTURE)):
                                #selecting Kutta elements
                                elem.SetValue(KratosMultiphysics.CompressiblePotentialFlowApplication.TRAILING_EDGE, True)
                                self.trailing_edge_model_part.Elements.append(elem)
                        elem.SetValue(KratosMultiphysics.ELEMENTAL_DISTANCES, distances)
        print('...Selecting wake elements finished...')


        #Select the element with a face to the airfoil as kutta and unmark it
        for elem in self.trailing_edge_model_part.Elements:
            counter_kutta_nodes = 0
            for elnode in elem.GetNodes():
                if(elnode.GetSolutionStepValue(KratosMultiphysics.CompressiblePotentialFlowApplication.AIRFOIL) == True):
                    elnode.SetSolutionStepValue(KratosMultiphysics.CompressiblePotentialFlowApplication.KUTTA, True)
                    counter_kutta_nodes += 1
            if(counter_kutta_nodes > 1):
                elem.SetValue(KratosMultiphysics.CompressiblePotentialFlowApplication.KUTTA, True)
                elem.Set(KratosMultiphysics.MARKER, False)
                for elnode in elem.GetNodes():
                    elnode.SetSolutionStepValue(KratosMultiphysics.CompressiblePotentialFlowApplication.KUTTA, True)
        
        number_of_trailing_edge_elements = self.trailing_edge_model_part.NumberOfElements()
        print('number_of_trailing_edge_elements = ', number_of_trailing_edge_elements)

        for i in range(number_of_trailing_edge_elements - 2):
            #Select the adyecent element also as KUTTA and unmark them
            for elem in self.trailing_edge_model_part.Elements:
                counter_kutta_nodes = 0
                #Loop over the nodes of the element
                for elnode in elem.GetNodes():
                    #Check whether the node is Kutta or not
                    if(elnode.GetSolutionStepValue(KratosMultiphysics.CompressiblePotentialFlowApplication.KUTTA) == True):
                        counter_kutta_nodes += 1
                if(counter_kutta_nodes > 1):
                    elem.SetValue(KratosMultiphysics.CompressiblePotentialFlowApplication.KUTTA, True)
                    elem.Set(KratosMultiphysics.MARKER, False)
                    for elnode in elem.GetNodes():
                        self.kutta_model_part.Nodes.append(elnode)

            for node in self.kutta_model_part.GetNodes():
                node.SetSolutionStepValue(KratosMultiphysics.CompressiblePotentialFlowApplication.KUTTA, True)

        #Deactivate the rest of the kutta elements
        for elem in self.trailing_edge_model_part.Elements:
            if(elem.GetValue(KratosMultiphysics.CompressiblePotentialFlowApplication.KUTTA) == False):
                elem.Set(KratosMultiphysics.STRUCTURE)
                #elem.Set(KratosMultiphysics.ACTIVE, False)
                #for elnode in elem.GetNodes():
                #    elnode.SetSolutionStepValue(KratosMultiphysics.CompressiblePotentialFlowApplication.DEACTIVATED_WAKE, True)


    def ExecuteInitialize(self):
        self.Execute()

    def ExecuteFinalizeSolutionStep(self):

        self.work_dir = '/home/inigo/simulations/naca0012/07_salome/05_MeshRefinement/'

        potential_jump_results_file_name = self.work_dir + 'plots/potential_jump/data/jump/potential_jump_results.dat'
        with open(potential_jump_results_file_name,'w') as potential_jump_file:

            for node in self.wake_model_part.GetNodes():
                x = node.X
                jump = node.GetSolutionStepValue(KratosMultiphysics.CompressiblePotentialFlowApplication.POTENTIAL_JUMP)

                if(abs(jump) > 1e-7):
                    potential_jump_file.write('{0:15f} {1:15f}\n'.format(x, jump))

            potential_jump_file.flush()

        potential_jump_tikz_file_name = self.work_dir + "plots/potential_jump/data/jump/jump.tikz"
        with open(potential_jump_tikz_file_name,'w') as jump_tikz_file:
            jump_tikz_file.write('\\begin{tikzpicture}\n' +
            '\\begin{axis}[\n' +
            '\t    title={Potential jump(x)},\n' +
            '\t    xlabel={$x$},\n' +
            '\t    ylabel={Potential Jump(x)},\n' +
            '\t    ymajorgrids=true,\n' +
            '\t    xmajorgrids=true,\n' +
            '\t    grid style=dashed,\n' +
            '\t    width=12cm\n' +
            ']\n\n' +
            '\\addplot[\n' +
            '\t    only marks,\n' +
            '\t    color=black,\n' +
            '\t    mark=*,\n' +
            '\t    ]\n' +
            '\t    table {potential_jump_results.dat};  \n' +
            '\t\end{axis}\n' +
            '\t\end{tikzpicture}')
            jump_tikz_file.flush()


