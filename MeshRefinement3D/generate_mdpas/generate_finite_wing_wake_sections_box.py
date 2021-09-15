# -*- coding: utf-8 -*-

###
### This file is generated automatically by SALOME v8.4.0 with dump python functionality
###
import os
import killSalome
import math

# Parameters:
Wing_span = 6.0
Domain_Length = 1000
Domain_Height = Domain_Length
Domain_Width = 1000
wake_angle_deg = 0.0

Smallest_Airfoil_Mesh_Size = TBD
Biggest_Airfoil_Mesh_Size = TBD
Wing_Tip_Mesh_Size = Smallest_Airfoil_Mesh_Size# * 5.0
Root_Mesh_Size = Biggest_Airfoil_Mesh_Size * 0.5
Fuselage_Mesh_Size = 0.8
LE_Mesh_Size = Smallest_Airfoil_Mesh_Size
TE_Mesh_Size = Smallest_Airfoil_Mesh_Size
Far_Field_Mesh_Size = Domain_Length/20.0

print 'Domain_Length = ', Domain_Length
print 'Smallest_Airfoil_Mesh_Size = ', Smallest_Airfoil_Mesh_Size
print 'Biggest_Airfoil_Mesh_Size = ', Biggest_Airfoil_Mesh_Size
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

geometry_path = "/media/inigo/10740FB2740F9A1C/Results/15_nasa_crm/03_model_gid/11_divide.igs"

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

            [Face_Inlet,Face_crm_cockpit,Face_crm_fuselage_middle_down,\
            Face_crm_fuselage_middle_middle,Face_crm_fuselage_middle_up,\
            Face_crm_fuselage_root_down,\
            Face_crm_fuselage_root_up,\
            Face_crm_fuselage_root,\
            Face_crm_wing_root_down,\
            Face_crm_wing_root_up,Face_Left_Wall,Face_crm_wing_root_te,\
            Face_crm_wing_down,Face_crm_wing_up,Face_crm_fuselage_ring_up,\
            Face_crm_fuselage_ring_down,Face_crm_fuselage_ring_middle,Face_crm_wing_te,\
            Face_crm_wing_tip_down,Face_crm_wing_tip_up,Face_crm_wing_tip_te,\
            Face_crm_fuselage_back,Face_Down_Wall,Face_Top_Wall,\
            Face_crm_tail_down,Face_crm_tail_up,Face_crm_tail_te,\
            Face_crm_tail_tip_le_down,Face_crm_tail_tip_le_up,Face_crm_tail_tip_te_down,\
            Face_crm_tail_tip_te_up,Face_Right_Wall,\
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
            [Obj1,Obj2,Edge_118,Edge_119] = geompy.ExtractShapes(Face_crm_fuselage_middle_middle, geompy.ShapeType["EDGE"], True)
            [Obj1,Edge_121,Obj2,Edge_123] = geompy.ExtractShapes(Face_crm_fuselage_middle_up, geompy.ShapeType["EDGE"], True)
            [Obj1,Edge_125,Edge_126,Edge_127] = geompy.ExtractShapes(Face_crm_fuselage_root_down, geompy.ShapeType["EDGE"], True)
            [Obj1,Edge_129,Edge_130,Edge_131] = geompy.ExtractShapes(Face_crm_fuselage_root_up, geompy.ShapeType["EDGE"], True)

            # Root
            [Obj1,Obj2,Obj3,Obj4,Obj5,Obj6,Obj7,Obj8,Edge_140,Obj9,Obj10,Edge_143,Edge_144,Edge_145,Edge_146] =             geompy.ExtractShapes(Face_crm_fuselage_root, geompy.ShapeType["EDGE"], True)

            # Wing
            # Root
            [Edge_wing_root_down_le,Edge_wing_root_le,Edge_wing_middle_down_le,Edge_wing_root_down_te,Edge_wing_middle_down_te,Edge_wing_root_te_down] = geompy.ExtractShapes(Face_crm_wing_root_down, geompy.ShapeType["EDGE"],             True)
            [Edge_wing_root_up_le,Obj1,Edge_wing_middle_up_le,Edge_wing_root_up_te,Edge_wing_middle_up_te,Edge_wing_root_te_up] = geompy.ExtractShapes(Face_crm_wing_root_up, geompy.ShapeType["EDGE"],           True)

            [Edge_root_te_down,Edge_root_te_up,Obj1,Obj2,Edge_wing_middle_te] = geompy.ExtractShapes(Face_crm_wing_root_te, geompy.ShapeType["EDGE"], True)
            [Obj1,Obj2,Edge_wing_le,Edge_wing_te_down,Edge_wing_tip_down_le,Edge_wing_tip_down_te] = geompy.ExtractShapes(Face_crm_wing_down, geompy.ShapeType["EDGE"], True)
            [Obj1,Obj2,Obj3,Edge_wing_te_up,Edge_wing_tip_up_le,Edge_wing_tip_up_te] = geompy.ExtractShapes(Face_crm_wing_up, geompy.ShapeType["EDGE"], True)

            # Fuselage
            [Obj1,Edge_192,Edge_193,Edge_194] = geompy.ExtractShapes(Face_crm_fuselage_ring_up, geompy.ShapeType["EDGE"], True)
            [Obj1,Obj2,Edge_197,Obj3,Edge_199,Edge_1100] = geompy.ExtractShapes(Face_crm_fuselage_ring_down, geompy.ShapeType         ["EDGE"], True)
            [Obj1,Obj2,Obj3,Edge_1104] = geompy.ExtractShapes(Face_crm_fuselage_ring_middle, geompy.ShapeType["EDGE"], True)

            # Wing tip
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

            # Making groups for submeshes
            # LE and TE edges
            Auto_group_for_Sub_mesh_LE_TE_Edges = geompy.CreateGroup(nasa_crm_igs, geompy.ShapeType["EDGE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_LE_TE_Edges, [Edge_wing_root_le,Edge_wing_root_te_down,Edge_wing_root_te_up,Edge_root_te_down,Edge_root_te_up,Edge_wing_middle_te,Edge_wing_le,Edge_wing_te_down,Edge_wing_te_up,Edge_wing_tip_te1,Edge_wing_tip_te2,Edge_wing_tip_te3,Edge_1119,Edge_tail_le,Edge_tail_te_down,Edge_tail_te_up,Edge_tail_root_te,Edge_tail_tip_te_down,Edge_tail_tip_te_up])

            # Airfoils' edges
            Auto_group_for_Sub_mesh_Airfoil_Edges = geompy.CreateGroup(nasa_crm_igs, geompy.ShapeType["EDGE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Airfoil_Edges, [Edge_wing_root_down_le,Edge_wing_middle_down_le,Edge_wing_root_down_te,Edge_wing_middle_down_te,Edge_wing_root_up_le,Edge_wing_middle_up_le,Edge_wing_root_up_te,Edge_wing_middle_up_te,Edge_tail_root_down_le,Edge_tail_root_down_te,Edge_tail_root_up_le,Edge_tail_root_up_te])

            # Tip airfoils' edges
            Auto_group_for_Sub_mesh_Tip_Airfoil_Edges = geompy.CreateGroup(nasa_crm_igs, geompy.ShapeType["EDGE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Tip_Airfoil_Edges, [Edge_wing_tip_down_le,Edge_wing_tip_down_te,Edge_wing_tip_up_le,Edge_wing_tip_up_te,Edge_tail_tip_down_le,Edge_tail_tip_down_te,Edge_tail_tip_up_le,Edge_tail_tip_up_te,Edge_tail_tip_middle_le,Edge_tail_tip_middle_te,Edge_wing_tip_middle_le,Edge_wing_tip_middle_te])

            # Tip middle edges
            Auto_group_for_Sub_mesh_Tip_Middle_Edges = geompy.CreateGroup(nasa_crm_igs, geompy.ShapeType["EDGE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Tip_Middle_Edges, [Edge_tail_tip_middle_down,Edge_tail_tip_middle_up])

            # Wing and tail surfaces
            Auto_group_for_Sub_mesh_Wing_Tail_Surfaces = geompy.CreateGroup(nasa_crm_igs, geompy.ShapeType["FACE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Wing_Tail_Surfaces, [Face_crm_wing_root_down,Face_crm_wing_root_up,Face_crm_wing_down,Face_crm_wing_up,Face_crm_tail_down,Face_crm_tail_up])

            # Trailing edge surfaces
            Auto_group_for_Sub_mesh_Wing_Tail_Tip_Surfaces = geompy.CreateGroup(nasa_crm_igs, geompy.ShapeType["FACE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Wing_Tail_Tip_Surfaces, [Face_crm_wing_tip_down,Face_crm_wing_tip_up,Face_crm_tail_tip_le_down,Face_crm_tail_tip_le_up,Face_crm_tail_tip_te_down,Face_crm_tail_tip_te_up])

            # Trailing edge surfaces
            Auto_group_for_Sub_mesh_Trailing_Edge_Surfaces = geompy.CreateGroup(nasa_crm_igs, geompy.ShapeType["FACE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Trailing_Edge_Surfaces, [Face_crm_wing_root_te,Face_crm_wing_te,Face_crm_wing_tip_te,Face_crm_tail_te])

            # Fuselage edges
            Auto_group_for_Sub_mesh_Fuselage_Edges = geompy.CreateGroup(nasa_crm_igs, geompy.ShapeType["EDGE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Fuselage_Edges, [Edge_105,Edge_106,Edge_107,Edge_108,Edge_109,Edge_110,Edge_113,Edge_121,Edge_129,Edge_192,Edge_194,Edge_1100,Edge_1104])

            # Fuselage transition edges
            Auto_group_for_Sub_mesh_Fuselage_Transition_Edges = geompy.CreateGroup(nasa_crm_igs, geompy.ShapeType["EDGE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Fuselage_Transition_Edges, [Edge_112,Edge_115,Edge_118,Edge_123,Edge_126,Edge_131,Edge_193,Edge_197,Edge_199,Edge_1126,Edge_1127])

            # Root edges
            Auto_group_for_Sub_mesh_Root_Edges = geompy.CreateGroup(nasa_crm_igs, geompy.ShapeType["EDGE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Root_Edges, [Edge_114,Edge_119,Edge_125,Edge_127,Edge_130,Edge_140,Edge_144,Edge_145,Edge_146, Edge_1133])

            # Fuselage surfaces
            Auto_group_for_Sub_mesh_Fuselage_Surfaces = geompy.CreateGroup(nasa_crm_igs, geompy.ShapeType["FACE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Fuselage_Surfaces, [Face_crm_fuselage_middle_down,Face_crm_fuselage_middle_middle,Face_crm_fuselage_middle_up,Face_crm_fuselage_root_down,Face_crm_fuselage_root_up,Face_crm_fuselage_ring_up,Face_crm_fuselage_ring_down,Face_crm_fuselage_ring_middle,Face_crm_cockpit,Face_crm_fuselage_back])

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
            Face_crm_fuselage_root_down,\
            Face_crm_fuselage_root_up,\
            Face_crm_fuselage_root,\
            Face_crm_wing_root_down,\
            Face_crm_wing_root_up,Face_crm_wing_root_te,\
            Face_crm_wing_down,Face_crm_wing_up,Face_crm_fuselage_ring_up,\
            Face_crm_fuselage_ring_down,Face_crm_fuselage_ring_middle,Face_crm_wing_te,\
            Face_crm_wing_tip_down,Face_crm_wing_tip_up,Face_crm_wing_tip_te,\
            Face_crm_fuselage_back,\
            Face_crm_tail_down,Face_crm_tail_up,Face_crm_tail_te,\
            Face_crm_tail_tip_le_down,Face_crm_tail_tip_le_up,Face_crm_tail_tip_te_down,\
            Face_crm_tail_tip_te_up])

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
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_fuselage_root_down, 'Face_crm_fuselage_root_down' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_fuselage_root_up, 'Face_crm_fuselage_root_up' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_fuselage_root, 'Face_crm_fuselage_root' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_wing_root_down, 'Face_crm_wing_root_down' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_crm_wing_root_up, 'Face_crm_wing_root_up' )
            geompy.addToStudyInFather( nasa_crm_igs, Face_Left_Wall, 'Face_Left_Wall' )
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

            geompy.addToStudyInFather( Face_crm_fuselage_middle_up, Edge_121, 'Edge_121' )
            geompy.addToStudyInFather( Face_crm_fuselage_middle_up, Edge_123, 'Edge_123' )

            geompy.addToStudyInFather( Face_crm_fuselage_root_down, Edge_125, 'Edge_125' )
            geompy.addToStudyInFather( Face_crm_fuselage_root_down, Edge_126, 'Edge_126' )
            geompy.addToStudyInFather( Face_crm_fuselage_root_down, Edge_127, 'Edge_127' )

            geompy.addToStudyInFather( Face_crm_fuselage_root_up, Edge_129, 'Edge_129' )
            geompy.addToStudyInFather( Face_crm_fuselage_root_up, Edge_130, 'Edge_130' )
            geompy.addToStudyInFather( Face_crm_fuselage_root_up, Edge_131, 'Edge_131' )

            geompy.addToStudyInFather( Face_crm_fuselage_root, Edge_140, 'Edge_140' )
            geompy.addToStudyInFather( Face_crm_fuselage_root, Edge_143, 'Edge_143' )
            geompy.addToStudyInFather( Face_crm_fuselage_root, Edge_144, 'Edge_144' )
            geompy.addToStudyInFather( Face_crm_fuselage_root, Edge_145, 'Edge_145' )
            geompy.addToStudyInFather( Face_crm_fuselage_root, Edge_146, 'Edge_146' )

            geompy.addToStudyInFather( Face_crm_wing_root_down, Edge_wing_root_down_le, 'Edge_wing_root_down_le' )
            geompy.addToStudyInFather( Face_crm_wing_root_down, Edge_wing_root_le, 'Edge_wing_root_le' )
            geompy.addToStudyInFather( Face_crm_wing_root_down, Edge_wing_middle_down_le, 'Edge_wing_middle_down_le' )
            geompy.addToStudyInFather( Face_crm_wing_root_down, Edge_wing_root_down_te, 'Edge_wing_root_down_te' )
            geompy.addToStudyInFather( Face_crm_wing_root_down, Edge_wing_middle_down_te, 'Edge_wing_middle_down_te' )
            geompy.addToStudyInFather( Face_crm_wing_root_down, Edge_wing_root_te_down, 'Edge_wing_root_te_down' )

            geompy.addToStudyInFather( Face_crm_wing_root_up, Edge_wing_root_up_le, 'Edge_wing_root_up_le' )
            geompy.addToStudyInFather( Face_crm_wing_root_up, Edge_wing_middle_up_le, 'Edge_wing_middle_up_le' )
            geompy.addToStudyInFather( Face_crm_wing_root_up, Edge_wing_root_up_te, 'Edge_wing_root_up_te' )
            geompy.addToStudyInFather( Face_crm_wing_root_up, Edge_wing_middle_up_te, 'Edge_wing_middle_up_te' )
            geompy.addToStudyInFather( Face_crm_wing_root_up, Edge_wing_root_te_up, 'Edge_wing_root_te_up' )

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

            geompy.addToStudyInFather( Face_crm_wing_tip_te, Edge_1119, 'Edge_1119' )

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

            # Groups
            geompy.addToStudyInFather( nasa_crm_igs, Auto_group_for_Sub_mesh_LE_TE_Edges, 'Auto_group_for_Sub_mesh_LE_TE_Edges' )
            geompy.addToStudyInFather( nasa_crm_igs, Auto_group_for_Sub_mesh_Airfoil_Edges, 'Auto_group_for_Sub_mesh_Airfoil_Edges' )
            geompy.addToStudyInFather( nasa_crm_igs, Auto_group_for_Sub_mesh_Tip_Airfoil_Edges, 'Auto_group_for_Sub_mesh_Tip_Airfoil_Edges' )
            geompy.addToStudyInFather( nasa_crm_igs, Auto_group_for_Sub_mesh_Tip_Middle_Edges, 'Auto_group_for_Sub_mesh_Tip_Middle_Edges' )
            geompy.addToStudyInFather( nasa_crm_igs, Auto_group_for_Sub_mesh_Wing_Tail_Surfaces, 'Auto_group_for_Sub_mesh_Wing_Tail_Surfaces' )
            geompy.addToStudyInFather( nasa_crm_igs, Auto_group_for_Sub_mesh_Wing_Tail_Tip_Surfaces, 'Auto_group_for_Sub_mesh_Wing_Tail_Tip_Surfaces' )
            geompy.addToStudyInFather( nasa_crm_igs, Auto_group_for_Sub_mesh_Trailing_Edge_Surfaces, 'Auto_group_for_Sub_mesh_Trailing_Edge_Surfaces' )

            geompy.addToStudyInFather( nasa_crm_igs, Auto_group_for_Sub_mesh_Fuselage_Edges, 'Auto_group_for_Sub_mesh_Fuselage_Edges' )
            geompy.addToStudyInFather( nasa_crm_igs, Auto_group_for_Sub_mesh_Fuselage_Transition_Edges, 'Auto_group_for_Sub_mesh_Fuselage_Transition_Edges' )

            geompy.addToStudyInFather( nasa_crm_igs, Auto_group_for_Sub_mesh_Root_Edges, 'Auto_group_for_Sub_mesh_Root_Edges' )
            geompy.addToStudyInFather( nasa_crm_igs, Auto_group_for_Sub_mesh_Fuselage_Surfaces, 'Auto_group_for_Sub_mesh_Fuselage_Surfaces' )

            geompy.addToStudyInFather( nasa_crm_igs, Auto_group_for_Sub_mesh_Aircraft_Surfaces, 'Auto_group_for_Sub_mesh_Aircraft_Surfaces' )

            geompy.addToStudyInFather( nasa_crm_igs, Auto_group_for_Sub_mesh_Far_Field_Edges, 'Auto_group_for_Sub_mesh_Far_Field_Edges' )

            geompy.addToStudyInFather( nasa_crm_igs, Auto_group_for_Sub_mesh_Far_Field_Surfaces, 'Auto_group_for_Sub_mesh_Far_Field_Surfaces' )

            ###
            ### SMESH component
            ###

            import  SMESH, SALOMEDS
            from salome.smesh import smeshBuilder

            smesh = smeshBuilder.New(theStudy)

            # Set NETGEN 3D
            Mesh_Domain = smesh.Mesh(nasa_crm_igs)

            NETGEN_3D = Mesh_Domain.Tetrahedron()
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
            Start_and_End_Length_Airfoils = Regular_1D_Airfoils.StartEndLength(Smallest_Airfoil_Mesh_Size,Biggest_Airfoil_Mesh_Size,[Edge_wing_root_down_te,Edge_wing_middle_down_te,Edge_wing_root_up_le,Edge_wing_middle_up_le,Edge_tail_root_down_te,Edge_tail_root_up_le,Edge_tail_root_up_te])
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

            # Root edges
            Regular_1D_Root = Mesh_Domain.Segment(geom=Auto_group_for_Sub_mesh_Root_Edges)
            Sub_mesh_Root_Edges = Regular_1D_Root.GetSubMesh()
            Local_Length_Root = Regular_1D_Root.LocalLength(Root_Mesh_Size,None,1e-07)

            # Fuselage 143 Edge
            Regular_1D_Fuselage_143_Edge = Mesh_Domain.Segment(geom=Edge_143)
            Start_and_End_Length_Fuselage_143_Edge = Regular_1D_Fuselage_143_Edge.StartEndLength(0.005,Root_Mesh_Size,[])
            Start_and_End_Length_Fuselage_143_Edge.SetObjectEntry( 'nasa_crm_igs' )
            Sub_mesh_Fuselage_143_Edge = Regular_1D_Fuselage_143_Edge.GetSubMesh()

            # Fuselage Transition Edges
            Regular_1D_Fuselage_Transition_Edges = Mesh_Domain.Segment(geom=Auto_group_for_Sub_mesh_Fuselage_Transition_Edges)
            Start_and_End_Length_Fuselage_Transition_Edges = Regular_1D_Fuselage_Transition_Edges.StartEndLength(Root_Mesh_Size,Fuselage_Mesh_Size,[Edge_115,Edge_123,Edge_126,Edge_131,Edge_193,Edge_197,Edge_199,Edge_1126])
            Start_and_End_Length_Fuselage_Transition_Edges.SetObjectEntry( 'nasa_crm_igs' )
            Sub_mesh_Fuselage_Transition_Edges = Regular_1D_Fuselage_Transition_Edges.GetSubMesh()

            # Fuselage edges
            Regular_1D_Fuselage = Mesh_Domain.Segment(geom=Auto_group_for_Sub_mesh_Fuselage_Edges)
            Sub_mesh_Fuselage_Edges = Regular_1D_Fuselage.GetSubMesh()
            Local_Length_Fuselage = Regular_1D_Fuselage.LocalLength(Fuselage_Mesh_Size,None,1e-07)

            # Far field edges
            Regular_1D_Far_Field_Edges = Mesh_Domain.Segment(geom=Auto_group_for_Sub_mesh_Far_Field_Edges)
            Sub_mesh_Far_Field_Edges = Regular_1D_Far_Field_Edges.GetSubMesh()
            Local_Length_Far_Field = Regular_1D_Far_Field_Edges.LocalLength(Far_Field_Mesh_Size,None,1e-07)

            # Wing surface
            NETGEN_2D = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_2D,geom=Auto_group_for_Sub_mesh_Wing_Tail_Surfaces)
            NETGEN_2D_Parameters_Wing = NETGEN_2D.Parameters()
            NETGEN_2D_Parameters_Wing.SetMaxSize( Biggest_Airfoil_Mesh_Size )
            NETGEN_2D_Parameters_Wing.SetOptimize( 1 )
            NETGEN_2D_Parameters_Wing.SetFineness( 5 )
            NETGEN_2D_Parameters_Wing.SetGrowthRate( Growth_Rate_Wing )
            NETGEN_2D_Parameters_Wing.SetNbSegPerEdge( 6.92154e-310 )
            NETGEN_2D_Parameters_Wing.SetNbSegPerRadius( 5.32336e-317 )
            NETGEN_2D_Parameters_Wing.SetMinSize( Smallest_Airfoil_Mesh_Size )
            NETGEN_2D_Parameters_Wing.SetUseSurfaceCurvature( 1 )
            NETGEN_2D_Parameters_Wing.SetQuadAllowed( 0 )
            NETGEN_2D_Parameters_Wing.SetSecondOrder( 106 )
            NETGEN_2D_Parameters_Wing.SetFuseEdges( 80 )
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

            # Root surface
            NETGEN_2D_Root = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_2D,geom=Face_crm_fuselage_root)
            NETGEN_2D_Parameters_Root = NETGEN_2D_Root.Parameters()
            NETGEN_2D_Parameters_Root.SetMaxSize( Biggest_Airfoil_Mesh_Size )
            NETGEN_2D_Parameters_Root.SetOptimize( 1 )
            NETGEN_2D_Parameters_Root.SetFineness( 5 )
            NETGEN_2D_Parameters_Root.SetGrowthRate( Growth_Rate_Wing*3.0 )
            NETGEN_2D_Parameters_Root.SetNbSegPerEdge( 6.92154e-310 )
            NETGEN_2D_Parameters_Root.SetNbSegPerRadius( 5.32336e-317 )
            NETGEN_2D_Parameters_Root.SetMinSize( 0.005 )
            NETGEN_2D_Parameters_Root.SetUseSurfaceCurvature( 1 )
            NETGEN_2D_Parameters_Root.SetQuadAllowed( 0 )
            NETGEN_2D_Parameters_Root.SetSecondOrder( 106 )
            NETGEN_2D_Parameters_Root.SetFuseEdges( 80 )
            Sub_mesh_Root_Surface = NETGEN_2D_Root.GetSubMesh()

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

            te_path = salome_output_path + '/Sub-mesh_TE_Case_' + str(case) + '_AOA_' + str(AOA) + '_Wing_Span_' + str(
              Wing_span) + '_Airfoil_Mesh_Size_' + str(Smallest_Airfoil_Mesh_Size) + '_Growth_Rate_Wing_' + str(
                Growth_Rate_Wing) + '_Growth_Rate_Domain_' + str(Growth_Rate_Domain) + '.dat'

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
              Mesh_Domain.ExportDAT( r'/' + far_field_path, Sub_mesh_Far_Field_Surface )
              pass
            except:
              print 'ExportPartToDAT() failed. Invalid file name?'
            try:
              Mesh_Domain.ExportDAT( r'/' + te_path, Sub_mesh_Trailing_Edge_Surface )
              pass
            except:
              print 'ExportPartToDAT() failed. Invalid file name?'

            ## Set names of Mesh objects
            smesh.SetName(NETGEN_3D.GetAlgorithm(), 'NETGEN 3D')
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

            smesh.SetName(Regular_1D_Root.GetAlgorithm(), 'Regular_1D_Root')
            smesh.SetName(Local_Length_Root, 'Local_Length_Root')
            smesh.SetName(Sub_mesh_Root_Edges, 'Sub_mesh_Root_Edges')

            smesh.SetName(Regular_1D_Fuselage_143_Edge.GetAlgorithm(), 'Regular_1D_Fuselage_143_Edge')
            smesh.SetName(Start_and_End_Length_Fuselage_143_Edge, 'Start_and_End_Length_Fuselage_143_Edge')
            smesh.SetName(Sub_mesh_Fuselage_143_Edge, 'Sub_mesh_Fuselage_143_Edge')

            smesh.SetName(Regular_1D_Fuselage_Transition_Edges.GetAlgorithm(), 'Regular_1D_Fuselage_Transition_Edges')
            smesh.SetName(Start_and_End_Length_Fuselage_Transition_Edges, 'Start_and_End_Length_Fuselage_Transition_Edges')
            smesh.SetName(Sub_mesh_Fuselage_Transition_Edges, 'Sub_mesh_Fuselage_Transition_Edges')

            smesh.SetName(Regular_1D_Fuselage.GetAlgorithm(), 'Regular_1D_Fuselage')
            smesh.SetName(Local_Length_Fuselage, 'Local_Length_Fuselage')
            smesh.SetName(Sub_mesh_Fuselage_Edges, 'Sub_mesh_Fuselage_Edges')

            smesh.SetName(Regular_1D_Far_Field_Edges.GetAlgorithm(), 'Regular_1D_Far_Field_Edges')
            smesh.SetName(Local_Length_Far_Field, 'Local_Length_Far_Field')
            smesh.SetName(Sub_mesh_Far_Field_Edges, 'Sub_mesh_Far_Field_Edges')

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

            smesh.SetName(NETGEN_2D_Aircraft.GetAlgorithm(), 'NETGEN_2D_Aircraft')
            smesh.SetName(NETGEN_2D_Parameters_Aircraft, 'NETGEN_2D_Parameters_Aircraft')
            smesh.SetName(Sub_mesh_Aircraft_Surface, 'Sub_mesh_Aircraft_Surface')

            smesh.SetName(NETGEN_2D_Far_Field.GetAlgorithm(), 'NETGEN_2D_Far_Field')
            smesh.SetName(NETGEN_2D_Parameters_FarField, 'NETGEN_2D_Parameters_FarField')
            smesh.SetName(Sub_mesh_Far_Field_Surface, 'Sub_mesh_Far_Field_Surface')

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
