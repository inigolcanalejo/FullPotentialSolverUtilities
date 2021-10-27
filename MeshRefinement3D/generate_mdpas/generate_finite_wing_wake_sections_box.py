# -*- coding: utf-8 -*-

###
### This file is generated automatically by SALOME v8.4.0 with dump python functionality
###
import os
import killSalome
import math

# Parameters:
Wing_span = TBD
Domain_Length = 1000
Domain_Height = Domain_Length
Domain_Width = 1000
wake_angle_deg = 0.0

Smallest_Airfoil_Mesh_Size = TBD
Biggest_Airfoil_Mesh_Size = TBD
Wing_Tip_Mesh_Size = Smallest_Airfoil_Mesh_Size# * 5.0
Root_Mesh_Size = Biggest_Airfoil_Mesh_Size * 1.0
Fuselage_Mesh_Size = 0.5
Engine_Trailing_Edge_Size = 0.03
Engine_Mesh_Size = 0.05
Growth_Rate_Engine = 0.1
LE_Mesh_Size = Smallest_Airfoil_Mesh_Size
TE_Mesh_Size = Smallest_Airfoil_Mesh_Size
Far_Field_Mesh_Size = Domain_Length/20.0

print 'Domain_Length = ', Domain_Length
print 'Smallest_Airfoil_Mesh_Size = ', Smallest_Airfoil_Mesh_Size
print 'Biggest_Airfoil_Mesh_Size = ', Biggest_Airfoil_Mesh_Size
print 'Fuselage_Mesh_Size = ', Fuselage_Mesh_Size
print 'Engine_Mesh_Size = ', Engine_Mesh_Size
print 'Far_Field_Mesh_Size = ', Far_Field_Mesh_Size

Number_Of_AOAS = TBD
Number_Of_Domains_Refinements = TBD
Number_Of_Wing_Refinements = TBD

Initial_AOA = TBD
AOA_Increment = TBD

Initial_Growth_Rate_Wing = TBD
Growth_Rate_Wing_Refinement_Factor = TBD

Initial_Growth_Rate_Domain = TBD
Growth_Rate_Domain_Refinement_Factor = TBD

Refinement_Box_Face_Mesh_Size = 0.1
Growth_Rate_Refinement_Box = 0.1
Growth_Rate_Far_Field = 0.2

salome_output_path = 'TBD'
mdpa_path = 'TBD'
if not os.path.exists(salome_output_path):
    os.makedirs(salome_output_path)
if not os.path.exists(mdpa_path):
    os.makedirs(mdpa_path)

case = 0
AOA = Initial_AOA

Initial_Smallest_Airfoil_Mesh_Size = Smallest_Airfoil_Mesh_Size
Initial_Biggest_Airfoil_Mesh_Size = Biggest_Airfoil_Mesh_Size

geometry_path = "/media/inigo/10740FB2740F9A1C/Results/15_nasa_crm/99_wing_body_nacelle_pylon_tail/05_model_gid/23_geometry_for_salome_nacelle3.igs"

trailing_edge_path = "/media/inigo/10740FB2740F9A1C/Results/15_nasa_crm/05_trailing_edge/trailing_edges_delete_tip.igs"

for k in range(Number_Of_AOAS):
    AOA = round(AOA, 1)
    Growth_Rate_Domain = Initial_Growth_Rate_Domain
    for j in range(Number_Of_Domains_Refinements):
        Growth_Rate_Domain = round(Growth_Rate_Domain, 2)
        Growth_Rate_Wing = Initial_Growth_Rate_Wing
        Smallest_Airfoil_Mesh_Size = Initial_Smallest_Airfoil_Mesh_Size
        Biggest_Airfoil_Mesh_Size = Initial_Biggest_Airfoil_Mesh_Size
        for i in range(Number_Of_Wing_Refinements):
            Growth_Rate_Wing = round(Growth_Rate_Wing, 2)
            Smallest_Airfoil_Mesh_Size = round(Smallest_Airfoil_Mesh_Size, 4)
            Biggest_Airfoil_Mesh_Size = round(Biggest_Airfoil_Mesh_Size, 3)
            print '\n case = ', case, ' AOA = ', AOA, ' Growth_Rate_Domain = ', Growth_Rate_Domain, ' Growth_Rate_Wing = ', Growth_Rate_Wing
            print 'Smallest_Airfoil_Mesh_Size = ', Smallest_Airfoil_Mesh_Size, ' Biggest_Airfoil_Mesh_Size = ', Biggest_Airfoil_Mesh_Size

            #'''
            import sys
            import salome

            salome.salome_init()
            theStudy = salome.myStudy

            import salome_notebook
            notebook = salome_notebook.NoteBook(theStudy)

            import os
            script_path = os.path.dirname(os.path.realpath(__file__))

            ###
            ### GEOM component
            ###

            import GEOM
            from salome.geom import geomBuilder
            import math
            import SALOMEDS

            import time as time
            print(' Starting geometry ')
            start_time = time.time()

            geompy = geomBuilder.New(theStudy)

            # Create origin and axis
            O = geompy.MakeVertex(0, 0, 0)
            OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
            OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
            OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)

            nasa_crm_igs = geompy.ImportIGES(geometry_path, True)



            [Face_Inlet,\
            Face_crm_cockpit,\
            Face_crm_fuselage_middle_down,\
            Face_crm_fuselage_middle_middle,\
            Face_crm_fuselage_middle_up,\
            Face_crm_engine_1,\
            Face_crm_engine_2,\
            Face_crm_engine_3,\
            Face_crm_engine_4,\
            Face_crm_engine_5,\
            Face_crm_engine_6,\
            Face_crm_pylon_1,\
            Face_crm_pylon_2,\
            Face_crm_engine_7,\
            Face_crm_engine_8,\
            Face_crm_engine_9,\
            Face_crm_engine_10,\
            Face_crm_engine_11,\
            Face_crm_engine_12,\
            Face_crm_pylon_3,\
            Face_crm_pylon_4,\
            Face_crm_fuselage_root_down,\
            Face_crm_engine_outlet_1,\
            Face_crm_engine_outlet_2,\
            Face_crm_pylon_5,\
            Face_crm_fuselage_root_down_down,\
            Face_crm_engine_outlet_3,\
            Face_crm_pylon_6,\
            Face_crm_engine_outlet_4,\
            Face_crm_pylon_7,\
            Face_crm_pylon_8,\
            Face_crm_fuselage_root_up_up,\
            Face_crm_pylon_9,\
            Face_crm_pylon_10,\
            Face_crm_wing_root_down,\
            Face_crm_wing_root_up,\
            Face_crm_pylon_11,\
            Face_crm_pylon_12,\
            Face_crm_pylon_13,\
            Face_crm_pylon_14,\
            Face_Left_Wall,\
            Face_crm_fuselage_root_up,\
            Face_crm_pylon_15,\
            Face_crm_pylon_16,\
            Face_crm_wing_root_down2,\
            Face_crm_wing_root_te, \
            Face_crm_wing_down, \
            Face_crm_wing_up,\
            Face_crm_fuselage_ring_up,\
            Face_crm_fuselage_ring_down,\
            Face_crm_fuselage_ring_middle,
            Face_crm_wing_te,\
            Face_crm_wing_tip_down,\
            Face_crm_wing_tip_up,\
            Face_crm_wing_tip_te,\
            Face_crm_fuselage_back,\
            Face_Down_Wall,\
            Face_Top_Wall,\
            Face_crm_tail_down,\
            Face_crm_tail_up,\
            Face_crm_tail_te,\
            Face_crm_tail_tip_le_down,\
            Face_crm_tail_tip_le_up,\
            Face_crm_tail_tip_te_down,\
            Face_crm_tail_tip_te_up,\
            Face_Right_Wall,\
            Face_Outlet] = geompy.ExtractShapes(nasa_crm_igs, geompy.ShapeType["FACE"], True)

            # Exploding far field
            [Edge_1,Edge_2,Edge_3,Edge_4] = geompy.ExtractShapes(Face_Inlet, geompy.ShapeType["EDGE"], True)
            [Obj1,Obj2,Obj3,Obj4,Obj5,Obj6,Obj7,Edge_5,Edge_6,Obj10,Obj11,Obj12,Obj13,Obj14,Obj15] = geompy.ExtractShapes(Face_Left_Wall, geompy.ShapeType["EDGE"], True)
            [Obj1,Edge_7,Edge_8,Obj2] = geompy.ExtractShapes(Face_Right_Wall, geompy.ShapeType["EDGE"], True)
            [Edge_9,Edge_10,Edge_11,Edge_12] = geompy.ExtractShapes(Face_Outlet, geompy.ShapeType["EDGE"], True)

            ######
            # Explode nasa crm
            ######
            # Fuselage
            [Edge_105,Edge_106,Edge_107,Edge_108,Edge_109,Edge_110] = geompy.ExtractShapes(Face_crm_cockpit, geompy.ShapeType["EDGE"], True)
            [Obj1,Edge_112,Edge_113,Edge_114,Edge_115] = geompy.ExtractShapes(Face_crm_fuselage_middle_down, geompy.ShapeType["EDGE"],           True)
            [Obj1,Obj2,Edge_118,Edge_119,Edge_220] = geompy.ExtractShapes(Face_crm_fuselage_middle_middle, geompy.ShapeType["EDGE"], True)
            [Obj1,Edge_121,Obj2,Edge_123] = geompy.ExtractShapes(Face_crm_fuselage_middle_up, geompy.ShapeType["EDGE"], True)
            [Obj1,Obj2,Edge_127,Obj3,Edge_129,Obj4,Obj5,Obj6,Edge_133] = geompy.ExtractShapes(Face_crm_fuselage_root_down, geompy.ShapeType["EDGE"], True)
            [Obj1,Obj2,Edge_136,Edge_137] = geompy.ExtractShapes(Face_crm_fuselage_root_down_down, geompy.ShapeType["EDGE"], True)
            [Obj1,Edge_139,Edge_140,Edge_141,Edge_142] = geompy.ExtractShapes(Face_crm_fuselage_root_up_up, geompy.ShapeType["EDGE"], True)

            # Wing-Root
            [Edge_wing_root_down_le,Edge_wing_root_le, Edge_wing_transition_1, Edge_wing_hole_1, Edge_wing_root_te_down,Edge_wing_hole_2,Edge_wing_root_down_te,Edge_wing_transition_2] = geompy.ExtractShapes(Face_crm_wing_root_down, geompy.ShapeType["EDGE"],             True)

            [Obj1,Edge_wing_root_le2, Edge_wing_hole_3, Edge_wing_middle_down_le,Edge_wing_hole_4,Edge_wing_middle_down_te,Obj2,Edge_wing_root_down_te2] = geompy.ExtractShapes(Face_crm_wing_root_down2, geompy.ShapeType["EDGE"],             True)

            [Obj1,Edge_wing_root_up_le,Obj2,Edge_wing_middle_up_le,Edge_wing_root_up_te,Edge_wing_middle_up_te,Edge_wing_root_te_up] = geompy.ExtractShapes(Face_crm_wing_root_up, geompy.ShapeType["EDGE"],           True)

            # Fuselage-root-up
            [Obj1,Obj2,Obj3,Obj4,Obj5,Obj6,Obj7,Edge_177,Edge_178,Edge_179] = geompy.ExtractShapes(Face_crm_fuselage_root_up, geompy.ShapeType["EDGE"], True)

            # Wing
            [Edge_root_te_down,Edge_root_te_up,Obj1,Obj2,Obj3,Edge_wing_middle_te] = geompy.ExtractShapes(Face_crm_wing_root_te, geompy.ShapeType["EDGE"], True)
            [Obj1,Obj2,Edge_wing_le,Edge_wing_te_down,Edge_wing_tip_down_le,Edge_wing_tip_down_te] = geompy.ExtractShapes(Face_crm_wing_down, geompy.ShapeType["EDGE"], True)
            [Obj1,Obj2,Obj3,Edge_wing_te_up,Edge_wing_tip_up_le,Edge_wing_tip_up_te] = geompy.ExtractShapes(Face_crm_wing_up, geompy.ShapeType["EDGE"], True)

            # Fuselage
            [Obj1,Edge_192,Edge_193,Edge_194] = geompy.ExtractShapes(Face_crm_fuselage_ring_up, geompy.ShapeType["EDGE"], True)
            [Obj1,Obj2,Edge_197,Obj3,Edge_199,Edge_1100] = geompy.ExtractShapes(Face_crm_fuselage_ring_down, geompy.ShapeType         ["EDGE"], True)
            [Obj1,Obj2,Obj3,Edge_1104] = geompy.ExtractShapes(Face_crm_fuselage_ring_middle, geompy.ShapeType["EDGE"], True)

            # Wing te and tip
            [Obj1,Obj2,Obj3,Edge_wing_tip_te1] = geompy.ExtractShapes(Face_crm_wing_te, geompy.ShapeType["EDGE"], True)
            [Obj1,Edge_wing_tip_middle_le,Obj2,Edge_wing_tip_middle_te,Edge_wing_tip_te2] = geompy.ExtractShapes(Face_crm_wing_tip_down, geompy.ShapeType["EDGE"], True)
            [Obj1,Obj2,Obj3,Obj4,Edge_wing_tip_te3] = geompy.ExtractShapes(Face_crm_wing_tip_up, geompy.ShapeType["EDGE"], True)
            [Edge_1119,Obj1,Obj2,Obj3] = geompy.ExtractShapes(Face_crm_wing_tip_te, geompy.ShapeType["EDGE"], True)

            # Fuselage back
            [Obj1,Obj2,Obj3,Edge_1126,Edge_1127,Obj4,Obj5,Obj6,Obj7,Obj8,Edge_1133] = geompy.ExtractShapes         (Face_crm_fuselage_back, geompy.ShapeType["EDGE"], True)

            # Tail
            [Edge_tail_root_down_le,Edge_tail_root_down_te,Edge_tail_le,Edge_tail_te_down,Edge_tail_tip_down_le,Edge_tail_tip_down_te] = geompy.ExtractShapes(Face_crm_tail_down, geompy.ShapeType["EDGE"],            True)
            [Edge_tail_root_up_le,Edge_tail_root_up_te,Obj1,Edge_tail_te_up,Edge_tail_tip_up_le,Edge_tail_tip_up_te] = geompy.ExtractShapes(Face_crm_tail_up, geompy.ShapeType["EDGE"],          True)
            [Edge_tail_root_te,Obj1,Obj2,Edge_tail_tip_te_down,Edge_tail_tip_te_up] = geompy.ExtractShapes(Face_crm_tail_te, geompy.ShapeType["EDGE"], True)

            # Tail tip
            [Obj1,Edge_tail_tip_middle_le,Edge_tail_tip_middle_down] = geompy.ExtractShapes(Face_crm_tail_tip_le_down, geompy.ShapeType["EDGE"], True)
            [Obj1,Obj2,Edge_tail_tip_middle_up] = geompy.ExtractShapes(Face_crm_tail_tip_le_up, geompy.ShapeType["EDGE"], True)
            [Obj1,Obj2,Edge_tail_tip_middle_te,Obj3] = geompy.ExtractShapes(Face_crm_tail_tip_te_down, geompy.ShapeType["EDGE"], True)

            # Explode Engine
            [Edge_301,Edge_302,Edge_303,Edge_304] = geompy.ExtractShapes(Face_crm_engine_1, geompy.ShapeType["EDGE"], True)
            [Obj1,Edge_306,Edge_307,Edge_308] = geompy.ExtractShapes(Face_crm_engine_2, geompy.ShapeType["EDGE"], True)

            [Edge_309,Obj1,Obj2,Edge_312] = geompy.ExtractShapes(Face_crm_engine_3, geompy.ShapeType["EDGE"], True)

            [Obj1,Obj2,Obj3,Edge_316] = geompy.ExtractShapes(Face_crm_engine_4, geompy.ShapeType["EDGE"], True)
            [Obj1,Edge_318,Edge_319,Edge_320,Edge_321] = geompy.ExtractShapes(Face_crm_engine_5, geompy.ShapeType["EDGE"], True)

            [Obj1,Obj2,Obj3,Edge_325,Edge_326] = geompy.ExtractShapes(Face_crm_engine_6, geompy.ShapeType["EDGE"], True)
            [Obj1,Edge_328,Edge_329,Edge_330,Edge_331] = geompy.ExtractShapes(Face_crm_engine_7, geompy.ShapeType["EDGE"], True)

            [Obj1,Obj2,Obj3,Edge_335,Edge_336] = geompy.ExtractShapes(Face_crm_engine_8, geompy.ShapeType["EDGE"], True)
            [Obj1,Edge_338,Edge_339,Edge_340] = geompy.ExtractShapes(Face_crm_engine_9, geompy.ShapeType["EDGE"], True)

            [Obj1,Obj2,Edge_343,Edge_344] = geompy.ExtractShapes(Face_crm_engine_10, geompy.ShapeType["EDGE"], True)
            [Obj1,Edge_346,Edge_347,Edge_348,Edge_349] = geompy.ExtractShapes(Face_crm_engine_11, geompy.ShapeType["EDGE"], True)

            [Obj1,Obj2,Edge_352,Edge_353,Edge_354] = geompy.ExtractShapes(Face_crm_engine_12, geompy.ShapeType["EDGE"], True)
            [Edge_500,Obj1,Obj2,Edge_501] = geompy.ExtractShapes(Face_crm_engine_outlet_1, geompy.ShapeType["EDGE"], True)
            [Obj1,Obj2,Obj3,Obj4,Obj5,Edge_502] = geompy.ExtractShapes(Face_crm_engine_outlet_2, geompy.ShapeType["EDGE"], True)
            [Obj1,Obj2,Obj3,Edge_503] = geompy.ExtractShapes(Face_crm_engine_outlet_3, geompy.ShapeType["EDGE"], True)


            # Explode pylon
            [Obj1,Edge_356,Edge_357] = geompy.ExtractShapes(Face_crm_pylon_1, geompy.ShapeType["EDGE"], True)
            [Obj1,Obj2,Edge_360] = geompy.ExtractShapes(Face_crm_pylon_2, geompy.ShapeType["EDGE"], True)

            [Obj1,Obj2,Edge_363,Edge_364,Edge_365] = geompy.ExtractShapes(Face_crm_pylon_3, geompy.ShapeType["EDGE"], True)
            [Obj1,Obj2,Obj3,Edge_369,Edge_370] = geompy.ExtractShapes(Face_crm_pylon_4, geompy.ShapeType["EDGE"], True)

            [Edge_371,Edge_372,Edge_373] = geompy.ExtractShapes(Face_crm_pylon_5, geompy.ShapeType["EDGE"], True)
            [Edge_374,Edge_375,Edge_376] = geompy.ExtractShapes(Face_crm_pylon_6, geompy.ShapeType["EDGE"], True)

            [Obj1,Obj2,Obj3,Edge_380,Edge_381] = geompy.ExtractShapes(Face_crm_pylon_7, geompy.ShapeType["EDGE"], True)
            [Obj1,Obj2,Obj3,Edge_385,Edge_386] = geompy.ExtractShapes(Face_crm_pylon_8, geompy.ShapeType["EDGE"], True)

            [Edge_387,Obj2,Obj1,Edge_390] = geompy.ExtractShapes(Face_crm_pylon_9, geompy.ShapeType["EDGE"], True)
            [Obj1,Obj2,Obj3,Edge_394] = geompy.ExtractShapes(Face_crm_pylon_10, geompy.ShapeType["EDGE"], True)

            [Edge_395,Obj1,Obj2,Edge_398,Edge_399] = geompy.ExtractShapes(Face_crm_pylon_11, geompy.ShapeType["EDGE"], True)
            [Edge_400,Obj1,Obj2,Obj3,Edge_404] = geompy.ExtractShapes(Face_crm_pylon_12, geompy.ShapeType["EDGE"], True)

            [Obj1,Obj2,Edge_407,Edge_408] = geompy.ExtractShapes(Face_crm_pylon_13, geompy.ShapeType["EDGE"], True)
            [Obj1,Obj2,Edge_411,Obj3] = geompy.ExtractShapes(Face_crm_pylon_14, geompy.ShapeType["EDGE"], True)
            [Obj1,Obj2,Obj3,Edge_416] = geompy.ExtractShapes(Face_crm_pylon_15, geompy.ShapeType["EDGE"], True)


            # Making groups for submeshes
            # LE and TE edges
            Auto_group_for_Sub_mesh_LE_TE_Edges = geompy.CreateGroup(nasa_crm_igs, geompy.ShapeType["EDGE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_LE_TE_Edges, [Edge_wing_root_le,Edge_wing_root_le2,Edge_wing_root_down_te,Edge_wing_root_down_te2,Edge_wing_root_te_up,Edge_root_te_down,Edge_root_te_up,Edge_wing_middle_te,Edge_wing_le,Edge_wing_te_down,Edge_wing_te_up,Edge_wing_tip_te1,Edge_wing_tip_te2,Edge_wing_tip_te3,Edge_tail_le,Edge_tail_te_down,Edge_tail_te_up,Edge_tail_root_te,Edge_tail_tip_te_down,Edge_tail_tip_te_up,Edge_1119])

            # Airfoils' edges
            Auto_group_for_Sub_mesh_Airfoil_Edges = geompy.CreateGroup(nasa_crm_igs, geompy.ShapeType["EDGE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Airfoil_Edges, [Edge_wing_root_down_le,Edge_wing_middle_down_le,Edge_wing_root_te_down,Edge_wing_middle_down_te,Edge_wing_root_up_le,Edge_wing_middle_up_le,Edge_wing_root_up_te,Edge_wing_middle_up_te,Edge_tail_root_down_le,Edge_tail_root_down_te,Edge_tail_root_up_le,Edge_tail_root_up_te])

            # Tip airfoils' edges
            Auto_group_for_Sub_mesh_Tip_Airfoil_Edges = geompy.CreateGroup(nasa_crm_igs, geompy.ShapeType["EDGE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Tip_Airfoil_Edges, [Edge_wing_tip_down_le,Edge_wing_tip_down_te,Edge_wing_tip_up_le,Edge_wing_tip_up_te,Edge_tail_tip_down_le,Edge_tail_tip_down_te,Edge_tail_tip_up_le,Edge_tail_tip_up_te,Edge_tail_tip_middle_le,Edge_tail_tip_middle_te,Edge_wing_tip_middle_le,Edge_wing_tip_middle_te])

            # Tip middle edges
            Auto_group_for_Sub_mesh_Tip_Middle_Edges = geompy.CreateGroup(nasa_crm_igs, geompy.ShapeType["EDGE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Tip_Middle_Edges, [Edge_tail_tip_middle_down,Edge_tail_tip_middle_up])

            # Wing hole
            Auto_group_for_Sub_mesh_Wing_Hole_Edges = geompy.CreateGroup(nasa_crm_igs, geompy.ShapeType["EDGE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Wing_Hole_Edges, [Edge_wing_hole_2,Edge_wing_hole_4])

            # Engine edges
            Auto_group_for_Sub_mesh_Engine_Outlet_Edges = geompy.CreateGroup(nasa_crm_igs, geompy.ShapeType["EDGE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Engine_Outlet_Edges, [Edge_330,Edge_331,Edge_335,Edge_336,Edge_348,Edge_349,Edge_353,Edge_354,Edge_500,Edge_501,Edge_502,Edge_503,Edge_395,Edge_400,Edge_371,Edge_372,Edge_373,Edge_374,Edge_375,Edge_376])

            Auto_group_for_Sub_mesh_Engine_Transition_Edges = geompy.CreateGroup(nasa_crm_igs, geompy.ShapeType["EDGE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Engine_Transition_Edges, [Edge_398,Edge_352,Edge_346,Edge_347,Edge_328,Edge_329,Edge_380,Edge_385])

            Auto_group_for_Sub_mesh_Pylon_Edges = geompy.CreateGroup(nasa_crm_igs, geompy.ShapeType["EDGE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Pylon_Edges, [Edge_387])

            Auto_group_for_Sub_mesh_Pylon_Transition_Edges = geompy.CreateGroup(nasa_crm_igs, geompy.ShapeType["EDGE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Pylon_Transition_Edges, [Edge_363,Edge_365,Edge_370])

            Auto_group_for_Sub_mesh_Engine_Edges = geompy.CreateGroup(nasa_crm_igs, geompy.ShapeType["EDGE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Engine_Edges, [Edge_301,Edge_302,Edge_303,Edge_304,Edge_306,Edge_307,Edge_308,Edge_309,Edge_312,Edge_316,Edge_318,Edge_319,Edge_320,Edge_321,Edge_325,Edge_326,Edge_338,Edge_339,Edge_340,Edge_343,Edge_344,Edge_356,Edge_357,Edge_360,Edge_364,Edge_369,Edge_381,Edge_386,Edge_390,Edge_394,Edge_399,Edge_404,Edge_407,Edge_408,Edge_411,Edge_416])

            # Wing and tail surfaces
            # Auto_group_for_Sub_mesh_Wing_Tail_Surfaces = geompy.CreateGroup(nasa_crm_igs, geompy.ShapeType["FACE"])
            # geompy.UnionList(Auto_group_for_Sub_mesh_Wing_Tail_Surfaces, [Face_crm_wing_root_down])

            Auto_group_for_Sub_mesh_Wing_Tail_Surfaces = geompy.CreateGroup(nasa_crm_igs, geompy.ShapeType["FACE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Wing_Tail_Surfaces, [Face_crm_tail_down,Face_crm_tail_up])

            Auto_group_for_Sub_mesh_Wing_Surfaces = geompy.CreateGroup(nasa_crm_igs, geompy.ShapeType["FACE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Wing_Surfaces, [Face_crm_wing_root_down,Face_crm_wing_root_up,Face_crm_wing_down,Face_crm_wing_up,Face_crm_wing_tip_down,Face_crm_wing_tip_up])

            # Trailing edge surfaces
            Auto_group_for_Sub_mesh_Wing_Tail_Tip_Surfaces = geompy.CreateGroup(nasa_crm_igs, geompy.ShapeType["FACE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Wing_Tail_Tip_Surfaces, [Face_crm_wing_tip_down,Face_crm_wing_tip_up,Face_crm_tail_tip_le_down,Face_crm_tail_tip_le_up,Face_crm_tail_tip_te_down,Face_crm_tail_tip_te_up])

            # Trailing edge surfaces
            Auto_group_for_Sub_mesh_Trailing_Edge_Surfaces = geompy.CreateGroup(nasa_crm_igs, geompy.ShapeType["FACE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Trailing_Edge_Surfaces, [Face_crm_wing_root_te,Face_crm_wing_te,Face_crm_wing_tip_te,Face_crm_tail_te,Face_crm_engine_outlet_1,Face_crm_engine_outlet_2,Face_crm_engine_outlet_3,Face_crm_engine_outlet_4,Face_crm_pylon_5,Face_crm_pylon_6])

            # Engine surfaces
            Auto_group_for_Sub_mesh_Engine_Surfaces = geompy.CreateGroup(nasa_crm_igs, geompy.ShapeType["FACE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Engine_Surfaces, [Face_crm_engine_1,Face_crm_engine_2,Face_crm_engine_3,Face_crm_engine_4,Face_crm_engine_9,Face_crm_engine_10,Face_crm_pylon_7,Face_crm_pylon_8,Face_crm_pylon_11,Face_crm_pylon_12,Face_crm_pylon_13,Face_crm_pylon_14,Face_crm_pylon_15,Face_crm_pylon_16])

            Auto_group_for_Sub_mesh_Engine_Outlet_Surfaces = geompy.CreateGroup(nasa_crm_igs, geompy.ShapeType["FACE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Engine_Outlet_Surfaces, [Face_crm_engine_outlet_1,Face_crm_engine_outlet_2,Face_crm_engine_outlet_3,Face_crm_engine_outlet_4,Face_crm_pylon_5,Face_crm_pylon_6])

            # All fuselage edges
            # Fuselage edges all
            Auto_group_for_Sub_mesh_Fuselage_Edges = geompy.CreateGroup(nasa_crm_igs, geompy.ShapeType["EDGE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Fuselage_Edges, [Edge_105,Edge_106,Edge_107,Edge_108,Edge_109,Edge_110,Edge_113,Edge_121,Edge_129,Edge_192,Edge_194,Edge_1100,Edge_1104,Edge_220,Edge_133,Edge_136,Edge_137,Edge_139,Edge_140,Edge_141,Edge_142,Edge_178,Edge_179, Edge_112,Edge_115,Edge_118,Edge_123,Edge_193,Edge_197,Edge_199,Edge_1126,Edge_1127, Edge_114,Edge_119,Edge_140, Edge_1133])

            # Fuselage transition edges
            Auto_group_for_Sub_mesh_Fuselage_Transition_Edges = geompy.CreateGroup(nasa_crm_igs, geompy.ShapeType["EDGE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Fuselage_Transition_Edges, [Edge_127])

            '''
            # # Fuselage edges
            # Auto_group_for_Sub_mesh_Fuselage_Edges = geompy.CreateGroup(nasa_crm_igs, geompy.ShapeType["EDGE"])
            # geompy.UnionList(Auto_group_for_Sub_mesh_Fuselage_Edges, [Edge_105,Edge_106,Edge_107,Edge_108,Edge_109,Edge_110,Edge_113,Edge_121,Edge_129,Edge_192,Edge_194,Edge_1100,Edge_1104])

            # # Fuselage transition edges
            # Auto_group_for_Sub_mesh_Fuselage_Transition_Edges = geompy.CreateGroup(nasa_crm_igs, geompy.ShapeType["EDGE"])
            # geompy.UnionList(Auto_group_for_Sub_mesh_Fuselage_Transition_Edges, [Edge_112,Edge_115,Edge_118,Edge_123,Edge_126,Edge_131,Edge_193,Edge_197,Edge_199,Edge_1126,Edge_1127])

            # # Root edges
            # Auto_group_for_Sub_mesh_Root_Edges = geompy.CreateGroup(nasa_crm_igs, geompy.ShapeType["EDGE"])
            # geompy.UnionList(Auto_group_for_Sub_mesh_Root_Edges, [Edge_114,Edge_119,Edge_125,Edge_127,Edge_130,Edge_140,Edge_144,Edge_145,Edge_146, Edge_1133])
            '''

            # Fuselage surfaces
            Auto_group_for_Sub_mesh_Fuselage_Surfaces = geompy.CreateGroup(nasa_crm_igs, geompy.ShapeType["FACE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Fuselage_Surfaces, [Face_crm_fuselage_middle_down,Face_crm_fuselage_middle_middle,Face_crm_fuselage_middle_up,Face_crm_fuselage_root_down_down,Face_crm_fuselage_root_up_up,Face_crm_fuselage_ring_up,Face_crm_fuselage_ring_down,Face_crm_fuselage_ring_middle,Face_crm_fuselage_back])

            Auto_group_for_Sub_mesh_Root_Surfaces = geompy.CreateGroup(nasa_crm_igs, geompy.ShapeType["FACE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Root_Surfaces, [Face_crm_fuselage_root_up,Face_crm_fuselage_root_down])

            # Far field edges
            Auto_group_for_Sub_mesh_Far_Field_Edges = geompy.CreateGroup(nasa_crm_igs, geompy.ShapeType["EDGE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Far_Field_Edges, [Edge_1,Edge_2,Edge_3,Edge_4,Edge_5,Edge_6,Edge_7,Edge_8,Edge_9,Edge_10,Edge_11,Edge_12])

            # Far field surfaces
            Auto_group_for_Sub_mesh_Far_Field_Surfaces = geompy.CreateGroup(nasa_crm_igs, geompy.ShapeType["FACE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Far_Field_Surfaces, [Face_Inlet, Face_Left_Wall, Face_Right_Wall, Face_Top_Wall, Face_Down_Wall, Face_Outlet])

            # Aircraft surface
            Auto_group_for_Sub_mesh_Aircraft_Surfaces = geompy.CreateGroup(nasa_crm_igs, geompy.ShapeType["FACE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Aircraft_Surfaces, [Face_crm_cockpit,Face_crm_fuselage_middle_down,\
            Face_crm_fuselage_middle_middle,Face_crm_fuselage_middle_up,\
            Face_crm_fuselage_root_down,Face_crm_fuselage_root_down_down,\
            Face_crm_fuselage_root_up_up,Face_crm_fuselage_root_up,\
            Face_crm_wing_root_down,Face_crm_wing_root_down2,\
            Face_crm_wing_root_up,Face_crm_wing_root_te,\
            Face_crm_wing_down,Face_crm_wing_up,Face_crm_fuselage_ring_up,\
            Face_crm_fuselage_ring_down,Face_crm_fuselage_ring_middle,Face_crm_wing_te,\
            Face_crm_wing_tip_down,Face_crm_wing_tip_up,Face_crm_wing_tip_te,\
            Face_crm_fuselage_back,\
            Face_crm_tail_down,Face_crm_tail_up,Face_crm_tail_te,\
            Face_crm_tail_tip_le_down,Face_crm_tail_tip_le_up,Face_crm_tail_tip_te_down,\
            Face_crm_tail_tip_te_up,Face_crm_engine_1,Face_crm_engine_2,Face_crm_engine_3,Face_crm_engine_4,Face_crm_engine_5,Face_crm_engine_6,Face_crm_engine_7,Face_crm_engine_8,Face_crm_engine_9,Face_crm_engine_10,Face_crm_engine_11,Face_crm_engine_12,Face_crm_pylon_1,Face_crm_pylon_2,Face_crm_pylon_3,Face_crm_pylon_4,Face_crm_pylon_7,Face_crm_pylon_8,Face_crm_pylon_9,Face_crm_pylon_10,Face_crm_pylon_11,Face_crm_pylon_12,Face_crm_pylon_13,Face_crm_pylon_14,Face_crm_pylon_15,Face_crm_pylon_16])

            # Generate stl wake
            wake_angle_rad = wake_angle_deg*math.pi/180.0
            Vector_Wake_Direction = geompy.MakeVectorDXDYDZ(math.cos(wake_angle_rad), 0, math.sin(wake_angle_rad))
            trailing_edge = geompy.ImportIGES(trailing_edge_path, True)
            Extrusion_Wake_stl = geompy.MakePrismVecH(trailing_edge, Vector_Wake_Direction, Domain_Length*0.6)

            [Wake_Face_Wing_Fuselage,Wake_Face_Wing_Root,Wake_Face_Wing_Out,Wake_Face_Tail_Fuselage,Wake_Face_Tail] = geompy.ExtractShapes(Extrusion_Wake_stl, geompy.ShapeType["FACE"], True)

            [Trailing_Edge_1,Wake_Side_Edge_2,Wake_Side_Edge_3,Outlet_Edge_4] = geompy.ExtractShapes(Wake_Face_Wing_Fuselage, geompy.ShapeType["EDGE"], True)
            [Trailing_Edge_2,Obj1,Wake_Side_Edge_4,Outlet_Edge_5] = geompy.ExtractShapes(Wake_Face_Wing_Root, geompy.ShapeType["EDGE"], True)
            [Trailing_Edge_3,Obj1,Wake_Side_Edge_5,Outlet_Edge_6] = geompy.ExtractShapes(Wake_Face_Wing_Out, geompy.ShapeType["EDGE"], True)
            # [Trailing_Edge_4,Obj1,Wake_Side_Edge_6,Outlet_Edge_7] = geompy.ExtractShapes(Wake_Face_Wing_Tip, geompy.ShapeType["EDGE"], True)
            [Trailing_Edge_5,Wake_Side_Edge_7,Wake_Side_Edge_8,Outlet_Edge_8] = geompy.ExtractShapes(Wake_Face_Tail_Fuselage, geompy.ShapeType["EDGE"], True)
            [Trailing_Edge_6,Obj1,Wake_Side_Edge_9,Outlet_Edge_9] = geompy.ExtractShapes(Wake_Face_Tail, geompy.ShapeType["EDGE"], True)

            # Wake trailing edges
            Auto_group_for_Sub_mesh_Wake_Trailing_Edges = geompy.CreateGroup(Extrusion_Wake_stl, geompy.ShapeType["EDGE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Wake_Trailing_Edges, [Trailing_Edge_2,Trailing_Edge_3, Trailing_Edge_1])

            Auto_group_for_Sub_mesh_Wake_Tail_Trailing_Edges = geompy.CreateGroup(Extrusion_Wake_stl, geompy.ShapeType["EDGE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Wake_Tail_Trailing_Edges, [Trailing_Edge_6, Trailing_Edge_5])

            # # Wake transition edges
            # Auto_group_for_Sub_mesh_Wake_Transition_Edges = geompy.CreateGroup(Extrusion_Wake_stl, geompy.ShapeType["EDGE"])
            # geompy.UnionList(Auto_group_for_Sub_mesh_Wake_Transition_Edges, [Wake_Side_Edge_2,Wake_Side_Edge_3,Wake_Side_Edge_4,Wake_Side_Edge_5,Wake_Side_Edge_6,Wake_Side_Edge_7,Wake_Side_Edge_8,Wake_Side_Edge_9])

            # # Wake outlet edges
            # Auto_group_for_Sub_mesh_Wake_Outlet_Edges = geompy.CreateGroup(Extrusion_Wake_stl, geompy.ShapeType["EDGE"])
            # geompy.UnionList(Auto_group_for_Sub_mesh_Wake_Outlet_Edges, [Outlet_Edge_4,Outlet_Edge_5,Outlet_Edge_6,Outlet_Edge_7,Outlet_Edge_8,Outlet_Edge_9])

            # Wing Wake surfaces

            Auto_group_for_Sub_mesh_Wake_Surfaces = geompy.CreateGroup(Extrusion_Wake_stl, geompy.ShapeType["FACE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Wake_Surfaces, [Wake_Face_Wing_Fuselage,Wake_Face_Wing_Root,Wake_Face_Wing_Out])

            Auto_group_for_Sub_mesh_Tail_Wake_Surfaces = geompy.CreateGroup(Extrusion_Wake_stl, geompy.ShapeType["FACE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Tail_Wake_Surfaces, [Wake_Face_Tail_Fuselage,Wake_Face_Tail])

            #'''

            exe_time = time.time() - start_time
            print(' Geometry execution took ', str(round(exe_time, 2)), ' sec')
            print(' Geometry execution took ' + str(round(exe_time/60, 2)) + ' min')

            # Adding to study
            geompy.addToStudy( O, 'O' )
            geompy.addToStudy( OX, 'OX' )
            geompy.addToStudy( OY, 'OY' )
            geompy.addToStudy( OZ, 'OZ' )
            geompy.addToStudy( nasa_crm_igs, 'nasa_crm_igs' )

            geompy.addToStudyInFather( nasa_crm_igs, Face_Inlet, 'Face_Inlet' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_cockpit, 'Face_crm_cockpit' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_fuselage_middle_down, 'Face_crm_fuselage_middle_down' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_fuselage_middle_middle, 'Face_crm_fuselage_middle_middle' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_fuselage_middle_up, 'Face_crm_fuselage_middle_up' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_engine_1, 'Face_crm_engine_1' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_engine_2, 'Face_crm_engine_2' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_engine_3, 'Face_crm_engine_3' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_engine_4, 'Face_crm_engine_4' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_engine_5, 'Face_crm_engine_5' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_engine_6, 'Face_crm_engine_6' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_engine_7, 'Face_crm_engine_7' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_engine_8, 'Face_crm_engine_8' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_pylon_1, 'Face_crm_pylon_1' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_pylon_2, 'Face_crm_pylon_2' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_engine_9, 'Face_crm_engine_9' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_engine_10, 'Face_crm_engine_10' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_engine_11, 'Face_crm_engine_11' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_engine_12, 'Face_crm_engine_12' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_pylon_3, 'Face_crm_pylon_3' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_pylon_4, 'Face_crm_pylon_4' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_fuselage_root_down, 'Face_crm_fuselage_root_down' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_engine_outlet_1, 'Face_crm_engine_outlet_1' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_engine_outlet_2, 'Face_crm_engine_outlet_2' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_pylon_5, 'Face_crm_pylon_5' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_fuselage_root_down_down, 'Face_crm_fuselage_root_down_down' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_engine_outlet_3, 'Face_crm_engine_outlet_3' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_pylon_6, 'Face_crm_pylon_6' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_engine_outlet_4, 'Face_crm_engine_outlet_4' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_pylon_7, 'Face_crm_pylon_7' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_pylon_8, 'Face_crm_pylon_8' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_fuselage_root_up_up, 'Face_crm_fuselage_root_up_up' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_pylon_9, 'Face_crm_pylon_9' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_pylon_10, 'Face_crm_pylon_10' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_wing_root_down, 'Face_crm_wing_root_down' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_wing_root_up, 'Face_crm_wing_root_up' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_pylon_11, 'Face_crm_pylon_11' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_pylon_12, 'Face_crm_pylon_12' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_pylon_13, 'Face_crm_pylon_13' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_pylon_14, 'Face_crm_pylon_14' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_Left_Wall, 'Face_Left_Wall' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_fuselage_root_up, 'Face_crm_fuselage_root_up' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_pylon_15, 'Face_crm_pylon_15' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_pylon_16, 'Face_crm_pylon_16' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_wing_root_down2, 'Face_crm_wing_root_down2' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_wing_root_te, 'Face_crm_wing_root_te' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_wing_down, 'Face_crm_wing_down' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_wing_up, 'Face_crm_wing_up' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_fuselage_ring_up, 'Face_crm_fuselage_ring_up' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_fuselage_ring_down, 'Face_crm_fuselage_ring_down' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_fuselage_ring_middle, 'Face_crm_fuselage_ring_middle' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_wing_te, 'Face_crm_wing_te' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_wing_tip_down, 'Face_crm_wing_tip_down' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_wing_tip_up, 'Face_crm_wing_tip_up' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_wing_tip_te, 'Face_crm_wing_tip_te' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_fuselage_back, 'Face_crm_fuselage_back' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_Down_Wall, 'Face_Down_Wall' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_Top_Wall, 'Face_Top_Wall' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_tail_down, 'Face_crm_tail_down' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_tail_up, 'Face_crm_tail_up' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_tail_te, 'Face_crm_tail_te' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_tail_tip_le_down, 'Face_crm_tail_tip_le_down' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_tail_tip_le_up, 'Face_crm_tail_tip_le_up' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_tail_tip_te_down, 'Face_crm_tail_tip_te_down' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_tail_tip_te_up, 'Face_crm_tail_tip_te_up' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_Right_Wall, 'Face_Right_Wall' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_Outlet, 'Face_Outlet' )

            geompy.addToStudyInFather( Face_Inlet, Edge_1, 'Edge_1' )
            geompy.addToStudyInFather( Face_Inlet, Edge_2, 'Edge_2' )
            geompy.addToStudyInFather( Face_Inlet, Edge_3, 'Edge_3' )
            geompy.addToStudyInFather( Face_Inlet, Edge_4, 'Edge_4' )

            geompy.addToStudyInFather( Face_Left_Wall, Edge_5, 'Edge_5' )
            geompy.addToStudyInFather( Face_Left_Wall, Edge_6, 'Edge_6' )

            geompy.addToStudyInFather( Face_Right_Wall, Edge_7, 'Edge_7' )
            geompy.addToStudyInFather( Face_Right_Wall, Edge_8, 'Edge_8' )

            geompy.addToStudyInFather( Face_Outlet, Edge_9, 'Edge_9' )
            geompy.addToStudyInFather( Face_Outlet, Edge_10, 'Edge_10' )
            geompy.addToStudyInFather( Face_Outlet, Edge_11, 'Edge_11' )
            geompy.addToStudyInFather( Face_Outlet, Edge_12, 'Edge_12' )

            geompy.addToStudyInFather( Face_crm_cockpit, Edge_105, 'Edge_105' )
            geompy.addToStudyInFather( Face_crm_cockpit, Edge_106, 'Edge_106' )
            geompy.addToStudyInFather( Face_crm_cockpit, Edge_107, 'Edge_107' )
            geompy.addToStudyInFather( Face_crm_cockpit, Edge_108, 'Edge_108' )
            geompy.addToStudyInFather( Face_crm_cockpit, Edge_109, 'Edge_109' )
            geompy.addToStudyInFather( Face_crm_cockpit, Edge_110, 'Edge_110' )

            geompy.addToStudyInFather( Face_crm_fuselage_middle_down, Edge_112, 'Edge_112' )
            geompy.addToStudyInFather( Face_crm_fuselage_middle_down, Edge_113, 'Edge_113' )
            geompy.addToStudyInFather( Face_crm_fuselage_middle_down, Edge_114, 'Edge_114' )
            geompy.addToStudyInFather( Face_crm_fuselage_middle_down, Edge_115, 'Edge_115' )

            geompy.addToStudyInFather( Face_crm_fuselage_middle_middle, Edge_118, 'Edge_118' )
            geompy.addToStudyInFather( Face_crm_fuselage_middle_middle, Edge_119, 'Edge_119' )
            geompy.addToStudyInFather( Face_crm_fuselage_middle_middle, Edge_220, 'Edge_220' )

            geompy.addToStudyInFather( Face_crm_fuselage_middle_up, Edge_121, 'Edge_121' )
            geompy.addToStudyInFather( Face_crm_fuselage_middle_up, Edge_123, 'Edge_123' )

            geompy.addToStudyInFather( Face_crm_fuselage_root_down, Edge_127, 'Edge_127' )
            geompy.addToStudyInFather( Face_crm_fuselage_root_down, Edge_129, 'Edge_129' )
            geompy.addToStudyInFather( Face_crm_fuselage_root_down, Edge_133, 'Edge_133' )

            geompy.addToStudyInFather( Face_crm_fuselage_root_down_down, Edge_136, 'Edge_136' )
            geompy.addToStudyInFather( Face_crm_fuselage_root_down_down, Edge_137, 'Edge_137' )

            geompy.addToStudyInFather( Face_crm_fuselage_root_up_up, Edge_139, 'Edge_139' )
            geompy.addToStudyInFather( Face_crm_fuselage_root_up_up, Edge_140, 'Edge_140' )
            geompy.addToStudyInFather( Face_crm_fuselage_root_up_up, Edge_141, 'Edge_141' )
            geompy.addToStudyInFather( Face_crm_fuselage_root_up_up, Edge_142, 'Edge_142' )

            geompy.addToStudyInFather( Face_crm_wing_root_down, Edge_wing_root_down_le, 'Edge_wing_root_down_le' )
            geompy.addToStudyInFather( Face_crm_wing_root_down, Edge_wing_root_le, 'Edge_wing_root_le' )
            geompy.addToStudyInFather( Face_crm_wing_root_down, Edge_wing_transition_1, 'Edge_wing_transition_1' )
            geompy.addToStudyInFather( Face_crm_wing_root_down, Edge_wing_hole_1, 'Edge_wing_hole_1' )
            geompy.addToStudyInFather( Face_crm_wing_root_down, Edge_wing_root_te_down, 'Edge_wing_root_te_down' )
            geompy.addToStudyInFather( Face_crm_wing_root_down, Edge_wing_hole_2, 'Edge_wing_hole_2' )
            geompy.addToStudyInFather( Face_crm_wing_root_down, Edge_wing_root_down_te, 'Edge_wing_root_down_te' )
            geompy.addToStudyInFather( Face_crm_wing_root_down, Edge_wing_transition_2, 'Edge_wing_transition_2' )

            geompy.addToStudyInFather( Face_crm_wing_root_down2, Edge_wing_root_le2, 'Edge_wing_root_le2' )
            geompy.addToStudyInFather( Face_crm_wing_root_down2, Edge_wing_hole_3, 'Edge_wing_hole_3' )
            geompy.addToStudyInFather( Face_crm_wing_root_down2, Edge_wing_middle_down_le, 'Edge_wing_middle_down_le' )
            geompy.addToStudyInFather( Face_crm_wing_root_down2, Edge_wing_hole_4, 'Edge_wing_hole_4' )
            geompy.addToStudyInFather( Face_crm_wing_root_down2, Edge_wing_middle_down_te, 'Edge_wing_middle_down_te' )
            geompy.addToStudyInFather( Face_crm_wing_root_down2, Edge_wing_root_down_te2, 'Edge_wing_root_down_te2' )

            geompy.addToStudyInFather( Face_crm_wing_root_up, Edge_wing_root_up_le, 'Edge_wing_root_up_le' )
            geompy.addToStudyInFather( Face_crm_wing_root_up, Edge_wing_middle_up_le, 'Edge_wing_middle_up_le' )
            geompy.addToStudyInFather( Face_crm_wing_root_up, Edge_wing_root_up_te, 'Edge_wing_root_up_te' )
            geompy.addToStudyInFather( Face_crm_wing_root_up, Edge_wing_middle_up_te, 'Edge_wing_middle_up_te' )
            geompy.addToStudyInFather( Face_crm_wing_root_up, Edge_wing_root_te_up, 'Edge_wing_root_te_up' )

            geompy.addToStudyInFather( Face_crm_fuselage_root_up, Edge_177, 'Edge_177' )
            geompy.addToStudyInFather( Face_crm_fuselage_root_up, Edge_178, 'Edge_178' )
            geompy.addToStudyInFather( Face_crm_fuselage_root_up, Edge_179, 'Edge_179' )

            geompy.addToStudyInFather( Face_crm_wing_root_te, Edge_root_te_down, 'Edge_root_te_down' )
            geompy.addToStudyInFather( Face_crm_wing_root_te, Edge_root_te_up, 'Edge_root_te_up' )
            geompy.addToStudyInFather( Face_crm_wing_root_te, Edge_wing_middle_te, 'Edge_wing_middle_te' )

            geompy.addToStudyInFather( Face_crm_wing_down, Edge_wing_le, 'Edge_wing_le' )
            geompy.addToStudyInFather( Face_crm_wing_down, Edge_wing_te_down, 'Edge_wing_te_down' )
            geompy.addToStudyInFather( Face_crm_wing_down, Edge_wing_tip_down_le, 'Edge_wing_tip_down_le' )
            geompy.addToStudyInFather( Face_crm_wing_down, Edge_wing_tip_down_te, 'Edge_wing_tip_down_te' )

            geompy.addToStudyInFather( Face_crm_wing_up, Edge_wing_te_up, 'Edge_wing_te_up' )
            geompy.addToStudyInFather( Face_crm_wing_up, Edge_wing_tip_up_le, 'Edge_wing_tip_up_le' )
            geompy.addToStudyInFather( Face_crm_wing_up, Edge_wing_tip_up_te, 'Edge_wing_tip_up_te' )

            geompy.addToStudyInFather( Face_crm_fuselage_ring_up, Edge_192, 'Edge_192' )
            geompy.addToStudyInFather( Face_crm_fuselage_ring_up, Edge_193, 'Edge_193' )
            geompy.addToStudyInFather( Face_crm_fuselage_ring_up, Edge_194, 'Edge_194' )

            geompy.addToStudyInFather( Face_crm_fuselage_ring_down, Edge_197, 'Edge_197' )
            geompy.addToStudyInFather( Face_crm_fuselage_ring_down, Edge_199, 'Edge_199' )
            geompy.addToStudyInFather( Face_crm_fuselage_ring_down, Edge_1100, 'Edge_1100' )

            geompy.addToStudyInFather( Face_crm_fuselage_ring_middle, Edge_1104, 'Edge_1104' )

            geompy.addToStudyInFather( Face_crm_wing_te, Edge_wing_tip_te1, 'Edge_wing_tip_te1' )

            geompy.addToStudyInFather( Face_crm_wing_tip_down, Edge_wing_tip_middle_le, 'Edge_wing_tip_middle_le' )
            geompy.addToStudyInFather( Face_crm_wing_tip_down, Edge_wing_tip_middle_te, 'Edge_wing_tip_middle_te' )
            geompy.addToStudyInFather( Face_crm_wing_tip_down, Edge_wing_tip_te2, 'Edge_wing_tip_te2' )

            geompy.addToStudyInFather( Face_crm_wing_tip_up, Edge_wing_tip_te3, 'Edge_wing_tip_te3' )

            geompy.addToStudyInFather( Face_crm_fuselage_back, Edge_1126, 'Edge_1126' )
            geompy.addToStudyInFather( Face_crm_fuselage_back, Edge_1127, 'Edge_1127' )
            geompy.addToStudyInFather( Face_crm_fuselage_back, Edge_1133, 'Edge_1133' )

            geompy.addToStudyInFather( Face_crm_tail_down, Edge_tail_root_down_le, 'Edge_tail_root_down_le' )
            geompy.addToStudyInFather( Face_crm_tail_down, Edge_tail_root_down_te, 'Edge_tail_root_down_te' )
            geompy.addToStudyInFather( Face_crm_tail_down, Edge_tail_le, 'Edge_tail_le' )
            geompy.addToStudyInFather( Face_crm_tail_down, Edge_tail_te_down, 'Edge_tail_te_down' )
            geompy.addToStudyInFather( Face_crm_tail_down, Edge_tail_tip_down_le, 'Edge_tail_tip_down_le' )
            geompy.addToStudyInFather( Face_crm_tail_down, Edge_tail_tip_down_te, 'Edge_tail_tip_down_te' )

            geompy.addToStudyInFather( Face_crm_tail_up, Edge_tail_root_up_le, 'Edge_tail_root_up_le' )
            geompy.addToStudyInFather( Face_crm_tail_up, Edge_tail_root_up_te, 'Edge_tail_root_up_te' )
            geompy.addToStudyInFather( Face_crm_tail_up, Edge_tail_te_up, 'Edge_tail_te_up' )
            geompy.addToStudyInFather( Face_crm_tail_up, Edge_tail_tip_up_le, 'Edge_tail_tip_up_le' )
            geompy.addToStudyInFather( Face_crm_tail_up, Edge_tail_tip_up_te, 'Edge_tail_tip_up_te' )

            geompy.addToStudyInFather( Face_crm_tail_te, Edge_tail_root_te, 'Edge_tail_root_te' )
            geompy.addToStudyInFather( Face_crm_tail_te, Edge_tail_tip_te_down, 'Edge_tail_tip_te_down' )
            geompy.addToStudyInFather( Face_crm_tail_te, Edge_tail_tip_te_up, 'Edge_tail_tip_te_up' )

            geompy.addToStudyInFather( Face_crm_tail_tip_le_down, Edge_tail_tip_middle_le, 'Edge_tail_tip_middle_le' )
            geompy.addToStudyInFather( Face_crm_tail_tip_le_down, Edge_tail_tip_middle_down, 'Edge_tail_tip_middle_down' )

            geompy.addToStudyInFather( Face_crm_tail_tip_le_up, Edge_tail_tip_middle_up, 'Edge_tail_tip_middle_up' )

            geompy.addToStudyInFather( Face_crm_tail_tip_te_down, Edge_tail_tip_middle_te, 'Edge_tail_tip_middle_te' )

            geompy.addToStudyInFather( Face_crm_engine_1, Edge_301, 'Edge_301' )
            geompy.addToStudyInFather( Face_crm_engine_1, Edge_302, 'Edge_302' )
            geompy.addToStudyInFather( Face_crm_engine_1, Edge_303, 'Edge_303' )
            geompy.addToStudyInFather( Face_crm_engine_1, Edge_304, 'Edge_304' )

            geompy.addToStudyInFather( Face_crm_engine_2, Edge_306, 'Edge_306' )
            geompy.addToStudyInFather( Face_crm_engine_2, Edge_307, 'Edge_307' )
            geompy.addToStudyInFather( Face_crm_engine_2, Edge_308, 'Edge_308' )

            geompy.addToStudyInFather( Face_crm_engine_3, Edge_309, 'Edge_309' )
            geompy.addToStudyInFather( Face_crm_engine_3, Edge_312, 'Edge_312' )

            geompy.addToStudyInFather( Face_crm_engine_4, Edge_316, 'Edge_316' )

            geompy.addToStudyInFather( Face_crm_engine_5, Edge_318, 'Edge_318' )
            geompy.addToStudyInFather( Face_crm_engine_5, Edge_319, 'Edge_319' )
            geompy.addToStudyInFather( Face_crm_engine_5, Edge_320, 'Edge_320' )
            geompy.addToStudyInFather( Face_crm_engine_5, Edge_321, 'Edge_321' )

            geompy.addToStudyInFather( Face_crm_engine_6, Edge_325, 'Edge_325' )
            geompy.addToStudyInFather( Face_crm_engine_6, Edge_326, 'Edge_326' )

            geompy.addToStudyInFather( Face_crm_engine_7, Edge_328, 'Edge_328' )
            geompy.addToStudyInFather( Face_crm_engine_7, Edge_329, 'Edge_329' )
            geompy.addToStudyInFather( Face_crm_engine_7, Edge_330, 'Edge_330' )
            geompy.addToStudyInFather( Face_crm_engine_7, Edge_331, 'Edge_331' )

            geompy.addToStudyInFather( Face_crm_engine_8, Edge_335, 'Edge_335' )
            geompy.addToStudyInFather( Face_crm_engine_8, Edge_336, 'Edge_336' )

            geompy.addToStudyInFather( Face_crm_engine_9, Edge_338, 'Edge_338' )
            geompy.addToStudyInFather( Face_crm_engine_9, Edge_339, 'Edge_339' )
            geompy.addToStudyInFather( Face_crm_engine_9, Edge_340, 'Edge_340' )

            geompy.addToStudyInFather( Face_crm_engine_10, Edge_343, 'Edge_343' )
            geompy.addToStudyInFather( Face_crm_engine_10, Edge_326, 'Edge_326' )

            geompy.addToStudyInFather( Face_crm_engine_11, Edge_346, 'Edge_346' )
            geompy.addToStudyInFather( Face_crm_engine_11, Edge_347, 'Edge_347' )
            geompy.addToStudyInFather( Face_crm_engine_11, Edge_348, 'Edge_348' )
            geompy.addToStudyInFather( Face_crm_engine_11, Edge_349, 'Edge_349' )

            geompy.addToStudyInFather( Face_crm_engine_12, Edge_352, 'Edge_352' )
            geompy.addToStudyInFather( Face_crm_engine_12, Edge_353, 'Edge_353' )
            geompy.addToStudyInFather( Face_crm_engine_12, Edge_354, 'Edge_354' )

            geompy.addToStudyInFather( Face_crm_engine_outlet_1, Edge_500, 'Edge_500' )
            geompy.addToStudyInFather( Face_crm_engine_outlet_1, Edge_501, 'Edge_501' )

            geompy.addToStudyInFather( Face_crm_engine_outlet_2, Edge_502, 'Edge_502' )

            geompy.addToStudyInFather( Face_crm_engine_outlet_3, Edge_503, 'Edge_503' )

            geompy.addToStudyInFather( Face_crm_pylon_1, Edge_356, 'Edge_356' )
            geompy.addToStudyInFather( Face_crm_pylon_1, Edge_357, 'Edge_357' )

            geompy.addToStudyInFather( Face_crm_pylon_2, Edge_360, 'Edge_360' )

            geompy.addToStudyInFather( Face_crm_pylon_3, Edge_363, 'Edge_363' )
            geompy.addToStudyInFather( Face_crm_pylon_3, Edge_364, 'Edge_364' )
            geompy.addToStudyInFather( Face_crm_pylon_3, Edge_365, 'Edge_365' )

            geompy.addToStudyInFather( Face_crm_pylon_4, Edge_369, 'Edge_369' )
            geompy.addToStudyInFather( Face_crm_pylon_4, Edge_370, 'Edge_370' )

            geompy.addToStudyInFather( Face_crm_pylon_5, Edge_371, 'Edge_371' )
            geompy.addToStudyInFather( Face_crm_pylon_5, Edge_372, 'Edge_372' )
            geompy.addToStudyInFather( Face_crm_pylon_5, Edge_373, 'Edge_373' )

            geompy.addToStudyInFather( Face_crm_pylon_6, Edge_374, 'Edge_374' )
            geompy.addToStudyInFather( Face_crm_pylon_6, Edge_375, 'Edge_375' )
            geompy.addToStudyInFather( Face_crm_pylon_6, Edge_376, 'Edge_376' )

            geompy.addToStudyInFather( Face_crm_pylon_7, Edge_380, 'Edge_380' )
            geompy.addToStudyInFather( Face_crm_pylon_7, Edge_381, 'Edge_381' )

            geompy.addToStudyInFather( Face_crm_pylon_8, Edge_385, 'Edge_385' )
            geompy.addToStudyInFather( Face_crm_pylon_8, Edge_386, 'Edge_386' )

            geompy.addToStudyInFather( Face_crm_pylon_9, Edge_387, 'Edge_387' )
            geompy.addToStudyInFather( Face_crm_pylon_9, Edge_390, 'Edge_390' )

            geompy.addToStudyInFather( Face_crm_pylon_10, Edge_394, 'Edge_394' )

            geompy.addToStudyInFather( Face_crm_pylon_11, Edge_395, 'Edge_395' )
            geompy.addToStudyInFather( Face_crm_pylon_11, Edge_398, 'Edge_398' )
            geompy.addToStudyInFather( Face_crm_pylon_11, Edge_399, 'Edge_399' )

            geompy.addToStudyInFather( Face_crm_pylon_12, Edge_400, 'Edge_400' )
            geompy.addToStudyInFather( Face_crm_pylon_12, Edge_404, 'Edge_404' )

            geompy.addToStudyInFather( Face_crm_pylon_13, Edge_407, 'Edge_407' )
            geompy.addToStudyInFather( Face_crm_pylon_13, Edge_408, 'Edge_408' )

            geompy.addToStudyInFather( Face_crm_pylon_14, Edge_411, 'Edge_411' )

            geompy.addToStudyInFather( Face_crm_pylon_15, Edge_416, 'Edge_416' )

            # Groups
            # Wing edges
            geompy.addToStudyInFather( nasa_crm_igs, Auto_group_for_Sub_mesh_LE_TE_Edges, 'Auto_group_for_Sub_mesh_LE_TE_Edges' )

            geompy.addToStudyInFather( nasa_crm_igs, Auto_group_for_Sub_mesh_Airfoil_Edges, 'Auto_group_for_Sub_mesh_Airfoil_Edges' )
            geompy.addToStudyInFather( nasa_crm_igs, Auto_group_for_Sub_mesh_Tip_Airfoil_Edges, 'Auto_group_for_Sub_mesh_Tip_Airfoil_Edges' )
            geompy.addToStudyInFather( nasa_crm_igs, Auto_group_for_Sub_mesh_Tip_Middle_Edges, 'Auto_group_for_Sub_mesh_Tip_Middle_Edges' )
            geompy.addToStudyInFather( nasa_crm_igs, Auto_group_for_Sub_mesh_Engine_Edges, 'Auto_group_for_Sub_mesh_Engine_Edges' )
            geompy.addToStudyInFather( nasa_crm_igs, Auto_group_for_Sub_mesh_Wing_Hole_Edges, 'Auto_group_for_Sub_mesh_Wing_Hole_Edges' )


            geompy.addToStudyInFather( nasa_crm_igs, Auto_group_for_Sub_mesh_Engine_Outlet_Edges, 'Auto_group_for_Sub_mesh_Engine_Outlet_Edges' )
            geompy.addToStudyInFather( nasa_crm_igs, Auto_group_for_Sub_mesh_Engine_Outlet_Surfaces, 'Auto_group_for_Sub_mesh_Engine_Outlet_Surfaces' )
            geompy.addToStudyInFather( nasa_crm_igs, Auto_group_for_Sub_mesh_Engine_Transition_Edges, 'Auto_group_for_Sub_mesh_Engine_Transition_Edges' )

            geompy.addToStudyInFather( nasa_crm_igs, Auto_group_for_Sub_mesh_Pylon_Edges, 'Auto_group_for_Sub_mesh_Pylon_Edges' )
            geompy.addToStudyInFather( nasa_crm_igs, Auto_group_for_Sub_mesh_Pylon_Transition_Edges, 'Auto_group_for_Sub_mesh_Pylon_Transition_Edges' )





            # Wing surfaces
            geompy.addToStudyInFather( nasa_crm_igs, Auto_group_for_Sub_mesh_Wing_Tail_Surfaces, 'Auto_group_for_Sub_mesh_Wing_Tail_Surfaces' )
            geompy.addToStudyInFather( nasa_crm_igs, Auto_group_for_Sub_mesh_Wing_Tail_Tip_Surfaces, 'Auto_group_for_Sub_mesh_Wing_Tail_Tip_Surfaces' )
            geompy.addToStudyInFather( nasa_crm_igs, Auto_group_for_Sub_mesh_Trailing_Edge_Surfaces, 'Auto_group_for_Sub_mesh_Trailing_Edge_Surfaces' )
            geompy.addToStudyInFather( nasa_crm_igs, Auto_group_for_Sub_mesh_Engine_Surfaces, 'Auto_group_for_Sub_mesh_Engine_Surfaces' )
            geompy.addToStudyInFather( nasa_crm_igs, Auto_group_for_Sub_mesh_Wing_Surfaces, 'Auto_group_for_Sub_mesh_Wing_Surfaces' )


            # Fuselage edges
            geompy.addToStudyInFather( nasa_crm_igs, Auto_group_for_Sub_mesh_Fuselage_Edges, 'Auto_group_for_Sub_mesh_Fuselage_Edges' )
            geompy.addToStudyInFather( nasa_crm_igs, Auto_group_for_Sub_mesh_Fuselage_Transition_Edges, 'Auto_group_for_Sub_mesh_Fuselage_Transition_Edges' )

            '''
            # geompy.addToStudyInFather( nasa_crm_igs, Auto_group_for_Sub_mesh_Root_Edges, 'Auto_group_for_Sub_mesh_Root_Edges' )
            '''
            geompy.addToStudyInFather( nasa_crm_igs, Auto_group_for_Sub_mesh_Fuselage_Surfaces, 'Auto_group_for_Sub_mesh_Fuselage_Surfaces' )
            geompy.addToStudyInFather( nasa_crm_igs, Auto_group_for_Sub_mesh_Root_Surfaces, 'Auto_group_for_Sub_mesh_Root_Surfaces' )
            geompy.addToStudyInFather( nasa_crm_igs, Auto_group_for_Sub_mesh_Aircraft_Surfaces, 'Auto_group_for_Sub_mesh_Aircraft_Surfaces' )

            geompy.addToStudyInFather( nasa_crm_igs, Auto_group_for_Sub_mesh_Far_Field_Edges, 'Auto_group_for_Sub_mesh_Far_Field_Edges' )

            geompy.addToStudyInFather( nasa_crm_igs, Auto_group_for_Sub_mesh_Far_Field_Surfaces, 'Auto_group_for_Sub_mesh_Far_Field_Surfaces' )

            geompy.addToStudy( trailing_edge, 'trailing_edge' )
            geompy.addToStudy( Vector_Wake_Direction, 'Vector_Wake_Direction' )
            geompy.addToStudy( Extrusion_Wake_stl, 'Extrusion_Wake_stl' )

            geompy.addToStudyInFather( Extrusion_Wake_stl, Wake_Face_Wing_Fuselage, 'Wake_Face_Wing_Fuselage' )
            geompy.addToStudyInFather( Extrusion_Wake_stl, Wake_Face_Wing_Root, 'Wake_Face_Wing_Root' )
            geompy.addToStudyInFather( Extrusion_Wake_stl, Wake_Face_Wing_Out, 'Wake_Face_Wing_Out' )
            # geompy.addToStudyInFather( Extrusion_Wake_stl, Wake_Face_Wing_Tip, 'Wake_Face_Wing_Tip' )
            geompy.addToStudyInFather( Extrusion_Wake_stl, Wake_Face_Tail_Fuselage, 'Wake_Face_Tail_Fuselage' )
            geompy.addToStudyInFather( Extrusion_Wake_stl, Wake_Face_Tail, 'Wake_Face_Tail' )

            geompy.addToStudyInFather( Extrusion_Wake_stl, Auto_group_for_Sub_mesh_Wake_Trailing_Edges, 'Auto_group_for_Sub_mesh_Wake_Trailing_Edges' )
            geompy.addToStudyInFather( Extrusion_Wake_stl, Auto_group_for_Sub_mesh_Wake_Tail_Trailing_Edges, 'Auto_group_for_Sub_mesh_Wake_Tail_Trailing_Edges' )

            # geompy.addToStudyInFather( Extrusion_Wake_stl, Auto_group_for_Sub_mesh_Wake_Transition_Edges, 'Auto_group_for_Sub_mesh_Wake_Transition_Edges' )
            # geompy.addToStudyInFather( Extrusion_Wake_stl, Auto_group_for_Sub_mesh_Wake_Outlet_Edges, 'Auto_group_for_Sub_mesh_Wake_Outlet_Edges' )
            geompy.addToStudyInFather( Extrusion_Wake_stl, Auto_group_for_Sub_mesh_Wake_Surfaces, 'Auto_group_for_Sub_mesh_Wake_Surfaces' )
            geompy.addToStudyInFather( Extrusion_Wake_stl, Auto_group_for_Sub_mesh_Tail_Wake_Surfaces, 'Auto_group_for_Sub_mesh_Tail_Wake_Surfaces' )

            ###
            ### SMESH component
            ###

            import  SMESH, SALOMEDS
            from salome.smesh import smeshBuilder

            smesh = smeshBuilder.New(theStudy)

            # Set NETGEN 3D
            Mesh_Domain = smesh.Mesh(nasa_crm_igs)

            NETGEN_3D = Mesh_Domain.Tetrahedron()
            #Viscous_Layers_1 = NETGEN_3D.ViscousLayers(0.01,2,2,[ 85, 102, 141, 155 ],0,StdMeshersBuilder.SURF_OFFSET_SMOOTH)
            NETGEN_3D_Parameters = NETGEN_3D.Parameters()
            NETGEN_3D_Parameters.SetMaxSize( Far_Field_Mesh_Size )
            NETGEN_3D_Parameters.SetOptimize( 1 )
            NETGEN_3D_Parameters.SetFineness( 5 )
            NETGEN_3D_Parameters.SetGrowthRate( Growth_Rate_Domain )
            NETGEN_3D_Parameters.SetNbSegPerEdge( 3 )
            NETGEN_3D_Parameters.SetNbSegPerRadius( 5 )
            NETGEN_3D_Parameters.SetMinSize( Smallest_Airfoil_Mesh_Size )
            NETGEN_3D_Parameters.SetUseSurfaceCurvature( 0 )
            NETGEN_3D_Parameters.SetSecondOrder( 106 )
            NETGEN_3D_Parameters.SetFuseEdges( 80 )
            NETGEN_3D_Parameters.SetQuadAllowed( 127 )

            # Leading and trailing edges
            Regular_1D_LE_TE = Mesh_Domain.Segment(geom=Auto_group_for_Sub_mesh_LE_TE_Edges)
            Sub_mesh_LE_TE = Regular_1D_LE_TE.GetSubMesh()
            Local_Length_LE_TE = Regular_1D_LE_TE.LocalLength(Smallest_Airfoil_Mesh_Size,None,1e-07)

            # Airfoils
            Regular_1D_Airfoils = Mesh_Domain.Segment(geom=Auto_group_for_Sub_mesh_Airfoil_Edges)
            Start_and_End_Length_Airfoils = Regular_1D_Airfoils.StartEndLength(Smallest_Airfoil_Mesh_Size,Biggest_Airfoil_Mesh_Size,[Edge_wing_root_te_down,Edge_wing_middle_down_te,Edge_wing_root_up_le,Edge_wing_middle_up_le,Edge_tail_root_down_te,Edge_tail_root_up_le])
            Start_and_End_Length_Airfoils.SetObjectEntry( 'nasa_crm_igs' )
            Sub_mesh_Airfoils = Regular_1D_Airfoils.GetSubMesh()

            # Wing and tail tip airfoils
            Regular_1D_Tip_Airfoils = Mesh_Domain.Segment(geom=Auto_group_for_Sub_mesh_Tip_Airfoil_Edges)
            Start_and_End_Length_Tip_Airfoils = Regular_1D_Tip_Airfoils.StartEndLength(Smallest_Airfoil_Mesh_Size,Wing_Tip_Mesh_Size,[Edge_wing_tip_down_te,Edge_wing_tip_up_le,Edge_tail_tip_up_le,Edge_tail_tip_down_te,Edge_tail_tip_middle_le,Edge_wing_tip_middle_te])
            Start_and_End_Length_Airfoils.SetObjectEntry( 'nasa_crm_igs' )
            Sub_mesh_Tip_Airfoils = Regular_1D_Tip_Airfoils.GetSubMesh()

            # Tail tip middle airfoils
            Regular_1D_Middle_Tip_Edges = Mesh_Domain.Segment(geom=Auto_group_for_Sub_mesh_Tip_Middle_Edges)
            Sub_mesh_Middle_Tip_Edges = Regular_1D_Middle_Tip_Edges.GetSubMesh()
            Local_Length_Middle_Tip_Edges = Regular_1D_Middle_Tip_Edges.LocalLength(Wing_Tip_Mesh_Size,None,1e-07)

            '''
            # # Root edges
            # Regular_1D_Root = Mesh_Domain.Segment(geom=Auto_group_for_Sub_mesh_Root_Edges)
            # Sub_mesh_Root_Edges = Regular_1D_Root.GetSubMesh()
            # Local_Length_Root = Regular_1D_Root.LocalLength(Root_Mesh_Size,None,1e-07)
            '''

            # Fuselage 177 Edge
            Regular_1D_Fuselage_143_Edge = Mesh_Domain.Segment(geom=Edge_177)
            Start_and_End_Length_Fuselage_143_Edge = Regular_1D_Fuselage_143_Edge.StartEndLength(Smallest_Airfoil_Mesh_Size,Fuselage_Mesh_Size,[])
            Start_and_End_Length_Fuselage_143_Edge.SetObjectEntry( 'nasa_crm_igs' )
            Sub_mesh_Fuselage_143_Edge = Regular_1D_Fuselage_143_Edge.GetSubMesh()

            # Fuselage Transition Edges
            Regular_1D_Fuselage_Transition_Edges = Mesh_Domain.Segment(geom=Auto_group_for_Sub_mesh_Fuselage_Transition_Edges)
            Start_and_End_Length_Fuselage_Transition_Edges = Regular_1D_Fuselage_Transition_Edges.StartEndLength(Smallest_Airfoil_Mesh_Size,Fuselage_Mesh_Size,[])
            Start_and_End_Length_Fuselage_Transition_Edges.SetObjectEntry( 'nasa_crm_igs' )
            Sub_mesh_Fuselage_Transition_Edges = Regular_1D_Fuselage_Transition_Edges.GetSubMesh()

            # Fuselage edges
            Regular_1D_Fuselage = Mesh_Domain.Segment(geom=Auto_group_for_Sub_mesh_Fuselage_Edges)
            Sub_mesh_Fuselage_Edges = Regular_1D_Fuselage.GetSubMesh()
            Local_Length_Fuselage = Regular_1D_Fuselage.LocalLength(Fuselage_Mesh_Size,None,1e-07)

            # Outlet Engine edges
            Regular_1D_Engine_Outlet = Mesh_Domain.Segment(geom=Auto_group_for_Sub_mesh_Engine_Outlet_Edges)
            Sub_mesh_Engine_Outlet_Edges = Regular_1D_Engine_Outlet.GetSubMesh()
            Local_Length_Engine_Outlet = Regular_1D_Engine_Outlet.LocalLength(Engine_Trailing_Edge_Size,None,1e-07)

            # Engine transition edges
            Regular_1D_Engine_Transition_Edges = Mesh_Domain.Segment(geom=Auto_group_for_Sub_mesh_Engine_Transition_Edges)
            Start_and_End_Length_Engine_Transition_Edges = Regular_1D_Engine_Transition_Edges.StartEndLength(Engine_Trailing_Edge_Size,Engine_Mesh_Size,[Edge_352,Edge_385,Edge_346,Edge_380,Edge_329])
            Start_and_End_Length_Engine_Transition_Edges.SetObjectEntry( 'nasa_crm_igs' )
            Sub_mesh_Engine_Transition_Edges = Regular_1D_Engine_Transition_Edges.GetSubMesh()

            # Pylon edges
            Regular_1D_Pylon_Edge = Mesh_Domain.Segment(geom=Auto_group_for_Sub_mesh_Pylon_Edges)
            Sub_mesh_Pylon_Edge = Regular_1D_Pylon_Edge.GetSubMesh()
            Local_Length_Pylon_Edge = Regular_1D_Pylon_Edge.LocalLength(Smallest_Airfoil_Mesh_Size*2.0,None,1e-07)

            # Pylon transition edges
            Regular_1D_Pylon_Transition_Edges = Mesh_Domain.Segment(geom=Auto_group_for_Sub_mesh_Pylon_Transition_Edges)
            Start_and_End_Length_Pylon_Transition_Edges = Regular_1D_Pylon_Transition_Edges.StartEndLength(Smallest_Airfoil_Mesh_Size*2.0,Engine_Mesh_Size,[Edge_363])
            Start_and_End_Length_Pylon_Transition_Edges.SetObjectEntry( 'nasa_crm_igs' )
            Sub_mesh_Pylon_Transition_Edges = Regular_1D_Pylon_Transition_Edges.GetSubMesh()

            # Engine edges
            Regular_1D_Engine = Mesh_Domain.Segment(geom=Auto_group_for_Sub_mesh_Engine_Edges)
            Sub_mesh_Engine_Edges = Regular_1D_Engine.GetSubMesh()
            Local_Length_Engine = Regular_1D_Engine.LocalLength(Engine_Mesh_Size,None,1e-07)

            # Transition
            Regular_1D_Wing_Transition1 = Mesh_Domain.Segment(geom=Edge_wing_transition_1)
            Start_and_End_Length_Wing_Transition_1_Edge = Regular_1D_Wing_Transition1.StartEndLength(Smallest_Airfoil_Mesh_Size,Smallest_Airfoil_Mesh_Size*2.0,[Edge_wing_transition_1])
            Start_and_End_Length_Wing_Transition_1_Edge.SetObjectEntry( 'nasa_crm_igs' )
            Sub_mesh_Wing_Transition_1_Edges = Regular_1D_Wing_Transition1.GetSubMesh()

            Regular_1D_Wing_Transition2 = Mesh_Domain.Segment(geom=Edge_wing_transition_2)
            Start_and_End_Length_Wing_Transition_2_Edge = Regular_1D_Wing_Transition2.StartEndLength(Smallest_Airfoil_Mesh_Size,Biggest_Airfoil_Mesh_Size,[Edge_wing_transition_2])
            Start_and_End_Length_Wing_Transition_2_Edge.SetObjectEntry( 'nasa_crm_igs' )
            Sub_mesh_Wing_Transition_2_Edges = Regular_1D_Wing_Transition2.GetSubMesh()

            # Wing hole edges
            Regular_1D_Wing_Hole_Edge1 = Mesh_Domain.Segment(geom=Edge_wing_hole_1)
            Start_and_End_Length_Wing_Hole_1_Edge = Regular_1D_Wing_Hole_Edge1.StartEndLength(Smallest_Airfoil_Mesh_Size*2.0,Biggest_Airfoil_Mesh_Size,[])
            Start_and_End_Length_Wing_Hole_1_Edge.SetObjectEntry( 'nasa_crm_igs' )
            Sub_mesh_Wing_Hole_1_Edges = Regular_1D_Wing_Hole_Edge1.GetSubMesh()

            Regular_1D_Wing_Hole_Edge2 = Mesh_Domain.Segment(geom=Edge_wing_hole_3)
            Start_and_End_Length_Wing_Hole_2_Edge = Regular_1D_Wing_Hole_Edge2.StartEndLength(Biggest_Airfoil_Mesh_Size,Smallest_Airfoil_Mesh_Size*2.0,[])
            Start_and_End_Length_Wing_Hole_2_Edge.SetObjectEntry( 'nasa_crm_igs' )
            Sub_mesh_Wing_Hole_2_Edges = Regular_1D_Wing_Hole_Edge2.GetSubMesh()

            Regular_1D_Wing_Hole = Mesh_Domain.Segment(geom=Auto_group_for_Sub_mesh_Wing_Hole_Edges)
            Sub_mesh_Wing_Hole_Edges = Regular_1D_Wing_Hole.GetSubMesh()
            Local_Length_Wing_Hole = Regular_1D_Wing_Hole.LocalLength(Biggest_Airfoil_Mesh_Size,None,1e-07)

            # Far field edges
            Regular_1D_Far_Field_Edges = Mesh_Domain.Segment(geom=Auto_group_for_Sub_mesh_Far_Field_Edges)
            Sub_mesh_Far_Field_Edges = Regular_1D_Far_Field_Edges.GetSubMesh()
            Local_Length_Far_Field = Regular_1D_Far_Field_Edges.LocalLength(Far_Field_Mesh_Size,None,1e-07)

            # Wing root up surface
            NETGEN_2D_Wing_Root_Up = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_2D,geom=Face_crm_wing_root_up)
            NETGEN_2D_Parameters_Wing_Root_Up = NETGEN_2D_Wing_Root_Up.Parameters()
            NETGEN_2D_Parameters_Wing_Root_Up.SetMaxSize( Biggest_Airfoil_Mesh_Size )
            NETGEN_2D_Parameters_Wing_Root_Up.SetOptimize( 1 )
            NETGEN_2D_Parameters_Wing_Root_Up.SetFineness( 3 )
            # NETGEN_2D_Parameters_Wing_Root_Up.SetGrowthRate( Growth_Rate_Wing )
            # NETGEN_2D_Parameters_Wing_Root_Up.SetNbSegPerEdge( 6.92154e-310 )
            # NETGEN_2D_Parameters_Wing_Root_Up.SetNbSegPerRadius( 5.32336e-317 )
            NETGEN_2D_Parameters_Wing_Root_Up.SetMinSize( Smallest_Airfoil_Mesh_Size )
            NETGEN_2D_Parameters_Wing_Root_Up.SetUseSurfaceCurvature( 1 )
            NETGEN_2D_Parameters_Wing_Root_Up.SetQuadAllowed( 0 )
            NETGEN_2D_Parameters_Wing_Root_Up.SetSecondOrder( 203 )
            NETGEN_2D_Parameters_Wing_Root_Up.SetFuseEdges( 160 )
            Sub_mesh_Wing_Root_Up_Surface = NETGEN_2D_Wing_Root_Up.GetSubMesh()

            # Wing root down surface
            NETGEN_2D_Wing_Root_Down = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_2D,geom=Face_crm_wing_root_down)
            NETGEN_2D_Parameters_Wing_Root_Down = NETGEN_2D_Wing_Root_Down.Parameters()
            NETGEN_2D_Parameters_Wing_Root_Down.SetMaxSize( Biggest_Airfoil_Mesh_Size )
            NETGEN_2D_Parameters_Wing_Root_Down.SetOptimize( 1 )
            NETGEN_2D_Parameters_Wing_Root_Down.SetFineness( 3 )
            # NETGEN_2D_Parameters_Wing_Root_Down.SetGrowthRate( Growth_Rate_Wing )
            # NETGEN_2D_Parameters_Wing_Root_Down.SetNbSegPerEdge( 6.92154e-310 )
            # NETGEN_2D_Parameters_Wing_Root_Down.SetNbSegPerRadius( 5.32336e-317 )
            NETGEN_2D_Parameters_Wing_Root_Down.SetMinSize( Smallest_Airfoil_Mesh_Size )
            NETGEN_2D_Parameters_Wing_Root_Down.SetUseSurfaceCurvature( 1 )
            NETGEN_2D_Parameters_Wing_Root_Down.SetQuadAllowed( 0 )
            NETGEN_2D_Parameters_Wing_Root_Down.SetSecondOrder( 203 )
            NETGEN_2D_Parameters_Wing_Root_Down.SetFuseEdges( 160 )
            Sub_mesh_Wing_Root_Down_Surface = NETGEN_2D_Wing_Root_Down.GetSubMesh()

            # Wing root down surface2
            NETGEN_2D_Wing_Root_Down2 = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_2D,geom=Face_crm_wing_root_down2)
            NETGEN_2D_Parameters_Wing_Root_Down2 = NETGEN_2D_Wing_Root_Down2.Parameters()
            NETGEN_2D_Parameters_Wing_Root_Down2.SetMaxSize( Biggest_Airfoil_Mesh_Size )
            NETGEN_2D_Parameters_Wing_Root_Down2.SetOptimize( 1 )
            NETGEN_2D_Parameters_Wing_Root_Down2.SetFineness( 3 )
            # NETGEN_2D_Parameters_Wing_Root_Down.SetGrowthRate( Growth_Rate_Wing )
            # NETGEN_2D_Parameters_Wing_Root_Down.SetNbSegPerEdge( 6.92154e-310 )
            # NETGEN_2D_Parameters_Wing_Root_Down.SetNbSegPerRadius( 5.32336e-317 )
            NETGEN_2D_Parameters_Wing_Root_Down2.SetMinSize( Smallest_Airfoil_Mesh_Size )
            NETGEN_2D_Parameters_Wing_Root_Down2.SetUseSurfaceCurvature( 1 )
            NETGEN_2D_Parameters_Wing_Root_Down2.SetQuadAllowed( 0 )
            NETGEN_2D_Parameters_Wing_Root_Down2.SetSecondOrder( 203 )
            NETGEN_2D_Parameters_Wing_Root_Down2.SetFuseEdges( 160 )
            Sub_mesh_Wing_Root_Down_Surface2 = NETGEN_2D_Wing_Root_Down2.GetSubMesh()

            # Wing up surface
            NETGEN_2D_Wing_Up = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_2D,geom=Face_crm_wing_up)
            NETGEN_2D_Parameters_Wing_Up = NETGEN_2D_Wing_Up.Parameters()
            NETGEN_2D_Parameters_Wing_Up.SetMaxSize( Biggest_Airfoil_Mesh_Size )
            NETGEN_2D_Parameters_Wing_Up.SetOptimize( 1 )
            NETGEN_2D_Parameters_Wing_Up.SetFineness( 3 )
            # NETGEN_2D_Parameters_Wing_Up.SetGrowthRate( Growth_Rate_Wing )
            # NETGEN_2D_Parameters_Wing_Up.SetNbSegPerEdge( 6.92154e-310 )
            # NETGEN_2D_Parameters_Wing_Up.SetNbSegPerRadius( 5.32336e-317 )
            NETGEN_2D_Parameters_Wing_Up.SetMinSize( Smallest_Airfoil_Mesh_Size )
            NETGEN_2D_Parameters_Wing_Up.SetUseSurfaceCurvature( 1 )
            NETGEN_2D_Parameters_Wing_Up.SetQuadAllowed( 0 )
            NETGEN_2D_Parameters_Wing_Up.SetSecondOrder( 203 )
            NETGEN_2D_Parameters_Wing_Up.SetFuseEdges( 160 )
            Sub_mesh_Wing_Up_Surface = NETGEN_2D_Wing_Up.GetSubMesh()

            # Wing down surface
            NETGEN_2D_Wing_Down = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_2D,geom=Face_crm_wing_down)
            NETGEN_2D_Parameters_Wing_Down = NETGEN_2D_Wing_Down.Parameters()
            NETGEN_2D_Parameters_Wing_Down.SetMaxSize( Biggest_Airfoil_Mesh_Size )
            NETGEN_2D_Parameters_Wing_Down.SetOptimize( 1 )
            NETGEN_2D_Parameters_Wing_Down.SetFineness( 3 )
            # NETGEN_2D_Parameters_Wing_Down.SetGrowthRate( Growth_Rate_Wing )
            # NETGEN_2D_Parameters_Wing_Down.SetNbSegPerEdge( 6.92154e-310 )
            # NETGEN_2D_Parameters_Wing_Down.SetNbSegPerRadius( 5.32336e-317 )
            NETGEN_2D_Parameters_Wing_Down.SetMinSize( Smallest_Airfoil_Mesh_Size )
            NETGEN_2D_Parameters_Wing_Down.SetUseSurfaceCurvature( 1 )
            NETGEN_2D_Parameters_Wing_Down.SetQuadAllowed( 0 )
            NETGEN_2D_Parameters_Wing_Down.SetSecondOrder( 203 )
            NETGEN_2D_Parameters_Wing_Down.SetFuseEdges( 160 )
            Sub_mesh_Wing_Down_Surface = NETGEN_2D_Wing_Down.GetSubMesh()

            # Wing tail up surface
            NETGEN_2D_Wing_Tail_Up = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_2D,geom=Face_crm_tail_up)
            NETGEN_2D_Parameters_Tail_Up = NETGEN_2D_Wing_Tail_Up.Parameters()
            NETGEN_2D_Parameters_Tail_Up.SetMaxSize( Biggest_Airfoil_Mesh_Size )
            NETGEN_2D_Parameters_Tail_Up.SetOptimize( 1 )
            NETGEN_2D_Parameters_Tail_Up.SetFineness( 5 )
            NETGEN_2D_Parameters_Tail_Up.SetGrowthRate( 0.3 )
            NETGEN_2D_Parameters_Tail_Up.SetNbSegPerEdge( 6.92154e-310 )
            NETGEN_2D_Parameters_Tail_Up.SetNbSegPerRadius( 5.32336e-317 )
            NETGEN_2D_Parameters_Tail_Up.SetMinSize( Smallest_Airfoil_Mesh_Size )
            NETGEN_2D_Parameters_Tail_Up.SetUseSurfaceCurvature( 1 )
            NETGEN_2D_Parameters_Tail_Up.SetQuadAllowed( 0 )
            NETGEN_2D_Parameters_Tail_Up.SetSecondOrder( 203 )
            NETGEN_2D_Parameters_Tail_Up.SetFuseEdges( 160 )
            Sub_mesh_Tail_Up_Surface = NETGEN_2D_Wing_Tail_Up.GetSubMesh()

            # Wing surface
            NETGEN_2D = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_2D,geom=Face_crm_tail_down)
            NETGEN_2D_Parameters_Wing = NETGEN_2D.Parameters()
            NETGEN_2D_Parameters_Wing.SetMaxSize( Biggest_Airfoil_Mesh_Size )
            NETGEN_2D_Parameters_Wing.SetOptimize( 1 )
            NETGEN_2D_Parameters_Wing.SetFineness( 5 )
            NETGEN_2D_Parameters_Wing.SetGrowthRate( 0.3 )
            NETGEN_2D_Parameters_Wing.SetNbSegPerEdge( 6.92154e-310 )
            NETGEN_2D_Parameters_Wing.SetNbSegPerRadius( 5.32336e-317 )
            NETGEN_2D_Parameters_Wing.SetMinSize( Smallest_Airfoil_Mesh_Size )
            NETGEN_2D_Parameters_Wing.SetUseSurfaceCurvature( 1 )
            NETGEN_2D_Parameters_Wing.SetQuadAllowed( 0 )
            NETGEN_2D_Parameters_Wing.SetSecondOrder( 203 )
            NETGEN_2D_Parameters_Wing.SetFuseEdges( 160 )
            Sub_mesh_Wing_Surface = NETGEN_2D.GetSubMesh()

            NETGEN_2D_Tip = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_2D,geom=Auto_group_for_Sub_mesh_Wing_Tail_Tip_Surfaces)
            NETGEN_2D_Parameters_Wing_Tip = NETGEN_2D_Tip.Parameters()
            NETGEN_2D_Parameters_Wing_Tip.SetMaxSize( Wing_Tip_Mesh_Size )
            NETGEN_2D_Parameters_Wing_Tip.SetOptimize( 1 )
            NETGEN_2D_Parameters_Wing_Tip.SetFineness( 5 )
            NETGEN_2D_Parameters_Wing_Tip.SetGrowthRate( Growth_Rate_Wing )
            NETGEN_2D_Parameters_Wing_Tip.SetNbSegPerEdge( 6.92154e-310 )
            NETGEN_2D_Parameters_Wing_Tip.SetNbSegPerRadius( 5.32336e-317 )
            NETGEN_2D_Parameters_Wing_Tip.SetMinSize( Smallest_Airfoil_Mesh_Size )
            NETGEN_2D_Parameters_Wing_Tip.SetUseSurfaceCurvature( 1 )
            NETGEN_2D_Parameters_Wing_Tip.SetQuadAllowed( 0 )
            NETGEN_2D_Parameters_Wing_Tip.SetSecondOrder( 106 )
            NETGEN_2D_Parameters_Wing_Tip.SetFuseEdges( 80 )
            Sub_mesh_Wing_Tip_Surface = NETGEN_2D_Tip.GetSubMesh()

            # Engine surface outlet
            NETGEN_2D_Engine_Outlet = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_2D,geom=Auto_group_for_Sub_mesh_Engine_Outlet_Surfaces)
            NETGEN_2D_Parameters_Engine_Outlet = NETGEN_2D_Engine_Outlet.Parameters()
            NETGEN_2D_Parameters_Engine_Outlet.SetMaxSize( Engine_Trailing_Edge_Size )
            NETGEN_2D_Parameters_Engine_Outlet.SetOptimize( 1 )
            NETGEN_2D_Parameters_Engine_Outlet.SetFineness( 5 )
            NETGEN_2D_Parameters_Engine_Outlet.SetGrowthRate( 0.1 )
            NETGEN_2D_Parameters_Engine_Outlet.SetNbSegPerEdge( 6.92154e-310 )
            NETGEN_2D_Parameters_Engine_Outlet.SetNbSegPerRadius( 5.32336e-317 )
            NETGEN_2D_Parameters_Engine_Outlet.SetMinSize( Engine_Trailing_Edge_Size )
            NETGEN_2D_Parameters_Engine_Outlet.SetUseSurfaceCurvature( 1 )
            NETGEN_2D_Parameters_Engine_Outlet.SetQuadAllowed( 0 )
            NETGEN_2D_Parameters_Engine_Outlet.SetSecondOrder( 106 )
            NETGEN_2D_Parameters_Engine_Outlet.SetFuseEdges( 80 )
            Sub_mesh_Engine_Outlet_Surface = NETGEN_2D_Engine_Outlet.GetSubMesh()

            # Trailing edges surface
            NETGEN_2D_Trailing_Edges = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_2D,geom=Auto_group_for_Sub_mesh_Trailing_Edge_Surfaces)
            NETGEN_2D_Parameters_Trailing_Edges = NETGEN_2D_Trailing_Edges.Parameters()
            NETGEN_2D_Parameters_Trailing_Edges.SetMaxSize( Smallest_Airfoil_Mesh_Size )
            NETGEN_2D_Parameters_Trailing_Edges.SetOptimize( 1 )
            NETGEN_2D_Parameters_Trailing_Edges.SetFineness( 5 )
            NETGEN_2D_Parameters_Trailing_Edges.SetGrowthRate( Growth_Rate_Wing )
            NETGEN_2D_Parameters_Trailing_Edges.SetNbSegPerEdge( 6.92154e-310 )
            NETGEN_2D_Parameters_Trailing_Edges.SetNbSegPerRadius( 5.32336e-317 )
            NETGEN_2D_Parameters_Trailing_Edges.SetMinSize( Smallest_Airfoil_Mesh_Size )
            NETGEN_2D_Parameters_Trailing_Edges.SetUseSurfaceCurvature( 1 )
            NETGEN_2D_Parameters_Trailing_Edges.SetQuadAllowed( 0 )
            NETGEN_2D_Parameters_Trailing_Edges.SetSecondOrder( 106 )
            NETGEN_2D_Parameters_Trailing_Edges.SetFuseEdges( 80 )
            Sub_mesh_Trailing_Edge_Surface = NETGEN_2D_Trailing_Edges.GetSubMesh()

            # Fuselage surface
            NETGEN_2D_Fuselage = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_2D,geom=Auto_group_for_Sub_mesh_Fuselage_Surfaces)
            NETGEN_2D_Parameters_Fuselage = NETGEN_2D_Fuselage.Parameters()
            NETGEN_2D_Parameters_Fuselage.SetMaxSize( Fuselage_Mesh_Size )
            NETGEN_2D_Parameters_Fuselage.SetOptimize( 1 )
            NETGEN_2D_Parameters_Fuselage.SetFineness( 5 )
            NETGEN_2D_Parameters_Fuselage.SetGrowthRate( 0.3 )
            NETGEN_2D_Parameters_Fuselage.SetNbSegPerEdge( 6.92154e-310 )
            NETGEN_2D_Parameters_Fuselage.SetNbSegPerRadius( 5.32336e-317 )
            NETGEN_2D_Parameters_Fuselage.SetMinSize( 0.005 )
            NETGEN_2D_Parameters_Fuselage.SetUseSurfaceCurvature( 1 )
            NETGEN_2D_Parameters_Fuselage.SetQuadAllowed( 0 )
            NETGEN_2D_Parameters_Fuselage.SetSecondOrder( 106 )
            NETGEN_2D_Parameters_Fuselage.SetFuseEdges( 80 )
            Sub_mesh_Fuselage_Surface = NETGEN_2D_Fuselage.GetSubMesh()

            # Engine surface
            NETGEN_2D_Engine1 = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_2D,geom=Face_crm_engine_1)
            NETGEN_2D_Parameters_Engine1 = NETGEN_2D_Engine1.Parameters()
            NETGEN_2D_Parameters_Engine1.SetMaxSize( Engine_Mesh_Size )
            NETGEN_2D_Parameters_Engine1.SetOptimize( 1 )
            NETGEN_2D_Parameters_Engine1.SetFineness( 5 )
            NETGEN_2D_Parameters_Engine1.SetGrowthRate( Growth_Rate_Engine )
            NETGEN_2D_Parameters_Engine1.SetNbSegPerEdge( 6.92154e-310 )
            NETGEN_2D_Parameters_Engine1.SetNbSegPerRadius( 5.32336e-317 )
            NETGEN_2D_Parameters_Engine1.SetMinSize( Engine_Trailing_Edge_Size )
            NETGEN_2D_Parameters_Engine1.SetUseSurfaceCurvature( 1 )
            NETGEN_2D_Parameters_Engine1.SetQuadAllowed( 0 )
            NETGEN_2D_Parameters_Engine1.SetSecondOrder( 106 )
            NETGEN_2D_Parameters_Engine1.SetFuseEdges( 80 )
            Sub_mesh_Engine_Surface1 = NETGEN_2D_Engine1.GetSubMesh()

            NETGEN_2D_Engine2 = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_2D,geom=Face_crm_engine_2)
            NETGEN_2D_Parameters_Engine2 = NETGEN_2D_Engine2.Parameters()
            NETGEN_2D_Parameters_Engine2.SetMaxSize( Engine_Mesh_Size )
            NETGEN_2D_Parameters_Engine2.SetOptimize( 1 )
            NETGEN_2D_Parameters_Engine2.SetFineness( 5 )
            NETGEN_2D_Parameters_Engine2.SetGrowthRate( Growth_Rate_Engine )
            NETGEN_2D_Parameters_Engine2.SetNbSegPerEdge( 6.92154e-310 )
            NETGEN_2D_Parameters_Engine2.SetNbSegPerRadius( 5.32336e-317 )
            NETGEN_2D_Parameters_Engine2.SetMinSize( Engine_Trailing_Edge_Size )
            NETGEN_2D_Parameters_Engine2.SetUseSurfaceCurvature( 1 )
            NETGEN_2D_Parameters_Engine2.SetQuadAllowed( 0 )
            NETGEN_2D_Parameters_Engine2.SetSecondOrder( 106 )
            NETGEN_2D_Parameters_Engine2.SetFuseEdges( 80 )
            Sub_mesh_Engine_Surface2 = NETGEN_2D_Engine2.GetSubMesh()

            NETGEN_2D_Engine3 = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_2D,geom=Face_crm_engine_3)
            NETGEN_2D_Parameters_Engine3 = NETGEN_2D_Engine3.Parameters()
            NETGEN_2D_Parameters_Engine3.SetMaxSize( Engine_Mesh_Size )
            NETGEN_2D_Parameters_Engine3.SetOptimize( 1 )
            NETGEN_2D_Parameters_Engine3.SetFineness( 5 )
            NETGEN_2D_Parameters_Engine3.SetGrowthRate( Growth_Rate_Engine )
            NETGEN_2D_Parameters_Engine3.SetNbSegPerEdge( 6.92154e-310 )
            NETGEN_2D_Parameters_Engine3.SetNbSegPerRadius( 5.32336e-317 )
            NETGEN_2D_Parameters_Engine3.SetMinSize( Engine_Trailing_Edge_Size )
            NETGEN_2D_Parameters_Engine3.SetUseSurfaceCurvature( 1 )
            NETGEN_2D_Parameters_Engine3.SetQuadAllowed( 0 )
            NETGEN_2D_Parameters_Engine3.SetSecondOrder( 106 )
            NETGEN_2D_Parameters_Engine3.SetFuseEdges( 80 )
            Sub_mesh_Engine_Surface3 = NETGEN_2D_Engine3.GetSubMesh()

            NETGEN_2D_Engine4 = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_2D,geom=Face_crm_engine_4)
            NETGEN_2D_Parameters_Engine4 = NETGEN_2D_Engine4.Parameters()
            NETGEN_2D_Parameters_Engine4.SetMaxSize( Engine_Mesh_Size )
            NETGEN_2D_Parameters_Engine4.SetOptimize( 1 )
            NETGEN_2D_Parameters_Engine4.SetFineness( 5 )
            NETGEN_2D_Parameters_Engine4.SetGrowthRate( Growth_Rate_Engine )
            NETGEN_2D_Parameters_Engine4.SetNbSegPerEdge( 6.92154e-310 )
            NETGEN_2D_Parameters_Engine4.SetNbSegPerRadius( 5.32336e-317 )
            NETGEN_2D_Parameters_Engine4.SetMinSize( Engine_Trailing_Edge_Size )
            NETGEN_2D_Parameters_Engine4.SetUseSurfaceCurvature( 1 )
            NETGEN_2D_Parameters_Engine4.SetQuadAllowed( 0 )
            NETGEN_2D_Parameters_Engine4.SetSecondOrder( 106 )
            NETGEN_2D_Parameters_Engine4.SetFuseEdges( 80 )
            Sub_mesh_Engine_Surface4 = NETGEN_2D_Engine4.GetSubMesh()

            NETGEN_2D_Engine5 = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_2D,geom=Face_crm_engine_5)
            NETGEN_2D_Parameters_Engine5 = NETGEN_2D_Engine5.Parameters()
            NETGEN_2D_Parameters_Engine5.SetMaxSize( Engine_Mesh_Size )
            NETGEN_2D_Parameters_Engine5.SetOptimize( 1 )
            NETGEN_2D_Parameters_Engine5.SetFineness( 5 )
            NETGEN_2D_Parameters_Engine5.SetGrowthRate( Growth_Rate_Engine )
            NETGEN_2D_Parameters_Engine5.SetNbSegPerEdge( 6.92154e-310 )
            NETGEN_2D_Parameters_Engine5.SetNbSegPerRadius( 5.32336e-317 )
            NETGEN_2D_Parameters_Engine5.SetMinSize( Engine_Trailing_Edge_Size )
            NETGEN_2D_Parameters_Engine5.SetUseSurfaceCurvature( 1 )
            NETGEN_2D_Parameters_Engine5.SetQuadAllowed( 0 )
            NETGEN_2D_Parameters_Engine5.SetSecondOrder( 106 )
            NETGEN_2D_Parameters_Engine5.SetFuseEdges( 80 )
            Sub_mesh_Engine_Surface5 = NETGEN_2D_Engine5.GetSubMesh()

            NETGEN_2D_Engine6 = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_2D,geom=Face_crm_engine_6)
            NETGEN_2D_Parameters_Engine6 = NETGEN_2D_Engine6.Parameters()
            NETGEN_2D_Parameters_Engine6.SetMaxSize( Engine_Mesh_Size )
            NETGEN_2D_Parameters_Engine6.SetOptimize( 1 )
            NETGEN_2D_Parameters_Engine6.SetFineness( 5 )
            NETGEN_2D_Parameters_Engine6.SetGrowthRate( Growth_Rate_Engine )
            NETGEN_2D_Parameters_Engine6.SetNbSegPerEdge( 6.92154e-310 )
            NETGEN_2D_Parameters_Engine6.SetNbSegPerRadius( 5.32336e-317 )
            NETGEN_2D_Parameters_Engine6.SetMinSize( Engine_Trailing_Edge_Size )
            NETGEN_2D_Parameters_Engine6.SetUseSurfaceCurvature( 1 )
            NETGEN_2D_Parameters_Engine6.SetQuadAllowed( 0 )
            NETGEN_2D_Parameters_Engine6.SetSecondOrder( 106 )
            NETGEN_2D_Parameters_Engine6.SetFuseEdges( 80 )
            Sub_mesh_Engine_Surface6 = NETGEN_2D_Engine6.GetSubMesh()

            NETGEN_2D_Engine7 = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_2D,geom=Face_crm_engine_7)
            NETGEN_2D_Parameters_Engine7 = NETGEN_2D_Engine7.Parameters()
            NETGEN_2D_Parameters_Engine7.SetMaxSize( Engine_Mesh_Size )
            NETGEN_2D_Parameters_Engine7.SetOptimize( 1 )
            NETGEN_2D_Parameters_Engine7.SetFineness( 5 )
            NETGEN_2D_Parameters_Engine7.SetGrowthRate( Growth_Rate_Engine )
            NETGEN_2D_Parameters_Engine7.SetNbSegPerEdge( 6.92154e-310 )
            NETGEN_2D_Parameters_Engine7.SetNbSegPerRadius( 5.32336e-317 )
            NETGEN_2D_Parameters_Engine7.SetMinSize( Engine_Trailing_Edge_Size )
            NETGEN_2D_Parameters_Engine7.SetUseSurfaceCurvature( 1 )
            NETGEN_2D_Parameters_Engine7.SetQuadAllowed( 0 )
            NETGEN_2D_Parameters_Engine7.SetSecondOrder( 106 )
            NETGEN_2D_Parameters_Engine7.SetFuseEdges( 80 )
            Sub_mesh_Engine_Surface7 = NETGEN_2D_Engine7.GetSubMesh()

            NETGEN_2D_Engine8 = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_2D,geom=Face_crm_engine_8)
            NETGEN_2D_Parameters_Engine8 = NETGEN_2D_Engine8.Parameters()
            NETGEN_2D_Parameters_Engine8.SetMaxSize( Engine_Mesh_Size )
            NETGEN_2D_Parameters_Engine8.SetOptimize( 1 )
            NETGEN_2D_Parameters_Engine8.SetFineness( 5 )
            NETGEN_2D_Parameters_Engine8.SetGrowthRate( Growth_Rate_Engine )
            NETGEN_2D_Parameters_Engine8.SetNbSegPerEdge( 6.92154e-310 )
            NETGEN_2D_Parameters_Engine8.SetNbSegPerRadius( 5.32336e-317 )
            NETGEN_2D_Parameters_Engine8.SetMinSize( Engine_Trailing_Edge_Size )
            NETGEN_2D_Parameters_Engine8.SetUseSurfaceCurvature( 1 )
            NETGEN_2D_Parameters_Engine8.SetQuadAllowed( 0 )
            NETGEN_2D_Parameters_Engine8.SetSecondOrder( 106 )
            NETGEN_2D_Parameters_Engine8.SetFuseEdges( 80 )
            Sub_mesh_Engine_Surface8 = NETGEN_2D_Engine8.GetSubMesh()

            NETGEN_2D_Engine9 = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_2D,geom=Face_crm_engine_9)
            NETGEN_2D_Parameters_Engine9 = NETGEN_2D_Engine9.Parameters()
            NETGEN_2D_Parameters_Engine9.SetMaxSize( Engine_Mesh_Size )
            NETGEN_2D_Parameters_Engine9.SetOptimize( 1 )
            NETGEN_2D_Parameters_Engine9.SetFineness( 5 )
            NETGEN_2D_Parameters_Engine9.SetGrowthRate( Growth_Rate_Engine )
            NETGEN_2D_Parameters_Engine9.SetNbSegPerEdge( 6.92154e-310 )
            NETGEN_2D_Parameters_Engine9.SetNbSegPerRadius( 5.32336e-317 )
            NETGEN_2D_Parameters_Engine9.SetMinSize( Engine_Trailing_Edge_Size )
            NETGEN_2D_Parameters_Engine9.SetUseSurfaceCurvature( 1 )
            NETGEN_2D_Parameters_Engine9.SetQuadAllowed( 0 )
            NETGEN_2D_Parameters_Engine9.SetSecondOrder( 106 )
            NETGEN_2D_Parameters_Engine9.SetFuseEdges( 80 )
            Sub_mesh_Engine_Surface9 = NETGEN_2D_Engine9.GetSubMesh()

            NETGEN_2D_Engine10 = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_2D,geom=Face_crm_engine_10)
            NETGEN_2D_Parameters_Engine10 = NETGEN_2D_Engine10.Parameters()
            NETGEN_2D_Parameters_Engine10.SetMaxSize( Engine_Mesh_Size )
            NETGEN_2D_Parameters_Engine10.SetOptimize( 1 )
            NETGEN_2D_Parameters_Engine10.SetFineness( 5 )
            NETGEN_2D_Parameters_Engine10.SetGrowthRate( Growth_Rate_Engine )
            NETGEN_2D_Parameters_Engine10.SetNbSegPerEdge( 6.92154e-310 )
            NETGEN_2D_Parameters_Engine10.SetNbSegPerRadius( 5.32336e-317 )
            NETGEN_2D_Parameters_Engine10.SetMinSize( Engine_Trailing_Edge_Size )
            NETGEN_2D_Parameters_Engine10.SetUseSurfaceCurvature( 1 )
            NETGEN_2D_Parameters_Engine10.SetQuadAllowed( 0 )
            NETGEN_2D_Parameters_Engine10.SetSecondOrder( 106 )
            NETGEN_2D_Parameters_Engine10.SetFuseEdges( 80 )
            Sub_mesh_Engine_Surface10 = NETGEN_2D_Engine10.GetSubMesh()

            NETGEN_2D_Engine11 = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_2D,geom=Face_crm_engine_11)
            NETGEN_2D_Parameters_Engine11 = NETGEN_2D_Engine11.Parameters()
            NETGEN_2D_Parameters_Engine11.SetMaxSize( Engine_Mesh_Size )
            NETGEN_2D_Parameters_Engine11.SetOptimize( 1 )
            NETGEN_2D_Parameters_Engine11.SetFineness( 5 )
            NETGEN_2D_Parameters_Engine11.SetGrowthRate( Growth_Rate_Engine )
            NETGEN_2D_Parameters_Engine11.SetNbSegPerEdge( 6.92154e-310 )
            NETGEN_2D_Parameters_Engine11.SetNbSegPerRadius( 5.32336e-317 )
            NETGEN_2D_Parameters_Engine11.SetMinSize( Engine_Trailing_Edge_Size )
            NETGEN_2D_Parameters_Engine11.SetUseSurfaceCurvature( 1 )
            NETGEN_2D_Parameters_Engine11.SetQuadAllowed( 0 )
            NETGEN_2D_Parameters_Engine11.SetSecondOrder( 106 )
            NETGEN_2D_Parameters_Engine11.SetFuseEdges( 80 )
            Sub_mesh_Engine_Surface11 = NETGEN_2D_Engine11.GetSubMesh()

            NETGEN_2D_Engine12 = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_2D,geom=Face_crm_engine_12)
            NETGEN_2D_Parameters_Engine12 = NETGEN_2D_Engine12.Parameters()
            NETGEN_2D_Parameters_Engine12.SetMaxSize( Engine_Mesh_Size )
            NETGEN_2D_Parameters_Engine12.SetOptimize( 1 )
            NETGEN_2D_Parameters_Engine12.SetFineness( 5 )
            NETGEN_2D_Parameters_Engine12.SetGrowthRate( Growth_Rate_Engine )
            NETGEN_2D_Parameters_Engine12.SetNbSegPerEdge( 6.92154e-310 )
            NETGEN_2D_Parameters_Engine12.SetNbSegPerRadius( 5.32336e-317 )
            NETGEN_2D_Parameters_Engine12.SetMinSize( Engine_Trailing_Edge_Size )
            NETGEN_2D_Parameters_Engine12.SetUseSurfaceCurvature( 1 )
            NETGEN_2D_Parameters_Engine12.SetQuadAllowed( 0 )
            NETGEN_2D_Parameters_Engine12.SetSecondOrder( 106 )
            NETGEN_2D_Parameters_Engine12.SetFuseEdges( 80 )
            Sub_mesh_Engine_Surface12 = NETGEN_2D_Engine12.GetSubMesh()

            NETGEN_2D_Pylon1 = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_2D,geom=Face_crm_pylon_1)
            NETGEN_2D_Parameters_Pylon1 = NETGEN_2D_Pylon1.Parameters()
            NETGEN_2D_Parameters_Pylon1.SetMaxSize( Engine_Mesh_Size )
            NETGEN_2D_Parameters_Pylon1.SetOptimize( 1 )
            NETGEN_2D_Parameters_Pylon1.SetFineness( 5 )
            NETGEN_2D_Parameters_Pylon1.SetGrowthRate( Growth_Rate_Engine )
            NETGEN_2D_Parameters_Pylon1.SetNbSegPerEdge( 6.92154e-310 )
            NETGEN_2D_Parameters_Pylon1.SetNbSegPerRadius( 5.32336e-317 )
            NETGEN_2D_Parameters_Pylon1.SetMinSize( Engine_Trailing_Edge_Size )
            NETGEN_2D_Parameters_Pylon1.SetUseSurfaceCurvature( 1 )
            NETGEN_2D_Parameters_Pylon1.SetQuadAllowed( 0 )
            NETGEN_2D_Parameters_Pylon1.SetSecondOrder( 106 )
            NETGEN_2D_Parameters_Pylon1.SetFuseEdges( 80 )
            Sub_mesh_Pylon_Surface1 = NETGEN_2D_Pylon1.GetSubMesh()

            NETGEN_2D_Pylon2 = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_2D,geom=Face_crm_pylon_2)
            NETGEN_2D_Parameters_Pylon2 = NETGEN_2D_Pylon2.Parameters()
            NETGEN_2D_Parameters_Pylon2.SetMaxSize( Engine_Mesh_Size )
            NETGEN_2D_Parameters_Pylon2.SetOptimize( 1 )
            NETGEN_2D_Parameters_Pylon2.SetFineness( 5 )
            NETGEN_2D_Parameters_Pylon2.SetGrowthRate( Growth_Rate_Engine )
            NETGEN_2D_Parameters_Pylon2.SetNbSegPerEdge( 6.92154e-310 )
            NETGEN_2D_Parameters_Pylon2.SetNbSegPerRadius( 5.32336e-317 )
            NETGEN_2D_Parameters_Pylon2.SetMinSize( Engine_Trailing_Edge_Size )
            NETGEN_2D_Parameters_Pylon2.SetUseSurfaceCurvature( 1 )
            NETGEN_2D_Parameters_Pylon2.SetQuadAllowed( 0 )
            NETGEN_2D_Parameters_Pylon2.SetSecondOrder( 106 )
            NETGEN_2D_Parameters_Pylon2.SetFuseEdges( 80 )
            Sub_mesh_Pylon_Surface2 = NETGEN_2D_Pylon2.GetSubMesh()

            NETGEN_2D_Pylon3 = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_2D,geom=Face_crm_pylon_3)
            NETGEN_2D_Parameters_Pylon3 = NETGEN_2D_Pylon3.Parameters()
            NETGEN_2D_Parameters_Pylon3.SetMaxSize( Engine_Mesh_Size )
            NETGEN_2D_Parameters_Pylon3.SetOptimize( 1 )
            NETGEN_2D_Parameters_Pylon3.SetFineness( 5 )
            NETGEN_2D_Parameters_Pylon3.SetGrowthRate( Growth_Rate_Engine )
            NETGEN_2D_Parameters_Pylon3.SetNbSegPerEdge( 6.92154e-310 )
            NETGEN_2D_Parameters_Pylon3.SetNbSegPerRadius( 5.32336e-317 )
            NETGEN_2D_Parameters_Pylon3.SetMinSize( Engine_Trailing_Edge_Size )
            NETGEN_2D_Parameters_Pylon3.SetUseSurfaceCurvature( 1 )
            NETGEN_2D_Parameters_Pylon3.SetQuadAllowed( 0 )
            NETGEN_2D_Parameters_Pylon3.SetSecondOrder( 106 )
            NETGEN_2D_Parameters_Pylon3.SetFuseEdges( 80 )
            Sub_mesh_Pylon_Surface3 = NETGEN_2D_Pylon3.GetSubMesh()

            NETGEN_2D_Pylon4 = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_2D,geom=Face_crm_pylon_4)
            NETGEN_2D_Parameters_Pylon4 = NETGEN_2D_Pylon4.Parameters()
            NETGEN_2D_Parameters_Pylon4.SetMaxSize( Engine_Mesh_Size )
            NETGEN_2D_Parameters_Pylon4.SetOptimize( 1 )
            NETGEN_2D_Parameters_Pylon4.SetFineness( 5 )
            NETGEN_2D_Parameters_Pylon4.SetGrowthRate( Growth_Rate_Engine )
            NETGEN_2D_Parameters_Pylon4.SetNbSegPerEdge( 6.92154e-310 )
            NETGEN_2D_Parameters_Pylon4.SetNbSegPerRadius( 5.32336e-317 )
            NETGEN_2D_Parameters_Pylon4.SetMinSize( Engine_Trailing_Edge_Size )
            NETGEN_2D_Parameters_Pylon4.SetUseSurfaceCurvature( 1 )
            NETGEN_2D_Parameters_Pylon4.SetQuadAllowed( 0 )
            NETGEN_2D_Parameters_Pylon4.SetSecondOrder( 106 )
            NETGEN_2D_Parameters_Pylon4.SetFuseEdges( 80 )
            Sub_mesh_Pylon_Surface4 = NETGEN_2D_Pylon4.GetSubMesh()

            NETGEN_2D_Pylon7 = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_2D,geom=Face_crm_pylon_7)
            NETGEN_2D_Parameters_Pylon7 = NETGEN_2D_Pylon7.Parameters()
            NETGEN_2D_Parameters_Pylon7.SetMaxSize( Engine_Mesh_Size )
            NETGEN_2D_Parameters_Pylon7.SetOptimize( 1 )
            NETGEN_2D_Parameters_Pylon7.SetFineness( 5 )
            NETGEN_2D_Parameters_Pylon7.SetGrowthRate( Growth_Rate_Engine )
            NETGEN_2D_Parameters_Pylon7.SetNbSegPerEdge( 6.92154e-310 )
            NETGEN_2D_Parameters_Pylon7.SetNbSegPerRadius( 5.32336e-317 )
            NETGEN_2D_Parameters_Pylon7.SetMinSize( Engine_Trailing_Edge_Size )
            NETGEN_2D_Parameters_Pylon7.SetUseSurfaceCurvature( 1 )
            NETGEN_2D_Parameters_Pylon7.SetQuadAllowed( 0 )
            NETGEN_2D_Parameters_Pylon7.SetSecondOrder( 106 )
            NETGEN_2D_Parameters_Pylon7.SetFuseEdges( 80 )
            Sub_mesh_Pylon_Surface7 = NETGEN_2D_Pylon7.GetSubMesh()

            NETGEN_2D_Pylon8 = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_2D,geom=Face_crm_pylon_8)
            NETGEN_2D_Parameters_Pylon8 = NETGEN_2D_Pylon8.Parameters()
            NETGEN_2D_Parameters_Pylon8.SetMaxSize( Engine_Mesh_Size )
            NETGEN_2D_Parameters_Pylon8.SetOptimize( 1 )
            NETGEN_2D_Parameters_Pylon8.SetFineness( 5 )
            NETGEN_2D_Parameters_Pylon8.SetGrowthRate( Growth_Rate_Engine )
            NETGEN_2D_Parameters_Pylon8.SetNbSegPerEdge( 6.92154e-310 )
            NETGEN_2D_Parameters_Pylon8.SetNbSegPerRadius( 5.32336e-317 )
            NETGEN_2D_Parameters_Pylon8.SetMinSize( Engine_Trailing_Edge_Size )
            NETGEN_2D_Parameters_Pylon8.SetUseSurfaceCurvature( 1 )
            NETGEN_2D_Parameters_Pylon8.SetQuadAllowed( 0 )
            NETGEN_2D_Parameters_Pylon8.SetSecondOrder( 106 )
            NETGEN_2D_Parameters_Pylon8.SetFuseEdges( 80 )
            Sub_mesh_Pylon_Surface8 = NETGEN_2D_Pylon8.GetSubMesh()

            NETGEN_2D_Pylon9 = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_2D,geom=Face_crm_pylon_9)
            NETGEN_2D_Parameters_Pylon9 = NETGEN_2D_Pylon9.Parameters()
            NETGEN_2D_Parameters_Pylon9.SetMaxSize( Engine_Mesh_Size )
            NETGEN_2D_Parameters_Pylon9.SetOptimize( 1 )
            NETGEN_2D_Parameters_Pylon9.SetFineness( 5 )
            NETGEN_2D_Parameters_Pylon9.SetGrowthRate( Growth_Rate_Engine )
            NETGEN_2D_Parameters_Pylon9.SetNbSegPerEdge( 6.92154e-310 )
            NETGEN_2D_Parameters_Pylon9.SetNbSegPerRadius( 5.32336e-317 )
            NETGEN_2D_Parameters_Pylon9.SetMinSize( Engine_Trailing_Edge_Size )
            NETGEN_2D_Parameters_Pylon9.SetUseSurfaceCurvature( 1 )
            NETGEN_2D_Parameters_Pylon9.SetQuadAllowed( 0 )
            NETGEN_2D_Parameters_Pylon9.SetSecondOrder( 106 )
            NETGEN_2D_Parameters_Pylon9.SetFuseEdges( 80 )
            Sub_mesh_Pylon_Surface9 = NETGEN_2D_Pylon9.GetSubMesh()

            NETGEN_2D_Pylon10 = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_2D,geom=Face_crm_pylon_10)
            NETGEN_2D_Parameters_Pylon10 = NETGEN_2D_Pylon10.Parameters()
            NETGEN_2D_Parameters_Pylon10.SetMaxSize( Engine_Mesh_Size )
            NETGEN_2D_Parameters_Pylon10.SetOptimize( 1 )
            NETGEN_2D_Parameters_Pylon10.SetFineness( 5 )
            NETGEN_2D_Parameters_Pylon10.SetGrowthRate( Growth_Rate_Engine )
            NETGEN_2D_Parameters_Pylon10.SetNbSegPerEdge( 6.92154e-310 )
            NETGEN_2D_Parameters_Pylon10.SetNbSegPerRadius( 5.32336e-317 )
            NETGEN_2D_Parameters_Pylon10.SetMinSize( Engine_Trailing_Edge_Size )
            NETGEN_2D_Parameters_Pylon10.SetUseSurfaceCurvature( 1 )
            NETGEN_2D_Parameters_Pylon10.SetQuadAllowed( 0 )
            NETGEN_2D_Parameters_Pylon10.SetSecondOrder( 106 )
            NETGEN_2D_Parameters_Pylon10.SetFuseEdges( 80 )
            Sub_mesh_Pylon_Surface10 = NETGEN_2D_Pylon10.GetSubMesh()

            NETGEN_2D_Pylon11 = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_2D,geom=Face_crm_pylon_11)
            NETGEN_2D_Parameters_Pylon11 = NETGEN_2D_Pylon11.Parameters()
            NETGEN_2D_Parameters_Pylon11.SetMaxSize( Engine_Mesh_Size )
            NETGEN_2D_Parameters_Pylon11.SetOptimize( 1 )
            NETGEN_2D_Parameters_Pylon11.SetFineness( 5 )
            NETGEN_2D_Parameters_Pylon11.SetGrowthRate( Growth_Rate_Engine )
            NETGEN_2D_Parameters_Pylon11.SetNbSegPerEdge( 6.92154e-310 )
            NETGEN_2D_Parameters_Pylon11.SetNbSegPerRadius( 5.32336e-317 )
            NETGEN_2D_Parameters_Pylon11.SetMinSize( Engine_Trailing_Edge_Size )
            NETGEN_2D_Parameters_Pylon11.SetUseSurfaceCurvature( 1 )
            NETGEN_2D_Parameters_Pylon11.SetQuadAllowed( 0 )
            NETGEN_2D_Parameters_Pylon11.SetSecondOrder( 106 )
            NETGEN_2D_Parameters_Pylon11.SetFuseEdges( 80 )
            Sub_mesh_Pylon_Surface11 = NETGEN_2D_Pylon11.GetSubMesh()

            NETGEN_2D_Pylon12 = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_2D,geom=Face_crm_pylon_12)
            NETGEN_2D_Parameters_Pylon12 = NETGEN_2D_Pylon12.Parameters()
            NETGEN_2D_Parameters_Pylon12.SetMaxSize( Engine_Mesh_Size )
            NETGEN_2D_Parameters_Pylon12.SetOptimize( 1 )
            NETGEN_2D_Parameters_Pylon12.SetFineness( 5 )
            NETGEN_2D_Parameters_Pylon12.SetGrowthRate( Growth_Rate_Engine )
            NETGEN_2D_Parameters_Pylon12.SetNbSegPerEdge( 6.92154e-310 )
            NETGEN_2D_Parameters_Pylon12.SetNbSegPerRadius( 5.32336e-317 )
            NETGEN_2D_Parameters_Pylon12.SetMinSize( Engine_Trailing_Edge_Size )
            NETGEN_2D_Parameters_Pylon12.SetUseSurfaceCurvature( 1 )
            NETGEN_2D_Parameters_Pylon12.SetQuadAllowed( 0 )
            NETGEN_2D_Parameters_Pylon12.SetSecondOrder( 106 )
            NETGEN_2D_Parameters_Pylon12.SetFuseEdges( 80 )
            Sub_mesh_Pylon_Surface12 = NETGEN_2D_Pylon12.GetSubMesh()

            NETGEN_2D_Pylon13 = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_2D,geom=Face_crm_pylon_13)
            NETGEN_2D_Parameters_Pylon13 = NETGEN_2D_Pylon13.Parameters()
            NETGEN_2D_Parameters_Pylon13.SetMaxSize( Engine_Mesh_Size )
            NETGEN_2D_Parameters_Pylon13.SetOptimize( 1 )
            NETGEN_2D_Parameters_Pylon13.SetFineness( 5 )
            NETGEN_2D_Parameters_Pylon13.SetGrowthRate( Growth_Rate_Engine )
            NETGEN_2D_Parameters_Pylon13.SetNbSegPerEdge( 6.92154e-310 )
            NETGEN_2D_Parameters_Pylon13.SetNbSegPerRadius( 5.32336e-317 )
            NETGEN_2D_Parameters_Pylon13.SetMinSize( Engine_Trailing_Edge_Size )
            NETGEN_2D_Parameters_Pylon13.SetUseSurfaceCurvature( 1 )
            NETGEN_2D_Parameters_Pylon13.SetQuadAllowed( 0 )
            NETGEN_2D_Parameters_Pylon13.SetSecondOrder( 106 )
            NETGEN_2D_Parameters_Pylon13.SetFuseEdges( 80 )
            Sub_mesh_Pylon_Surface13 = NETGEN_2D_Pylon13.GetSubMesh()

            NETGEN_2D_Pylon14 = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_2D,geom=Face_crm_pylon_14)
            NETGEN_2D_Parameters_Pylon14 = NETGEN_2D_Pylon14.Parameters()
            NETGEN_2D_Parameters_Pylon14.SetMaxSize( Engine_Mesh_Size )
            NETGEN_2D_Parameters_Pylon14.SetOptimize( 1 )
            NETGEN_2D_Parameters_Pylon14.SetFineness( 5 )
            NETGEN_2D_Parameters_Pylon14.SetGrowthRate( Growth_Rate_Engine )
            NETGEN_2D_Parameters_Pylon14.SetNbSegPerEdge( 6.92154e-310 )
            NETGEN_2D_Parameters_Pylon14.SetNbSegPerRadius( 5.32336e-317 )
            NETGEN_2D_Parameters_Pylon14.SetMinSize( Engine_Trailing_Edge_Size )
            NETGEN_2D_Parameters_Pylon14.SetUseSurfaceCurvature( 1 )
            NETGEN_2D_Parameters_Pylon14.SetQuadAllowed( 0 )
            NETGEN_2D_Parameters_Pylon14.SetSecondOrder( 106 )
            NETGEN_2D_Parameters_Pylon14.SetFuseEdges( 80 )
            Sub_mesh_Pylon_Surface14 = NETGEN_2D_Pylon14.GetSubMesh()

            NETGEN_2D_Pylon15 = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_2D,geom=Face_crm_pylon_15)
            NETGEN_2D_Parameters_Pylon15 = NETGEN_2D_Pylon15.Parameters()
            NETGEN_2D_Parameters_Pylon15.SetMaxSize( Engine_Mesh_Size )
            NETGEN_2D_Parameters_Pylon15.SetOptimize( 1 )
            NETGEN_2D_Parameters_Pylon15.SetFineness( 5 )
            NETGEN_2D_Parameters_Pylon15.SetGrowthRate( Growth_Rate_Engine )
            NETGEN_2D_Parameters_Pylon15.SetNbSegPerEdge( 6.92154e-310 )
            NETGEN_2D_Parameters_Pylon15.SetNbSegPerRadius( 5.32336e-317 )
            NETGEN_2D_Parameters_Pylon15.SetMinSize( Engine_Trailing_Edge_Size )
            NETGEN_2D_Parameters_Pylon15.SetUseSurfaceCurvature( 1 )
            NETGEN_2D_Parameters_Pylon15.SetQuadAllowed( 0 )
            NETGEN_2D_Parameters_Pylon15.SetSecondOrder( 106 )
            NETGEN_2D_Parameters_Pylon15.SetFuseEdges( 80 )
            Sub_mesh_Pylon_Surface15 = NETGEN_2D_Pylon15.GetSubMesh()

            NETGEN_2D_Pylon16 = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_2D,geom=Face_crm_pylon_16)
            NETGEN_2D_Parameters_Pylon16 = NETGEN_2D_Pylon16.Parameters()
            NETGEN_2D_Parameters_Pylon16.SetMaxSize( Engine_Mesh_Size )
            NETGEN_2D_Parameters_Pylon16.SetOptimize( 1 )
            NETGEN_2D_Parameters_Pylon16.SetFineness( 5 )
            NETGEN_2D_Parameters_Pylon16.SetGrowthRate( Growth_Rate_Engine )
            NETGEN_2D_Parameters_Pylon16.SetNbSegPerEdge( 6.92154e-310 )
            NETGEN_2D_Parameters_Pylon16.SetNbSegPerRadius( 5.32336e-317 )
            NETGEN_2D_Parameters_Pylon16.SetMinSize( Engine_Trailing_Edge_Size )
            NETGEN_2D_Parameters_Pylon16.SetUseSurfaceCurvature( 1 )
            NETGEN_2D_Parameters_Pylon16.SetQuadAllowed( 0 )
            NETGEN_2D_Parameters_Pylon16.SetSecondOrder( 106 )
            NETGEN_2D_Parameters_Pylon16.SetFuseEdges( 80 )
            Sub_mesh_Pylon_Surface16 = NETGEN_2D_Pylon16.GetSubMesh()

            # NETGEN_2D_Engine = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_2D,geom=Auto_group_for_Sub_mesh_Engine_Surfaces)
            # NETGEN_2D_Parameters_Engine = NETGEN_2D_Engine.Parameters()
            # NETGEN_2D_Parameters_Engine.SetMaxSize( Engine_Mesh_Size )
            # NETGEN_2D_Parameters_Engine.SetOptimize( 1 )
            # NETGEN_2D_Parameters_Engine.SetFineness( 5 )
            # NETGEN_2D_Parameters_Engine.SetGrowthRate( Growth_Rate_Engine )
            # NETGEN_2D_Parameters_Engine.SetNbSegPerEdge( 6.92154e-310 )
            # NETGEN_2D_Parameters_Engine.SetNbSegPerRadius( 5.32336e-317 )
            # NETGEN_2D_Parameters_Engine.SetMinSize( Engine_Trailing_Edge_Size )
            # NETGEN_2D_Parameters_Engine.SetUseSurfaceCurvature( 1 )
            # NETGEN_2D_Parameters_Engine.SetQuadAllowed( 0 )
            # NETGEN_2D_Parameters_Engine.SetSecondOrder( 106 )
            # NETGEN_2D_Parameters_Engine.SetFuseEdges( 80 )
            # Sub_mesh_Engine_Surface = NETGEN_2D_Engine.GetSubMesh()

            # Root surface
            NETGEN_2D_Root = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_2D,geom=Auto_group_for_Sub_mesh_Root_Surfaces)
            NETGEN_2D_Parameters_Root = NETGEN_2D_Root.Parameters()
            NETGEN_2D_Parameters_Root.SetMaxSize( Fuselage_Mesh_Size )
            NETGEN_2D_Parameters_Root.SetOptimize( 1 )
            NETGEN_2D_Parameters_Root.SetFineness( 5 )
            NETGEN_2D_Parameters_Root.SetGrowthRate( 0.3 )
            NETGEN_2D_Parameters_Root.SetNbSegPerEdge( 6.92154e-310 )
            NETGEN_2D_Parameters_Root.SetNbSegPerRadius( 5.32336e-317 )
            NETGEN_2D_Parameters_Root.SetMinSize( 0.005 )
            NETGEN_2D_Parameters_Root.SetUseSurfaceCurvature( 1 )
            NETGEN_2D_Parameters_Root.SetQuadAllowed( 0 )
            NETGEN_2D_Parameters_Root.SetSecondOrder( 106 )
            NETGEN_2D_Parameters_Root.SetFuseEdges( 80 )
            Sub_mesh_Root_Surface = NETGEN_2D_Root.GetSubMesh()

            # Cockpit surface
            NETGEN_2D_Cockpit = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_2D,geom=Face_crm_cockpit)
            NETGEN_2D_Parameters_Cockpit = NETGEN_2D_Cockpit.Parameters()
            NETGEN_2D_Parameters_Cockpit.SetMaxSize( Fuselage_Mesh_Size )
            NETGEN_2D_Parameters_Cockpit.SetOptimize( 1 )
            NETGEN_2D_Parameters_Cockpit.SetFineness( 1 )
            #NETGEN_2D_Parameters_Cockpit.SetGrowthRate( 0.3 )
            # NETGEN_2D_Parameters_Cockpit.SetNbSegPerEdge( 6.92154e-310 )
            # NETGEN_2D_Parameters_Cockpit.SetNbSegPerRadius( 5.32336e-317 )
            NETGEN_2D_Parameters_Cockpit.SetMinSize( Fuselage_Mesh_Size )
            NETGEN_2D_Parameters_Cockpit.SetUseSurfaceCurvature( 0 )
            NETGEN_2D_Parameters_Cockpit.SetQuadAllowed( 0 )
            NETGEN_2D_Parameters_Cockpit.SetSecondOrder( 106 )
            NETGEN_2D_Parameters_Cockpit.SetFuseEdges( 80 )
            Sub_mesh_Cockpit_Surface = NETGEN_2D_Cockpit.GetSubMesh()

            # Far field surface
            NETGEN_2D_Far_Field = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_2D,geom=Auto_group_for_Sub_mesh_Far_Field_Surfaces)
            Sub_mesh_Far_Field_Surface = NETGEN_2D_Far_Field.GetSubMesh()
            NETGEN_2D_Parameters_FarField = NETGEN_2D_Far_Field.Parameters()
            NETGEN_2D_Parameters_FarField.SetMaxSize( Far_Field_Mesh_Size )
            NETGEN_2D_Parameters_FarField.SetOptimize( 1 )
            NETGEN_2D_Parameters_Wing.SetFineness( 5 )
            NETGEN_2D_Parameters_Wing.SetGrowthRate( Growth_Rate_Far_Field )
            NETGEN_2D_Parameters_FarField.SetMinSize( Smallest_Airfoil_Mesh_Size )
            NETGEN_2D_Parameters_FarField.SetUseSurfaceCurvature( 1 )
            NETGEN_2D_Parameters_FarField.SetQuadAllowed( 0 )
            NETGEN_2D_Parameters_FarField.SetSecondOrder( 106 )
            NETGEN_2D_Parameters_FarField.SetFuseEdges( 80 )

            # Aircraft surface
            NETGEN_2D_Aircraft = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_2D,geom=Auto_group_for_Sub_mesh_Aircraft_Surfaces)
            NETGEN_2D_Parameters_Aircraft = NETGEN_2D_Aircraft.Parameters()
            NETGEN_2D_Parameters_Aircraft.SetMaxSize( Fuselage_Mesh_Size )
            NETGEN_2D_Parameters_Aircraft.SetOptimize( 1 )
            NETGEN_2D_Parameters_Aircraft.SetFineness( 5 )
            NETGEN_2D_Parameters_Aircraft.SetGrowthRate( 0.3 )
            NETGEN_2D_Parameters_Aircraft.SetNbSegPerEdge( 6.92154e-310 )
            NETGEN_2D_Parameters_Aircraft.SetNbSegPerRadius( 5.32336e-317 )
            NETGEN_2D_Parameters_Aircraft.SetMinSize( 0.005 )
            NETGEN_2D_Parameters_Aircraft.SetUseSurfaceCurvature( 1 )
            NETGEN_2D_Parameters_Aircraft.SetQuadAllowed( 0 )
            NETGEN_2D_Parameters_Aircraft.SetSecondOrder( 106 )
            NETGEN_2D_Parameters_Aircraft.SetFuseEdges( 80 )
            Sub_mesh_Aircraft_Surface = NETGEN_2D_Aircraft.GetSubMesh()

            # Wing surface
            NETGEN_2D_Only_Wing = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_2D,geom=Auto_group_for_Sub_mesh_Wing_Surfaces)
            NETGEN_2D_Parameters_Only_Wing = NETGEN_2D_Only_Wing.Parameters()
            NETGEN_2D_Parameters_Only_Wing.SetMaxSize( Fuselage_Mesh_Size )
            NETGEN_2D_Parameters_Only_Wing.SetOptimize( 1 )
            NETGEN_2D_Parameters_Only_Wing.SetFineness( 5 )
            NETGEN_2D_Parameters_Only_Wing.SetGrowthRate( 0.3 )
            NETGEN_2D_Parameters_Only_Wing.SetNbSegPerEdge( 6.92154e-310 )
            NETGEN_2D_Parameters_Only_Wing.SetNbSegPerRadius( 5.32336e-317 )
            NETGEN_2D_Parameters_Only_Wing.SetMinSize( 0.005 )
            NETGEN_2D_Parameters_Only_Wing.SetUseSurfaceCurvature( 1 )
            NETGEN_2D_Parameters_Only_Wing.SetQuadAllowed( 0 )
            NETGEN_2D_Parameters_Only_Wing.SetSecondOrder( 106 )
            NETGEN_2D_Parameters_Only_Wing.SetFuseEdges( 80 )
            Sub_mesh_Only_Wing_Surface = NETGEN_2D_Only_Wing.GetSubMesh()

            #'''
            import time as time
            print(' Starting meshing ')
            start_time = time.time()
            # Compute mesh
            isDone = Mesh_Domain.Compute()
            exe_time = time.time() - start_time
            print(' Mesh execution took ', str(round(exe_time, 2)), ' sec')
            print(' Mesh execution took ' + str(round(exe_time/60, 2)) + ' min')

            NumberOfNodes = Mesh_Domain.NbNodes()
            NumberOfElements = Mesh_Domain.NbTetras()
            print(' Information about volume mesh:')
            print(' Number of nodes       :', NumberOfNodes)
            print(' Number of elements    :', NumberOfElements)

            filter = smesh.GetFilter(SMESH.NODE, SMESH.FT_EqualNodes, Tolerance=1e-7)
            print( ' Equal nodes: ', Mesh_Domain.GetIdsFromFilter( filter ) )
            print( ' Number of equal nodes: ', len( Mesh_Domain.GetIdsFromFilter( filter ) ))

            equalEdgesFilter   = smesh.GetFilter(SMESH.EDGE, SMESH.FT_EqualEdges)
            print( ' Equal edges: ', Mesh_Domain.GetIdsFromFilter( equalEdgesFilter ) )
            print( ' Number of equal edges: ', len( Mesh_Domain.GetIdsFromFilter( equalEdgesFilter ) ))

            equalFacesFilter   = smesh.GetFilter(SMESH.FACE, SMESH.FT_EqualFaces)
            print( ' Equal faces: ', Mesh_Domain.GetIdsFromFilter( equalFacesFilter ) )
            print( ' Number of equal faces: ', len( Mesh_Domain.GetIdsFromFilter( equalFacesFilter ) ))

            equalVolumesFilter = smesh.GetFilter(SMESH.VOLUME, SMESH.FT_EqualVolumes)
            print( ' Equal volumes: ', Mesh_Domain.GetIdsFromFilter( equalVolumesFilter ) )
            print( ' Number of equal volumes: ', len( Mesh_Domain.GetIdsFromFilter( equalVolumesFilter ) ))


            #isDone = Mesh_Domain.SetMeshOrder( [ [ Sub_mesh_Fuselage, smeshObj_1, Sub_mesh_LE_TE, Sub_mesh_Airfoils ] ])

            fluid_path = salome_output_path + '/Mesh_Domain_Case_' + str(case) + '_AOA_' + str(AOA) + '_Wing_Span_' + str(
              Wing_span) + '_Airfoil_Mesh_Size_' + str(Smallest_Airfoil_Mesh_Size) + '_Growth_Rate_Wing_' + str(
                Growth_Rate_Wing) + '_Growth_Rate_Domain_' + str(Growth_Rate_Domain) + '.dat'

            far_field_path = salome_output_path + '/Sub-mesh_FarField_Case_' + str(case) + '_AOA_' + str(AOA) + '_Wing_Span_' + str(
              Wing_span) + '_Airfoil_Mesh_Size_' + str(Smallest_Airfoil_Mesh_Size) + '_Growth_Rate_Wing_' + str(
                Growth_Rate_Wing) + '_Growth_Rate_Domain_' + str(Growth_Rate_Domain) + '.dat'

            body_surface_path = salome_output_path + '/Sub-mesh_Wing_Case_' + str(case) + '_AOA_' + str(AOA) + '_Wing_Span_' + str(
              Wing_span) + '_Airfoil_Mesh_Size_' + str(Smallest_Airfoil_Mesh_Size) + '_Growth_Rate_Wing_' + str(
                Growth_Rate_Wing) + '_Growth_Rate_Domain_' + str(Growth_Rate_Domain) + '.dat'

            wing_surface_path = salome_output_path + '/Sub-mesh_Only_Wing_Case_' + str(case) + '_AOA_' + str(AOA) + '_Wing_Span_' + str(
              Wing_span) + '_Airfoil_Mesh_Size_' + str(Smallest_Airfoil_Mesh_Size) + '_Growth_Rate_Wing_' + str(
                Growth_Rate_Wing) + '_Growth_Rate_Domain_' + str(Growth_Rate_Domain) + '.dat'

            te_path = salome_output_path + '/Sub-mesh_TE_Case_' + str(case) + '_AOA_' + str(AOA) + '_Wing_Span_' + str(
              Wing_span) + '_Airfoil_Mesh_Size_' + str(Smallest_Airfoil_Mesh_Size) + '_Growth_Rate_Wing_' + str(
                Growth_Rate_Wing) + '_Growth_Rate_Domain_' + str(Growth_Rate_Domain) + '.dat'

            engine_te_path = salome_output_path + '/Sub-mesh_Engine_TE_Case_' + str(case) + '_AOA_' + str(AOA) + '_Wing_Span_' + str(Wing_span) + '_Airfoil_Mesh_Size_' + str(Smallest_Airfoil_Mesh_Size) + '_Growth_Rate_Wing_' + str(Growth_Rate_Wing) + '_Growth_Rate_Domain_' + str(Growth_Rate_Domain) + '.dat'

            # Export data files
            try:
              Mesh_Domain.ExportDAT( r'/' + fluid_path )
              pass
            except:
              print 'ExportDAT() failed. Invalid file name?'
            try:
              Mesh_Domain.ExportDAT( r'/' + body_surface_path, Sub_mesh_Aircraft_Surface )
              pass
            except:
              print 'ExportPartToDAT() failed. Invalid file name?'
            try:
              Mesh_Domain.ExportDAT( r'/' + wing_surface_path, Sub_mesh_Only_Wing_Surface )
              pass
            except:
              print 'ExportPartToDAT() failed. Invalid file name?'
            try:
              Mesh_Domain.ExportDAT( r'/' + far_field_path, Sub_mesh_Far_Field_Surface )
              pass
            except:
              print 'ExportPartToDAT() failed. Invalid file name?'
            try:
              Mesh_Domain.ExportDAT( r'/' + te_path, Sub_mesh_Trailing_Edge_Surface )
              pass
            except:
              print 'ExportPartToDAT() failed. Invalid file name?'
            try:
              Mesh_Domain.ExportDAT( r'/' + engine_te_path, Sub_mesh_Engine_Outlet_Surface )
              pass
            except:
              print 'ExportPartToDAT() failed. Invalid file name?'
            #'''

            '''
            # Mesh wake and export STL
            Mesh_Wake_Surface = smesh.Mesh(Auto_group_for_Sub_mesh_Wake_Surfaces)
            NETGEN_1D_2D_2 = Mesh_Wake_Surface.Triangle(algo=smeshBuilder.NETGEN_1D2D)
            NETGEN_2D_Parameters_Wake = NETGEN_1D_2D_2.Parameters()
            NETGEN_2D_Parameters_Wake.SetSecondOrder( 0 )
            NETGEN_2D_Parameters_Wake.SetOptimize( 1 )
            NETGEN_2D_Parameters_Wake.SetMinSize( 1.0 )
            NETGEN_2D_Parameters_Wake.SetUseSurfaceCurvature( 1 )
            NETGEN_2D_Parameters_Wake.SetFuseEdges( 1 )
            NETGEN_2D_Parameters_Wake.SetQuadAllowed( 0 )
            NETGEN_2D_Parameters_Wake.SetMaxSize( 2.0 )
            NETGEN_2D_Parameters_Wake.SetFineness( 4 )

            # TE edges
            Regular_1D_Wake_TE = Mesh_Wake_Surface.Segment(geom=Auto_group_for_Sub_mesh_Wake_Trailing_Edges)
            Local_Length_Wake_TE = Regular_1D_Wake_TE.LocalLength(0.1,None,1e-07)
            status = Mesh_Wake_Surface.AddHypothesis(Regular_1D_Wake_TE,Auto_group_for_Sub_mesh_Wake_Trailing_Edges)
            Sub_mesh_Wake_TE_Edges = Regular_1D_Wake_TE.GetSubMesh()

            # Mesh tail wake and export STL
            Mesh_Tail_Wake_Surface = smesh.Mesh(Auto_group_for_Sub_mesh_Tail_Wake_Surfaces)
            NETGEN_1D_2D_3 = Mesh_Tail_Wake_Surface.Triangle(algo=smeshBuilder.NETGEN_1D2D)
            NETGEN_2D_Parameters_Tail_Wake = NETGEN_1D_2D_3.Parameters()
            NETGEN_2D_Parameters_Tail_Wake.SetSecondOrder( 0 )
            NETGEN_2D_Parameters_Tail_Wake.SetOptimize( 1 )
            NETGEN_2D_Parameters_Tail_Wake.SetMinSize( 1.0 )
            NETGEN_2D_Parameters_Tail_Wake.SetUseSurfaceCurvature( 1 )
            NETGEN_2D_Parameters_Tail_Wake.SetFuseEdges( 1 )
            NETGEN_2D_Parameters_Tail_Wake.SetQuadAllowed( 0 )
            NETGEN_2D_Parameters_Tail_Wake.SetMaxSize( 2.0 )
            NETGEN_2D_Parameters_Tail_Wake.SetFineness( 4 )

            # TE edges
            Regular_1D_Tail_Wake_TE = Mesh_Tail_Wake_Surface.Segment(geom=Auto_group_for_Sub_mesh_Wake_Tail_Trailing_Edges)
            Local_Length_Tail_Wake_TE = Regular_1D_Tail_Wake_TE.LocalLength(0.1,None,1e-07)
            status = Mesh_Tail_Wake_Surface.AddHypothesis(Regular_1D_Tail_Wake_TE,Auto_group_for_Sub_mesh_Wake_Tail_Trailing_Edges)
            Sub_mesh_Wake_Tail_TE_Edges = Regular_1D_Tail_Wake_TE.GetSubMesh()

            # # Outlet edges
            # Regular_1D_Wake_Outlet_Edges = Mesh_Wake_Surface.Segment(geom=Auto_group_for_Sub_mesh_Wake_Outlet_Edges)
            # Sub_mesh_Wake_Outlet_Edges = Regular_1D_Wake_Outlet_Edges.GetSubMesh()
            # Local_Length_Wake_Outlet_Edges = Regular_1D_Wake_Outlet_Edges.LocalLength(2.0,None,1e-07)

            # # Fuselage Transition Edges
            # Regular_1D_Wake_Transition_Edges = Mesh_Wake_Surface.Segment(geom=Auto_group_for_Sub_mesh_Wake_Transition_Edges)
            # Start_and_End_Length_Wake_Transition_Edges = Regular_1D_Wake_Transition_Edges.StartEndLength(0.1,2.0,[])
            # Start_and_End_Length_Wake_Transition_Edges.SetObjectEntry( 'Extrusion_Wake_stl' )
            # Sub_mesh_Wake_Transition_Edges = Regular_1D_Wake_Transition_Edges.GetSubMesh()

            #'''
            '''
            isDone = Mesh_Wake_Surface.SetMeshOrder( [ [ Sub_mesh_Wake_TE_Edges] ])

            print(' Starting meshing ')
            start_time = time.time()
            # Compute mesh
            isDone = Mesh_Wake_Surface.Compute()
            exe_time = time.time() - start_time
            print(' Mesh execution took ', str(round(exe_time, 2)), ' sec')
            print(' Mesh execution took ' + str(round(exe_time/60, 2)) + ' min')

            print(' Starting meshing ')
            start_time = time.time()
            # Compute mesh
            isDone = Mesh_Tail_Wake_Surface.Compute()
            exe_time = time.time() - start_time
            print(' Mesh execution took ', str(round(exe_time, 2)), ' sec')
            print(' Mesh execution took ' + str(round(exe_time/60, 2)) + ' min')



            wake_path = mdpa_path + '/wake_Case_' + str(case) + '_AOA_' + str(AOA) + '_Wing_Span_' + str(
              Wing_span) + '_Airfoil_Mesh_Size_' + str(Smallest_Airfoil_Mesh_Size) + '_Growth_Rate_Wing_' + str(
                Growth_Rate_Wing) + '_Growth_Rate_Domain_' + str(Growth_Rate_Domain) + '.stl'
            try:
                Mesh_Wake_Surface.ExportSTL( wake_path, 1 )
                pass
            except:
                print 'ExportSTL() failed. Invalid file name?'

            '''

            ## Set names of Mesh objects
            smesh.SetName(NETGEN_3D.GetAlgorithm(), 'NETGEN 3D')
            #smesh.SetName(Viscous_Layers_1, 'Viscous Layers_1')
            smesh.SetName(NETGEN_3D_Parameters, 'NETGEN_3D_Parameters')
            smesh.SetName(Mesh_Domain.GetMesh(), 'Mesh_Domain')

            smesh.SetName(Regular_1D_LE_TE.GetAlgorithm(), 'Regular_1D_LE_TE')
            smesh.SetName(Local_Length_LE_TE, 'Local_Length_LE_TE')
            smesh.SetName(Sub_mesh_LE_TE, 'Sub_mesh_LE_TE')

            smesh.SetName(Regular_1D_Airfoils.GetAlgorithm(), 'Regular_1D_Airfoils')
            smesh.SetName(Start_and_End_Length_Airfoils, 'Start_and_End_Length_Airfoils')
            smesh.SetName(Sub_mesh_Airfoils, 'Sub_mesh_Airfoils')

            smesh.SetName(Regular_1D_Tip_Airfoils.GetAlgorithm(), 'Regular_1D_Tip_Airfoils')
            smesh.SetName(Start_and_End_Length_Tip_Airfoils, 'Start_and_End_Length_Tip_Airfoils')
            smesh.SetName(Sub_mesh_Tip_Airfoils, 'Sub_mesh_Tip_Airfoils')

            smesh.SetName(Regular_1D_Middle_Tip_Edges.GetAlgorithm(), 'Regular_1D_Middle_Tip_Edges')
            smesh.SetName(Local_Length_Middle_Tip_Edges, 'Local_Length_Middle_Tip_Edges')
            smesh.SetName(Sub_mesh_Middle_Tip_Edges, 'Sub_mesh_Middle_Tip_Edges')

            '''
            # smesh.SetName(Regular_1D_Root.GetAlgorithm(), 'Regular_1D_Root')
            # smesh.SetName(Local_Length_Root, 'Local_Length_Root')
            # smesh.SetName(Sub_mesh_Root_Edges, 'Sub_mesh_Root_Edges')

            '''
            smesh.SetName(Regular_1D_Fuselage_143_Edge.GetAlgorithm(), 'Regular_1D_Fuselage_143_Edge')
            smesh.SetName(Start_and_End_Length_Fuselage_143_Edge, 'Start_and_End_Length_Fuselage_143_Edge')
            smesh.SetName(Sub_mesh_Fuselage_143_Edge, 'Sub_mesh_Fuselage_143_Edge')

            smesh.SetName(Regular_1D_Fuselage_Transition_Edges.GetAlgorithm(), 'Regular_1D_Fuselage_Transition_Edges')
            smesh.SetName(Start_and_End_Length_Fuselage_Transition_Edges, 'Start_and_End_Length_Fuselage_Transition_Edges')
            smesh.SetName(Sub_mesh_Fuselage_Transition_Edges, 'Sub_mesh_Fuselage_Transition_Edges')

            smesh.SetName(Regular_1D_Fuselage.GetAlgorithm(), 'Regular_1D_Fuselage')
            smesh.SetName(Local_Length_Fuselage, 'Local_Length_Fuselage')
            smesh.SetName(Sub_mesh_Fuselage_Edges, 'Sub_mesh_Fuselage_Edges')

            smesh.SetName(Regular_1D_Engine_Outlet.GetAlgorithm(), 'Regular_1D_Engine_Outlet')
            smesh.SetName(Local_Length_Engine_Outlet, 'Local_Length_Engine_Outlet')
            smesh.SetName(Sub_mesh_Engine_Outlet_Edges, 'Sub_mesh_Engine_Outlet_Edges')

            smesh.SetName(Regular_1D_Engine_Transition_Edges.GetAlgorithm(), 'Regular_1D_Engine_Transition_Edges')
            smesh.SetName(Start_and_End_Length_Engine_Transition_Edges, 'Start_and_End_Length_Engine_Transition_Edges')
            smesh.SetName(Sub_mesh_Engine_Transition_Edges, 'Sub_mesh_Engine_Transition_Edges')

            smesh.SetName(Regular_1D_Pylon_Edge.GetAlgorithm(), 'Regular_1D_Pylon_Edge')
            smesh.SetName(Local_Length_Pylon_Edge, 'Local_Length_Pylon_Edge')
            smesh.SetName(Sub_mesh_Pylon_Edge, 'Sub_mesh_Pylon_Edge')

            smesh.SetName(Regular_1D_Pylon_Transition_Edges.GetAlgorithm(), 'Regular_1D_Pylon_Transition_Edges')
            smesh.SetName(Start_and_End_Length_Pylon_Transition_Edges, 'Start_and_End_Length_Pylon_Transition_Edges')
            smesh.SetName(Sub_mesh_Pylon_Transition_Edges, 'Sub_mesh_Pylon_Transition_Edges')

            smesh.SetName(Regular_1D_Engine.GetAlgorithm(), 'Regular_1D_Engine')
            smesh.SetName(Local_Length_Engine, 'Local_Length_Engine')
            smesh.SetName(Sub_mesh_Engine_Edges, 'Sub_mesh_Engine_Edges')

            smesh.SetName(Regular_1D_Wing_Hole_Edge1.GetAlgorithm(), 'Regular_1D_Wing_Hole_Edge1')
            smesh.SetName(Start_and_End_Length_Wing_Hole_1_Edge, 'Start_and_End_Length_Wing_Hole_1_Edge')
            smesh.SetName(Sub_mesh_Wing_Hole_1_Edges, 'Sub_mesh_Wing_Hole_1_Edges')

            smesh.SetName(Regular_1D_Wing_Hole_Edge2.GetAlgorithm(), 'Regular_1D_Wing_Hole_Edge2')
            smesh.SetName(Start_and_End_Length_Wing_Hole_2_Edge, 'Start_and_End_Length_Wing_Hole_2_Edge')
            smesh.SetName(Sub_mesh_Wing_Hole_2_Edges, 'Sub_mesh_Wing_Hole_2_Edges')

            smesh.SetName(Regular_1D_Wing_Transition1.GetAlgorithm(), 'Regular_1D_Wing_Transition1')
            smesh.SetName(Start_and_End_Length_Wing_Transition_1_Edge, 'Start_and_End_Length_Wing_Transition_1_Edge')
            smesh.SetName(Sub_mesh_Wing_Transition_1_Edges, 'Sub_mesh_Wing_Transition_1_Edges')

            smesh.SetName(Regular_1D_Wing_Transition2.GetAlgorithm(), 'Regular_1D_Wing_Transition2')
            smesh.SetName(Start_and_End_Length_Wing_Transition_2_Edge, 'Start_and_End_Length_Wing_Transition_2_Edge')
            smesh.SetName(Sub_mesh_Wing_Transition_2_Edges, 'Sub_mesh_Wing_Transition_2_Edges')

            smesh.SetName(Regular_1D_Wing_Hole.GetAlgorithm(), 'Regular_1D_Wing_Hole')
            smesh.SetName(Local_Length_Wing_Hole, 'Local_Length_Wing_Hole')
            smesh.SetName(Sub_mesh_Wing_Hole_Edges, 'Sub_mesh_Wing_Hole_Edges')

            smesh.SetName(Regular_1D_Far_Field_Edges.GetAlgorithm(), 'Regular_1D_Far_Field_Edges')
            smesh.SetName(Local_Length_Far_Field, 'Local_Length_Far_Field')
            smesh.SetName(Sub_mesh_Far_Field_Edges, 'Sub_mesh_Far_Field_Edges')

            smesh.SetName(NETGEN_2D_Wing_Root_Up.GetAlgorithm(), 'NETGEN_2D_Wing_Root_Up')
            smesh.SetName(NETGEN_2D_Parameters_Wing_Root_Up, 'NETGEN_2D_Parameters_Wing_Root_Up')
            smesh.SetName(Sub_mesh_Wing_Root_Up_Surface, 'Sub_mesh_Wing_Root_Up_Surface')

            smesh.SetName(NETGEN_2D_Wing_Root_Down.GetAlgorithm(), 'NETGEN_2D_Wing_Root_Down')
            smesh.SetName(NETGEN_2D_Parameters_Wing_Root_Down, 'NETGEN_2D_Parameters_Wing_Root_Down')
            smesh.SetName(Sub_mesh_Wing_Root_Down_Surface, 'Sub_mesh_Wing_Root_Down_Surface')

            smesh.SetName(NETGEN_2D_Wing_Up.GetAlgorithm(), 'NETGEN_2D_Wing_Up')
            smesh.SetName(NETGEN_2D_Parameters_Wing_Up, 'NETGEN_2D_Parameters_Wing_Up')
            smesh.SetName(Sub_mesh_Wing_Up_Surface, 'Sub_mesh_Wing_Up_Surface')

            smesh.SetName(NETGEN_2D_Wing_Down.GetAlgorithm(), 'NETGEN_2D_Wing_Down')
            smesh.SetName(NETGEN_2D_Parameters_Wing_Down, 'NETGEN_2D_Parameters_Wing_Down')
            smesh.SetName(Sub_mesh_Wing_Down_Surface, 'Sub_mesh_Wing_Down_Surface')

            smesh.SetName(NETGEN_2D_Wing_Tail_Up.GetAlgorithm(), 'NETGEN_2D_Wing_Tail_Up')
            smesh.SetName(NETGEN_2D_Parameters_Tail_Up, 'NETGEN_2D_Parameters_Tail_Up')
            smesh.SetName(Sub_mesh_Tail_Up_Surface, 'Sub_mesh_Tail_Up_Surface')

            smesh.SetName(NETGEN_2D.GetAlgorithm(), 'NETGEN_2D')
            smesh.SetName(NETGEN_2D_Parameters_Wing, 'NETGEN 2D Parameters_Wing')
            smesh.SetName(Sub_mesh_Wing_Surface, 'Sub-mesh_Wing_Surface')

            smesh.SetName(NETGEN_2D_Tip.GetAlgorithm(), 'NETGEN_2D_Tip')
            smesh.SetName(NETGEN_2D_Parameters_Wing_Tip, 'NETGEN_2D_Parameters_Wing_Tip')
            smesh.SetName(Sub_mesh_Wing_Tip_Surface, 'Sub_mesh_Wing_Tip_Surface')

            smesh.SetName(NETGEN_2D_Trailing_Edges.GetAlgorithm(), 'NETGEN_2D_Trailing_Edges')
            smesh.SetName(NETGEN_2D_Parameters_Trailing_Edges, 'NETGEN_2D_Parameters_Trailing_Edges')
            smesh.SetName(Sub_mesh_Trailing_Edge_Surface, 'Sub_mesh_Trailing_Edge_Surface')

            smesh.SetName(NETGEN_2D_Root.GetAlgorithm(), 'NETGEN_2D_Root')
            smesh.SetName(NETGEN_2D_Parameters_Root, 'NETGEN_2D_Parameters_Root')
            smesh.SetName(Sub_mesh_Root_Surface, 'Sub_mesh_Root_Surface')

            smesh.SetName(NETGEN_2D_Fuselage.GetAlgorithm(), 'NETGEN_2D_Fuselage')
            smesh.SetName(NETGEN_2D_Parameters_Fuselage, 'NETGEN_2D_Parameters_Fuselage')
            smesh.SetName(Sub_mesh_Fuselage_Surface, 'Sub_mesh_Fuselage_Surface')

            # smesh.SetName(NETGEN_2D_Engine.GetAlgorithm(), 'NETGEN_2D_Engine')
            # smesh.SetName(NETGEN_2D_Parameters_Engine, 'NETGEN_2D_Parameters_Engine')
            # smesh.SetName(Sub_mesh_Engine_Surface, 'Sub_mesh_Engine_Surface')

            smesh.SetName(NETGEN_2D_Engine_Outlet.GetAlgorithm(), 'NETGEN_2D_Engine_Outlet')
            smesh.SetName(NETGEN_2D_Parameters_Engine_Outlet, 'NETGEN_2D_Parameters_Engine_Outlet')
            smesh.SetName(Sub_mesh_Engine_Outlet_Surface, 'Sub_mesh_Engine_Outlet_Surface')

            smesh.SetName(NETGEN_2D_Cockpit.GetAlgorithm(), 'NETGEN_2D_Cockpit')
            smesh.SetName(NETGEN_2D_Parameters_Cockpit, 'NETGEN_2D_Parameters_Cockpit')
            smesh.SetName(Sub_mesh_Cockpit_Surface, 'Sub_mesh_Cockpit_Surface')

            smesh.SetName(NETGEN_2D_Aircraft.GetAlgorithm(), 'NETGEN_2D_Aircraft')
            smesh.SetName(NETGEN_2D_Parameters_Aircraft, 'NETGEN_2D_Parameters_Aircraft')
            smesh.SetName(Sub_mesh_Aircraft_Surface, 'Sub_mesh_Aircraft_Surface')

            smesh.SetName(NETGEN_2D_Only_Wing.GetAlgorithm(), 'NETGEN_2D_Only_Wing')
            smesh.SetName(NETGEN_2D_Parameters_Only_Wing, 'NETGEN_2D_Parameters_Only_Wing')
            smesh.SetName(Sub_mesh_Only_Wing_Surface, 'Sub_mesh_Only_Wing_Surface')

            smesh.SetName(NETGEN_2D_Far_Field.GetAlgorithm(), 'NETGEN_2D_Far_Field')
            smesh.SetName(NETGEN_2D_Parameters_FarField, 'NETGEN_2D_Parameters_FarField')
            smesh.SetName(Sub_mesh_Far_Field_Surface, 'Sub_mesh_Far_Field_Surface')

            '''
            # # Wake stuff
            # smesh.SetName(NETGEN_1D_2D_2.GetAlgorithm(), 'NETGEN_1D_2D_2')
            # smesh.SetName(NETGEN_2D_Parameters_Wake, 'NETGEN_2D_Parameters_Wake')
            # smesh.SetName(Mesh_Wake_Surface, 'Mesh_Wake_Surface')

            # smesh.SetName(Regular_1D_Wake_TE.GetAlgorithm(), 'Regular_1D_Wake_TE')
            # smesh.SetName(Local_Length_Wake_TE, 'Local_Length_Wake_TE')
            # smesh.SetName(Sub_mesh_Wake_TE_Edges, 'Sub_mesh_Wake_TE_Edges')

            # smesh.SetName(NETGEN_1D_2D_3.GetAlgorithm(), 'NETGEN_1D_2D_3')
            # smesh.SetName(NETGEN_2D_Parameters_Tail_Wake, 'NETGEN_2D_Parameters_Tail_Wake')
            # smesh.SetName(Mesh_Tail_Wake_Surface, 'Mesh_Tail_Wake_Surface')

            # smesh.SetName(Regular_1D_Tail_Wake_TE.GetAlgorithm(), 'Regular_1D_Tail_Wake_TE')
            # smesh.SetName(Local_Length_Tail_Wake_TE, 'Local_Length_Tail_Wake_TE')
            # smesh.SetName(Sub_mesh_Wake_Tail_TE_Edges, 'Sub_mesh_Wake_Tail_TE_Edges')

            # smesh.SetName(Regular_1D_Wake_Outlet_Edges.GetAlgorithm(), 'Regular_1D_Wake_Outlet_Edges')
            # smesh.SetName(Local_Length_Wake_Outlet_Edges, 'Local_Length_Wake_Outlet_Edges')
            # smesh.SetName(Sub_mesh_Wake_Outlet_Edges, 'Sub_mesh_Wake_Outlet_Edges')

            # smesh.SetName(Regular_1D_Wake_Transition_Edges.GetAlgorithm(), 'Regular_1D_Wake_Transition_Edges')
            # smesh.SetName(Start_and_End_Length_Wake_Transition_Edges, 'Start_and_End_Length_Wake_Transition_Edges')
            # smesh.SetName(Sub_mesh_Wake_Transition_Edges, 'Sub_mesh_Wake_Transition_Edges')
            '''

            # Saving file to open from salome's gui
            file_name = salome_output_path + "/generate_finite_wing_sections_box_separating.hdf"
            salome.myStudyManager.SaveAs(file_name, salome.myStudy, 0)

            # with open('case/results_3d_finite_wing.dat', 'a+') as file:
            #   file.write('\n{0:5.0f} {1:5.0f} {2:10.0f} {3:10.4f} {4:10.3f} {5:10.0f} {6:10.2f} {7:10.2f} {8:15.1e} {9:15.1e} {10:10.1f}'.format(
            #     AOA, # 0
            #     Wing_span, # 1
            #     Domain_Length, # 2
            #     Smallest_Airfoil_Mesh_Size, # 3
            #     Biggest_Airfoil_Mesh_Size, # 4
            #     Far_Field_Mesh_Size, # 5
            #     Growth_Rate_Wing, # 6
            #     Growth_Rate_Domain, # 7
            #     NumberOfNodes/1000.0, # 8
            #     NumberOfElements/1000.0, # 9
            #     exe_time/60.0)) # 10
            #   file.flush()
            #'''

            #Airfoil_MeshSize *= Airfoil_Refinement_Factor
            #FarField_MeshSize /= FarField_Refinement_Factor
            #Growth_Rate_Wing -= Growth_Rate_Wing_Refinement_Factor
            Growth_Rate_Wing /= Growth_Rate_Wing_Refinement_Factor
            Smallest_Airfoil_Mesh_Size /= 2.0
            # Biggest_Airfoil_Mesh_Size /= 2.0
            case +=1
        Growth_Rate_Domain /= Growth_Rate_Domain_Refinement_Factor
    AOA += AOA_Increment

if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser(True)

sys.exit()
os.exit(0)
killSalome.killAllPorts()

