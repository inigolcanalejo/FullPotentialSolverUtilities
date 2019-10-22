# -*- coding: utf-8 -*-

###
### This file is generated automatically by SALOME v8.4.0 with dump python functionality
###

# Parameters:
Wing_span = TBD
Domain_Length = 100
Domain_Height = Domain_Length
Domain_Width = 100

Outlet_Min_Mesh_Size = 0.1
Outlet_Max_Mesh_Size = 0.5
Growth_Rate_Wake = 0.7

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
        Growth_Rate_Domain = round(Growth_Rate_Domain, 1)
        Growth_Rate_Wing = Initial_Growth_Rate_Wing
        for i in range(Number_Of_Wing_Refinements):
            Growth_Rate_Wing = round(Growth_Rate_Wing, 1)
            print '\n case = ', case, ' AOA = ', AOA, ' Growth_Rate_Domain = ', Growth_Rate_Domain, ' Growth_Rate_Wing = ', Growth_Rate_Wing

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

            # Create face
            Face_Airfoil = geompy.MakeFaceWires([Curve_UpperSurface_LE, Curve_UpperSurface_TE, Curve_LowerSurface_TE, Curve_LowerSurface_LE], 1)

            # Rotate around center to AOA
            geompy.Rotate(Face_Airfoil, OY, AOA*math.pi/180.0)

            # Extrusion of the wing
            Extrusion_Wing = geompy.MakePrismVecH2Ways(Face_Airfoil, OY, Wing_span/2.0)

            # Exploding wing
            [Face_Left_Wing_1,Face_Lower_LE_1,Face_Upper_LE_1,Face_Right_Wing_1,Face_Lower_TE_1,Face_Upper_TE_1] = geompy.ExtractShapes(Extrusion_Wing, geompy.ShapeType["FACE"], True)

            # Eploding Face_Lower_TE
            [Obj1,Obj2,Obj3,Edge_TE_1] = geompy.ExtractShapes(Face_Lower_TE_1, geompy.ShapeType["EDGE"], True)

            # Partition wing
            Partition_Wing = geompy.MakePartition([Extrusion_Wing], [Face_Airfoil], [], [], geompy.ShapeType["SOLID"], 0, [], 0)

            # Domain generation
            Face_Domain = geompy.MakeFaceHW(Domain_Length, Domain_Height, 3)
            Extrusion_Domain = geompy.MakePrismVecH2Ways(Face_Domain, OY, Domain_Width/2.0)

            # Cut wing from the domain
            Cut_Domain = geompy.MakeCutList(Extrusion_Domain, [Partition_Wing], True)

            # Generate wake
            Vector_Wake_Direction = geompy.MakeVectorDXDYDZ(1, 0, 0)
            Extrusion_Wake = geompy.MakePrismVecH(Edge_TE_1, Vector_Wake_Direction, Domain_Length*0.5)

            # Generate wake
            Vector_Wake_Direction = geompy.MakeVectorDXDYDZ(1, 0, 0)
            Translation_1 = geompy.MakeTranslation(Edge_TE_1, 0, 0, 0)
            Vertex_1 = geompy.MakeVertex(0.5*math.cos(AOA*math.pi/180.0), 0, -0.5*math.sin(AOA*math.pi/180.0))
            Scale_1 = geompy.MakeScaleTransform(Translation_1, Vertex_1, 0.999875)
            Extrusion_Wake_stl = geompy.MakePrismVecH(Scale_1, Vector_Wake_Direction, Domain_Length*0.5)

            # Partition
            Partition_2 = geompy.MakePartition([Cut_Domain], [Extrusion_Wake], [], [], geompy.ShapeType["SOLID"], 0, [], 1)

            # Explode
            [Face_Inlet,Face_Left_Wall,Face_Lower_LE_Left,Face_Upper_LE_Left,Face_Left_Wing,Face_Lower_LE_Right,Face_Upper_LE_Right,Face_Down_Wall,Face_Top_Wall,Face_Right_Wing,Face_Lower_TE_Left,Face_Upper_TE_Left,Face_Lower_TE_Right,Face_Upper_TE_Right,Face_Right_Wall,Face_Wake,Face_Outlet] = geompy.ExtractShapes(Partition_2, geompy.ShapeType["FACE"], True)

            # Exploding far field
            [Edge_1,Edge_2,Edge_3,Edge_4] = geompy.ExtractShapes(Face_Inlet, geompy.ShapeType["EDGE"], True)
            [Obj1,Edge_6,Edge_7,Obj2] = geompy.ExtractShapes(Face_Left_Wall, geompy.ShapeType["EDGE"], True)
            [Obj1,Edge_8,Edge_9,Obj2] = geompy.ExtractShapes(Face_Right_Wall, geompy.ShapeType["EDGE"], True)
            [Edge_5,Edge_10,Edge_Wake_Outlet,Edge_11,Edge_12] = geompy.ExtractShapes(Face_Outlet, geompy.ShapeType["EDGE"], True)

            # Exploding wing
            [Edge_LE_Left,Edge_Left_LowerLE,Edge_Middle_LowerLE,Edge_Left_Lower_Middle] = geompy.ExtractShapes(Face_Lower_LE_Left, geompy.ShapeType["EDGE"], True)
            [Obj1,        Edge_Left_UpperLE,Edge_Middle_UpperLE,Edge_Left_Upper_Middle] = geompy.ExtractShapes(Face_Upper_LE_Left, geompy.ShapeType["EDGE"], True)
            [Edge_LE_Right,Obj1,            Edge_Right_LowerLE, Edge_Right_Lower_Middle]= geompy.ExtractShapes(Face_Lower_LE_Right, geompy.ShapeType["EDGE"], True)
            [Obj1,         Obj2,            Edge_Right_UpperLE, Edge_Right_Upper_Middle]= geompy.ExtractShapes(Face_Upper_LE_Right, geompy.ShapeType["EDGE"], True)

            [Obj1        ,Edge_Left_Lower_TE,Edge_Middle_LowerTE,Edge_TE_Left] = geompy.ExtractShapes(Face_Lower_TE_Left, geompy.ShapeType["EDGE"], True)
            [Obj1        ,Edge_Left_Upper_TE,Edge_Middle_UpperTE,Obj2        ] = geompy.ExtractShapes(Face_Upper_TE_Left, geompy.ShapeType["EDGE"], True)
            [Obj1        ,Obj2              ,Edge_Right_LowerTE, Edge_TE_Right]= geompy.ExtractShapes(Face_Lower_TE_Right, geompy.ShapeType["EDGE"], True)
            [Obj1        ,Obj2              ,Edge_Right_UpperTE, Obj3]         = geompy.ExtractShapes(Face_Upper_TE_Right, geompy.ShapeType["EDGE"], True)

            # Exploding wake
            [Obj1,Obj3,Edge_Wake_Left,Edge_Wake_Right,Obj2] = geompy.ExtractShapes(Face_Wake, geompy.ShapeType["EDGE"], True)

            # Exploding Edge_Wake_Outlet
            [Vertex_1,Vertex_2] = geompy.ExtractShapes(Edge_Wake_Outlet, geompy.ShapeType["VERTEX"], True)

            # Making groups for submeshes
            # Vertex
            Auto_group_for_Sub_mesh_Wake_Vertex = geompy.CreateGroup(Partition_2, geompy.ShapeType["VERTEX"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Wake_Vertex, [Vertex_1, Vertex_2])

            #Edges
            # Wake edges
            Auto_group_for_Sub_mesh_Wake_Edges = geompy.CreateGroup(Partition_2, geompy.ShapeType["EDGE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Wake_Edges, [Edge_Wake_Left, Edge_Wake_Right])

            # Far field edges
            Auto_group_for_Sub_mesh_Far_Field_Edges = geompy.CreateGroup(Partition_2, geompy.ShapeType["EDGE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Far_Field_Edges, [Edge_1, Edge_2, Edge_3, Edge_4, Edge_6, Edge_7, Edge_8, Edge_9, Edge_5, Edge_10, Edge_11, Edge_12])

            # TE Airfoil edges
            Auto_group_for_Sub_mesh_LE_Airfoils = geompy.CreateGroup(Partition_2, geompy.ShapeType["EDGE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_LE_Airfoils, [Edge_Left_LowerLE, Edge_Left_UpperLE, Edge_Right_LowerLE, Edge_Right_UpperLE])

            # LE Airfoil edges
            Auto_group_for_Sub_mesh_TE_Airfoils = geompy.CreateGroup(Partition_2, geompy.ShapeType["EDGE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_TE_Airfoils, [Edge_Left_Lower_TE, Edge_Left_Upper_TE, Edge_Right_LowerTE, Edge_Right_UpperTE])

            # LE edges
            Auto_group_for_Sub_mesh_LE_Edges = geompy.CreateGroup(Partition_2, geompy.ShapeType["EDGE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_LE_Edges, [Edge_LE_Left, Edge_LE_Right])

            # TE edges
            Auto_group_for_Sub_mesh_TE_Edges = geompy.CreateGroup(Partition_2, geompy.ShapeType["EDGE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_TE_Edges, [Edge_TE_Left, Edge_TE_Right])

            # Middle
            Auto_group_for_Sub_mesh_Middle = geompy.CreateGroup(Partition_2, geompy.ShapeType["EDGE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Middle, [Edge_Left_Lower_Middle, Edge_Left_Upper_Middle, Edge_Right_Lower_Middle, Edge_Right_Upper_Middle])

            # Middle airfoil edges
            Auto_group_for_Sub_mesh_Middle_Airfoils = geompy.CreateGroup(Partition_2, geompy.ShapeType["EDGE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Middle_Airfoils, [Edge_Middle_LowerLE, Edge_Middle_UpperLE, Edge_Middle_LowerTE, Edge_Middle_UpperTE])

            #Surfaces
            # Far field surface
            Auto_group_for_Sub_mesh_Far_Field_Surface = geompy.CreateGroup(Partition_2, geompy.ShapeType["FACE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Far_Field_Surface, [Face_Inlet, Face_Left_Wall, Face_Down_Wall, Face_Top_Wall, Face_Right_Wall, Face_Outlet])

            # Wing surface
            Auto_group_for_Sub_mesh_Wing_Surface = geompy.CreateGroup(Partition_2, geompy.ShapeType["FACE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_Wing_Surface, [Face_Left_Wing, Face_Lower_LE_Left, Face_Upper_LE_Left, Face_Lower_LE_Right, Face_Upper_LE_Right, Face_Right_Wing, Face_Lower_TE_Left, Face_Upper_TE_Left, Face_Lower_TE_Right, Face_Upper_TE_Right])

            # Adding to study
            geompy.addToStudy( O, 'O' )
            geompy.addToStudy( OX, 'OX' )
            geompy.addToStudy( OY, 'OY' )
            geompy.addToStudy( OZ, 'OZ' )
            geompy.addToStudy( Curve_UpperSurface_LE, 'Curve_UpperSurface_LE' )
            geompy.addToStudy( Curve_UpperSurface_TE, 'Curve_UpperSurface_TE' )
            geompy.addToStudy( Curve_LowerSurface_TE, 'Curve_LowerSurface_TE' )
            geompy.addToStudy( Curve_LowerSurface_LE, 'Curve_LowerSurface_LE' )
            geompy.addToStudy( Face_Airfoil, 'Face_Airfoil' )
            geompy.addToStudy( Extrusion_Wing, 'Extrusion_Wing' )

            geompy.addToStudyInFather( Extrusion_Wing, Face_Left_Wing_1, 'Face_Left_Wing_1' )
            geompy.addToStudyInFather( Extrusion_Wing, Face_Lower_LE_1, 'Face_Lower_LE_1' )
            geompy.addToStudyInFather( Extrusion_Wing, Face_Upper_LE_1, 'Face_Upper_LE_1' )
            geompy.addToStudyInFather( Extrusion_Wing, Face_Right_Wing_1, 'Face_Right_Wing_1' )
            geompy.addToStudyInFather( Extrusion_Wing, Face_Lower_TE_1, 'Face_Lower_TE_1' )
            geompy.addToStudyInFather( Partition_Wing, Face_Upper_TE_1, 'Face_Upper_TE_1' )

            geompy.addToStudyInFather( Face_Lower_TE_1, Edge_TE_1,       'Edge_TE_1' )

            geompy.addToStudy( Partition_Wing, 'Partition_Wing' )

            geompy.addToStudy( Face_Domain, 'Face_Domain' )
            geompy.addToStudy( Extrusion_Domain, 'Extrusion_Domain' )
            geompy.addToStudy( Cut_Domain, 'Cut_Domain' )

            geompy.addToStudy( Extrusion_Wake, 'Extrusion_Wake' )
            geompy.addToStudy( Extrusion_Wake_stl, 'Extrusion_Wake_stl' )

            geompy.addToStudy( Partition_2, 'Partition_2' )

            geompy.addToStudyInFather( Partition_2, Face_Inlet, 'Face_Inlet' )
            geompy.addToStudyInFather( Partition_2, Face_Left_Wall, 'Face_Left_Wall' )
            geompy.addToStudyInFather( Partition_2, Face_Lower_LE_Left, 'Face_Lower_LE_Left' )
            geompy.addToStudyInFather( Partition_2, Face_Upper_LE_Left, 'Face_Upper_LE_Left' )
            geompy.addToStudyInFather( Partition_2, Face_Left_Wing, 'Face_Left_Wing' )
            geompy.addToStudyInFather( Partition_2, Face_Lower_LE_Right, 'Face_Lower_LE_Right' )
            geompy.addToStudyInFather( Partition_2, Face_Upper_LE_Right, 'Face_Upper_LE_Right' )
            geompy.addToStudyInFather( Partition_2, Face_Down_Wall, 'Face_Down_Wall' )
            geompy.addToStudyInFather( Partition_2, Face_Top_Wall, 'Face_Top_Wall' )
            geompy.addToStudyInFather( Partition_2, Face_Right_Wing, 'Face_Right_Wing' )
            geompy.addToStudyInFather( Partition_2, Face_Lower_TE_Left, 'Face_Lower_TE_Left' )
            geompy.addToStudyInFather( Partition_2, Face_Upper_TE_Left, 'Face_Upper_TE_Left' )
            geompy.addToStudyInFather( Partition_2, Face_Lower_TE_Right, 'Face_Lower_TE_Right' )
            geompy.addToStudyInFather( Partition_2, Face_Upper_TE_Right, 'Face_Upper_TE_Right' )
            geompy.addToStudyInFather( Partition_2, Face_Right_Wall, 'Face_Right_Wall' )
            geompy.addToStudyInFather( Partition_2, Face_Wake, 'Face_Wake' )
            geompy.addToStudyInFather( Partition_2, Face_Outlet, 'Face_Outlet' )

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
            geompy.addToStudyInFather( Face_Outlet, Edge_Wake_Outlet, 'Edge_Wake_Outlet' )

            geompy.addToStudyInFather( Face_Lower_LE_Left, Edge_LE_Left,           'Edge_LE_Left' )
            geompy.addToStudyInFather( Face_Lower_LE_Left, Edge_Left_LowerLE,      'Edge_Left_LowerLE' )
            geompy.addToStudyInFather( Face_Lower_LE_Left, Edge_Middle_LowerLE,    'Edge_Middle_LowerLE' )
            geompy.addToStudyInFather( Face_Lower_LE_Left, Edge_Left_Lower_Middle, 'Edge_Left_Lower_Middle' )

            geompy.addToStudyInFather( Face_Upper_LE_Left, Edge_Left_UpperLE,       'Edge_Left_UpperLE' )
            geompy.addToStudyInFather( Face_Upper_LE_Left, Edge_Middle_UpperLE,     'Edge_Middle_UpperLE' )
            geompy.addToStudyInFather( Face_Upper_LE_Left, Edge_Left_Upper_Middle,  'Edge_Left_Upper_Middle' )

            geompy.addToStudyInFather( Face_Lower_LE_Right, Edge_LE_Right,          'Edge_LE_Right' )
            geompy.addToStudyInFather( Face_Lower_LE_Right, Edge_Right_LowerLE,     'Edge_Right_LowerLE' )
            geompy.addToStudyInFather( Face_Lower_LE_Right, Edge_Right_Lower_Middle,'Edge_Right_Lower_Middle' )

            geompy.addToStudyInFather( Face_Upper_LE_Right, Edge_Right_UpperLE,     'Edge_Right_UpperLE' )
            geompy.addToStudyInFather( Face_Upper_LE_Right, Edge_Right_Upper_Middle,'Edge_Right_Upper_Middle' )

            geompy.addToStudyInFather( Face_Lower_TE_Left, Edge_Left_Lower_TE,       'Edge_Left_Lower_TE' )
            geompy.addToStudyInFather( Face_Lower_TE_Left, Edge_Middle_LowerTE,     'Edge_Middle_LowerTE' )
            geompy.addToStudyInFather( Face_Lower_TE_Left, Edge_TE_Left,            'Edge_TE_Left' )

            geompy.addToStudyInFather( Face_Upper_TE_Left, Edge_Left_Upper_TE,      'Edge_Left_Upper_TE' )
            geompy.addToStudyInFather( Face_Upper_TE_Left, Edge_Middle_UpperTE,     'Edge_Middle_UpperTE' )

            geompy.addToStudyInFather( Face_Lower_TE_Right, Edge_Right_LowerTE,     'Edge_Right_LowerTE' )
            geompy.addToStudyInFather( Face_Lower_TE_Right, Edge_TE_Right,          'Edge_TE_Right' )

            geompy.addToStudyInFather( Face_Upper_TE_Right, Edge_Right_UpperTE,     'Edge_Right_UpperTE' )

            geompy.addToStudyInFather( Face_Wake, Edge_Wake_Left, 'Edge_Wake_Left' )
            geompy.addToStudyInFather( Face_Wake, Edge_Wake_Right, 'Edge_Wake_Right' )

            geompy.addToStudyInFather( Edge_Wake_Outlet, Vertex_1, 'Vertex_1' )
            geompy.addToStudyInFather( Edge_Wake_Outlet, Vertex_2, 'Vertex_2' )

            geompy.addToStudyInFather( Partition_2, Auto_group_for_Sub_mesh_Far_Field_Surface, 'Auto_group_for_Sub-mesh_Far_Field_Surface' )
            geompy.addToStudyInFather( Partition_2, Auto_group_for_Sub_mesh_Wing_Surface, 'Auto_group_for_Sub-mesh_Wing_Surface' )
            geompy.addToStudyInFather( Partition_2, Auto_group_for_Sub_mesh_Far_Field_Edges, 'Auto_group_for_Sub-mesh_Far_Field_Edges' )
            geompy.addToStudyInFather( Partition_2, Auto_group_for_Sub_mesh_LE_Airfoils, 'Auto_group_for_Sub-mesh_LE_Airfoils' )
            geompy.addToStudyInFather( Partition_2, Auto_group_for_Sub_mesh_TE_Airfoils, 'Auto_group_for_Sub-mesh_TE_Airfoils' )
            geompy.addToStudyInFather( Partition_2, Auto_group_for_Sub_mesh_LE_Edges, 'Auto_group_for_Sub_mesh_LE_Edges' )
            geompy.addToStudyInFather( Partition_2, Auto_group_for_Sub_mesh_TE_Edges, 'Auto_group_for_Sub_mesh_TE_Edges' )
            geompy.addToStudyInFather( Partition_2, Auto_group_for_Sub_mesh_Middle, 'Auto_group_for_Sub-mesh_Middle' )
            geompy.addToStudyInFather( Partition_2, Auto_group_for_Sub_mesh_Wake_Vertex, 'Auto_group_for_Sub-mesh_Wake_Vertex' )
            geompy.addToStudyInFather( Partition_2, Auto_group_for_Sub_mesh_Wake_Edges, 'Auto_group_for_Sub-mesh_Wake_Edges' )
            geompy.addToStudyInFather( Partition_2, Auto_group_for_Sub_mesh_Middle_Airfoils, 'Auto_group_for_Sub_mesh_Middle_Airfoils' )

            ###
            ### SMESH component
            ###

            import  SMESH, SALOMEDS
            from salome.smesh import smeshBuilder

            smesh = smeshBuilder.New(theStudy)

            # Set NETGEN 3D
            Mesh_Domain = smesh.Mesh(Partition_2)
            NETGEN_3D = Mesh_Domain.Tetrahedron()
            NETGEN_3D_Parameters_1 = NETGEN_3D.Parameters()
            NETGEN_3D_Parameters_1.SetMaxSize( Far_Field_Mesh_Size )
            NETGEN_3D_Parameters_1.SetOptimize( 1 )
            NETGEN_3D_Parameters_1.SetFineness( 5 )
            NETGEN_3D_Parameters_1.SetGrowthRate( Growth_Rate_Domain )
            NETGEN_3D_Parameters_1.SetNbSegPerEdge( 3 )
            NETGEN_3D_Parameters_1.SetNbSegPerRadius( 5 )
            NETGEN_3D_Parameters_1.SetMinSize( Smallest_Airfoil_Mesh_Size )
            NETGEN_3D_Parameters_1.SetUseSurfaceCurvature( 0 )
            NETGEN_3D_Parameters_1.SetSecondOrder( 106 )
            NETGEN_3D_Parameters_1.SetFuseEdges( 80 )
            NETGEN_3D_Parameters_1.SetQuadAllowed( 127 )

            # Far field surface
            NETGEN_2D = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_2D,geom=Auto_group_for_Sub_mesh_Far_Field_Surface)
            Sub_mesh_Far_Field_Surface = NETGEN_2D.GetSubMesh()
            NETGEN_2D_Parameters_FarField = NETGEN_2D.Parameters()
            NETGEN_2D_Parameters_FarField.SetMaxSize( Far_Field_Mesh_Size )
            NETGEN_2D_Parameters_FarField.SetOptimize( 1 )
            NETGEN_2D_Parameters_FarField.SetFineness( 1 )
            NETGEN_2D_Parameters_FarField.SetMinSize( Outlet_Min_Mesh_Size )
            NETGEN_2D_Parameters_FarField.SetUseSurfaceCurvature( 1 )
            NETGEN_2D_Parameters_FarField.SetQuadAllowed( 0 )
            NETGEN_2D_Parameters_FarField.SetSecondOrder( 106 )
            NETGEN_2D_Parameters_FarField.SetFuseEdges( 80 )

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

            # Wake surface
            NETGEN_2D_2 = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_2D,geom=Face_Wake)
            Sub_mesh_Wake_Surface = NETGEN_2D_2.GetSubMesh()
            NETGEN_2D_Parameters_Wake = NETGEN_2D_2.Parameters()
            NETGEN_2D_Parameters_Wake.SetMaxSize( Outlet_Max_Mesh_Size )
            NETGEN_2D_Parameters_Wake.SetOptimize( 1 )
            NETGEN_2D_Parameters_Wake.SetFineness( 5 )
            NETGEN_2D_Parameters_Wing.SetGrowthRate( Growth_Rate_Wake )
            NETGEN_2D_Parameters_Wake.SetMinSize( Smallest_Airfoil_Mesh_Size )
            NETGEN_2D_Parameters_Wake.SetUseSurfaceCurvature( 1 )
            NETGEN_2D_Parameters_Wake.SetQuadAllowed( 0 )
            NETGEN_2D_Parameters_Wake.SetSecondOrder( 106 )
            NETGEN_2D_Parameters_Wake.SetFuseEdges( 80 )

            # Vertex
            Length_Near_Vertex_Wake = smesh.CreateHypothesis('SegmentLengthAroundVertex')
            Length_Near_Vertex_Wake.SetLength( Outlet_Min_Mesh_Size )
            SegmentAroundVertex_0D = smesh.CreateHypothesis('SegmentAroundVertex_0D')
            status = Mesh_Domain.AddHypothesis(SegmentAroundVertex_0D,Auto_group_for_Sub_mesh_Wake_Vertex)
            status = Mesh_Domain.AddHypothesis(Length_Near_Vertex_Wake,Auto_group_for_Sub_mesh_Wake_Vertex)
            Sub_mesh_Wake_Vertex = Mesh_Domain.GetSubMesh( Auto_group_for_Sub_mesh_Wake_Vertex, 'Sub-mesh_Wake_Vertex' )

            # Wake edges
            Regular_1D_17 = Mesh_Domain.Segment(geom=Auto_group_for_Sub_mesh_Wake_Edges)
            Start_and_End_Length_Wake = Regular_1D_17.StartEndLength(Smallest_Airfoil_Mesh_Size,Outlet_Min_Mesh_Size,[])
            Start_and_End_Length_Wake.SetObjectEntry( 'Partition_2' )
            Sub_mesh_Wake_Edges = Regular_1D_17.GetSubMesh()

            # Wake outlet edge
            Regular_1D_6 = Mesh_Domain.Segment(geom=Edge_Wake_Outlet)
            Local_Length_Wake_Outlet_Edge = Regular_1D_6.LocalLength(Outlet_Max_Mesh_Size,None,1e-07)
            Sub_mesh_Wake_Outlet_Edge = Regular_1D_6.GetSubMesh()

            # Far field edges
            Regular_1D = Mesh_Domain.Segment(geom=Auto_group_for_Sub_mesh_Far_Field_Edges)
            Local_Length_Far_Field = Regular_1D.LocalLength(Far_Field_Mesh_Size,None,1e-07)
            Sub_mesh_Far_Field_Edges = Regular_1D.GetSubMesh()

            # LE Airfoils
            Regular_1D_1 = Mesh_Domain.Segment(geom=Auto_group_for_Sub_mesh_LE_Airfoils)
            Start_and_End_Length_LE = Regular_1D_1.StartEndLength(Smallest_Airfoil_Mesh_Size,Biggest_Airfoil_Mesh_Size,[])
            Start_and_End_Length_LE.SetObjectEntry( 'Partition_2' )
            Sub_mesh_LE_Airfoils = Regular_1D_1.GetSubMesh()

            # TE Airfoils
            Regular_1D_2 = Mesh_Domain.Segment(geom=Auto_group_for_Sub_mesh_TE_Airfoils)
            Start_and_End_Length_TE = Regular_1D_2.StartEndLength(Biggest_Airfoil_Mesh_Size,Smallest_Airfoil_Mesh_Size,[])
            Start_and_End_Length_TE.SetObjectEntry( 'Partition_2' )
            Sub_mesh_TE_Airfoils = Regular_1D_2.GetSubMesh()

            # TE
            Regular_1D_3 = Mesh_Domain.Segment(geom=Auto_group_for_Sub_mesh_TE_Edges)
            Sub_mesh_TE = Regular_1D_3.GetSubMesh()
            Local_Length_TE = Regular_1D_3.LocalLength(TE_Mesh_Size,None,1e-07)

            # LE
            Regular_1D_4 = Mesh_Domain.Segment(geom=Auto_group_for_Sub_mesh_LE_Edges)
            Sub_mesh_LE = Regular_1D_4.GetSubMesh()
            Local_Length_LE = Regular_1D_4.LocalLength(LE_Mesh_Size,None,1e-07)

            # Middle
            Regular_1D_5 = Mesh_Domain.Segment(geom=Auto_group_for_Sub_mesh_Middle)
            Local_Length_Middle = Regular_1D_5.LocalLength(Biggest_Airfoil_Mesh_Size,None,1e-07)
            Sub_mesh_Middle = Regular_1D_5.GetSubMesh()

            # Middle Airfoils
            Regular_1D_7 = Mesh_Domain.Segment(geom=Auto_group_for_Sub_mesh_Middle_Airfoils)
            Start_and_End_Length_Middle = Regular_1D_7.StartEndLength(Smallest_Airfoil_Mesh_Size, Biggest_Airfoil_Mesh_Size,[ 47, 56 ])
            Start_and_End_Length_Middle.SetObjectEntry( 'Partition_2' )
            Sub_mesh_Middle_Airfoils = Regular_1D_7.GetSubMesh()

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

            trefftz_plane_cut_path = salome_output_path + '/Sub_mesh_Trefft_Plane_Cut_Case_' + str(case) + '_AOA_' + str(AOA) + '_Wing_Span_' + str(
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
              Mesh_Domain.ExportDAT( r'/' + trefftz_plane_cut_path, Sub_mesh_Wake_Outlet_Edge )
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


            ## Set names of Mesh objects
            smesh.SetName(NETGEN_3D.GetAlgorithm(), 'NETGEN 3D')
            smesh.SetName(Regular_1D.GetAlgorithm(), 'Regular_1D')
            smesh.SetName(NETGEN_2D.GetAlgorithm(), 'NETGEN 2D')
            smesh.SetName(NETGEN_2D_Parameters_FarField, 'NETGEN 2D Parameters_FarField')
            smesh.SetName(NETGEN_2D_Parameters_Wing, 'NETGEN 2D Parameters_Wing')
            smesh.SetName(NETGEN_2D_Parameters_Wake, 'NETGEN_2D_Parameters_Wake')
            smesh.SetName(NETGEN_3D_Parameters_1, 'NETGEN 3D Parameters_1')
            smesh.SetName(Start_and_End_Length_TE, 'Start and End Length_TE')
            smesh.SetName(Local_Length_TE, 'Local Length_TE')
            smesh.SetName(Local_Length_Far_Field, 'Local Length_Far_Field')
            smesh.SetName(Start_and_End_Length_LE, 'Start and End Length_LE')
            smesh.SetName(Local_Length_Middle, 'Local Length_Middle')
            smesh.SetName(Start_and_End_Length_Wake, 'Start_and_End_Length_Wake')
            smesh.SetName(SegmentAroundVertex_0D, 'SegmentAroundVertex_0D')
            smesh.SetName(Length_Near_Vertex_Wake, 'Length_Near_Vertex_Wake')
            smesh.SetName(Local_Length_Wake_Outlet_Edge, 'Local_Length_Wake_Outlet_Edge')
            smesh.SetName(Start_and_End_Length_Middle, 'Start_and_End_Length_Middle')

            smesh.SetName(Mesh_Domain.GetMesh(), 'Mesh_Domain')
            smesh.SetName(Sub_mesh_Far_Field_Edges, 'Sub-mesh_Far_Field_Edges')
            smesh.SetName(Sub_mesh_Wing_Surface, 'Sub-mesh_Wing_Surface')
            smesh.SetName(Sub_mesh_Far_Field_Surface, 'Sub-mesh_Far_Field_Surface')
            smesh.SetName(Sub_mesh_Middle, 'Sub-mesh_Middle')
            smesh.SetName(Sub_mesh_TE, 'Sub-mesh_TE')
            smesh.SetName(Sub_mesh_LE, 'Sub_mesh_LE')
            smesh.SetName(Sub_mesh_TE_Airfoils, 'Sub-mesh_TE_Airfoils')
            smesh.SetName(Sub_mesh_LE_Airfoils, 'Sub-mesh_LE_Airfoils')
            smesh.SetName(Mesh_Wake_Surface, 'Mesh_Wake_Surface')
            smesh.SetName(Sub_mesh_Wake_Edges, 'Sub_mesh_Wake_Edges')
            smesh.SetName(Sub_mesh_Wake_Surface, 'Sub_mesh_Wake_Surface')
            smesh.SetName(Sub_mesh_Wake_Vertex, 'Sub-mesh_Wake_Vertex')
            smesh.SetName(Sub_mesh_Wake_Outlet_Edge, 'Sub_mesh_Wake_Outlet_Edge')
            smesh.SetName(Sub_mesh_Middle_Airfoils, 'Sub_mesh_Middle_Airfoils')

            # # Saving file to open from salome's gui
            # file_name = "/salome_files/generate_finite_wing_middle.hdf"
            # salome.myStudyManager.SaveAs(script_path + file_name, salome.myStudy, 0)

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
            Growth_Rate_Wing -= Growth_Rate_Wing_Refinement_Factor
            case +=1
        Growth_Rate_Domain -= Growth_Rate_Domain_Refinement_Factor
    AOA += AOA_Increment


if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser(True)
