from __future__ import print_function, absolute_import, division #makes KratosMultiphysics backward compatible with python 2.6 and 2.7
# importing the Kratos Library
import KratosMultiphysics
KratosMultiphysics.CheckForPreviousImport()


def CreateSolver(main_model_part, custom_settings):
    return LaplacianSolver(main_model_part, custom_settings)

class LaplacianSolver:
    def __init__(self, model_part, custom_settings):
        self.MoveMeshFlag = False

        #TODO: shall obtain the compute_model_part from the MODEL once the object is implemented
        self.main_model_part = model_part    
        
        ##settings string in json format
        default_settings = KratosMultiphysics.Parameters("""
        {
            "solver_type": "potential_flow_solver",
            "echo_level": 1,
            "relative_tolerance": 1e-5,
            "absolute_tolerance": 1e-9,
            "maximum_iterations": 1,
            "compute_reactions": false,
            "compute_condition_number": false,
            "reform_dofs_at_each_step": false,
            "calculate_solution_norm" : false,
            "volume_model_part_name" : "volume_model_part",
            "skin_parts":[],
            "no_skin_parts"                : [],
            "model_import_settings": {
                    "input_type": "mdpa",
                    "input_filename": "unknown_name"
            },
            "element_replace_settings": {
                    "element_name":"CompressiblePotentialFlowElement2D3N",
                    "condition_name": "PotentialWallCondition2D2N"
            },
            "linear_solver_settings": {
                    "solver_type": "AMGCL",
                    "max_iteration": 400,
                    "gmres_krylov_space_dimension": 100,
                    "smoother_type":"ilu0",
                    "coarsening_type":"ruge_stuben",
                    "coarse_enough" : 5000,
                    "krylov_type": "lgmres",
                    "tolerance": 1e-9,
                    "verbosity": 3,
                    "scaling": false
            }
        }""")
                    
        ##overwrite the default settings with user-provided parameters
        self.settings = custom_settings
        self.settings.ValidateAndAssignDefaults(default_settings)
        
        #construct the linear solvers
        import linear_solver_factory
        self.linear_solver = linear_solver_factory.ConstructSolver(self.settings["linear_solver_settings"])

        print("Construction of LaplacianSolver finished")

    def AddVariables(self):
        self.main_model_part.AddNodalSolutionStepVariable(KratosMultiphysics.POTENTIAL)
        self.main_model_part.AddNodalSolutionStepVariable(KratosMultiphysics.AUXILIARY_VELOCITY_POTENTIAL)
        self.main_model_part.AddNodalSolutionStepVariable(KratosMultiphysics.NODAL_H)
        self.main_model_part.AddNodalSolutionStepVariable(KratosMultiphysics.DISTANCE)
        self.main_model_part.AddNodalSolutionStepVariable(KratosMultiphysics.NORMAL)
        self.main_model_part.AddNodalSolutionStepVariable(KratosMultiphysics.CompressiblePotentialFlowApplication.VELOCITY_INFINITY)
        self.main_model_part.AddNodalSolutionStepVariable(KratosMultiphysics.CompressiblePotentialFlowApplication.VELOCITY_LOWER)
        self.main_model_part.AddNodalSolutionStepVariable(KratosMultiphysics.CompressiblePotentialFlowApplication.PRESSURE_LOWER)
        self.main_model_part.AddNodalSolutionStepVariable(KratosMultiphysics.CompressiblePotentialFlowApplication.UPPER_SURFACE)
        self.main_model_part.AddNodalSolutionStepVariable(KratosMultiphysics.CompressiblePotentialFlowApplication.LOWER_SURFACE)
        self.main_model_part.AddNodalSolutionStepVariable(KratosMultiphysics.CompressiblePotentialFlowApplication.UPPER_WAKE)
        self.main_model_part.AddNodalSolutionStepVariable(KratosMultiphysics.CompressiblePotentialFlowApplication.LOWER_WAKE)
        self.main_model_part.AddNodalSolutionStepVariable(KratosMultiphysics.CompressiblePotentialFlowApplication.POTENTIAL_JUMP)
        self.main_model_part.AddNodalSolutionStepVariable(KratosMultiphysics.TEMPERATURE)
        self.main_model_part.AddNodalSolutionStepVariable(KratosMultiphysics.INTERNAL_ENERGY)
        self.main_model_part.AddNodalSolutionStepVariable(KratosMultiphysics.EXTERNAL_ENERGY)
        self.main_model_part.AddNodalSolutionStepVariable(KratosMultiphysics.CompressiblePotentialFlowApplication.ENERGY_NORM_REFERENCE)
        self.main_model_part.AddNodalSolutionStepVariable(KratosMultiphysics.CompressiblePotentialFlowApplication.POTENTIAL_ENERGY_REFERENCE)
        self.main_model_part.AddNodalSolutionStepVariable(KratosMultiphysics.CompressiblePotentialFlowApplication.AIRFOIL)
        self.main_model_part.AddNodalSolutionStepVariable(KratosMultiphysics.CompressiblePotentialFlowApplication.TRAILING_EDGE)
        self.main_model_part.AddNodalSolutionStepVariable(KratosMultiphysics.CompressiblePotentialFlowApplication.KUTTA)
        self.main_model_part.AddNodalSolutionStepVariable(KratosMultiphysics.CompressiblePotentialFlowApplication.DEACTIVATED_WAKE)
        self.main_model_part.AddNodalSolutionStepVariable(KratosMultiphysics.CompressiblePotentialFlowApplication.ALL_TRAILING_EDGE)
        self.main_model_part.AddNodalSolutionStepVariable(KratosMultiphysics.CompressiblePotentialFlowApplication.ZERO_VELOCITY_CONDITION)

    def AddDofs(self):
        KratosMultiphysics.VariableUtils().AddDof(KratosMultiphysics.POTENTIAL, self.main_model_part)
        KratosMultiphysics.VariableUtils().AddDof(KratosMultiphysics.AUXILIARY_VELOCITY_POTENTIAL, self.main_model_part)
        KratosMultiphysics.VariableUtils().AddDof(KratosMultiphysics.NODAL_H, self.main_model_part)

        #KratosMultiphysics.VariableUtils().SetNonHistoricalVariable(KratosMultiphysics.CompressiblePotentialFlowApplication.TRAILING_EDGE, 0, self.main_model_part.GetNodes())
        #KratosMultiphysics.VariableUtils().SetNonHistoricalVariable(KratosMultiphysics.CompressiblePotentialFlowApplication.KUTTA, 0, self.main_model_part.GetNodes())

    def Initialize(self):
        time_scheme = KratosMultiphysics.ResidualBasedIncrementalUpdateStaticScheme()
        move_mesh_flag = False #USER SHOULD NOT CHANGE THIS

        builder_and_solver = KratosMultiphysics.ResidualBasedBlockBuilderAndSolverWithConstraints(self.linear_solver)
        
        self.solver = KratosMultiphysics.ResidualBasedLinearStrategy(
            self.main_model_part, 
            time_scheme, 
            self.linear_solver,
            builder_and_solver,
            self.settings["compute_reactions"].GetBool(), 
            self.settings["reform_dofs_at_each_step"].GetBool(), 
            self.settings["calculate_solution_norm"].GetBool(), 
            move_mesh_flag)
        
        (self.solver).SetEchoLevel(self.settings["echo_level"].GetInt())
        self.solver.Check()
        
    def ImportModelPart(self):
        
        if(self.settings["model_import_settings"]["input_type"].GetString() == "mdpa"):
            #here it would be the place to import restart data if required
            print(self.settings["model_import_settings"]["input_filename"].GetString())
            KratosMultiphysics.ModelPartIO(self.settings["model_import_settings"]["input_filename"].GetString()).ReadModelPart(self.main_model_part)
                     
            throw_errors = False
            KratosMultiphysics.TetrahedralMeshOrientationCheck(self.main_model_part,throw_errors).Execute()
            #here we replace the dummy elements we read with proper elements
            if(self.main_model_part.ProcessInfo[KratosMultiphysics.DOMAIN_SIZE] == 3):
                self.settings.AddEmptyValue("element_replace_settings")
                self.settings["element_replace_settings"] = KratosMultiphysics.Parameters("""
                    {
                    "element_name":"CompressiblePotentialFlowElement3D4N",
                    "condition_name": "PotentialWallCondition3D3N"
                    }
                    """)
            elif(self.main_model_part.ProcessInfo[KratosMultiphysics.DOMAIN_SIZE] != 2):
                raise Exception("Domain size is not 2 or 3!!")
            
            print('self.settings["element_replace_settings"] =', self.settings["element_replace_settings"])
            KratosMultiphysics.ReplaceElementsAndConditionsProcess(self.main_model_part, self.settings["element_replace_settings"]).Execute()
            
        else:
            raise Exception("other input options are not yet implemented")
        
        current_buffer_size = self.main_model_part.GetBufferSize()
        if(self.GetMinimumBufferSize() > current_buffer_size):
            self.main_model_part.SetBufferSize( self.GetMinimumBufferSize() )
                
        print ("model reading finished")
        
    def GetMinimumBufferSize(self):
        return 2;
    
    def GetComputingModelPart(self):
        return self.main_model_part
        
    def GetOutputVariables(self):
        pass
        
    def ComputeDeltaTime(self):
        pass
        
    def SaveRestart(self):
        pass #one should write the restart file here
        
    def Solve(self):
        (self.solver).Solve()

        self.ComputeConditionNumber()

    def SetEchoLevel(self, level):
        (self.solver).SetEchoLevel(level)

    def Clear(self):
        (self.solver).Clear()

    def ComputeConditionNumber(self):
        NumberOfNodes = self.main_model_part.NumberOfNodes()
        self.work_dir = '/home/inigo/simulations/naca0012/07_salome/05_MeshRefinement/'
        #self.work_dir = '/home/inigo/simulations/naca0012/07_salome/06_Rectangle/'

        Size1 = self.solver.GetSystemMatrix()
        print('Size1 =',Size1.Size1())

        if(NumberOfNodes < 5.0e1):

            print('\nComputing condition number . . .\n')

            import eigen_solver_factory
            settings_max = KratosMultiphysics.Parameters("""
            {
                "solver_type"             : "power_iteration_highest_eigenvalue_solver",
                "max_iteration"           : 10000,
                "tolerance"               : 1e-9,
                "required_eigen_number"   : 1,
                "verbosity"               : 0,
                "linear_solver_settings"  : {
                    "solver_type"             : "SuperLUSolver",
                    "max_iteration"           : 500,
                    "tolerance"               : 1e-9,
                    "scaling"                 : false,
                    "verbosity"               : 0
                }
            }
            """)
            eigen_solver_max = eigen_solver_factory.ConstructSolver(settings_max)
            settings_min = KratosMultiphysics.Parameters("""
            {
                "solver_type"             : "power_iteration_eigenvalue_solver",
                "max_iteration"           : 10000,
                "tolerance"               : 1e-9,
                "required_eigen_number"   : 1,
                "verbosity"               : 0,
                "linear_solver_settings"  : {
                    "solver_type"             : "SuperLUSolver",
                    "max_iteration"           : 500,
                    "tolerance"               : 1e-9,
                    "scaling"                 : false,
                    "verbosity"               : 0
                }
            }
            """)

            eigen_solver_min = eigen_solver_factory.ConstructSolver(settings_min)
            condition_number = KratosMultiphysics.ConditionNumberUtility().GetConditionNumber(self.solver.GetSystemMatrix(), eigen_solver_max, eigen_solver_min)

            if(abs(condition_number - 1.0) < 1e-4):
                print('Singular System. Not able to compute Condition Number. Zero EigenValue')
                with open (self.work_dir + "mesh_refinement_loads.dat",'a') as loads_file:
                    loads_file.write('%16s' % ("Zero Eigen"))
                    loads_file.flush()

                with open (self.work_dir + "plots/results/all_cases.dat",'a') as all_cases_file:
                    all_cases_file.write('%16s' % ("Zero Eigen"))
                    all_cases_file.flush()

            else:
                print('condition_number = {:.2e}'.format(condition_number))

                with open (self.work_dir + "mesh_refinement_loads.dat",'a') as loads_file:
                    loads_file.write('{0:16.2e}'.format(condition_number))
                    loads_file.flush()

                with open (self.work_dir + "plots/results/all_cases.dat",'a') as all_cases_file:
                    all_cases_file.write('{0:16.2e}'.format(condition_number))
                    all_cases_file.flush()

                condition_results_file_name = self.work_dir + "plots/condition_number/data/condition/condition_results.dat"
                with open(condition_results_file_name,'a') as condition_file:
                    condition_file.write('{0:16.2e} {1:16.2e}\n'.format(NumberOfNodes, condition_number))
                    condition_file.flush()

            print('\nComputing condition number finished . . .\n')
        else:
            with open (self.work_dir + "mesh_refinement_loads.dat",'a') as loads_file:
                loads_file.write('%16s' % ("Not Comp."))
                loads_file.flush()

            with open (self.work_dir + "plots/results/all_cases.dat",'a') as all_cases_file:
                all_cases_file.write('%16s' % ("Not Comp."))
                all_cases_file.flush()



