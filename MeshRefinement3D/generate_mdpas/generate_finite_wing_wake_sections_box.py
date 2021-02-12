# -*- coding: utf-8 -*-

###
### This file is generated automatically by SALOME v8.4.0 with dump python functionality
###
import os
import killSalome

# Parameters:
Wing_span = TBD
Domain_Length = 100
Domain_Height = Domain_Length
Domain_Width = 100
separating_domains = True

# Outlet_Min_Mesh_Size = 0.05
# Outlet_Max_Mesh_Size = 0.1
# Growth_Rate_Wake = 0.7
Refinement_Box_Face_Min_Mesh_Size = 0.2
Refinement_Box_Face_Max_Mesh_Size = 0.5

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
if not os.path.exists(salome_output_path):
    os.makedirs(salome_output_path)
if not os.path.exists(mdpa_path):
    os.makedirs(mdpa_path)

case = 0
AOA = Initial_AOA

Initial_Smallest_Airfoil_Mesh_Size = Smallest_Airfoil_Mesh_Size
Initial_Biggest_Airfoil_Mesh_Size = Biggest_Airfoil_Mesh_Size

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
            Smallest_Airfoil_Mesh_Size = round(Smallest_Airfoil_Mesh_Size, 3)
            Biggest_Airfoil_Mesh_Size = round(Biggest_Airfoil_Mesh_Size, 3)
            print '\n case = ', case, ' AOA = ', AOA, ' Growth_Rate_Domain = ', Growth_Rate_Domain, ' Growth_Rate_Wing = ', Growth_Rate_Wing
            print 'Smallest_Airfoil_Mesh_Size = ', Smallest_Airfoil_Mesh_Size, ' Biggest_Airfoil_Mesh_Size = ', Biggest_Airfoil_Mesh_Size

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


            geompy = geomBuilder.New(theStudy)

            # Create origin and axis
            O = geompy.MakeVertex(0, 0, 0)
            OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
            OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
            OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)

            # Create naca0012
            Curve_UpperSurface_LE = geompy.MakeCurveParametric("t - 0.5", "0.0", "0.6*(0.2969*sqrt(t) - 0.1260*t - 0.3516*t**2 + 0.2843*t**3 - 0.1036*t**4)", 0, 0.5, 999, GEOM.Interpolation, True)
            Curve_UpperSurface_TE = geompy.MakeCurveParametric("t - 0.5", "0.0", "0.6*(0.2969*sqrt(t) - 0.1260*t - 0.3516*t**2 + 0.2843*t**3 - 0.1036*t**4)", 0.5, 1, 999, GEOM.Interpolation, True)
            Curve_LowerSurface_TE = geompy.MakeCurveParametric("t - 0.5", "0.0", "-0.6*(0.2969*sqrt(t) - 0.1260*t - 0.3516*t**2 + 0.2843*t**3 - 0.1036*t**4)", 0.5, 1, 999, GEOM.Interpolation, True)
            Curve_LowerSurface_LE = geompy.MakeCurveParametric("t - 0.5", "0.0", "-0.6*(0.2969*sqrt(t) - 0.1260*t - 0.3516*t**2 + 0.2843*t**3 - 0.1036*t**4)", 0, 0.5, 999, GEOM.Interpolation, True)

            Wire_Airfoil = geompy.MakeWire([Curve_UpperSurface_LE, Curve_UpperSurface_TE, Curve_LowerSurface_TE, Curve_LowerSurface_LE], 1e-07)
            geompy.Rotate(Wire_Airfoil, OY, AOA*math.pi/180.0)

            # Create face
            Face_Airfoil = geompy.MakeFaceWires([Curve_UpperSurface_LE, Curve_UpperSurface_TE, Curve_LowerSurface_TE, Curve_LowerSurface_LE], 1)

            # Rotate around center to AOA
            geompy.Rotate(Face_Airfoil, OY, AOA*math.pi/180.0)
            Face_Airfoil_Section_100 = geompy.MakeTranslation(Wire_Airfoil, 0, 1, 0)
            Face_Airfoil_Section_150 = geompy.MakeTranslation(Wire_Airfoil, 0, 1.5, 0)
            Face_Airfoil_Section_180 = geompy.MakeTranslation(Wire_Airfoil, 0, 1.8, 0)

            # Extrusion of the wing
            Extrusion_Wing = geompy.MakePrismVecH2Ways(Face_Airfoil, OY, Wing_span/2.0)

            # Exploding wing
            [Face_Left_Wing_1,Face_Lower_LE_1,Face_Upper_LE_1,Face_Right_Wing_1,Face_Lower_TE_1,Face_Upper_TE_1] = geompy.ExtractShapes(Extrusion_Wing, geompy.ShapeType["FACE"], True)

            # Eploding Face_Lower_TE
            [Obj1,Obj2,Obj3,Edge_TE_1] = geompy.ExtractShapes(Face_Lower_TE_1, geompy.ShapeType["EDGE"], True)

            # Generate stl wake
            Vector_Wake_Direction = geompy.MakeVectorDXDYDZ(1, 0, 0)
            Translation_1 = geompy.MakeTranslation(Edge_TE_1, 0, 0, 0)
            Vertex_1 = geompy.MakeVertex(0.5*math.cos(AOA*math.pi/180.0), 0, -0.5*math.sin(AOA*math.pi/180.0))
            Scale_1 = geompy.MakeScaleTransform(Translation_1, Vertex_1, 0.999875)
            Extrusion_Wake_stl = geompy.MakePrismVecH(Scale_1, Vector_Wake_Direction, Domain_Length*0.5)

            # Partition wing
            Partition_Wing = geompy.MakePartition([Extrusion_Wing], [Wire_Airfoil], [], [], geompy.ShapeType["SOLID"], 0, [], 0)
            Partition_Wing_1 = geompy.MakePartition([Partition_Wing], [Face_Airfoil_Section_100], [], [], geompy.ShapeType["SOLID"], 0, [], 0)
            Partition_Wing_2 = geompy.MakePartition([Partition_Wing_1], [Face_Airfoil_Section_150], [], [], geompy.ShapeType["SOLID"], 0, [], 0)
            Partition_Wing_3 = geompy.MakePartition([Partition_Wing_2], [Face_Airfoil_Section_180], [], [], geompy.ShapeType["SOLID"], 0, [], 0)

            # Refinement Box
            Face_Refinement_Box = geompy.MakeFaceHW(1, 5, 2)
            geompy.TranslateDXDYDZ(Face_Refinement_Box, -1, 0, 0)
            Extrusion_Refinement_Box = geompy.MakePrismVecH(Face_Refinement_Box, OX, Domain_Width/2.0 + 1.0)
            Cut_Refinement_Box = geompy.MakeCutList(Extrusion_Refinement_Box, [Partition_Wing_3], True)

            # Making Domain
            Face_Domain = geompy.MakeFaceHW(Domain_Length, Domain_Height, 3)
            Extrusion_Domain = geompy.MakePrismVecH2Ways(Face_Domain, OY,  Domain_Width/2.0)
            Cut_Domain = geompy.MakeCutList(Extrusion_Domain, [Extrusion_Refinement_Box], True)
            Partition_Domain = geompy.MakePartition([Cut_Refinement_Box, Cut_Domain], [], [], [], geompy.ShapeType["SOLID"], 0, [], 0)
            # Partition_Domain = geompy.MakeGlueFaces([Cut_Refinement_Box, Cut_Domain], 1e-07)

            if separating_domains:
                print ('Separating domains geometries')
                # Explode partition
                [Solid_Domain,Solid_Refinement_Box] = geompy.ExtractShapes(Partition_Domain, geompy.ShapeType["SOLID"], True)

                # Explode Domain
                [Face_Inlet,Face_Left_Wall,Face_Refinementbox_Inlet,\
                    Face_Down_Wall,Face_Top_Wall,Face_Right_Wall,\
                    Obj1,Obj2,\
                    Obj3,Obj4,\
                    Face_Outlet] = geompy.ExtractShapes(Solid_Domain, geompy.ShapeType["FACE"], True)

                # Explode Refinement Box
                [Face_Refinementbox_Inlet_1,Face_Lower_LE_Left,Face_Upper_LE_Left,Face_Left_Wing,\
                    Face_Lower_LE_Right_0,Face_Upper_LE_Right_0,\
                    Face_Lower_LE_Right_1,Face_Upper_LE_Right_1,\
                    Face_Lower_LE_Right_2,Face_Upper_LE_Right_2,\
                    Face_Lower_LE_Right_3,Face_Upper_LE_Right_3,\
                    Face_Right_Wing,\
                    Face_Lower_TE_Left,Face_Upper_TE_Left,\
                    Face_Lower_TE_Right_0,Face_Upper_TE_Right_0,\
                    Face_Lower_TE_Right_1,Face_Upper_TE_Right_1,\
                    Face_Lower_TE_Right_2,Face_Upper_TE_Right_2,\
                    Face_Lower_TE_Right_3,Face_Upper_TE_Right_3,\
                    Face_Refinementbox_Left_1,Face_Refinementbox_Down_1,\
                    Face_Refinementbox_Top_1,Face_Refinementbox_Right_1,\
                    Face_Refinementbox_Outlet_1] = geompy.ExtractShapes(Solid_Refinement_Box, geompy.ShapeType["FACE"], True)
            else:
                print ('Using one single domain')
                # Explode partition
                [Face_Inlet,Face_Left_Wall,Face_Refinementbox_Inlet_1,\
                    Face_Lower_LE_Left,Face_Upper_LE_Left,Face_Left_Wing,\
                    Face_Lower_LE_Right_0,Face_Upper_LE_Right_0,\
                    Face_Lower_LE_Right_1,Face_Upper_LE_Right_1,\
                    Face_Lower_LE_Right_2,Face_Upper_LE_Right_2,\
                    Face_Lower_LE_Right_3,Face_Upper_LE_Right_3,\
                    Face_Down_Wall,Face_Top_Wall,Face_Right_Wing,\
                    Face_Lower_TE_Left,Face_Upper_TE_Left,\
                    Face_Lower_TE_Right_0,Face_Upper_TE_Right_0,\
                    Face_Lower_TE_Right_1,Face_Upper_TE_Right_1,\
                    Face_Lower_TE_Right_2,Face_Upper_TE_Right_2,\
                    Face_Lower_TE_Right_3,Face_Upper_TE_Right_3,\
                    Face_Right_Wall,\
                    Face_Refinementbox_Left_1,Face_Refinementbox_Down_1,\
                    Face_Refinementbox_Top_1,Face_Refinementbox_Right_1,\
                    Face_Refinementbox_Outlet_1,\
                    Face_Outlet] = geompy.ExtractShapes(Partition_Domain, geompy.ShapeType["FACE"], True)

            # Exploding far field
            [Edge_1,Edge_2,Edge_3,Edge_4] = geompy.ExtractShapes(Face_Inlet, geompy.ShapeType["EDGE"], True)
            [Obj1,Edge_6,Edge_7,Obj2] = geompy.ExtractShapes(Face_Left_Wall, geompy.ShapeType["EDGE"], True)
            [Obj1,Edge_8,Edge_9,Obj2] = geompy.ExtractShapes(Face_Right_Wall, geompy.ShapeType["EDGE"], True)
            [Edge_5,Obj1,Edge_10,Obj2,Obj3,Edge_11,Obj4,Edge_12] = geompy.ExtractShapes(Face_Outlet, geompy.ShapeType["EDGE"], True)

            # Exploding refinement box faces
            [Edge_Ref_In_Left,Edge_Ref_In_Bottom,Edge_Ref_In_Top,Edge_Ref_In_Right] = geompy.ExtractShapes(Face_Refinementbox_Inlet_1, geompy.ShapeType["EDGE"], True)
            [Obj1,Edge_Ref_Left_Bottom,Edge_Ref_Left_Top,Obj2] = geompy.ExtractShapes(Face_Refinementbox_Left_1, geompy.ShapeType["EDGE"], True)
            [Obj1,Edge_Ref_Right_Bottom,Edge_Ref_Right_Top,Obj2] = geompy.ExtractShapes(Face_Refinementbox_Right_1, geompy.ShapeType["EDGE"], True)
            [Edge_Ref_Out_Left,Edge_Ref_Out_Bottom,Edge_Ref_Out_Top,Edge_Ref_Out_Right] = geompy.ExtractShapes(Face_Refinementbox_Outlet_1, geompy.ShapeType["EDGE"], True)

            # # Exploding Edge_Ref_Out_Bottom
            # [Vertex_1,Vertex_2] = geompy.ExtractShapes(Edge_Ref_Out_Bottom, geompy.ShapeType["VERTEX"], True)
            # [Vertex_3,Vertex_4] = geompy.ExtractShapes(Edge_Ref_Out_Top, geompy.ShapeType["VERTEX"], True)

            # Exploding wing
            [Edge_LE_Left,    Edge_Left_LowerLE,Edge_Middle_LowerLE,      Edge_Left_Lower_Middle]     = geompy.ExtractShapes(Face_Lower_LE_Left, geompy.ShapeType["EDGE"], True)
            [Obj1,            Edge_Left_UpperLE,Edge_Middle_UpperLE,      Edge_Left_Upper_Middle]     = geompy.ExtractShapes(Face_Upper_LE_Left, geompy.ShapeType["EDGE"], True)
            [Edge_LE_Right_0, Obj1,             Edge_LowerLE_Section_100, Edge_Right_Lower_Middle_0]  = geompy.ExtractShapes(Face_Lower_LE_Right_0, geompy.ShapeType["EDGE"], True)
            [Obj1,            Obj2,             Edge_UpperLE_Section_100, Edge_Right_Upper_Middle_0]  = geompy.ExtractShapes(Face_Upper_LE_Right_0, geompy.ShapeType["EDGE"], True)

            [Edge_LE_Right_1, Obj1,             Edge_LowerLE_Section_150, Edge_Right_Lower_Middle_1]  = geompy.ExtractShapes(Face_Lower_LE_Right_1, geompy.ShapeType["EDGE"], True)
            [Obj1,            Obj2,             Edge_UpperLE_Section_150, Edge_Right_Upper_Middle_1]  = geompy.ExtractShapes(Face_Upper_LE_Right_1, geompy.ShapeType["EDGE"], True)

            [Edge_LE_Right_2, Obj1,             Edge_LowerLE_Section_180, Edge_Right_Lower_Middle_2]  = geompy.ExtractShapes(Face_Lower_LE_Right_2, geompy.ShapeType["EDGE"], True)
            [Obj1,            Obj2,             Edge_UpperLE_Section_180, Edge_Right_Upper_Middle_2]  = geompy.ExtractShapes(Face_Upper_LE_Right_2, geompy.ShapeType["EDGE"], True)

            [Edge_LE_Right_3, Obj1,             Edge_Right_LowerLE,       Edge_Right_Lower_Middle_3]  = geompy.ExtractShapes(Face_Lower_LE_Right_3, geompy.ShapeType["EDGE"], True)
            [Obj1,            Obj2,             Edge_Right_UpperLE,       Edge_Right_Upper_Middle_3]  = geompy.ExtractShapes(Face_Upper_LE_Right_3, geompy.ShapeType["EDGE"], True)

            [Obj1 , Edge_Left_Lower_TE, Edge_Middle_LowerTE,      Edge_TE_Left]    = geompy.ExtractShapes(Face_Lower_TE_Left, geompy.ShapeType["EDGE"], True)
            [Obj1 , Edge_Left_Upper_TE, Edge_Middle_UpperTE,      Obj2        ]    = geompy.ExtractShapes(Face_Upper_TE_Left, geompy.ShapeType["EDGE"], True)
            [Obj1 , Obj2              , Edge_LowerTE_Section_100, Edge_TE_Right_0] = geompy.ExtractShapes(Face_Lower_TE_Right_0, geompy.ShapeType["EDGE"], True)
            [Obj1 , Obj2              , Edge_UpperTE_Section_100, Obj3]            = geompy.ExtractShapes(Face_Upper_TE_Right_0, geompy.ShapeType["EDGE"], True)

            [Obj1 , Obj2              , Edge_LowerTE_Section_150, Edge_TE_Right_1] = geompy.ExtractShapes(Face_Lower_TE_Right_1, geompy.ShapeType["EDGE"], True)
            [Obj1 , Obj2              , Edge_UpperTE_Section_150, Obj3]            = geompy.ExtractShapes(Face_Upper_TE_Right_1, geompy.ShapeType["EDGE"], True)

            [Obj1 , Obj2              , Edge_LowerTE_Section_180, Edge_TE_Right_2] = geompy.ExtractShapes(Face_Lower_TE_Right_2, geompy.ShapeType["EDGE"], True)
            [Obj1 , Obj2              , Edge_UpperTE_Section_180, Obj3]            = geompy.ExtractShapes(Face_Upper_TE_Right_2, geompy.ShapeType["EDGE"], True)

            [Obj1 , Obj2              , Edge_Right_LowerTE,       Edge_TE_Right_3] = geompy.ExtractShapes(Face_Lower_TE_Right_3, geompy.ShapeType["EDGE"], True)
            [Obj1 , Obj2              , Edge_Right_UpperTE,       Obj3]            = geompy.ExtractShapes(Face_Upper_TE_Right_3, geompy.ShapeType["EDGE"], True)

            # Making groups for submeshes
            # # Vertex
            # Auto_group_for_Sub_mesh_Wake_Vertex = geompy.CreateGroup(Partition_Domain, geompy.ShapeType["VERTEX"])
            # geompy.UnionList(Auto_group_for_Sub_mesh_Wake_Vertex, [Vertex_1, Vertex_2, Vertex_3, Vertex_4])

            # Far field edges
            Auto_group_for_Sub_mesh_Far_Field_Edges = geompy.CreateGroup(Partition_Domain, geompy.ShapeType["EDGE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Far_Field_Edges, [Edge_1, Edge_2, Edge_3, Edge_4, Edge_6, Edge_7, Edge_8, Edge_9, Edge_5, Edge_10, Edge_11, Edge_12])

            # Refinemenet box inlet edges
            Auto_group_for_Sub_mesh_Refinement_Box_Edges = geompy.CreateGroup(Partition_Domain, geompy.ShapeType["EDGE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Refinement_Box_Edges, [Edge_Ref_In_Left, Edge_Ref_In_Bottom, Edge_Ref_In_Top, Edge_Ref_In_Right])

            # Refinemenet box side edges
            Auto_group_for_Sub_mesh_Refinement_Box_Side_Edges = geompy.CreateGroup(Partition_Domain, geompy.ShapeType["EDGE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Refinement_Box_Side_Edges, [Edge_Ref_Left_Bottom, Edge_Ref_Left_Top, Edge_Ref_Right_Bottom, Edge_Ref_Right_Top])

            # Refinement box outlet edges
            Auto_group_for_Sub_mesh_Refinement_Box_Outlet_Edges = geompy.CreateGroup(Partition_Domain, geompy.ShapeType["EDGE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Refinement_Box_Outlet_Edges, [Edge_Ref_Out_Bottom, Edge_Ref_Out_Top, Edge_Ref_Out_Left, Edge_Ref_Out_Right])

            # TE Airfoil edges
            Auto_group_for_Sub_mesh_LE_Airfoils = geompy.CreateGroup(Partition_Domain, geompy.ShapeType["EDGE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_LE_Airfoils, [Edge_Left_LowerLE, Edge_Left_UpperLE, Edge_Right_LowerLE, Edge_Right_UpperLE])

            # LE Airfoil edges
            Auto_group_for_Sub_mesh_TE_Airfoils = geompy.CreateGroup(Partition_Domain, geompy.ShapeType["EDGE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_TE_Airfoils, [Edge_Left_Lower_TE, Edge_Left_Upper_TE, Edge_Right_LowerTE, Edge_Right_UpperTE])

            # LE edges
            Auto_group_for_Sub_mesh_LE_Edges = geompy.CreateGroup(Partition_Domain, geompy.ShapeType["EDGE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_LE_Edges, [Edge_LE_Left, Edge_LE_Right_0, Edge_LE_Right_1, Edge_LE_Right_2, Edge_LE_Right_3])

            # TE edges
            Auto_group_for_Sub_mesh_TE_Edges = geompy.CreateGroup(Partition_Domain, geompy.ShapeType["EDGE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_TE_Edges, [Edge_TE_Left, Edge_TE_Right_0, Edge_TE_Right_1, Edge_TE_Right_2, Edge_TE_Right_3])

            # Middle
            Auto_group_for_Sub_mesh_Middle = geompy.CreateGroup(Partition_Domain, geompy.ShapeType["EDGE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Middle, [Edge_Left_Lower_Middle, Edge_Left_Upper_Middle, Edge_Right_Lower_Middle_0, Edge_Right_Lower_Middle_1, \
              Edge_Right_Lower_Middle_2, Edge_Right_Lower_Middle_3, Edge_Right_Upper_Middle_0, Edge_Right_Upper_Middle_1, Edge_Right_Upper_Middle_2, Edge_Right_Upper_Middle_3])

            # Middle section edges
            Auto_group_for_Sub_mesh_Middle_Airfoils = geompy.CreateGroup(Partition_Domain, geompy.ShapeType["EDGE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Middle_Airfoils, [Edge_Middle_LowerLE, Edge_Middle_UpperLE, Edge_Middle_LowerTE, Edge_Middle_UpperTE])

            # Section 100 edges
            Auto_group_for_Sub_mesh_Section_100 = geompy.CreateGroup(Partition_Domain, geompy.ShapeType["EDGE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Section_100, [Edge_LowerLE_Section_100, Edge_UpperLE_Section_100, Edge_LowerTE_Section_100, Edge_UpperTE_Section_100])

            # Section 150 edges
            Auto_group_for_Sub_mesh_Section_150 = geompy.CreateGroup(Partition_Domain, geompy.ShapeType["EDGE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Section_150, [Edge_LowerLE_Section_150, Edge_UpperLE_Section_150, Edge_LowerTE_Section_150, Edge_UpperTE_Section_150])

            # Section 180 edges
            Auto_group_for_Sub_mesh_Section_180 = geompy.CreateGroup(Partition_Domain, geompy.ShapeType["EDGE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Section_180, [Edge_LowerLE_Section_180, Edge_UpperLE_Section_180, Edge_LowerTE_Section_180, Edge_UpperTE_Section_180])

            #Surfaces
            # Far field surface
            Auto_group_for_Sub_mesh_Far_Field_Surface = geompy.CreateGroup(Partition_Domain, geompy.ShapeType["FACE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Far_Field_Surface, [Face_Inlet, Face_Left_Wall, Face_Down_Wall, Face_Top_Wall, Face_Right_Wall, Face_Outlet])

            # Refinement box faces
            Auto_group_for_Sub_mesh_Refinement_Box_Faces_Sides = geompy.CreateGroup(Partition_Domain, geompy.ShapeType["FACE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Refinement_Box_Faces_Sides, [Face_Refinementbox_Inlet_1])
            Auto_group_for_Sub_mesh_Refinement_Box_Faces_Coarse = geompy.CreateGroup(Partition_Domain, geompy.ShapeType["FACE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Refinement_Box_Faces_Coarse, [Face_Refinementbox_Down_1, Face_Refinementbox_Top_1, Face_Refinementbox_Outlet_1, Face_Refinementbox_Left_1, Face_Refinementbox_Right_1])

            # Wing surface
            Auto_group_for_Sub_mesh_Wing_Surface = geompy.CreateGroup(Partition_Domain, geompy.ShapeType["FACE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Wing_Surface, [Face_Left_Wing, Face_Lower_LE_Left, Face_Upper_LE_Left, \
              Face_Lower_LE_Right_0,Face_Upper_LE_Right_0,\
              Face_Lower_LE_Right_1,Face_Upper_LE_Right_1,\
              Face_Lower_LE_Right_2,Face_Upper_LE_Right_2,\
              Face_Lower_LE_Right_3,Face_Upper_LE_Right_3,\
              Face_Right_Wing, Face_Lower_TE_Left, Face_Upper_TE_Left,\
              Face_Lower_TE_Right_0,Face_Upper_TE_Right_0,\
              Face_Lower_TE_Right_1,Face_Upper_TE_Right_1,\
              Face_Lower_TE_Right_2,Face_Upper_TE_Right_2,\
              Face_Lower_TE_Right_3,Face_Upper_TE_Right_3])

            # Adding to study
            geompy.addToStudy( O, 'O' )
            geompy.addToStudy( OX, 'OX' )
            geompy.addToStudy( OY, 'OY' )
            geompy.addToStudy( OZ, 'OZ' )
            geompy.addToStudy( Curve_UpperSurface_LE, 'Curve_UpperSurface_LE' )
            geompy.addToStudy( Curve_UpperSurface_TE, 'Curve_UpperSurface_TE' )
            geompy.addToStudy( Curve_LowerSurface_TE, 'Curve_LowerSurface_TE' )
            geompy.addToStudy( Curve_LowerSurface_LE, 'Curve_LowerSurface_LE' )
            geompy.addToStudy( Wire_Airfoil, 'Wire_Airfoil' )
            geompy.addToStudy( Face_Airfoil, 'Face_Airfoil' )
            geompy.addToStudy( Face_Airfoil_Section_100, 'Face_Airfoil_Section_100' )
            geompy.addToStudy( Face_Airfoil_Section_150, 'Face_Airfoil_Section_150' )
            geompy.addToStudy( Face_Airfoil_Section_180, 'Face_Airfoil_Section_180' )
            geompy.addToStudy( Extrusion_Wing, 'Extrusion_Wing' )

            geompy.addToStudyInFather( Extrusion_Wing, Face_Left_Wing_1, 'Face_Left_Wing_1' )
            geompy.addToStudyInFather( Extrusion_Wing, Face_Lower_LE_1, 'Face_Lower_LE_1' )
            geompy.addToStudyInFather( Extrusion_Wing, Face_Upper_LE_1, 'Face_Upper_LE_1' )
            geompy.addToStudyInFather( Extrusion_Wing, Face_Right_Wing_1, 'Face_Right_Wing_1' )
            geompy.addToStudyInFather( Extrusion_Wing, Face_Lower_TE_1, 'Face_Lower_TE_1' )
            geompy.addToStudyInFather( Partition_Wing, Face_Upper_TE_1, 'Face_Upper_TE_1' )

            geompy.addToStudyInFather( Face_Lower_TE_1, Edge_TE_1,       'Edge_TE_1' )

            geompy.addToStudy( Partition_Wing, 'Partition_Wing' )
            geompy.addToStudy( Partition_Wing_1, 'Partition_Wing_1' )
            geompy.addToStudy( Partition_Wing_2, 'Partition_Wing_2' )
            geompy.addToStudy( Partition_Wing_3, 'Partition_Wing_3' )
            geompy.addToStudy( Extrusion_Wake_stl, 'Extrusion_Wake_stl' )
            geompy.addToStudy( Face_Refinement_Box, 'Face_Refinement_Box' )
            geompy.addToStudy( Extrusion_Refinement_Box, 'Extrusion_Refinement_Box' )
            geompy.addToStudy( Cut_Refinement_Box, 'Cut_Refinement_Box' )
            geompy.addToStudy( Face_Domain, 'Face_Domain' )
            geompy.addToStudy( Extrusion_Domain, 'Extrusion_Domain' )
            geompy.addToStudy( Cut_Domain, 'Cut_Domain' )
            geompy.addToStudy( Partition_Domain, 'Partition_Domain' )

            if separating_domains:
                print ('Adding two domains')
                geompy.addToStudyInFather( Partition_Domain, Solid_Domain, 'Solid_Domain' )
                geompy.addToStudyInFather( Partition_Domain, Solid_Refinement_Box, 'Solid_Refinement_Box' )

                geompy.addToStudyInFather( Solid_Domain, Face_Inlet, 'Face_Inlet' )
                geompy.addToStudyInFather( Solid_Domain, Face_Left_Wall, 'Face_Left_Wall' )
                geompy.addToStudyInFather( Solid_Domain, Face_Down_Wall, 'Face_Down_Wall' )
                geompy.addToStudyInFather( Solid_Domain, Face_Top_Wall, 'Face_Top_Wall' )
                geompy.addToStudyInFather( Solid_Domain, Face_Right_Wall, 'Face_Right_Wall' )
                geompy.addToStudyInFather( Solid_Domain, Face_Outlet, 'Face_Outlet' )

                geompy.addToStudyInFather( Solid_Refinement_Box, Face_Refinementbox_Inlet_1, 'Face_Refinementbox_Inlet_1' )
                geompy.addToStudyInFather( Solid_Refinement_Box, Face_Lower_LE_Left, 'Face_Lower_LE_Left' )
                geompy.addToStudyInFather( Solid_Refinement_Box, Face_Upper_LE_Left, 'Face_Upper_LE_Left' )
                geompy.addToStudyInFather( Solid_Refinement_Box, Face_Left_Wing, 'Face_Left_Wing' )
                geompy.addToStudyInFather( Solid_Refinement_Box, Face_Lower_LE_Right_0, 'Face_Lower_LE_Right_0' )
                geompy.addToStudyInFather( Solid_Refinement_Box, Face_Upper_LE_Right_0, 'Face_Upper_LE_Right_0' )
                geompy.addToStudyInFather( Solid_Refinement_Box, Face_Lower_LE_Right_1, 'Face_Lower_LE_Right_1' )
                geompy.addToStudyInFather( Solid_Refinement_Box, Face_Upper_LE_Right_1, 'Face_Upper_LE_Right_1' )
                geompy.addToStudyInFather( Solid_Refinement_Box, Face_Lower_LE_Right_2, 'Face_Lower_LE_Right_2' )
                geompy.addToStudyInFather( Solid_Refinement_Box, Face_Upper_LE_Right_2, 'Face_Upper_LE_Right_2' )
                geompy.addToStudyInFather( Solid_Refinement_Box, Face_Lower_LE_Right_3, 'Face_Lower_LE_Right_3' )
                geompy.addToStudyInFather( Solid_Refinement_Box, Face_Upper_LE_Right_3, 'Face_Upper_LE_Right_3' )
                geompy.addToStudyInFather( Solid_Refinement_Box, Face_Right_Wing, 'Face_Right_Wing' )
                geompy.addToStudyInFather( Solid_Refinement_Box, Face_Lower_TE_Left, 'Face_Lower_TE_Left' )
                geompy.addToStudyInFather( Solid_Refinement_Box, Face_Upper_TE_Left, 'Face_Upper_TE_Left' )
                geompy.addToStudyInFather( Solid_Refinement_Box, Face_Lower_TE_Right_0, 'Face_Lower_TE_Right_0' )
                geompy.addToStudyInFather( Solid_Refinement_Box, Face_Upper_TE_Right_0, 'Face_Upper_TE_Right_0' )
                geompy.addToStudyInFather( Solid_Refinement_Box, Face_Lower_TE_Right_1, 'Face_Lower_TE_Right_1' )
                geompy.addToStudyInFather( Solid_Refinement_Box, Face_Upper_TE_Right_1, 'Face_Upper_TE_Right_1' )
                geompy.addToStudyInFather( Solid_Refinement_Box, Face_Lower_TE_Right_2, 'Face_Lower_TE_Right_2' )
                geompy.addToStudyInFather( Solid_Refinement_Box, Face_Upper_TE_Right_2, 'Face_Upper_TE_Right_2' )
                geompy.addToStudyInFather( Solid_Refinement_Box, Face_Lower_TE_Right_3, 'Face_Lower_TE_Right_3' )
                geompy.addToStudyInFather( Solid_Refinement_Box, Face_Upper_TE_Right_3, 'Face_Upper_TE_Right_3' )
                geompy.addToStudyInFather( Solid_Refinement_Box, Face_Refinementbox_Left_1, 'Face_Refinementbox_Left_1' )
                geompy.addToStudyInFather( Solid_Refinement_Box, Face_Refinementbox_Down_1, 'Face_Refinementbox_Down_1' )
                geompy.addToStudyInFather( Solid_Refinement_Box, Face_Refinementbox_Top_1, 'Face_Refinementbox_Top_1' )
                geompy.addToStudyInFather( Solid_Refinement_Box, Face_Refinementbox_Right_1, 'Face_Refinementbox_Right_1' )
                geompy.addToStudyInFather( Solid_Refinement_Box, Face_Refinementbox_Outlet_1, 'Face_Refinementbox_Outlet_1' )
            else:
                print ('Adding one single domain')
                geompy.addToStudyInFather( Partition_Domain, Face_Inlet, 'Face_Inlet' )
                geompy.addToStudyInFather( Partition_Domain, Face_Left_Wall, 'Face_Left_Wall' )
                geompy.addToStudyInFather( Partition_Domain, Face_Down_Wall, 'Face_Down_Wall' )
                geompy.addToStudyInFather( Partition_Domain, Face_Top_Wall, 'Face_Top_Wall' )
                geompy.addToStudyInFather( Partition_Domain, Face_Right_Wall, 'Face_Right_Wall' )
                geompy.addToStudyInFather( Partition_Domain, Face_Outlet, 'Face_Outlet' )

                geompy.addToStudyInFather( Partition_Domain, Face_Refinementbox_Inlet_1, 'Face_Refinementbox_Inlet_1' )
                geompy.addToStudyInFather( Partition_Domain, Face_Lower_LE_Left, 'Face_Lower_LE_Left' )
                geompy.addToStudyInFather( Partition_Domain, Face_Upper_LE_Left, 'Face_Upper_LE_Left' )
                geompy.addToStudyInFather( Partition_Domain, Face_Left_Wing, 'Face_Left_Wing' )
                geompy.addToStudyInFather( Partition_Domain, Face_Lower_LE_Right_0, 'Face_Lower_LE_Right_0' )
                geompy.addToStudyInFather( Partition_Domain, Face_Upper_LE_Right_0, 'Face_Upper_LE_Right_0' )
                geompy.addToStudyInFather( Partition_Domain, Face_Lower_LE_Right_1, 'Face_Lower_LE_Right_1' )
                geompy.addToStudyInFather( Partition_Domain, Face_Upper_LE_Right_1, 'Face_Upper_LE_Right_1' )
                geompy.addToStudyInFather( Partition_Domain, Face_Lower_LE_Right_2, 'Face_Lower_LE_Right_2' )
                geompy.addToStudyInFather( Partition_Domain, Face_Upper_LE_Right_2, 'Face_Upper_LE_Right_2' )
                geompy.addToStudyInFather( Partition_Domain, Face_Lower_LE_Right_3, 'Face_Lower_LE_Right_3' )
                geompy.addToStudyInFather( Partition_Domain, Face_Upper_LE_Right_3, 'Face_Upper_LE_Right_3' )
                geompy.addToStudyInFather( Partition_Domain, Face_Right_Wing, 'Face_Right_Wing' )
                geompy.addToStudyInFather( Partition_Domain, Face_Lower_TE_Left, 'Face_Lower_TE_Left' )
                geompy.addToStudyInFather( Partition_Domain, Face_Upper_TE_Left, 'Face_Upper_TE_Left' )
                geompy.addToStudyInFather( Partition_Domain, Face_Lower_TE_Right_0, 'Face_Lower_TE_Right_0' )
                geompy.addToStudyInFather( Partition_Domain, Face_Upper_TE_Right_0, 'Face_Upper_TE_Right_0' )
                geompy.addToStudyInFather( Partition_Domain, Face_Lower_TE_Right_1, 'Face_Lower_TE_Right_1' )
                geompy.addToStudyInFather( Partition_Domain, Face_Upper_TE_Right_1, 'Face_Upper_TE_Right_1' )
                geompy.addToStudyInFather( Partition_Domain, Face_Lower_TE_Right_2, 'Face_Lower_TE_Right_2' )
                geompy.addToStudyInFather( Partition_Domain, Face_Upper_TE_Right_2, 'Face_Upper_TE_Right_2' )
                geompy.addToStudyInFather( Partition_Domain, Face_Lower_TE_Right_3, 'Face_Lower_TE_Right_3' )
                geompy.addToStudyInFather( Partition_Domain, Face_Upper_TE_Right_3, 'Face_Upper_TE_Right_3' )
                geompy.addToStudyInFather( Partition_Domain, Face_Refinementbox_Left_1, 'Face_Refinementbox_Left_1' )
                geompy.addToStudyInFather( Partition_Domain, Face_Refinementbox_Down_1, 'Face_Refinementbox_Down_1' )
                geompy.addToStudyInFather( Partition_Domain, Face_Refinementbox_Top_1, 'Face_Refinementbox_Top_1' )
                geompy.addToStudyInFather( Partition_Domain, Face_Refinementbox_Right_1, 'Face_Refinementbox_Right_1' )
                geompy.addToStudyInFather( Partition_Domain, Face_Refinementbox_Outlet_1, 'Face_Refinementbox_Outlet_1' )


            geompy.addToStudyInFather( Face_Inlet, Edge_1, 'Edge_1' )
            geompy.addToStudyInFather( Face_Inlet, Edge_2, 'Edge_2' )
            geompy.addToStudyInFather( Face_Inlet, Edge_3, 'Edge_3' )
            geompy.addToStudyInFather( Face_Inlet, Edge_4, 'Edge_4' )

            geompy.addToStudyInFather( Face_Left_Wall, Edge_6, 'Edge_6' )
            geompy.addToStudyInFather( Face_Left_Wall, Edge_7, 'Edge_7' )

            geompy.addToStudyInFather( Face_Right_Wall, Edge_8, 'Edge_8' )
            geompy.addToStudyInFather( Face_Right_Wall, Edge_9, 'Edge_9' )

            geompy.addToStudyInFather( Face_Outlet, Edge_5, 'Edge_5' )
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

            # geompy.addToStudyInFather( Edge_Ref_Out_Bottom, Vertex_1, 'Vertex_1' )
            # geompy.addToStudyInFather( Edge_Ref_Out_Bottom, Vertex_2, 'Vertex_2' )
            # geompy.addToStudyInFather( Edge_Ref_Out_Top, Vertex_3, 'Vertex_3' )
            # geompy.addToStudyInFather( Edge_Ref_Out_Top, Vertex_4, 'Vertex_4' )

            geompy.addToStudyInFather( Face_Lower_LE_Left, Edge_LE_Left,           'Edge_LE_Left' )
            geompy.addToStudyInFather( Face_Lower_LE_Left, Edge_Left_LowerLE,      'Edge_Left_LowerLE' )
            geompy.addToStudyInFather( Face_Lower_LE_Left, Edge_Middle_LowerLE,    'Edge_Middle_LowerLE' )
            geompy.addToStudyInFather( Face_Lower_LE_Left, Edge_Left_Lower_Middle, 'Edge_Left_Lower_Middle' )

            geompy.addToStudyInFather( Face_Upper_LE_Left, Edge_Left_UpperLE,       'Edge_Left_UpperLE' )
            geompy.addToStudyInFather( Face_Upper_LE_Left, Edge_Middle_UpperLE,     'Edge_Middle_UpperLE' )
            geompy.addToStudyInFather( Face_Upper_LE_Left, Edge_Left_Upper_Middle,  'Edge_Left_Upper_Middle' )

            geompy.addToStudyInFather( Face_Lower_LE_Right_0, Edge_LE_Right_0,          'Edge_LE_Right_0' )
            geompy.addToStudyInFather( Face_Lower_LE_Right_0, Edge_LowerLE_Section_100, 'Edge_LowerLE_Section_100' )
            geompy.addToStudyInFather( Face_Lower_LE_Right_0, Edge_Right_Lower_Middle_0,'Edge_Right_Lower_Middle_0' )

            geompy.addToStudyInFather( Face_Upper_LE_Right_0, Edge_UpperLE_Section_100, 'Edge_UpperLE_Section_100' )
            geompy.addToStudyInFather( Face_Upper_LE_Right_0, Edge_Right_Upper_Middle_0,'Edge_Right_Upper_Middle_0' )

            geompy.addToStudyInFather( Face_Lower_LE_Right_1, Edge_LE_Right_1,          'Edge_LE_Right_1' )
            geompy.addToStudyInFather( Face_Lower_LE_Right_1, Edge_LowerLE_Section_150, 'Edge_LowerLE_Section_150' )
            geompy.addToStudyInFather( Face_Lower_LE_Right_1, Edge_Right_Lower_Middle_1,'Edge_Right_Lower_Middle_1' )

            geompy.addToStudyInFather( Face_Upper_LE_Right_1, Edge_UpperLE_Section_100, 'Edge_UpperLE_Section_100' )
            geompy.addToStudyInFather( Face_Upper_LE_Right_1, Edge_Right_Upper_Middle_0,'Edge_Right_Upper_Middle_0' )

            geompy.addToStudyInFather( Face_Lower_LE_Right_2, Edge_LE_Right_2,          'Edge_LE_Right_2' )
            geompy.addToStudyInFather( Face_Lower_LE_Right_2, Edge_LowerLE_Section_180, 'Edge_LowerLE_Section_180' )
            geompy.addToStudyInFather( Face_Lower_LE_Right_2, Edge_Right_Lower_Middle_2,'Edge_Right_Lower_Middle_2' )

            geompy.addToStudyInFather( Face_Upper_LE_Right_2, Edge_UpperLE_Section_180, 'Edge_UpperLE_Section_180' )
            geompy.addToStudyInFather( Face_Upper_LE_Right_2, Edge_Right_Upper_Middle_2,'Edge_Right_Upper_Middle_2' )

            geompy.addToStudyInFather( Face_Lower_LE_Right_3, Edge_LE_Right_3,          'Edge_LE_Right_3' )
            geompy.addToStudyInFather( Face_Lower_LE_Right_3, Edge_Right_LowerLE,     'Edge_Right_LowerLE' )
            geompy.addToStudyInFather( Face_Lower_LE_Right_3, Edge_Right_Lower_Middle_3,'Edge_Right_Lower_Middle_3' )

            geompy.addToStudyInFather( Face_Upper_LE_Right_3, Edge_Right_UpperLE,     'Edge_Right_UpperLE' )
            geompy.addToStudyInFather( Face_Upper_LE_Right_3, Edge_Right_Upper_Middle_3,'Edge_Right_Upper_Middle_3' )

            geompy.addToStudyInFather( Face_Lower_TE_Left, Edge_Left_Lower_TE,       'Edge_Left_Lower_TE' )
            geompy.addToStudyInFather( Face_Lower_TE_Left, Edge_Middle_LowerTE,     'Edge_Middle_LowerTE' )
            geompy.addToStudyInFather( Face_Lower_TE_Left, Edge_TE_Left,            'Edge_TE_Left' )

            geompy.addToStudyInFather( Face_Upper_TE_Left, Edge_Left_Upper_TE,      'Edge_Left_Upper_TE' )
            geompy.addToStudyInFather( Face_Upper_TE_Left, Edge_Middle_UpperTE,     'Edge_Middle_UpperTE' )

            geompy.addToStudyInFather( Face_Lower_TE_Right_0, Edge_LowerTE_Section_100,     'Edge_LowerTE_Section_100' )
            geompy.addToStudyInFather( Face_Lower_TE_Right_0, Edge_TE_Right_0,          'Edge_TE_Right_0' )

            geompy.addToStudyInFather( Face_Upper_TE_Right_0, Edge_UpperTE_Section_100,     'Edge_UpperTE_Section_100' )

            geompy.addToStudyInFather( Face_Lower_TE_Right_1, Edge_LowerTE_Section_150,     'Edge_LowerTE_Section_150' )
            geompy.addToStudyInFather( Face_Lower_TE_Right_1, Edge_TE_Right_1,          'Edge_TE_Right_1' )

            geompy.addToStudyInFather( Face_Upper_TE_Right_1, Edge_UpperTE_Section_150,     'Edge_UpperTE_Section_150' )

            geompy.addToStudyInFather( Face_Lower_TE_Right_2, Edge_LowerTE_Section_180,     'Edge_LowerTE_Section_180' )
            geompy.addToStudyInFather( Face_Lower_TE_Right_2, Edge_TE_Right_2,          'Edge_TE_Right_2' )

            geompy.addToStudyInFather( Face_Upper_TE_Right_2, Edge_UpperTE_Section_180,     'Edge_UpperTE_Section_180' )

            geompy.addToStudyInFather( Face_Lower_TE_Right_3, Edge_Right_LowerTE,     'Edge_Right_LowerTE' )
            geompy.addToStudyInFather( Face_Lower_TE_Right_3, Edge_TE_Right_3,          'Edge_TE_Right_3' )

            geompy.addToStudyInFather( Face_Upper_TE_Right_3, Edge_Right_UpperTE,     'Edge_Right_UpperTE' )



            geompy.addToStudyInFather( Partition_Domain, Auto_group_for_Sub_mesh_Far_Field_Surface, 'Auto_group_for_Sub-mesh_Far_Field_Surface' )
            geompy.addToStudyInFather( Partition_Domain, Auto_group_for_Sub_mesh_Wing_Surface, 'Auto_group_for_Sub-mesh_Wing_Surface' )
            geompy.addToStudyInFather( Partition_Domain, Auto_group_for_Sub_mesh_Far_Field_Edges, 'Auto_group_for_Sub-mesh_Far_Field_Edges' )
            geompy.addToStudyInFather( Partition_Domain, Auto_group_for_Sub_mesh_LE_Airfoils, 'Auto_group_for_Sub-mesh_LE_Airfoils' )
            geompy.addToStudyInFather( Partition_Domain, Auto_group_for_Sub_mesh_TE_Airfoils, 'Auto_group_for_Sub-mesh_TE_Airfoils' )
            geompy.addToStudyInFather( Partition_Domain, Auto_group_for_Sub_mesh_LE_Edges, 'Auto_group_for_Sub_mesh_LE_Edges' )
            geompy.addToStudyInFather( Partition_Domain, Auto_group_for_Sub_mesh_TE_Edges, 'Auto_group_for_Sub_mesh_TE_Edges' )
            geompy.addToStudyInFather( Partition_Domain, Auto_group_for_Sub_mesh_Middle, 'Auto_group_for_Sub-mesh_Middle' )

            geompy.addToStudyInFather( Partition_Domain, Auto_group_for_Sub_mesh_Middle_Airfoils, 'Auto_group_for_Sub_mesh_Middle_Airfoils' )
            geompy.addToStudyInFather( Partition_Domain, Auto_group_for_Sub_mesh_Section_100, 'Auto_group_for_Sub_mesh_Section_100' )
            geompy.addToStudyInFather( Partition_Domain, Auto_group_for_Sub_mesh_Section_150, 'Auto_group_for_Sub_mesh_Section_150' )
            geompy.addToStudyInFather( Partition_Domain, Auto_group_for_Sub_mesh_Section_180, 'Auto_group_for_Sub_mesh_Section_180' )
            geompy.addToStudyInFather( Partition_Domain, Auto_group_for_Sub_mesh_Refinement_Box_Edges, 'Auto_group_for_Sub-mesh_Refinement_Box_Edges' )
            geompy.addToStudyInFather( Partition_Domain, Auto_group_for_Sub_mesh_Refinement_Box_Side_Edges, 'Auto_group_for_Sub_mesh_Refinement_Box_Side_Edges' )
            geompy.addToStudyInFather( Partition_Domain, Auto_group_for_Sub_mesh_Refinement_Box_Outlet_Edges, 'Auto_group_for_Sub-mesh_Refinement_Box_Outlet_Edges' )
            # geompy.addToStudyInFather( Partition_Domain, Auto_group_for_Sub_mesh_Wake_Vertex, 'Auto_group_for_Sub-mesh_Wake_Vertex' )
            geompy.addToStudyInFather( Partition_Domain, Auto_group_for_Sub_mesh_Refinement_Box_Faces_Sides, 'Auto_group_for_Sub-mesh_Refinement_Box_Faces_Sides' )
            geompy.addToStudyInFather( Partition_Domain, Auto_group_for_Sub_mesh_Refinement_Box_Faces_Coarse, 'Auto_group_for_Sub-mesh_Refinement_Box_Faces_Coarse' )

            ###
            ### SMESH component
            ###

            import  SMESH, SALOMEDS
            from salome.smesh import smeshBuilder

            smesh = smeshBuilder.New(theStudy)

            # Set NETGEN 3D
            Mesh_Domain = smesh.Mesh(Partition_Domain)
            #'''
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
            #'''

            if separating_domains:
                print ('Meshing two domains separately')
                # Solid Domain:
                NETGEN_3D_1 = Mesh_Domain.Tetrahedron(geom=Solid_Domain)
                Sub_mesh_Domain = NETGEN_3D_1.GetSubMesh()
                NETGEN_3D_Parameters_Domain = NETGEN_3D_1.Parameters()
                NETGEN_3D_Parameters_Domain.SetMaxSize( Far_Field_Mesh_Size )
                NETGEN_3D_Parameters_Domain.SetOptimize( 1 )
                NETGEN_3D_Parameters_Domain.SetFineness( 5 )
                NETGEN_3D_Parameters_Domain.SetGrowthRate( Growth_Rate_Domain )
                NETGEN_3D_Parameters_Domain.SetNbSegPerEdge( 3 )
                NETGEN_3D_Parameters_Domain.SetNbSegPerRadius( 5 )
                NETGEN_3D_Parameters_Domain.SetMinSize( Refinement_Box_Face_Min_Mesh_Size )
                NETGEN_3D_Parameters_Domain.SetUseSurfaceCurvature( 0 )
                NETGEN_3D_Parameters_Domain.SetSecondOrder( 142 )
                NETGEN_3D_Parameters_Domain.SetFuseEdges( 208 )
                NETGEN_3D_Parameters_Domain.SetQuadAllowed( 127 )

                # Refinement box:
                NETGEN_3D_2 = Mesh_Domain.Tetrahedron(geom=Solid_Refinement_Box)
                Sub_mesh_Refinement_Box = NETGEN_3D_2.GetSubMesh()
                NETGEN_3D_Parameters_Refinement_Box = NETGEN_3D_2.Parameters()
                NETGEN_3D_Parameters_Refinement_Box.SetMaxSize( Refinement_Box_Face_Max_Mesh_Size )
                NETGEN_3D_Parameters_Refinement_Box.SetOptimize( 1 )
                NETGEN_3D_Parameters_Refinement_Box.SetFineness( 5 )
                NETGEN_3D_Parameters_Refinement_Box.SetGrowthRate( Growth_Rate_Refinement_Box )
                NETGEN_3D_Parameters_Refinement_Box.SetNbSegPerEdge( 3 )
                NETGEN_3D_Parameters_Refinement_Box.SetNbSegPerRadius( 5 )
                NETGEN_3D_Parameters_Refinement_Box.SetMinSize( Smallest_Airfoil_Mesh_Size )
                NETGEN_3D_Parameters_Refinement_Box.SetUseSurfaceCurvature( 0 )
                NETGEN_3D_Parameters_Refinement_Box.SetSecondOrder( 142 )
                NETGEN_3D_Parameters_Refinement_Box.SetFuseEdges( 208 )
                NETGEN_3D_Parameters_Refinement_Box.SetQuadAllowed( 127 )

            # Far field surface
            NETGEN_2D = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_2D,geom=Auto_group_for_Sub_mesh_Far_Field_Surface)
            Sub_mesh_Far_Field_Surface = NETGEN_2D.GetSubMesh()
            NETGEN_2D_Parameters_FarField = NETGEN_2D.Parameters()
            NETGEN_2D_Parameters_FarField.SetMaxSize( Far_Field_Mesh_Size )
            NETGEN_2D_Parameters_FarField.SetOptimize( 1 )
            NETGEN_2D_Parameters_FarField.SetFineness( 1 )
            NETGEN_2D_Parameters_FarField.SetMinSize( Refinement_Box_Face_Min_Mesh_Size )
            NETGEN_2D_Parameters_FarField.SetUseSurfaceCurvature( 1 )
            NETGEN_2D_Parameters_FarField.SetQuadAllowed( 0 )
            NETGEN_2D_Parameters_FarField.SetSecondOrder( 106 )
            NETGEN_2D_Parameters_FarField.SetFuseEdges( 80 )

            # Refinement box faces fine
            NETGEN_2D_Refinement_Box_Fine = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_2D,geom=Auto_group_for_Sub_mesh_Refinement_Box_Faces_Sides)
            Sub_mesh_Refinement_Box_Faces_Sides = NETGEN_2D_Refinement_Box_Fine.GetSubMesh()
            NETGEN_2D_Parameters_Refinement_Box_Sides = NETGEN_2D_Refinement_Box_Fine.Parameters()
            NETGEN_2D_Parameters_Refinement_Box_Sides.SetMaxSize( Refinement_Box_Face_Max_Mesh_Size )
            NETGEN_2D_Parameters_Refinement_Box_Sides.SetOptimize( 1 )
            NETGEN_2D_Parameters_Refinement_Box_Sides.SetFineness( 5 )
            NETGEN_2D_Parameters_Refinement_Box_Sides.SetGrowthRate( Growth_Rate_Refinement_Box )
            NETGEN_2D_Parameters_Refinement_Box_Sides.SetNbSegPerEdge( 6.92922e-310 )
            NETGEN_2D_Parameters_Refinement_Box_Sides.SetNbSegPerRadius( 4.47651e-317 )
            NETGEN_2D_Parameters_Refinement_Box_Sides.SetMinSize( Refinement_Box_Face_Min_Mesh_Size )
            NETGEN_2D_Parameters_Refinement_Box_Sides.SetUseSurfaceCurvature( 1 )
            NETGEN_2D_Parameters_Refinement_Box_Sides.SetQuadAllowed( 0 )
            NETGEN_2D_Parameters_Refinement_Box_Sides.SetSecondOrder( 142 )
            NETGEN_2D_Parameters_Refinement_Box_Sides.SetFuseEdges( 208 )

            # Refinement box faces coarse
            NETGEN_2D_2 = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_2D,geom=Auto_group_for_Sub_mesh_Refinement_Box_Faces_Coarse)
            Sub_mesh_Refinement_Box_Faces_Coarse = NETGEN_2D_2.GetSubMesh()
            NETGEN_2D_Parameters_Refinement_Box_Coarse = NETGEN_2D_2.Parameters()
            NETGEN_2D_Parameters_Refinement_Box_Coarse.SetMaxSize( Refinement_Box_Face_Max_Mesh_Size )
            NETGEN_2D_Parameters_Refinement_Box_Coarse.SetOptimize( 1 )
            NETGEN_2D_Parameters_Refinement_Box_Coarse.SetFineness( 5 )
            NETGEN_2D_Parameters_Refinement_Box_Coarse.SetGrowthRate( Growth_Rate_Refinement_Box )
            NETGEN_2D_Parameters_Refinement_Box_Coarse.SetNbSegPerEdge( 6.92922e-310 )
            NETGEN_2D_Parameters_Refinement_Box_Coarse.SetNbSegPerRadius( 4.47651e-317 )
            NETGEN_2D_Parameters_Refinement_Box_Coarse.SetMinSize( Refinement_Box_Face_Min_Mesh_Size )
            NETGEN_2D_Parameters_Refinement_Box_Coarse.SetUseSurfaceCurvature( 1 )
            NETGEN_2D_Parameters_Refinement_Box_Coarse.SetQuadAllowed( 0 )
            NETGEN_2D_Parameters_Refinement_Box_Coarse.SetSecondOrder( 142 )
            NETGEN_2D_Parameters_Refinement_Box_Coarse.SetFuseEdges( 208 )

            # Wing surface
            NETGEN_2D_1 = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_2D,geom=Auto_group_for_Sub_mesh_Wing_Surface)
            Sub_mesh_Wing_Surface = NETGEN_2D_1.GetSubMesh()
            NETGEN_2D_Parameters_Wing = NETGEN_2D_1.Parameters()
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

            # Vertex
            # Length_Near_Vertex_Wake = smesh.CreateHypothesis('SegmentLengthAroundVertex')
            # Length_Near_Vertex_Wake.SetLength( Refinement_Box_Face_Min_Mesh_Size )
            # SegmentAroundVertex_0D = smesh.CreateHypothesis('SegmentAroundVertex_0D')
            # status = Mesh_Domain.AddHypothesis(SegmentAroundVertex_0D,Auto_group_for_Sub_mesh_Wake_Vertex)
            # status = Mesh_Domain.AddHypothesis(Length_Near_Vertex_Wake,Auto_group_for_Sub_mesh_Wake_Vertex)
            # Sub_mesh_Wake_Vertex = Mesh_Domain.GetSubMesh( Auto_group_for_Sub_mesh_Wake_Vertex, 'Sub-mesh_Wake_Vertex' )

            # Far field edges
            Regular_1D = Mesh_Domain.Segment(geom=Auto_group_for_Sub_mesh_Far_Field_Edges)
            Local_Length_Far_Field = Regular_1D.LocalLength(Far_Field_Mesh_Size,None,1e-07)
            Sub_mesh_Far_Field_Edges = Regular_1D.GetSubMesh()

            # Refinement box edges fine
            Regular_1D_23 = Mesh_Domain.Segment(geom=Auto_group_for_Sub_mesh_Refinement_Box_Edges)
            Sub_mesh_Refinement_Box_Edges = Regular_1D_23.GetSubMesh()
            Local_Length_Refinement_Box_Edges = Regular_1D_23.LocalLength(Refinement_Box_Face_Min_Mesh_Size,None,1e-07)

            # Refinement box side edges
            Regular_1D_25 = Mesh_Domain.Segment(geom=Auto_group_for_Sub_mesh_Refinement_Box_Side_Edges)
            Start_and_End_Length_Refinement = Regular_1D_25.StartEndLength(Refinement_Box_Face_Min_Mesh_Size,Refinement_Box_Face_Max_Mesh_Size,[])
            Start_and_End_Length_Refinement.SetObjectEntry( 'Partition_Domain' )
            Sub_mesh_Refinement_Side_Edges = Regular_1D_25.GetSubMesh()

            # Refinement box edges coarse
            Regular_1D_24 = Mesh_Domain.Segment(geom=Auto_group_for_Sub_mesh_Refinement_Box_Outlet_Edges)
            Sub_mesh_Refinement_Box_Outlet_Edges = Regular_1D_24.GetSubMesh()
            Local_Length_Refinement_Box_Outlet_Edges = Regular_1D_24.LocalLength(Refinement_Box_Face_Max_Mesh_Size,None,1e-07)

            # LE Airfoils
            Regular_1D_1 = Mesh_Domain.Segment(geom=Auto_group_for_Sub_mesh_LE_Airfoils)
            Start_and_End_Length_LE = Regular_1D_1.StartEndLength(Smallest_Airfoil_Mesh_Size,Biggest_Airfoil_Mesh_Size,[])
            Start_and_End_Length_LE.SetObjectEntry( 'Partition_Domain' )
            Sub_mesh_LE_Airfoils = Regular_1D_1.GetSubMesh()

            # TE Airfoils
            Regular_1D_2 = Mesh_Domain.Segment(geom=Auto_group_for_Sub_mesh_TE_Airfoils)
            Start_and_End_Length_TE = Regular_1D_2.StartEndLength(Biggest_Airfoil_Mesh_Size,Smallest_Airfoil_Mesh_Size,[])
            Start_and_End_Length_TE.SetObjectEntry( 'Partition_Domain' )
            Sub_mesh_TE_Airfoils = Regular_1D_2.GetSubMesh()

            # TE
            Regular_1D_3 = Mesh_Domain.Segment(geom=Auto_group_for_Sub_mesh_TE_Edges)
            Sub_mesh_TE = Regular_1D_3.GetSubMesh()
            Local_Length_TE = Regular_1D_3.LocalLength(Smallest_Airfoil_Mesh_Size,None,1e-07)

            # LE
            Regular_1D_4 = Mesh_Domain.Segment(geom=Auto_group_for_Sub_mesh_LE_Edges)
            Sub_mesh_LE = Regular_1D_4.GetSubMesh()
            Local_Length_LE = Regular_1D_4.LocalLength(Smallest_Airfoil_Mesh_Size,None,1e-07)

            # Middle
            Regular_1D_5 = Mesh_Domain.Segment(geom=Auto_group_for_Sub_mesh_Middle)
            Local_Length_Middle = Regular_1D_5.LocalLength(Biggest_Airfoil_Mesh_Size,None,1e-07)
            Sub_mesh_Middle = Regular_1D_5.GetSubMesh()


            # Middle Airfoils
            Regular_1D_7 = Mesh_Domain.Segment(geom=Auto_group_for_Sub_mesh_Middle_Airfoils)
            Start_and_End_Length_Middle = Regular_1D_7.StartEndLength(Smallest_Airfoil_Mesh_Size, Biggest_Airfoil_Mesh_Size,[ 42, 51 ])
            Start_and_End_Length_Middle.SetObjectEntry( 'Partition_Domain' )
            Sub_mesh_Middle_Airfoils = Regular_1D_7.GetSubMesh()


            # Section 100
            Regular_1D_8 = Mesh_Domain.Segment(geom=Auto_group_for_Sub_mesh_Section_100)
            Start_and_End_Length_Section_100 = Regular_1D_8.StartEndLength(Smallest_Airfoil_Mesh_Size, Biggest_Airfoil_Mesh_Size,[ 58, 73 ])
            Start_and_End_Length_Section_100.SetObjectEntry( 'Partition_Domain' )
            Sub_mesh_Section_100 = Regular_1D_8.GetSubMesh()


            # Section 150
            Regular_1D_9 = Mesh_Domain.Segment(geom=Auto_group_for_Sub_mesh_Section_150)
            Start_and_End_Length_Section_150 = Regular_1D_9.StartEndLength(Smallest_Airfoil_Mesh_Size, Biggest_Airfoil_Mesh_Size,[ 83, 93 ])
            Start_and_End_Length_Section_150.SetObjectEntry( 'Partition_Domain' )
            Sub_mesh_Section_150 = Regular_1D_9.GetSubMesh()

            # Section 180
            Regular_1D_10 = Mesh_Domain.Segment(geom=Auto_group_for_Sub_mesh_Section_180)
            Start_and_End_Length_Section_180 = Regular_1D_10.StartEndLength(Smallest_Airfoil_Mesh_Size, Biggest_Airfoil_Mesh_Size,[ 103, 113 ])
            Start_and_End_Length_Section_180.SetObjectEntry( 'Partition_Domain' )
            Sub_mesh_Section_180 = Regular_1D_10.GetSubMesh()

            import time as time
            print(' Starting meshing ')
            start_time = time.time()
            # Compute mesh
            isDone = Mesh_Domain.Compute()
            exe_time = time.time() - start_time
            print(' Mesh execution took ', str(round(exe_time, 2)), ' sec')

            NumberOfNodes = Mesh_Domain.NbNodes()
            NumberOfElements = Mesh_Domain.NbTetras()
            print(' Information about volume mesh:')
            print(' Number of nodes       :', NumberOfNodes)
            print(' Number of elements    :', NumberOfElements)

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

            middle_airfoil = salome_output_path + '/Sub_mesh_Middle_Airfoil_Case_' + str(case) + '_AOA_' + str(AOA) + '_Wing_Span_' + str(
              Wing_span) + '_Airfoil_Mesh_Size_' + str(Smallest_Airfoil_Mesh_Size) + '_Growth_Rate_Wing_' + str(
                Growth_Rate_Wing) + '_Growth_Rate_Domain_' + str(Growth_Rate_Domain) + '.dat'

            section_100 = salome_output_path + '/Sub_mesh_Section_100_Case_' + str(case) + '_AOA_' + str(AOA) + '_Wing_Span_' + str(
              Wing_span) + '_Airfoil_Mesh_Size_' + str(Smallest_Airfoil_Mesh_Size) + '_Growth_Rate_Wing_' + str(
                Growth_Rate_Wing) + '_Growth_Rate_Domain_' + str(Growth_Rate_Domain) + '.dat'

            section_150 = salome_output_path + '/Sub_mesh_Section_150_Case_' + str(case) + '_AOA_' + str(AOA) + '_Wing_Span_' + str(
              Wing_span) + '_Airfoil_Mesh_Size_' + str(Smallest_Airfoil_Mesh_Size) + '_Growth_Rate_Wing_' + str(
                Growth_Rate_Wing) + '_Growth_Rate_Domain_' + str(Growth_Rate_Domain) + '.dat'

            section_180 = salome_output_path + '/Sub_mesh_Section_180_Case_' + str(case) + '_AOA_' + str(AOA) + '_Wing_Span_' + str(
              Wing_span) + '_Airfoil_Mesh_Size_' + str(Smallest_Airfoil_Mesh_Size) + '_Growth_Rate_Wing_' + str(
                Growth_Rate_Wing) + '_Growth_Rate_Domain_' + str(Growth_Rate_Domain) + '.dat'

            # Export data files
            try:
              Mesh_Domain.ExportDAT( r'/' + fluid_path )
              pass
            except:
              print 'ExportDAT() failed. Invalid file name?'
            try:
              Mesh_Domain.ExportDAT( r'/' + body_surface_path, Sub_mesh_Wing_Surface )
              pass
            except:
              print 'ExportPartToDAT() failed. Invalid file name?'
            try:
              Mesh_Domain.ExportDAT( r'/' + far_field_path, Sub_mesh_Far_Field_Surface )
              pass
            except:
              print 'ExportPartToDAT() failed. Invalid file name?'
            try:
              Mesh_Domain.ExportDAT( r'/' + te_path, Sub_mesh_TE )
              pass
            except:
              print 'ExportPartToDAT() failed. Invalid file name?'
            try:
              Mesh_Domain.ExportDAT( r'/' + middle_airfoil, Sub_mesh_Middle_Airfoils )
              pass
            except:
              print 'ExportPartToDAT() failed. Invalid file name?'
            try:
              Mesh_Domain.ExportDAT( r'/' + section_100, Sub_mesh_Section_100 )
              pass
            except:
              print 'ExportPartToDAT() failed. Invalid file name?'
            try:
              Mesh_Domain.ExportDAT( r'/' + section_150, Sub_mesh_Section_150 )
              pass
            except:
              print 'ExportPartToDAT() failed. Invalid file name?'
            try:
              Mesh_Domain.ExportDAT( r'/' + section_180, Sub_mesh_Section_180 )
              pass
            except:
              print 'ExportPartToDAT() failed. Invalid file name?'

            # Mesh wake and export STL
            Mesh_Wake_Surface = smesh.Mesh(Extrusion_Wake_stl)
            status = Mesh_Wake_Surface.AddHypothesis(NETGEN_2D_Parameters_FarField)
            NETGEN_1D_2D_2 = Mesh_Wake_Surface.Triangle(algo=smeshBuilder.NETGEN_1D2D)
            isDone = Mesh_Wake_Surface.Compute()
            wake_path = mdpa_path + '/wake_Case_' + str(case) + '_AOA_' + str(AOA) + '_Wing_Span_' + str(
              Wing_span) + '_Airfoil_Mesh_Size_' + str(Smallest_Airfoil_Mesh_Size) + '_Growth_Rate_Wing_' + str(
                Growth_Rate_Wing) + '_Growth_Rate_Domain_' + str(Growth_Rate_Domain) + '.stl'
            try:
                Mesh_Wake_Surface.ExportSTL( wake_path, 1 )
                pass
            except:
                print 'ExportSTL() failed. Invalid file name?'


            # Set names of Mesh objects
            smesh.SetName(NETGEN_3D_Parameters, 'NETGEN_3D_Parameters')
            smesh.SetName(NETGEN_3D.GetAlgorithm(), 'NETGEN 3D')
            smesh.SetName(NETGEN_2D.GetAlgorithm(), 'NETGEN 2D')
            smesh.SetName(Mesh_Domain.GetMesh(), 'Mesh_Domain')

            if separating_domains:
                print ('Adding two separate meshes')
                smesh.SetName(NETGEN_3D_Parameters_Domain, 'NETGEN 3D Parameters_Domain')
                smesh.SetName(Sub_mesh_Domain, 'Sub-mesh_Domain')

                smesh.SetName(NETGEN_3D_Parameters_Refinement_Box, 'NETGEN 3D Parameters_Refinement_Box')
                smesh.SetName(Sub_mesh_Refinement_Box, 'Sub-mesh_Refinement_Box')

            smesh.SetName(Regular_1D_23.GetAlgorithm(), 'Regular_1D_23')
            smesh.SetName(Local_Length_Refinement_Box_Edges, 'Local Length_Refinement_Box_Edges')
            smesh.SetName(Sub_mesh_Refinement_Box_Edges, 'Sub-mesh_Refinement_Box_Edges')

            smesh.SetName(Regular_1D_24.GetAlgorithm(), 'Regular_1D_24')
            smesh.SetName(Local_Length_Refinement_Box_Outlet_Edges, 'Local Length_Refinement_Box_Outlet_Edges')
            smesh.SetName(Sub_mesh_Refinement_Box_Outlet_Edges, 'Sub-mesh_Refinement_Box_Outlet_Edges')

            smesh.SetName(Regular_1D_25.GetAlgorithm(), 'Regular_1D_25')
            smesh.SetName(Start_and_End_Length_Refinement, 'Start_and_End_Length_Refinement')
            smesh.SetName(Sub_mesh_Refinement_Side_Edges, 'Sub_mesh_Refinement_Side_Edges')

            # smesh.SetName(SegmentAroundVertex_0D, 'SegmentAroundVertex_0D')
            # smesh.SetName(Length_Near_Vertex_Wake, 'Length_Near_Vertex_Wake')
            # smesh.SetName(Sub_mesh_Wake_Vertex, 'Sub-mesh_Wake_Vertex')

            smesh.SetName(NETGEN_2D_Parameters_Refinement_Box_Sides, 'NETGEN 2D Parameters_Refinement_Box_Sides')
            smesh.SetName(NETGEN_2D_Parameters_Refinement_Box_Coarse, 'NETGEN 2D Parameters_Refinement_Box_Coarse')
            smesh.SetName(Sub_mesh_Refinement_Box_Faces_Sides, 'Sub-mesh_Refinement_Box_Faces_Sides')
            smesh.SetName(Sub_mesh_Refinement_Box_Faces_Coarse, 'Sub-mesh_Refinement_Box_Faces_Coarse')

            smesh.SetName(Regular_1D.GetAlgorithm(), 'Regular_1D')
            smesh.SetName(Regular_1D_1.GetAlgorithm(), 'Regular_1D_1')
            smesh.SetName(Regular_1D_2.GetAlgorithm(), 'Regular_1D_2')
            smesh.SetName(Regular_1D_3.GetAlgorithm(), 'Regular_1D_3')
            smesh.SetName(Regular_1D_4.GetAlgorithm(), 'Regular_1D_4')
            smesh.SetName(Regular_1D_5.GetAlgorithm(), 'Regular_1D_5')
            smesh.SetName(Regular_1D_7.GetAlgorithm(), 'Regular_1D_7')
            smesh.SetName(Regular_1D_8.GetAlgorithm(), 'Regular_1D_8')
            smesh.SetName(Regular_1D_9.GetAlgorithm(), 'Regular_1D_9')
            smesh.SetName(Regular_1D_10.GetAlgorithm(), 'Regular_1D_10')

            smesh.SetName(NETGEN_2D_Parameters_FarField, 'NETGEN 2D Parameters_FarField')
            smesh.SetName(NETGEN_2D_Parameters_Wing, 'NETGEN 2D Parameters_Wing')
            smesh.SetName(Start_and_End_Length_TE, 'Start and End Length_TE')
            smesh.SetName(Local_Length_TE, 'Local Length_TE')
            smesh.SetName(Local_Length_LE, 'Local Length_LE')
            smesh.SetName(Local_Length_Far_Field, 'Local Length_Far_Field')
            smesh.SetName(Start_and_End_Length_LE, 'Start and End Length_LE')
            smesh.SetName(Local_Length_Middle, 'Local Length_Middle')
            smesh.SetName(Start_and_End_Length_Middle, 'Start_and_End_Length_Middle')
            smesh.SetName(Start_and_End_Length_Section_100, 'Start_and_End_Length_Section_100')
            smesh.SetName(Start_and_End_Length_Section_150, 'Start_and_End_Length_Section_150')
            smesh.SetName(Start_and_End_Length_Section_180, 'Start_and_End_Length_Section_180')

            smesh.SetName(Sub_mesh_Far_Field_Edges, 'Sub-mesh_Far_Field_Edges')
            smesh.SetName(Sub_mesh_Wing_Surface, 'Sub-mesh_Wing_Surface')
            smesh.SetName(Sub_mesh_Far_Field_Surface, 'Sub-mesh_Far_Field_Surface')
            smesh.SetName(Sub_mesh_Middle, 'Sub-mesh_Middle')
            smesh.SetName(Sub_mesh_TE, 'Sub-mesh_TE')
            smesh.SetName(Sub_mesh_LE, 'Sub_mesh_LE')
            smesh.SetName(Sub_mesh_TE_Airfoils, 'Sub-mesh_TE_Airfoils')
            smesh.SetName(Sub_mesh_LE_Airfoils, 'Sub-mesh_LE_Airfoils')
            smesh.SetName(Mesh_Wake_Surface, 'Mesh_Wake_Surface')
            smesh.SetName(Sub_mesh_Middle_Airfoils, 'Sub_mesh_Middle_Airfoils')
            smesh.SetName(Sub_mesh_Section_100, 'Sub_mesh_Section_100')
            smesh.SetName(Sub_mesh_Section_150, 'Sub_mesh_Section_150')
            smesh.SetName(Sub_mesh_Section_180, 'Sub_mesh_Section_180')

            # Saving file to open from salome's gui
            if separating_domains:
                file_name = salome_output_path + "/generate_finite_wing_sections_box_separating.hdf"
                salome.myStudyManager.SaveAs(file_name, salome.myStudy, 0)
            else:
                file_name = salome_output_path + "/generate_finite_wing_sections_box_together.hdf"
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
