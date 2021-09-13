# -*- coding: utf-8 -*-

###
### This file is generated automatically by SALOME v8.4.0 with dump python functionality
###
import os
import killSalome
import math

# Parameters:
Domain_Length = 200
Domain_Height = Domain_Length
Domain_Width = 200
wake_angle_deg = 0.0

Smallest_Airfoil_Mesh_Size = TBD
Biggest_Airfoil_Mesh_Size = TBD
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

            # Wing
            [Obj1,Obj2,Obj3,Edge_wing_tip_te1] = geompy.ExtractShapes(Face_crm_wing_te, geompy.ShapeType["EDGE"], True)
            [Obj1,Edge_wing_tip_middle_le,Obj2,Edge_wing_tip_middle_te,Edge_wing_tip_te2] = geompy.ExtractShapes(Face_crm_wing_tip_down, geompy.ShapeType["EDGE"], True)
            [Obj1,Obj2,Obj3,Obj4,Edge_wing_tip_te3] = geompy.ExtractShapes(Face_crm_wing_tip_up, geompy.ShapeType["EDGE"], True)
            [Edge_1119,Obj1,Obj2,Obj3] = geompy.ExtractShapes(Face_crm_wing_tip_te, geompy.ShapeType["EDGE"], True)

            [Edge_123,Edge_124,Edge_125,Edge_126,Edge_127,Edge_128,Edge_129,Edge_130,Edge_131,Edge_132,Edge_133] = geompy.ExtractShapes         (Face_crm_fuselage_back, geompy.ShapeType["EDGE"], True)
            [Edge_142,Edge_143,Edge_144,Edge_145,Edge_146,Edge_147] = geompy.ExtractShapes(Face_crm_tail_down, geompy.ShapeType["EDGE"],            True)
            [Edge_148,Edge_149,Edge_150,Edge_151,Edge_152,Edge_153] = geompy.ExtractShapes(Face_crm_tail_up, geompy.ShapeType["EDGE"],          True)
            [Edge_154,Edge_155,Edge_156,Edge_157,Edge_158] = geompy.ExtractShapes(Face_crm_tail_te, geompy.ShapeType["EDGE"], True)
            [Edge_159,Edge_160,Edge_161] = geompy.ExtractShapes(Face_crm_tail_tip_le_down, geompy.ShapeType["EDGE"], True)
            [Edge_162,Edge_163,Edge_164] = geompy.ExtractShapes(Face_crm_tail_tip_le_up, geompy.ShapeType["EDGE"], True)
            [Edge_165,Edge_166,Edge_167,Edge_168] = geompy.ExtractShapes(Face_crm_tail_tip_te_down, geompy.ShapeType["EDGE"], True)
            [Edge_169,Edge_170,Edge_171,Edge_172] = geompy.ExtractShapes(Face_crm_tail_tip_te_up, geompy.ShapeType["EDGE"], True)

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

            geompy.addToStudyInFather( Face_crm_fuselage_back, Edge_123, 'Edge_123' )
            geompy.addToStudyInFather( Face_crm_fuselage_back, Edge_124, 'Edge_124' )
            geompy.addToStudyInFather( Face_crm_fuselage_back, Edge_125, 'Edge_125' )
            geompy.addToStudyInFather( Face_crm_fuselage_back, Edge_126, 'Edge_126' )
            geompy.addToStudyInFather( Face_crm_fuselage_back, Edge_127, 'Edge_127' )
            geompy.addToStudyInFather( Face_crm_fuselage_back, Edge_128, 'Edge_128' )
            geompy.addToStudyInFather( Face_crm_fuselage_back, Edge_129, 'Edge_129' )
            geompy.addToStudyInFather( Face_crm_fuselage_back, Edge_130, 'Edge_130' )
            geompy.addToStudyInFather( Face_crm_fuselage_back, Edge_131, 'Edge_131' )
            geompy.addToStudyInFather( Face_crm_fuselage_back, Edge_132, 'Edge_132' )
            geompy.addToStudyInFather( Face_crm_fuselage_back, Edge_133, 'Edge_133' )
            geompy.addToStudyInFather( Face_Down_Wall, Edge_134, 'Edge_134' )
            geompy.addToStudyInFather( Face_Down_Wall, Edge_135, 'Edge_135' )
            geompy.addToStudyInFather( Face_Down_Wall, Edge_136, 'Edge_136' )
            geompy.addToStudyInFather( Face_Down_Wall, Edge_137, 'Edge_137' )
            geompy.addToStudyInFather( Face_Top_Wall, Edge_138, 'Edge_138' )
            geompy.addToStudyInFather( Face_Top_Wall, Edge_139, 'Edge_139' )
            geompy.addToStudyInFather( Face_Top_Wall, Edge_140, 'Edge_140' )
            geompy.addToStudyInFather( Face_Top_Wall, Edge_141, 'Edge_141' )
            geompy.addToStudyInFather( Face_crm_tail_down, Edge_142, 'Edge_142' )
            geompy.addToStudyInFather( Face_crm_tail_down, Edge_143, 'Edge_143' )
            geompy.addToStudyInFather( Face_crm_tail_down, Edge_144, 'Edge_144' )
            geompy.addToStudyInFather( Face_crm_tail_down, Edge_145, 'Edge_145' )
            geompy.addToStudyInFather( Face_crm_tail_down, Edge_146, 'Edge_146' )
            geompy.addToStudyInFather( Face_crm_tail_down, Edge_147, 'Edge_147' )
            geompy.addToStudyInFather( Face_crm_tail_up, Edge_148, 'Edge_148' )
            geompy.addToStudyInFather( Face_crm_tail_up, Edge_149, 'Edge_149' )
            geompy.addToStudyInFather( Face_crm_tail_up, Edge_150, 'Edge_150' )
            geompy.addToStudyInFather( Face_crm_tail_up, Edge_151, 'Edge_151' )
            geompy.addToStudyInFather( Face_crm_tail_up, Edge_152, 'Edge_152' )
            geompy.addToStudyInFather( Face_crm_tail_up, Edge_153, 'Edge_153' )
            geompy.addToStudyInFather( Face_crm_tail_te, Edge_154, 'Edge_154' )
            geompy.addToStudyInFather( Face_crm_tail_te, Edge_155, 'Edge_155' )
            geompy.addToStudyInFather( Face_crm_tail_te, Edge_156, 'Edge_156' )
            geompy.addToStudyInFather( Face_crm_tail_te, Edge_157, 'Edge_157' )
            geompy.addToStudyInFather( Face_crm_tail_te, Edge_158, 'Edge_158' )
            geompy.addToStudyInFather( Face_crm_tail_tip_le_down, Edge_159, 'Edge_159' )
            geompy.addToStudyInFather( Face_crm_tail_tip_le_down, Edge_160, 'Edge_160' )
            geompy.addToStudyInFather( Face_crm_tail_tip_le_down, Edge_161, 'Edge_161' )
            geompy.addToStudyInFather( Face_crm_tail_tip_le_up, Edge_162, 'Edge_162' )
            geompy.addToStudyInFather( Face_crm_tail_tip_le_up, Edge_163, 'Edge_163' )
            geompy.addToStudyInFather( Face_crm_tail_tip_le_up, Edge_164, 'Edge_164' )
            geompy.addToStudyInFather( Face_crm_tail_tip_te_down, Edge_165, 'Edge_165' )
            geompy.addToStudyInFather( Face_crm_tail_tip_te_down, Edge_166, 'Edge_166' )
            geompy.addToStudyInFather( Face_crm_tail_tip_te_down, Edge_167, 'Edge_167' )
            geompy.addToStudyInFather( Face_crm_tail_tip_te_down, Edge_168, 'Edge_168' )
            geompy.addToStudyInFather( Face_crm_tail_tip_te_up, Edge_169, 'Edge_169' )
            geompy.addToStudyInFather( Face_crm_tail_tip_te_up, Edge_170, 'Edge_170' )
            geompy.addToStudyInFather( Face_crm_tail_tip_te_up, Edge_171, 'Edge_171' )
            geompy.addToStudyInFather( Face_crm_tail_tip_te_up, Edge_172, 'Edge_172' )
            geompy.addToStudyInFather( Face_Right, Edge_173, 'Edge_173' )
            geompy.addToStudyInFather( Face_Right, Edge_174, 'Edge_174' )
            geompy.addToStudyInFather( Face_Right, Edge_175, 'Edge_175' )
            geompy.addToStudyInFather( Face_Right, Edge_176, 'Edge_176' )
            geompy.addToStudyInFather( Face_Outlet, Edge_177, 'Edge_177' )
            geompy.addToStudyInFather( Face_Outlet, Edge_178, 'Edge_178' )
            geompy.addToStudyInFather( Face_Outlet, Edge_179, 'Edge_179' )
            geompy.addToStudyInFather( Face_Outlet, Edge_180, 'Edge_180' )

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
