# Note that this has to be on the path in order to work, or you manually specify the path
import kratos_io_utilities as kratos_utils
import global_utilities as global_utils
from math import log10, floor
import os

def round_to_1(x):
    return round(x, -int(floor(log10(abs(x)))))

script_path = os.path.dirname(os.path.realpath(__file__))
salome_output_path = script_path + '/salome_output'
mdpa_path = script_path + '/case'


print('Writing mdpa...')
model = kratos_utils.MainModelPart() # Main mesh object to which we will add the submeshes (Kratos Name: ModelPart)

# Specifying the names of the submeshes (Kratos Name: SubModelPart)
smp_dict_fluid           = {"smp_name": "Parts_Parts_Auto1"}
smp_dict_far_field       = {"smp_name": "PotentialWallCondition3D_Far_field_Auto1"}
smp_dict_body_surface   = {"smp_name": "Body3D_Body_Auto1"}
smp_dict_trailing_edge   = {"smp_name": "Wake3D_Wake_Auto1"}

file_name_fluid         = salome_output_path + '/Mesh_Domain.dat'
file_name_far_field     = salome_output_path + '/Sub-mesh_FarField.dat'
file_name_body_surface = salome_output_path + '/Sub-mesh_Wing.dat'
file_name_trailing_edge = salome_output_path + '/Sub-mesh_TE.dat'

def ReadDatFile(file_name):
    valid_file, nodes, geom_entities = global_utils.ReadAndParseSalomeDatFile(os.path.join(os.getcwd(),file_name))
    if not valid_file:
        raise Exception("Invalid File!\n" + file_name)
    return nodes, geom_entities

nodes_fluid,            geom_entities_fluid         = ReadDatFile(file_name_fluid)
nodes_far_field,        geom_entities_far_field     = ReadDatFile(file_name_far_field)
nodes_body_surface,     geom_entities_body_surface  = ReadDatFile(file_name_body_surface)
nodes_trailing_edge,     geom_entities_trailing_edge  = ReadDatFile(file_name_trailing_edge)

# Here we specify which Kratos-entities will be created from the general geometric entities
mesh_dict_fluid         = {'write_smp': 1,
                       'entity_creation': {304: {'Element': {'Element3D4N': '1'}}}}
mesh_dict_far_field     = {'write_smp': 1,
                       'entity_creation': {203: {'Condition': {'SurfaceCondition3D3N': '0'}}}}
mesh_dict_body_surface = {'write_smp': 1,
                       'entity_creation': {203: {'Condition': {'SurfaceCondition3D3N': '0'}}}}
mesh_dict_trailing_edge = {'write_smp': 1,
                       'entity_creation': {102: {'Condition': {'LineCondition2D2N': '0'}}}}

model.AddMesh(smp_dict_fluid,           mesh_dict_fluid,            nodes_fluid,            geom_entities_fluid)
model.AddMesh(smp_dict_far_field,       mesh_dict_far_field,        nodes_far_field,        geom_entities_far_field)
model.AddMesh(smp_dict_body_surface,   mesh_dict_body_surface,    nodes_body_surface,    geom_entities_body_surface)
model.AddMesh(smp_dict_trailing_edge,   mesh_dict_trailing_edge,    nodes_trailing_edge,    geom_entities_trailing_edge)

mdpa_info = "mdpa for demonstration purposes"
mdpa_file_name = mdpa_path + '/salome_wing'

model.WriteMesh(mdpa_file_name, mdpa_info)
