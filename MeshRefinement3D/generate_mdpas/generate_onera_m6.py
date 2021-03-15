# -*- coding: utf-8 -*-

###
### This file is generated automatically by SALOME v8.4.0 with dump python functionality
###
import os
import killSalome

# Parameters:
Wing_span = TBD
Domain_Length = 25
Domain_Height = Domain_Length
Domain_Width = 25
separating_domains = True

# Outlet_Min_Mesh_Size = 0.05
# Outlet_Max_Mesh_Size = 0.1
# Growth_Rate_Wake = 0.7
Refinement_Box_Face_Min_Mesh_Size = 0.1
Refinement_Box_Face_Max_Mesh_Size = 0.1

Smallest_Airfoil_Mesh_Size = TBD
Biggest_Airfoil_Mesh_Size = TBD
LE_Mesh_Size = Smallest_Airfoil_Mesh_Size
TE_Mesh_Size = Smallest_Airfoil_Mesh_Size
Far_Field_Mesh_Size = Domain_Length/20.0

print '\nWing_span = ', Wing_span
print 'Domain_Length = ', Domain_Length
print 'Smallest_Airfoil_Mesh_Size = ', Smallest_Airfoil_Mesh_Size
print 'Biggest_Airfoil_Mesh_Size = ', Biggest_Airfoil_Mesh_Size
print 'Far_Field_Mesh_Size = ', Far_Field_Mesh_Size
print 'Refinement_Box_Face_Min_Mesh_Size = ', Refinement_Box_Face_Min_Mesh_Size
print 'Refinement_Box_Face_Max_Mesh_Size = ', Refinement_Box_Face_Max_Mesh_Size

# print '\nOutlet_Min_Mesh_Size = ', Outlet_Min_Mesh_Size
# print 'Outlet_Max_Mesh_Size = ', Outlet_Max_Mesh_Size
# print 'Growth_Rate_Wake = ', Growth_Rate_Wake

Number_Of_AOAS = TBD
Number_Of_Domains_Refinements = TBD
Number_Of_Wing_Refinements = TBD

Initial_AOA = TBD
AOA_Increment = TBD

Initial_Growth_Rate_Wing = TBD
Growth_Rate_Wing_Refinement_Factor = TBD

Initial_Growth_Rate_Domain = TBD
Growth_Rate_Domain_Refinement_Factor = TBD

Growth_Rate_Refinement_Box = 0.1

salome_output_path = 'TBD'
mdpa_path = 'TBD'
geometry_path = "/home/inigo/software/FullPotentialSolverUtilities/MeshRefinement3D/generate_mdpas/onera_m6_geometry/AileM6_with_sharp_TE_gid_divided.igs"
if not os.path.exists(salome_output_path):
    os.makedirs(salome_output_path)
if not os.path.exists(mdpa_path):
    os.makedirs(mdpa_path)

case = 0
AOA = Initial_AOA

Initial_Smallest_Airfoil_Mesh_Size = Smallest_Airfoil_Mesh_Size
Initial_Biggest_Airfoil_Mesh_Size = Biggest_Airfoil_Mesh_Size

for k in range(Number_Of_AOAS):
    AOA = round(AOA, 2)
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

            AileM6_with_sharp_TE_igs_1 = geompy.ImportIGES(geometry_path)

            # Rotate around center to AOA
            geompy.Rotate(AileM6_with_sharp_TE_igs_1, OY, AOA*math.pi/180.0)

            # Refinement Box
            Refinement_Box_Height = 0.5
            Gap = 0.2
            Extrusion_Box_Length = Domain_Width/2.0 + Gap
            Face_Refinement_Box = geompy.MakeFaceHW(Refinement_Box_Height, Extrusion_Box_Length, 3)
            geompy.TranslateDXDYDZ(Face_Refinement_Box, (Domain_Width-Extrusion_Box_Length)/2.0, 0, 0)
            Extrusion_Refinement_Box = geompy.MakePrismVecH(Face_Refinement_Box, OY, Wing_span + Gap)
            Cut_Refinement_Box = geompy.MakeCutList(Extrusion_Refinement_Box, [AileM6_with_sharp_TE_igs_1], True)

            # Making Domain
            Face_Domain = geompy.MakeFaceHW(Domain_Length, Domain_Height, 3)
            Extrusion_Domain = geompy.MakePrismVecH(Face_Domain, OY,  Domain_Width/2.0)
            Cut_Domain = geompy.MakeCutList(Extrusion_Domain, [Extrusion_Refinement_Box], True)
            Partition_Domain = geompy.MakePartition([Cut_Refinement_Box, Cut_Domain], [], [], [], geompy.ShapeType["SOLID"], 0, [], 0)

            # Explode Partition
            [Solid_Domain,Solid_Refinement_Box] = geompy.ExtractShapes(Partition_Domain, geompy.ShapeType["SOLID"], True)

            # Explode Domain
            [Face_Inlet,Face_Refinementbox_Inlet,Face_Left_Wall,Face_Down_Wall,\
                Face_Top_Wall,Face_Right_Wall,\
                Obj1,Obj2,\
                Obj3,\
                Face_Outlet] = geompy.ExtractShapes(Solid_Domain, geompy.ShapeType["FACE"], True)

            # Explode Refinement Box
            [Face_Refinementbox_Inlet_1,Face_Wing_Lower,Face_Wing_Upper,Face_Wing_Tip_Upper,\
                    Face_Wing_Tip_Lower,Face_Refinementbox_Left_1,\
                    Face_Refinementbox_Down_1,Face_Refinementbox_Top_1,\
                    Face_Refinementbox_Right_1,Face_Refinementbox_Outlet_1] = geompy.ExtractShapes(Solid_Refinement_Box, geompy.ShapeType["FACE"], True)

            # Exploding far field
            [Edge_1,Edge_2,Edge_3,Edge_4] = geompy.ExtractShapes(Face_Inlet, geompy.ShapeType["EDGE"], True)
            [Obj1,Obj2,Edge_6,Edge_7,Obj3,Obj4,Obj5,Obj6] = geompy.ExtractShapes(Face_Left_Wall, geompy.ShapeType["EDGE"], True)
            [Obj1,Edge_8,Edge_9,Obj2] = geompy.ExtractShapes(Face_Right_Wall, geompy.ShapeType["EDGE"], True)
            [Edge_17,Edge_18,Obj2,Obj3,Obj4,Edge_10,Edge_11,Edge_12] = geompy.ExtractShapes(Face_Outlet, geompy.ShapeType["EDGE"], True)

            # Exploding refinement box faces
            [Edge_Ref_In_Left,Edge_Ref_In_Bottom,Edge_Ref_In_Top,Edge_Ref_In_Right] = geompy.ExtractShapes(Face_Refinementbox_Inlet_1, geompy.ShapeType["EDGE"], True)
            [Obj1,Obj2,Obj3,Obj4,Obj5,Edge_Ref_Left_Bottom,Edge_Ref_Left_Top,Obj8] = geompy.ExtractShapes(Face_Refinementbox_Left_1, geompy.ShapeType["EDGE"], True)
            [Obj1,Edge_Ref_Right_Bottom,Edge_Ref_Right_Top,Obj2] = geompy.ExtractShapes(Face_Refinementbox_Right_1, geompy.ShapeType["EDGE"], True)
            [Edge_Ref_Out_Left,Edge_Ref_Out_Bottom,Edge_Ref_Out_Top,Edge_Ref_Out_Right] = geompy.ExtractShapes(Face_Refinementbox_Outlet_1, geompy.ShapeType["EDGE"], True)

            # Exploding wing
            [Edge_Wing_Left_Lower_LE, Edge_LE, Edge_Wing_Left_Lower_TE, Edge_Wing_Right_Lower_LE1, Edge_Wing_Right_Lower_LE2, Edge_TE, Edge_Wing_Right_Lower_TE2, Edge_Wing_Right_Lower_TE1] = geompy.ExtractShapes(Face_Wing_Lower, geompy.ShapeType["EDGE"], True)

            [Edge_Wing_Left_Upper_LE, Obj1, Edge_Wing_Left_Upper_TE, Edge_Wing_Right_Upper_LE1, Edge_Wing_Right_Upper_LE2, Obj2, Edge_Wing_Right_Upper_TE2, Edge_Wing_Right_Upper_TE1] = geompy.ExtractShapes(Face_Wing_Upper, geompy.ShapeType["EDGE"], True)

            [Obj1, Edge_Wing_Tip_LE1, Obj2, Edge_Wing_Tip_LE2,Obj3, Edge_Wing_Tip_TE2, Obj4, Edge_Wing_Tip_TE1] = geompy.ExtractShapes(Face_Wing_Tip_Upper, geompy.ShapeType["EDGE"], True)

            # [Edge_Wing_Right_Lower_LE1, Edge_Wing_Tip_LE1, Edge_Wing_Right_Lower_LE2, Edge_Wing_Tip_LE2,Edge_Wing_Right_Lower_TE2, Edge_Wing_Tip_TE2, Edge_Wing_Right_Lower_TE1, Edge_Wing_Tip_TE1] = geompy.ExtractShapes(Face_Wing_Tip_Lower, geompy.ShapeType["EDGE"], True)

            # Making groups for submeshes
            # LE edges
            Auto_group_for_Sub_mesh_LE_Edges = geompy.CreateGroup(Partition_Domain, geompy.ShapeType["EDGE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_LE_Edges, [Edge_LE, Edge_Wing_Tip_LE1, Edge_Wing_Right_Lower_LE1, Edge_Wing_Right_Upper_LE1, Edge_Wing_Right_Lower_LE2, Edge_Wing_Right_Upper_LE2, Edge_Wing_Tip_LE2])

            # TE edges
            Auto_group_for_Sub_mesh_TE_Edges = geompy.CreateGroup(Partition_Domain, geompy.ShapeType["EDGE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_TE_Edges, [Edge_TE, Edge_Wing_Tip_TE1, Edge_Wing_Right_Lower_TE1, Edge_Wing_Right_Upper_TE1, Edge_Wing_Right_Lower_TE2, Edge_Wing_Right_Upper_TE2, Edge_Wing_Tip_TE2])

            # LE Airfoil edges
            Auto_group_for_Sub_mesh_LE_Airfoils = geompy.CreateGroup(Partition_Domain, geompy.ShapeType["EDGE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_LE_Airfoils, [Edge_Wing_Left_Lower_LE, Edge_Wing_Left_Upper_LE])

            # TE Airfoil edges
            Auto_group_for_Sub_mesh_TE_Airfoils = geompy.CreateGroup(Partition_Domain, geompy.ShapeType["EDGE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_TE_Airfoils, [Edge_Wing_Left_Lower_TE, Edge_Wing_Left_Upper_TE])

            # Wing surface
            Auto_group_for_Sub_mesh_Wing_Surface = geompy.CreateGroup(Partition_Domain, geompy.ShapeType["FACE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Wing_Surface, [Face_Wing_Lower, Face_Wing_Upper,Face_Wing_Tip_Upper,\
                    Face_Wing_Tip_Lower])

            '''
            # Far field edges
            Auto_group_for_Sub_mesh_Far_Field_Edges = geompy.CreateGroup(Partition_Domain, geompy.ShapeType["EDGE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Far_Field_Edges, [Edge_1, Edge_2, Edge_3, Edge_4, Edge_6, Edge_7, Edge_8, Edge_9, Edge_10, Edge_11, Edge_12])

            # Refinemenet box inlet edges
            Auto_group_for_Sub_mesh_Refinement_Box_Edges_Inlet = geompy.CreateGroup(Partition_Domain, geompy.ShapeType["EDGE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Refinement_Box_Edges_Inlet, [Edge_Ref_In_Left, Edge_Ref_In_Bottom, Edge_Ref_In_Top, Edge_Ref_In_Right])

            # Refinemenet box side edges
            Auto_group_for_Sub_mesh_Refinement_Box_Side_Edges = geompy.CreateGroup(Partition_Domain, geompy.ShapeType["EDGE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Refinement_Box_Side_Edges, [Edge_Ref_Left_Bottom, Edge_Ref_Left_Top, Edge_Ref_Right_Bottom, Edge_Ref_Right_Top])

            # Refinement box outlet edges
            Auto_group_for_Sub_mesh_Refinement_Box_Outlet_Edges = geompy.CreateGroup(Partition_Domain, geompy.ShapeType["EDGE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Refinement_Box_Outlet_Edges, [Edge_Ref_Out_Bottom, Edge_Ref_Out_Top, Edge_Ref_Out_Left, Edge_Ref_Out_Right])

            #Surfaces
            # Far field surface
            Auto_group_for_Sub_mesh_Far_Field_Surface = geompy.CreateGroup(Partition_Domain, geompy.ShapeType["FACE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Far_Field_Surface, [Face_Inlet, Face_Left_Wall, Face_Down_Wall, Face_Top_Wall, Face_Right_Wall, Face_Outlet, Face_Refinementbox_Outlet_1])

            # Refinement box faces
            Auto_group_for_Sub_mesh_Refinement_Box_Faces_Sides = geompy.CreateGroup(Partition_Domain, geompy.ShapeType["FACE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Refinement_Box_Faces_Sides, [Face_Refinementbox_Inlet_1])
            Auto_group_for_Sub_mesh_Refinement_Box_Faces_Coarse = geompy.CreateGroup(Partition_Domain, geompy.ShapeType["FACE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Refinement_Box_Faces_Coarse, [Face_Refinementbox_Down_1, Face_Refinementbox_Top_1, Face_Refinementbox_Left_1, Face_Refinementbox_Right_1])

            [Face_Refinementbox_Inlet_1,Face_Wing_Lower,Face_Wing_Upper,Face_Wing_Tip_Upper,\
                    Face_Wing_Tip_Lower,Face_Refinementbox_Left_1,\
                    Face_Refinementbox_Down_1,Face_Refinementbox_Top_1,\
                    Face_Refinementbox_Right_1,Face_Refinementbox_Outlet_1] = geompy.ExtractShapes(Solid_Refinement_Box, geompy.ShapeType["FACE"], True)

            '''
            geompy.addToStudy( O, 'O' )
            geompy.addToStudy( OX, 'OX' )
            geompy.addToStudy( OY, 'OY' )
            geompy.addToStudy( OZ, 'OZ' )
            geompy.addToStudy( AileM6_with_sharp_TE_igs_1, 'AileM6_with_sharp_TE.igs_1' )

            geompy.addToStudy( Cut_Refinement_Box, 'Cut_Refinement_Box' )
            geompy.addToStudy( Face_Domain, 'Face_Domain' )
            geompy.addToStudy( Extrusion_Domain, 'Extrusion_Domain' )
            geompy.addToStudy( Cut_Domain, 'Cut_Domain' )
            geompy.addToStudy( Partition_Domain, 'Partition_Domain' )

            geompy.addToStudyInFather( Partition_Domain, Solid_Domain, 'Solid_Domain' )
            geompy.addToStudyInFather( Partition_Domain, Solid_Refinement_Box, 'Solid_Refinement_Box' )

            geompy.addToStudyInFather( Solid_Domain, Face_Inlet, 'Face_Inlet' )
            geompy.addToStudyInFather( Solid_Domain, Face_Left_Wall, 'Face_Left_Wall' )
            geompy.addToStudyInFather( Solid_Domain, Face_Down_Wall, 'Face_Down_Wall' )
            geompy.addToStudyInFather( Solid_Domain, Face_Top_Wall, 'Face_Top_Wall' )
            geompy.addToStudyInFather( Solid_Domain, Face_Right_Wall, 'Face_Right_Wall' )
            geompy.addToStudyInFather( Solid_Domain, Face_Outlet, 'Face_Outlet' )

            geompy.addToStudyInFather( Solid_Refinement_Box, Face_Refinementbox_Inlet_1, 'Face_Refinementbox_Inlet_1' )
            geompy.addToStudyInFather( Solid_Refinement_Box, Face_Wing_Lower, 'Face_Wing_Lower' )
            geompy.addToStudyInFather( Solid_Refinement_Box, Face_Wing_Upper, 'Face_Wing_Upper' )
            geompy.addToStudyInFather( Solid_Refinement_Box, Face_Wing_Tip_Upper, 'Face_Wing_Tip_Upper' )
            geompy.addToStudyInFather( Solid_Refinement_Box, Face_Wing_Tip_Lower, 'Face_Wing_Tip_Lower' )
            geompy.addToStudyInFather( Solid_Refinement_Box, Face_Refinementbox_Left_1, 'Face_Refinementbox_Left_1' )
            geompy.addToStudyInFather( Solid_Refinement_Box, Face_Refinementbox_Down_1, 'Face_Refinementbox_Down_1' )
            geompy.addToStudyInFather( Solid_Refinement_Box, Face_Refinementbox_Top_1, 'Face_Refinementbox_Top_1' )
            geompy.addToStudyInFather( Solid_Refinement_Box, Face_Refinementbox_Right_1, 'Face_Refinementbox_Right_1' )
            geompy.addToStudyInFather( Solid_Refinement_Box, Face_Refinementbox_Outlet_1, 'Face_Refinementbox_Outlet_1' )

            geompy.addToStudyInFather( Face_Inlet, Edge_1, 'Edge_1' )
            geompy.addToStudyInFather( Face_Inlet, Edge_2, 'Edge_2' )
            geompy.addToStudyInFather( Face_Inlet, Edge_3, 'Edge_3' )
            geompy.addToStudyInFather( Face_Inlet, Edge_4, 'Edge_4' )

            geompy.addToStudyInFather( Face_Left_Wall, Edge_6, 'Edge_6' )
            geompy.addToStudyInFather( Face_Left_Wall, Edge_7, 'Edge_7' )

            geompy.addToStudyInFather( Face_Right_Wall, Edge_8, 'Edge_8' )
            geompy.addToStudyInFather( Face_Right_Wall, Edge_9, 'Edge_9' )

            geompy.addToStudyInFather( Face_Outlet, Edge_17, 'Edge_17' )
            geompy.addToStudyInFather( Face_Outlet, Edge_18, 'Edge_18' )
            geompy.addToStudyInFather( Face_Outlet, Edge_10, 'Edge_10' )
            geompy.addToStudyInFather( Face_Outlet, Edge_11, 'Edge_11' )
            geompy.addToStudyInFather( Face_Outlet, Edge_12, 'Edge_12' )

            geompy.addToStudyInFather( Face_Refinementbox_Inlet_1, Edge_Ref_In_Left, 'Edge_Ref_In_Left' )
            geompy.addToStudyInFather( Face_Refinementbox_Inlet_1, Edge_Ref_In_Bottom, 'Edge_Ref_In_Bottom' )
            geompy.addToStudyInFather( Face_Refinementbox_Inlet_1, Edge_Ref_In_Top, 'Edge_Ref_In_Top' )
            geompy.addToStudyInFather( Face_Refinementbox_Inlet_1, Edge_Ref_In_Right, 'Edge_Ref_In_Right' )

            geompy.addToStudyInFather( Face_Refinementbox_Left_1, Edge_Ref_Left_Bottom, 'Edge_Ref_Left_Bottom' )
            geompy.addToStudyInFather( Face_Refinementbox_Left_1, Edge_Ref_Left_Top, 'Edge_Ref_Left_Top' )

            geompy.addToStudyInFather( Face_Refinementbox_Right_1, Edge_Ref_Right_Bottom, 'Edge_Ref_Right_Bottom' )
            geompy.addToStudyInFather( Face_Refinementbox_Right_1, Edge_Ref_Right_Top, 'Edge_Ref_Right_Top' )

            geompy.addToStudyInFather( Face_Refinementbox_Outlet_1, Edge_Ref_Out_Left, 'Edge_Ref_Out_Left' )
            geompy.addToStudyInFather( Face_Refinementbox_Outlet_1, Edge_Ref_Out_Bottom, 'Edge_Ref_Out_Bottom' )
            geompy.addToStudyInFather( Face_Refinementbox_Outlet_1, Edge_Ref_Out_Top, 'Edge_Ref_Out_Top' )
            geompy.addToStudyInFather( Face_Refinementbox_Outlet_1, Edge_Ref_Out_Right, 'Edge_Ref_Out_Right' )

            geompy.addToStudyInFather( Face_Wing_Lower, Edge_Wing_Left_Lower_LE, 'Edge_Wing_Left_Lower_LE' )
            geompy.addToStudyInFather( Face_Wing_Lower, Edge_LE, 'Edge_LE' )
            geompy.addToStudyInFather( Face_Wing_Lower, Edge_Wing_Left_Lower_TE, 'Edge_Wing_Left_Lower_TE' )
            geompy.addToStudyInFather( Face_Wing_Lower, Edge_Wing_Right_Lower_LE1, 'Edge_Wing_Right_Lower_LE1' )
            geompy.addToStudyInFather( Face_Wing_Lower, Edge_Wing_Right_Lower_LE2, 'Edge_Wing_Right_Lower_LE2' )
            geompy.addToStudyInFather( Face_Wing_Lower, Edge_TE, 'Edge_TE' )
            geompy.addToStudyInFather( Face_Wing_Lower, Edge_Wing_Right_Lower_TE2, 'Edge_Wing_Right_Lower_TE2' )
            geompy.addToStudyInFather( Face_Wing_Lower, Edge_Wing_Right_Lower_TE1, 'Edge_Wing_Right_Lower_TE1' )

            geompy.addToStudyInFather( Face_Wing_Upper, Edge_Wing_Left_Upper_LE, 'Edge_Wing_Left_Upper_LE' )
            geompy.addToStudyInFather( Face_Wing_Upper, Edge_Wing_Left_Upper_TE, 'Edge_Wing_Left_Upper_TE' )
            geompy.addToStudyInFather( Face_Wing_Upper, Edge_Wing_Right_Upper_LE1, 'Edge_Wing_Right_Upper_LE1' )
            geompy.addToStudyInFather( Face_Wing_Upper, Edge_Wing_Right_Upper_LE2, 'Edge_Wing_Right_Upper_LE2' )
            geompy.addToStudyInFather( Face_Wing_Upper, Edge_Wing_Right_Upper_TE2, 'Edge_Wing_Right_Upper_TE2' )
            geompy.addToStudyInFather( Face_Wing_Upper, Edge_Wing_Right_Upper_TE1, 'Edge_Wing_Right_Upper_TE1' )

            geompy.addToStudyInFather( Face_Wing_Tip_Upper, Edge_Wing_Tip_LE1, 'Edge_Wing_Tip_LE1' )
            geompy.addToStudyInFather( Face_Wing_Tip_Upper, Edge_Wing_Tip_LE2, 'Edge_Wing_Tip_LE2' )
            geompy.addToStudyInFather( Face_Wing_Tip_Upper, Edge_Wing_Tip_TE2, 'Edge_Wing_Tip_TE2' )
            geompy.addToStudyInFather( Face_Wing_Tip_Upper, Edge_Wing_Tip_TE1, 'Edge_Wing_Tip_TE1' )

            geompy.addToStudyInFather( Partition_Domain, Auto_group_for_Sub_mesh_LE_Edges, 'Auto_group_for_Sub_mesh_LE_Edges' )
            geompy.addToStudyInFather( Partition_Domain, Auto_group_for_Sub_mesh_TE_Edges, 'Auto_group_for_Sub_mesh_TE_Edges' )
            geompy.addToStudyInFather( Partition_Domain, Auto_group_for_Sub_mesh_LE_Airfoils, 'Auto_group_for_Sub-mesh_LE_Airfoils' )
            geompy.addToStudyInFather( Partition_Domain, Auto_group_for_Sub_mesh_TE_Airfoils, 'Auto_group_for_Sub-mesh_TE_Airfoils' )
            geompy.addToStudyInFather( Partition_Domain, Auto_group_for_Sub_mesh_Wing_Surface, 'Auto_group_for_Sub-mesh_Wing_Surface' )

            '''

            geompy.addToStudyInFather( Partition_Domain, Auto_group_for_Sub_mesh_Far_Field_Surface, 'Auto_group_for_Sub-mesh_Far_Field_Surface' )

            geompy.addToStudyInFather( Partition_Domain, Auto_group_for_Sub_mesh_Far_Field_Edges, 'Auto_group_for_Sub-mesh_Far_Field_Edges' )
            geompy.addToStudyInFather( Partition_Domain, Auto_group_for_Sub_mesh_Refinement_Box_Edges_Inlet, 'Auto_group_for_Sub-mesh_Refinement_Box_Edges' )
            geompy.addToStudyInFather( Partition_Domain, Auto_group_for_Sub_mesh_Refinement_Box_Side_Edges, 'Auto_group_for_Sub_mesh_Refinement_Box_Side_Edges' )
            geompy.addToStudyInFather( Partition_Domain, Auto_group_for_Sub_mesh_Refinement_Box_Outlet_Edges, 'Auto_group_for_Sub-mesh_Refinement_Box_Outlet_Edges' )
            geompy.addToStudyInFather( Partition_Domain, Auto_group_for_Sub_mesh_Refinement_Box_Faces_Sides, 'Auto_group_for_Sub-mesh_Refinement_Box_Faces_Sides' )
            geompy.addToStudyInFather( Partition_Domain, Auto_group_for_Sub_mesh_Refinement_Box_Faces_Coarse, 'Auto_group_for_Sub-mesh_Refinement_Box_Faces_Coarse' )


            '''

            ###
            ### SMESH component
            ###

            import  SMESH, SALOMEDS
            from salome.smesh import smeshBuilder

            smesh = smeshBuilder.New(theStudy)

            # Set NETGEN 3D
            Mesh_Domain = smesh.Mesh(Partition_Domain)

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

            # LE
            Regular_1D_4 = Mesh_Domain.Segment(geom=Auto_group_for_Sub_mesh_LE_Edges)
            Sub_mesh_LE = Regular_1D_4.GetSubMesh()
            Local_Length_LE = Regular_1D_4.LocalLength(Smallest_Airfoil_Mesh_Size,None,1e-07)

            # TE
            Regular_1D_3 = Mesh_Domain.Segment(geom=Auto_group_for_Sub_mesh_TE_Edges)
            Sub_mesh_TE = Regular_1D_3.GetSubMesh()
            Local_Length_TE = Regular_1D_3.LocalLength(Smallest_Airfoil_Mesh_Size,None,1e-07)

            # LE Airfoils
            Regular_1D_1 = Mesh_Domain.Segment(geom=Auto_group_for_Sub_mesh_LE_Airfoils)
            Start_and_End_Length_LE = Regular_1D_1.StartEndLength(Smallest_Airfoil_Mesh_Size,Biggest_Airfoil_Mesh_Size,[51,71])
            Start_and_End_Length_LE.SetObjectEntry( 'Partition_Domain' )
            Sub_mesh_LE_Airfoils = Regular_1D_1.GetSubMesh()

            # TE Airfoils
            Regular_1D_2 = Mesh_Domain.Segment(geom=Auto_group_for_Sub_mesh_TE_Airfoils)
            Start_and_End_Length_TE = Regular_1D_2.StartEndLength(Biggest_Airfoil_Mesh_Size,Smallest_Airfoil_Mesh_Size,[53, 73])
            Start_and_End_Length_TE.SetObjectEntry( 'Partition_Domain' )
            Sub_mesh_TE_Airfoils = Regular_1D_2.GetSubMesh()

            # # Far field edges
            # Regular_1D = Mesh_Domain.Segment(geom=Auto_group_for_Sub_mesh_Far_Field_Edges)
            # Local_Length_Far_Field = Regular_1D.LocalLength(Far_Field_Mesh_Size,None,1e-07)
            # Sub_mesh_Far_Field_Edges = Regular_1D.GetSubMesh()

            # Wing surface
            NETGEN_2D = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_2D,geom=Auto_group_for_Sub_mesh_Wing_Surface)
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

            isDone = Mesh_Domain.Compute()

            ## Set names of Mesh objects
            smesh.SetName(NETGEN_3D.GetAlgorithm(), 'NETGEN 3D')
            smesh.SetName(NETGEN_3D_Parameters, 'NETGEN_3D_Parameters')
            smesh.SetName(Mesh_Domain.GetMesh(), 'Mesh_Domain')

            smesh.SetName(Regular_1D_4.GetAlgorithm(), 'Regular_1D_4')
            smesh.SetName(Local_Length_LE, 'Local_Length_LE')
            smesh.SetName(Sub_mesh_LE, 'Sub_mesh_LE')

            smesh.SetName(Regular_1D_3.GetAlgorithm(), 'Regular_1D_3')
            smesh.SetName(Local_Length_TE, 'Local_Length_TE')
            smesh.SetName(Sub_mesh_TE, 'Sub_mesh_TE')

            smesh.SetName(Regular_1D_1.GetAlgorithm(), 'Regular_1D_1')
            smesh.SetName(Start_and_End_Length_LE, 'Start_and_End_Length_LE')
            smesh.SetName(Sub_mesh_LE_Airfoils, 'Sub_mesh_LE_Airfoils')

            smesh.SetName(Regular_1D_2.GetAlgorithm(), 'Regular_1D_2')
            smesh.SetName(Start_and_End_Length_TE, 'Start_and_End_Length_TE')
            smesh.SetName(Sub_mesh_TE_Airfoils, 'Sub_mesh_TE_Airfoils')

            smesh.SetName(NETGEN_2D.GetAlgorithm(), 'NETGEN_2D')
            smesh.SetName(NETGEN_2D_Parameters_Wing, 'NETGEN 2D Parameters_Wing')
            smesh.SetName(Sub_mesh_Wing_Surface, 'Sub-mesh_Wing_Surface')


            '''

            # smesh.SetName(Regular_1D.GetAlgorithm(), 'Regular_1D')
            # smesh.SetName(Local_Length_Far_Field, 'Local_Length_Far_Field')
            # smesh.SetName(Sub_mesh_Far_Field_Edges, 'Sub_mesh_Far_Field_Edges')
            '''



            # Saving file to open from salome's gui
            file_name = salome_output_path + "/generate_onera_m6.hdf"
            salome.myStudyManager.SaveAs(file_name, salome.myStudy, 0)

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
