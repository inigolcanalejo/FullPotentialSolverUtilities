# Note that this has to be on the path in order to work, or you manually specify the path
import kratos_io_utilities as kratos_utils
import global_utilities as global_utils
from math import log10, floor
import os

def round_to_1(x):
    return round(x, -int(floor(log10(abs(x)))))

Number_Of_Refinements = TBD
Number_Of_AOAS = TBD
Number_Of_Domains_Size = TBD

Initial_AOA = TBD
AOA_Increment = TBD

Initial_Airfoil_MeshSize = TBD
Airfoil_Refinement_Factor = TBD

Initial_FarField_MeshSize = TBD
FarField_Refinement_Factor = TBD

Initial_Domain_Size = TBD
Domain_Size_Factor = TBD


salome_output_path = 'TBD'
mdpa_path = 'TBD'

case = 0
Domain_Length = Initial_Domain_Size
Domain_Width = Initial_Domain_Size

for k in range(Number_Of_Domains_Size):
    Domain_Length = int(Domain_Length)
    Domain_Width = int(Domain_Width)
    FarField_MeshSize = int(Domain_Length / 50.0)
    AOA = Initial_AOA
    for j in range(Number_Of_AOAS):
        print('Writing mdpa...')
        Airfoil_MeshSize = Initial_Airfoil_MeshSize
        #FarField_MeshSize = Initial_FarField_MeshSize
        for i in range(Number_Of_Refinements):
            #round(Airfoil_MeshSize, 1)
            Airfoil_MeshSize = round_to_1(Airfoil_MeshSize)
            print('Domain_Size = ', Domain_Length, 'AOA = ', AOA, 'FarField_MeshSize = ', FarField_MeshSize, 'Airfoil_MeshSize', Airfoil_MeshSize)
            model = kratos_utils.MainModelPart() # Main mesh object to which we will add the submeshes (Kratos Name: ModelPart)

            # Specifying the names of the submeshes (Kratos Name: SubModelPart)
            smp_dict_fluid           = {"smp_name": "Parts_Parts_Auto1"}
            smp_dict_far_field       = {"smp_name": "PotentialWallCondition2D_Far_field_Auto1"}
            smp_dict_upper_surface   = {"smp_name": "Body2D_LeadingEdge"}
            smp_dict_lower_surface   = {"smp_name": "Body2D_TrailingEdge"}
            smp_dict_middle_surface   = {"smp_name": "Body2D_MiddleSurface"}
            smp_dict_body_surface   = {"smp_name": "Body2D_BodySurface"}

            file_name_fluid         = salome_output_path + '/Parts_Parts_Auto1_Case_' + str(case) + '_DS_' + str(Domain_Length) + '_AOA_' + str(
                AOA) + '_Far_Field_Mesh_Size_' + str(FarField_MeshSize) + '_Airfoil_Mesh_Size_' + str(Airfoil_MeshSize) + '.dat'
            file_name_far_field     = salome_output_path + '/PotentialWallCondition2D_Far_field_Auto1_Case_' + str(case) + '_DS_' + str(Domain_Length) + '_AOA_' + str(
                AOA) + '_Far_Field_Mesh_Size_' + str(FarField_MeshSize) + '_Airfoil_Mesh_Size_' + str(Airfoil_MeshSize) + '.dat'
            file_name_upper_surface = salome_output_path + '/Body2D_UpperSurface_Case_' + str(case) + '_DS_' + str(Domain_Length) + '_AOA_' + str(
                AOA) + '_Far_Field_Mesh_Size_' + str(FarField_MeshSize) + '_Airfoil_Mesh_Size_' + str(Airfoil_MeshSize) + '.dat'
            file_name_lower_surface = salome_output_path + '/Body2D_LowerSurface_Case_' + str(case) + '_DS_' + str(Domain_Length) + '_AOA_' + str(
                AOA) + '_Far_Field_Mesh_Size_' + str(FarField_MeshSize) + '_Airfoil_Mesh_Size_' + str(Airfoil_MeshSize) + '.dat'
            file_name_middle_surface = salome_output_path + '/Body2D_MiddleSurface_Case_' + str(case) + '_DS_' + str(Domain_Length) + '_AOA_' + str(
                AOA) + '_Far_Field_Mesh_Size_' + str(FarField_MeshSize) + '_Airfoil_Mesh_Size_' + str(Airfoil_MeshSize) + '.dat'
            file_name_body_surface = salome_output_path + '/Body2D_Surface_Case_' + str(case) + '_DS_' + str(Domain_Length) + '_AOA_' + str(
                AOA) + '_Far_Field_Mesh_Size_' + str(FarField_MeshSize) + '_Airfoil_Mesh_Size_' + str(Airfoil_MeshSize) + '.dat'

            def ReadDatFile(file_name):
                valid_file, nodes, geom_entities = global_utils.ReadAndParseSalomeDatFile(os.path.join(os.getcwd(),file_name))
                if not valid_file:
                    raise Exception("Invalid File!\n" + file_name)
                return nodes, geom_entities

            nodes_fluid,            geom_entities_fluid         = ReadDatFile(file_name_fluid)
            nodes_far_field,        geom_entities_far_field     = ReadDatFile(file_name_far_field)
            nodes_body_surface,     geom_entities_body_surface  = ReadDatFile(file_name_body_surface)
            nodes_upper_surface,    geom_entities_upper_surface = ReadDatFile(file_name_upper_surface)
            nodes_lower_surface,    geom_entities_lower_surface = ReadDatFile(file_name_lower_surface)
            nodes_middle_surface,   geom_entities_middle_surface = ReadDatFile(file_name_middle_surface)

            # Here we specify which Kratos-entities will be created from the general geometric entities
            mesh_dict_fluid         = {'write_smp': 1,
                                   'entity_creation': {203: {'Element': {'Element2D3N': '1'}}}}
            mesh_dict_far_field     = {'write_smp': 1,
                                   'entity_creation': {102: {'Condition': {'LineCondition2D2N': '0'}}}}
            mesh_dict_upper_surface = {'write_smp': 1,
                                   'entity_creation': {102: {'Condition': {'LineCondition2D2N': '0'}}}}
            mesh_dict_lower_surface = {'write_smp': 1,
                                   'entity_creation': {102: {'Condition': {'LineCondition2D2N': '0'}}}}
            mesh_dict_middle_surface = {'write_smp': 1,
                                   'entity_creation': {102: {'Condition': {'LineCondition2D2N': '0'}}}}
            mesh_dict_body_surface = {'write_smp': 1,
                                   'entity_creation': {102: {'Condition': {'LineCondition2D2N': '0'}}}}

            model.AddMesh(smp_dict_fluid,           mesh_dict_fluid,            nodes_fluid,            geom_entities_fluid)
            model.AddMesh(smp_dict_far_field,       mesh_dict_far_field,        nodes_far_field,        geom_entities_far_field)
            model.AddMesh(smp_dict_upper_surface,   mesh_dict_upper_surface,    nodes_upper_surface,    geom_entities_upper_surface)
            model.AddMesh(smp_dict_lower_surface,   mesh_dict_lower_surface,    nodes_lower_surface,    geom_entities_lower_surface)
            model.AddMesh(smp_dict_middle_surface,  mesh_dict_middle_surface,   nodes_middle_surface,   geom_entities_middle_surface)
            model.AddMesh(smp_dict_body_surface,    mesh_dict_body_surface,     nodes_body_surface,     geom_entities_body_surface)

            mdpa_info = "mdpa for demonstration purposes"
            mdpa_file_name = mdpa_path + '/naca0012_Case_' + str(case) + '_DS_' + str(Domain_Length) + '_AOA_' + str(
                AOA) + '_Far_Field_Mesh_Size_' + str(FarField_MeshSize) + '_Airfoil_Mesh_Size_' + str(Airfoil_MeshSize)



            model.WriteMesh(mdpa_file_name, mdpa_info)
            '''
            if(case % 2 == 0):
                Airfoil_Refinement_Factor_Effective = 2
            else:
                Airfoil_Refinement_Factor_Effective = 5
            '''
            Airfoil_MeshSize *= Airfoil_Refinement_Factor
            #FarField_MeshSize /= FarField_Refinement_Factor
            case += 1
        AOA += AOA_Increment
    Domain_Length *= Domain_Size_Factor
    Domain_Width *= Domain_Size_Factor
