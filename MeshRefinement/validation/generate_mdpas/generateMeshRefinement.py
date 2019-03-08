# -*- coding: utf-8 -*-

###
### This file is generated automatically by SALOME v8.4.0 with dump python functionality
###
import os
'''
run this script with:
salome -t python generateMeshRefinement.py
'''
Number_Of_Refinements = TBD
Number_Of_AOAS = TBD

Initial_AOA = TBD
AOA_Increment = TBD

Initial_Airfoil_MeshSize = TBD
Airfoil_Refinement_Factor = TBD

Initial_FarField_MeshSize = TBD
FarField_Refinement_Factor = TBD


Domain_Length = 100.0
Domain_Width = 50.0

path = os.getcwd()
output_path = '/home/inigo/simulations/naca0012/07_salome/05_MeshRefinement/output_salome'

case = 0
AOA = Initial_AOA
for j in range(Number_Of_AOAS):
    Airfoil_MeshSize = Initial_Airfoil_MeshSize
    FarField_MeshSize = Initial_FarField_MeshSize
    for i in range(Number_Of_Refinements):
        print 'AOA = ', AOA, 'FarField_MeshSize = ', FarField_MeshSize, 'Airfoil_MeshSize', Airfoil_MeshSize
        Min_Airfoil_MeshSize = Airfoil_MeshSize/10.0
        Deflection = Min_Airfoil_MeshSize/10.0

        import sys
        import salome

        salome.salome_init()
        theStudy = salome.myStudy

        import salome_notebook
        notebook = salome_notebook.NoteBook(theStudy)
        sys.path.insert( 0, r'/'+path)

        ###
        ### GEOM component
        ###

        import GEOM
        from salome.geom import geomBuilder
        import math
        import SALOMEDS


        geompy = geomBuilder.New(theStudy)

        #Create origin and axis
        O = geompy.MakeVertex(0, 0, 0)
        OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
        OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
        OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)

        #Create naca0012 with center in origin
        Curve_UpperSurface = geompy.MakeCurveParametric("t-0.5", "0.6*(0.2969*sqrt(t) - 0.1260*t - 0.3516*t**2 + 0.2843*t**3 - 0.1036*t**4)", "0", 0, 1, 999, GEOM.Interpolation, True)
        Curve_LowerSurface = geompy.MakeCurveParametric("t-0.5", "-0.6*(0.2969*sqrt(t) - 0.1260*t - 0.3516*t**2 + 0.2843*t**3 - 0.1036*t**4)", "0", 0, 1, 999, GEOM.Interpolation, True)

        #Rotate around center to AOA 5°
        geompy.Rotate(Curve_UpperSurface, OZ, -AOA*math.pi/180.0)
        geompy.Rotate(Curve_LowerSurface, OZ, -AOA*math.pi/180.0)

        #Create face
        Face_Airfoil = geompy.MakeFaceWires([Curve_UpperSurface, Curve_LowerSurface], 1)

        #Create domain
        Face_Domain = geompy.MakeFaceHW(Domain_Length, Domain_Width, 1)

        #Cut the airfoil from the domain
        Cut_Domain = geompy.MakeCutList(Face_Domain, [Face_Airfoil], True)

        #Explode edges
        [Edge_Inlet,Edge_WallDown,Edge_LowerSurface,Edge_UpperSurface,Edge_WallUp,Edge_Outlet] = geompy.ExtractShapes(Cut_Domain, geompy.ShapeType["EDGE"], True)
        #[Vertex_LE,Vertex_TE] = geompy.ExtractShapes(Edge_UpperSurface, geompy.ShapeType["VERTEX"], True)
        Parts_Parts_Auto1 = geompy.CreateGroup(Cut_Domain, geompy.ShapeType["FACE"])
        geompy.UnionIDs(Parts_Parts_Auto1, [1])
        PotentialWallCondition2D_Far_field_Auto1 = geompy.CreateGroup(Cut_Domain, geompy.ShapeType["EDGE"])
        geompy.UnionIDs(PotentialWallCondition2D_Far_field_Auto1, [10, 3, 8, 6])
        #Wake2D_Wake_Auto1 = geompy.CreateGroup(Cut_Domain, geompy.ShapeType["VERTEX"])
        #geompy.UnionIDs(Wake2D_Wake_Auto1, [14])
        Body2D_UpperSurface = geompy.CreateGroup(Cut_Domain, geompy.ShapeType["EDGE"])
        geompy.UnionIDs(Body2D_UpperSurface, [12])
        Body2D_LowerSurface = geompy.CreateGroup(Cut_Domain, geompy.ShapeType["EDGE"])
        geompy.UnionIDs(Body2D_LowerSurface, [15])

        #Add to study
        geompy.addToStudy( O, 'O' )
        geompy.addToStudy( OX, 'OX' )
        geompy.addToStudy( OY, 'OY' )
        geompy.addToStudy( OZ, 'OZ' )
        geompy.addToStudy( Curve_UpperSurface, 'Curve_UpperSurface' )
        geompy.addToStudy( Curve_LowerSurface, 'Curve_LowerSurface' )
        geompy.addToStudy( Face_Airfoil, 'Face_Airfoil' )
        geompy.addToStudy( Face_Domain, 'Face_Domain' )
        geompy.addToStudy( Cut_Domain, 'Cut_Domain' )
        geompy.addToStudyInFather( Cut_Domain, Edge_Inlet, 'Edge_Inlet' )
        geompy.addToStudyInFather( Cut_Domain, Edge_WallDown, 'Edge_WallDown' )
        geompy.addToStudyInFather( Cut_Domain, Edge_LowerSurface, 'Edge_LowerSurface' )
        geompy.addToStudyInFather( Cut_Domain, Edge_UpperSurface, 'Edge_UpperSurface' )
        geompy.addToStudyInFather( Cut_Domain, Edge_WallUp, 'Edge_WallUp' )
        geompy.addToStudyInFather( Cut_Domain, Edge_Outlet, 'Edge_Outlet' )
        #geompy.addToStudyInFather( Edge_UpperSurface, Vertex_LE, 'Vertex_LE' )
        #geompy.addToStudyInFather( Edge_UpperSurface, Vertex_TE, 'Vertex_TE' )
        geompy.addToStudyInFather( Cut_Domain, Parts_Parts_Auto1, 'Parts_Parts_Auto1' )
        geompy.addToStudyInFather( Cut_Domain, PotentialWallCondition2D_Far_field_Auto1, 'PotentialWallCondition2D_Far_field_Auto1' )
        geompy.addToStudyInFather( Cut_Domain, Body2D_UpperSurface, 'Body2D_UpperSurface' )
        #geompy.addToStudyInFather( Cut_Domain, Wake2D_Wake_Auto1, 'Wake2D_Wake_Auto1' )
        geompy.addToStudyInFather( Cut_Domain, Body2D_LowerSurface, 'Body2D_LowerSurface' )

        ###
        ### SMESH component
        ###

        import  SMESH, SALOMEDS
        from salome.smesh import smeshBuilder

        smesh = smeshBuilder.New(theStudy)
        Fluid = smesh.Mesh(Cut_Domain)

        #Set NETGEN
        NETGEN_1D_2D = Fluid.Triangle(algo=smeshBuilder.NETGEN_1D2D)
        NETGEN_2D_Parameters_1 = NETGEN_1D_2D.Parameters()
        NETGEN_2D_Parameters_1.SetMaxSize( FarField_MeshSize )
        NETGEN_2D_Parameters_1.SetSecondOrder( 0 )
        NETGEN_2D_Parameters_1.SetOptimize( 1 )
        NETGEN_2D_Parameters_1.SetFineness( 4 )
        NETGEN_2D_Parameters_1.SetMinSize( 1e-08 )
        NETGEN_2D_Parameters_1.SetUseSurfaceCurvature( 1 )
        NETGEN_2D_Parameters_1.SetFuseEdges( 1 )
        NETGEN_2D_Parameters_1.SetQuadAllowed( 0 )

        ##Set submeshes
        #UpperSurface
        Regular_1D = Fluid.Segment(geom=Body2D_UpperSurface)
        UpperSurface = Regular_1D.GetSubMesh()
        Adaptive_1 = Regular_1D.Adaptive(Min_Airfoil_MeshSize, Airfoil_MeshSize, Deflection)

        #LowerSurface
        Regular_1D_1 = Fluid.Segment(geom=Body2D_LowerSurface)
        LowerSurface = Regular_1D_1.GetSubMesh()
        status = Fluid.AddHypothesis(Adaptive_1,Body2D_LowerSurface)

        #FarField
        Regular_1D_2 = Fluid.Segment(geom=PotentialWallCondition2D_Far_field_Auto1)
        FarField = Regular_1D_2.GetSubMesh()
        Local_Length_1 = Regular_1D_2.LocalLength(FarField_MeshSize,None,1e-07)

        #KuttaVertex
        #Length_Near_Vertex_TE = smesh.CreateHypothesis('SegmentLengthAroundVertex')
        #Length_Near_Vertex_TE.SetLength( 0.00995143 )
        #Wake = Fluid.GetSubMesh( Wake2D_Wake_Auto1, 'Sub-mesh_4' )
        #SegmentAroundVertex_0D = smesh.CreateHypothesis('SegmentAroundVertex_0D')
        #status = Fluid.AddHypothesis(SegmentAroundVertex_0D,Wake2D_Wake_Auto1)
        #status = Fluid.AddHypothesis(Length_Near_Vertex_TE,Wake2D_Wake_Auto1)

        #Mesh
        isDone = Fluid.Compute()

        ## Set names of Mesh objects
        smesh.SetName(FarField, 'FarField')
        smesh.SetName(NETGEN_1D_2D.GetAlgorithm(), 'NETGEN 1D-2D')
        smesh.SetName(Regular_1D.GetAlgorithm(), 'Regular_1D')
        #smesh.SetName(SegmentAroundVertex_0D, 'SegmentAroundVertex_0D')
        #smesh.SetName(Wake, 'Wake')
        smesh.SetName(Fluid.GetMesh(), 'Fluid')
        smesh.SetName(Adaptive_1, 'Adaptive_1')
        smesh.SetName(NETGEN_2D_Parameters_1, 'NETGEN 2D Parameters_1')
        #smesh.SetName(Length_Near_Vertex_TE, 'Length Near Vertex_TE')
        smesh.SetName(Local_Length_1, 'Local Length_1')
        smesh.SetName(LowerSurface, 'LowerSurface')
        smesh.SetName(UpperSurface, 'UpperSurface')

        #Save
        #salome.myStudyManager.SaveAs("generate_Mesh" + str(i) + ".hdf", theStudy, False)

        fluid_path = output_path + '/Parts_Parts_Auto1_Case_' + str(case) + '_AOA_' + str(
            AOA) + '_Far_Field_Mesh_Size_' + str(FarField_MeshSize) + '_Airfoil_Mesh_Size_' + str(Airfoil_MeshSize) + '.dat'

        far_field_path = output_path + '/PotentialWallCondition2D_Far_field_Auto1_Case_' + str(case) + '_AOA_' + str(
            AOA) + '_Far_Field_Mesh_Size_' + str(FarField_MeshSize) + '_Airfoil_Mesh_Size_' + str(Airfoil_MeshSize) + '.dat'

        upper_surface_path = output_path + '/Body2D_UpperSurface_Case_' + str(case) + '_AOA_' + str(
            AOA) + '_Far_Field_Mesh_Size_' + str(FarField_MeshSize) + '_Airfoil_Mesh_Size_' + str(Airfoil_MeshSize) + '.dat'

        lower_surface_path = output_path + '/Body2D_LowerSurface_Case_' + str(case) + '_AOA_' + str(
            AOA) + '_Far_Field_Mesh_Size_' + str(FarField_MeshSize) + '_Airfoil_Mesh_Size_' + str(Airfoil_MeshSize) + '.dat'

        try:
            Fluid.ExportDAT( r'/' + fluid_path)
            pass
        except:
            print 'ExportDAT() failed. Invalid file name?'
        try:
            Fluid.ExportDAT( r'/' + far_field_path, FarField )
            pass
        except:
            print 'ExportPartToDAT() failed. Invalid file name?'
        try:
            Fluid.ExportDAT( r'/' + upper_surface_path, UpperSurface )
            pass
        except:
            print 'ExportPartToDAT() failed. Invalid file name?'
        try:
            Fluid.ExportDAT( r'/' + lower_surface_path, LowerSurface )
            pass
        except:
            print 'ExportPartToDAT() failed. Invalid file name?'

        Airfoil_MeshSize /= Airfoil_Refinement_Factor
        FarField_MeshSize /= FarField_Refinement_Factor
        case +=1
    AOA += AOA_Increment

if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser(True)
