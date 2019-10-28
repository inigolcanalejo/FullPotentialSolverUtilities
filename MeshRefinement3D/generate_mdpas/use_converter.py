# Note that this has to be on the path in order to work, or you manually specify the path
import kratos_io_utilities as kratos_utils
import global_utilities as global_utils
from math import log10, floor
import os

def round_to_1(x):
    return round(x, -int(floor(log10(abs(x)))))

# Parameters:
Wing_span = TBD
Domain_Length = 100
Domain_Height = Domain_Length
Domain_Width = 100

Smallest_Airfoil_Mesh_Size = TBD
Initial_Smallest_Airfoil_Mesh_Size = Smallest_Airfoil_Mesh_Size
Biggest_Airfoil_Mesh_Size = TBD
LE_Mesh_Size = Smallest_Airfoil_Mesh_Size
TE_Mesh_Size = Smallest_Airfoil_Mesh_Size
Far_Field_Mesh_Size = Domain_Length/10.0


Number_Of_AOAS = TBD
Number_Of_Domains_Refinements = TBD
Number_Of_Wing_Refinements = TBD

Initial_AOA = TBD
AOA_Increment = TBD

Initial_Growth_Rate_Wing = TBD
Growth_Rate_Wing_Refinement_Factor = TBD

Initial_Growth_Rate_Domain = TBD
Growth_Rate_Domain_Refinement_Factor = TBD

salome_output_path = 'TBD'
mdpa_path = 'TBD'

case = 0
AOA = Initial_AOA

for k in range(Number_Of_AOAS):
    AOA = round(AOA, 1)
    Growth_Rate_Domain = Initial_Growth_Rate_Domain
    for j in range(Number_Of_Domains_Refinements):
        Growth_Rate_Domain = round(Growth_Rate_Domain, 2)
        Growth_Rate_Wing = Initial_Growth_Rate_Wing
        Smallest_Airfoil_Mesh_Size = Initial_Smallest_Airfoil_Mesh_Size
        for i in range(Number_Of_Wing_Refinements):
            #round(Airfoil_MeshSize, 1)
            #Airfoil_MeshSize = round_to_1(Airfoil_MeshSize)
            Growth_Rate_Wing = round(Growth_Rate_Wing, 2)
            Smallest_Airfoil_Mesh_Size = round(Smallest_Airfoil_Mesh_Size, 3)
            print('Writing mdpa...')
            print('\n case = ', case, ' AOA = ', AOA, ' Growth_Rate_Domain = ', Growth_Rate_Domain, ' Growth_Rate_Wing = ', Growth_Rate_Wing)
            print('Smallest_Airfoil_Mesh_Size = ', Smallest_Airfoil_Mesh_Size)
            model = kratos_utils.MainModelPart() # Main mesh object to which we will add the submeshes (Kratos Name: ModelPart)

            # Specifying the names of the submeshes (Kratos Name: SubModelPart)
            smp_dict_fluid           = {"smp_name": "Parts_Parts_Auto1"}
            smp_dict_far_field       = {"smp_name": "PotentialWallCondition3D_Far_field_Auto1"}
            smp_dict_body_surface   = {"smp_name": "Body3D_Body_Auto1"}
            smp_dict_trailing_edge   = {"smp_name": "Wake3D_Wake_Auto1"}
            smp_dict_middle_airfoil   = {"smp_name": "Middle_Airfoil"}
            smp_dict_trefft_plane_cut   = {"smp_name": "Trefft_Plane_Cut"}

            file_name_fluid         = salome_output_path + '/Mesh_Domain_Case_' + str(case) + '_AOA_' + str(AOA) + '_Wing_Span_' + str(
              Wing_span) + '_Airfoil_Mesh_Size_' + str(Smallest_Airfoil_Mesh_Size) + '_Growth_Rate_Wing_' + str(
                Growth_Rate_Wing) + '_Growth_Rate_Domain_' + str(Growth_Rate_Domain) + '.dat'

            file_name_far_field     = salome_output_path + '/Sub-mesh_FarField_Case_' + str(case) + '_AOA_' + str(AOA) + '_Wing_Span_' + str(
              Wing_span) + '_Airfoil_Mesh_Size_' + str(Smallest_Airfoil_Mesh_Size) + '_Growth_Rate_Wing_' + str(
                Growth_Rate_Wing) + '_Growth_Rate_Domain_' + str(Growth_Rate_Domain) + '.dat'

            file_name_body_surface = salome_output_path + '/Sub-mesh_Wing_Case_' + str(case) + '_AOA_' + str(AOA) + '_Wing_Span_' + str(
              Wing_span) + '_Airfoil_Mesh_Size_' + str(Smallest_Airfoil_Mesh_Size) + '_Growth_Rate_Wing_' + str(
                Growth_Rate_Wing) + '_Growth_Rate_Domain_' + str(Growth_Rate_Domain) + '.dat'

            file_name_trailing_edge = salome_output_path + '/Sub-mesh_TE_Case_' + str(case) + '_AOA_' + str(AOA) + '_Wing_Span_' + str(
              Wing_span) + '_Airfoil_Mesh_Size_' + str(Smallest_Airfoil_Mesh_Size) + '_Growth_Rate_Wing_' + str(
                Growth_Rate_Wing) + '_Growth_Rate_Domain_' + str(Growth_Rate_Domain) + '.dat'

            file_name_middle_airfoil = salome_output_path + '/Sub_mesh_Middle_Airfoil_Case_' + str(case) + '_AOA_' + str(AOA) + '_Wing_Span_' + str(
              Wing_span) + '_Airfoil_Mesh_Size_' + str(Smallest_Airfoil_Mesh_Size) + '_Growth_Rate_Wing_' + str(
                Growth_Rate_Wing) + '_Growth_Rate_Domain_' + str(Growth_Rate_Domain) + '.dat'

            file_name_trefft_plane_cut = salome_output_path + '/Sub_mesh_Trefft_Plane_Cut_Case_' + str(case) + '_AOA_' + str(AOA) + '_Wing_Span_' + str(
              Wing_span) + '_Airfoil_Mesh_Size_' + str(Smallest_Airfoil_Mesh_Size) + '_Growth_Rate_Wing_' + str(
                Growth_Rate_Wing) + '_Growth_Rate_Domain_' + str(Growth_Rate_Domain) + '.dat'

            def ReadDatFile(file_name):
                valid_file, nodes, geom_entities = global_utils.ReadAndParseSalomeDatFile(os.path.join(os.getcwd(),file_name))
                if not valid_file:
                    print('Attention: Invalid File!\n' + file_name)
                    #raise Exception("Invalid File!\n" + file_name)
                return valid_file, nodes, geom_entities

            valid_file_fluid,           nodes_fluid,            geom_entities_fluid         = ReadDatFile(file_name_fluid)
            valid_file_far_field,       nodes_far_field,        geom_entities_far_field     = ReadDatFile(file_name_far_field)
            valid_file_body_surface,    nodes_body_surface,     geom_entities_body_surface  = ReadDatFile(file_name_body_surface)
            valid_file_trailing_edge,   nodes_trailing_edge,     geom_entities_trailing_edge  = ReadDatFile(file_name_trailing_edge)
            valid_file_middle_airfoil,  nodes_middle_airfoil,     geom_entities_middle_airfoil  = ReadDatFile(file_name_middle_airfoil)
            valid_file_trefft_plane_cut,  nodes_trefft_plane_cut,     geom_entities_trefft_plane_cut  = ReadDatFile(file_name_trefft_plane_cut)

            # Here we specify which Kratos-entities will be created from the general geometric entities
            mesh_dict_fluid         = {'write_smp': 1,
                                   'entity_creation': {304: {'Element': {'Element3D4N': '1'}}}}
            mesh_dict_far_field     = {'write_smp': 1,
                                   'entity_creation': {203: {'Condition': {'SurfaceCondition3D3N': '0'}}}}
            mesh_dict_body_surface = {'write_smp': 1,
                                   'entity_creation': {203: {'Condition': {'SurfaceCondition3D3N': '0'}}}}
            mesh_dict_trailing_edge = {'write_smp': 1,
                                   'entity_creation': {102: {'Condition': {'LineCondition2D2N': '0'}}}}
            mesh_dict_middle_airfoil = {'write_smp': 1,
                                   'entity_creation': {102: {'Condition': {'LineCondition2D2N': '0'}}}}
            mesh_dict_trefft_plane_cut = {'write_smp': 1,
                                   'entity_creation': {102: {'Condition': {'LineCondition2D2N': '0'}}}}

            model.AddMesh(smp_dict_fluid,           mesh_dict_fluid,            nodes_fluid,            geom_entities_fluid)
            model.AddMesh(smp_dict_far_field,       mesh_dict_far_field,        nodes_far_field,        geom_entities_far_field)
            model.AddMesh(smp_dict_body_surface,   mesh_dict_body_surface,    nodes_body_surface,    geom_entities_body_surface)
            model.AddMesh(smp_dict_trailing_edge,   mesh_dict_trailing_edge,    nodes_trailing_edge,    geom_entities_trailing_edge)
            if valid_file_middle_airfoil:
                model.AddMesh(smp_dict_middle_airfoil,   mesh_dict_middle_airfoil,    nodes_middle_airfoil,    geom_entities_middle_airfoil)
            if valid_file_trefft_plane_cut:
                model.AddMesh(smp_dict_trefft_plane_cut,   mesh_dict_trefft_plane_cut,    nodes_trefft_plane_cut,    geom_entities_trefft_plane_cut)

            mdpa_info = "mdpa for demonstration purposes"
            mdpa_file_name = mdpa_path + '/wing_Case_' + str(case) + '_AOA_' + str(AOA) + '_Wing_Span_' + str(
              Wing_span) + '_Airfoil_Mesh_Size_' + str(Smallest_Airfoil_Mesh_Size) + '_Growth_Rate_Wing_' + str(
                Growth_Rate_Wing) + '_Growth_Rate_Domain_' + str(Growth_Rate_Domain)

            model.WriteMesh(mdpa_file_name, mdpa_info)

            #Growth_Rate_Wing -= Growth_Rate_Wing_Refinement_Factor
            Growth_Rate_Wing /= Growth_Rate_Wing_Refinement_Factor
            Smallest_Airfoil_Mesh_Size /= 2.0
            case +=1
        Growth_Rate_Domain /= Growth_Rate_Domain_Refinement_Factor
    AOA += AOA_Increment
