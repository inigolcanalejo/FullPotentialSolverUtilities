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
Number_Of_Domains_Size = TBD

Initial_AOA = TBD
AOA_Increment = TBD

Initial_Airfoil_MeshSize = TBD
Airfoil_Refinement_Factor = TBD

Initial_FarField_MeshSize = TBD
FarField_Refinement_Factor = TBD

Initial_Domain_Size = TBD
Domain_Size_Factor = TBD

Ratio = 1.1
Growth_Rate = 0.05

path = os.getcwd()
salome_output_path = 'TBD'
if not os.path.exists(salome_output_path):
    os.makedirs(salome_output_path)

case = 0
Domain_Length = Initial_Domain_Size
Domain_Width = Initial_Domain_Size

for k in range(Number_Of_Domains_Size):
    Domain_Length = int(Domain_Length)
    Domain_Width = int(Domain_Width)
    FarField_MeshSize = int(Domain_Length / 50.0)
    AOA = Initial_AOA
    for j in range(Number_Of_AOAS):
        Airfoil_MeshSize = Initial_Airfoil_MeshSize
        #FarField_MeshSize = Initial_FarField_MeshSize
        for i in range(Number_Of_Refinements):
            print 'Domain_Size = ', Domain_Length, 'AOA = ', AOA, 'FarField_MeshSize = ', FarField_MeshSize, 'Airfoil_MeshSize', Airfoil_MeshSize

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

            #Create naca0012 with center in origin and trailing edge at x = 0.5
            Curve_UpperSurface_LE = geompy.MakeCurveParametric("t - 0.5", "0.6*(0.2969*sqrt(t) - 0.1260*t - 0.3516*t**2 + 0.2843*t**3 - 0.1036*t**4)", "0", 0, 0.5, 999, GEOM.Interpolation, True)
            Curve_UpperSurface_TE = geompy.MakeCurveParametric("t - 0.5", "0.6*(0.2969*sqrt(t) - 0.1260*t - 0.3516*t**2 + 0.2843*t**3 - 0.1036*t**4)", "0", 0.5, 1, 999, GEOM.Interpolation, True)
            Curve_LowerSurface_TE = geompy.MakeCurveParametric("t - 0.5", "-0.6*(0.2969*sqrt(t) - 0.1260*t - 0.3516*t**2 + 0.2843*t**3 - 0.1036*t**4)", "0", 0.5, 1, 999, GEOM.Interpolation, True)
            Curve_LowerSurface_LE = geompy.MakeCurveParametric("t - 0.5", "-0.6*(0.2969*sqrt(t) - 0.1260*t - 0.3516*t**2 + 0.2843*t**3 - 0.1036*t**4)", "0", 0, 0.5, 999, GEOM.Interpolation, True)

            # #Create original naca0012
            # Curve_UpperSurface_LE = geompy.MakeCurveParametric("t - 0.5", "0.6*(0.2969*sqrt(t) - 0.1260*t - 0.3516*t**2 + 0.2843*t**3 - 0.1015*t**4)", "0", 0, 0.5, 999, GEOM.Interpolation, True)
            # Curve_UpperSurface_TE = geompy.MakeCurveParametric("t - 0.5", "0.6*(0.2969*sqrt(t) - 0.1260*t - 0.3516*t**2 + 0.2843*t**3 - 0.1015*t**4)", "0", 0.5, 1.008930411365, 999, GEOM.Interpolation, True)
            # Curve_LowerSurface_TE = geompy.MakeCurveParametric("t - 0.5", "-0.6*(0.2969*sqrt(t) - 0.1260*t - 0.3516*t**2 + 0.2843*t**3 - 0.1015*t**4)", "0", 0.5, 1.008930411365, 999, GEOM.Interpolation, True)
            # Curve_LowerSurface_LE = geompy.MakeCurveParametric("t - 0.5", "-0.6*(0.2969*sqrt(t) - 0.1260*t - 0.3516*t**2 + 0.2843*t**3 - 0.1015*t**4)", "0", 0, 0.5, 999, GEOM.Interpolation, True)

            geompy.ChangeOrientationShell(Curve_UpperSurface_TE)
            geompy.ChangeOrientationShell(Curve_LowerSurface_TE)

            #Create face
            Face_Airfoil = geompy.MakeFaceWires([Curve_UpperSurface_LE, Curve_UpperSurface_TE, Curve_LowerSurface_TE, Curve_LowerSurface_LE], 1)

            #Rotate around center to AOA
            geompy.Rotate(Face_Airfoil, OZ, -AOA*math.pi/180.0)

            #Create domain
            Face_Domain = geompy.MakeFaceHW(Domain_Length, Domain_Width, 1)

            #Cut the airfoil from the domain
            Cut_Domain = geompy.MakeCutList(Face_Domain, [Face_Airfoil], True)

            #Explode edges
            [Edge_1,Edge_2,Edge_LowerSurface_LE,Edge_UpperSurface_LE,Edge_LowerSurface_TE,Edge_UpperSurface_TE,Edge_7,Edge_8] = geompy.ExtractShapes(Cut_Domain, geompy.ShapeType["EDGE"], True)

            [Auto_group_for_Sub_mesh_1,Auto_group_for_Sub_mesh_1_1] = geompy.ExtractShapes(Edge_LowerSurface_TE, geompy.ShapeType["VERTEX"], True)

            #LowerSurface
            Auto_group_for_Sub_mesh_1 = geompy.CreateGroup(Cut_Domain, geompy.ShapeType["EDGE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_1, [Edge_LowerSurface_LE, Edge_LowerSurface_TE])

            #LowerSurface2
            Auto_group_for_Sub_mesh_1_1 = geompy.CreateGroup(Cut_Domain, geompy.ShapeType["EDGE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_1_1, [Edge_LowerSurface_LE, Edge_LowerSurface_TE])

            #UpperSurface
            Auto_group_for_Sub_mesh_2 = geompy.CreateGroup(Cut_Domain, geompy.ShapeType["EDGE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_2, [Edge_UpperSurface_LE, Edge_UpperSurface_TE])

            #Body
            Body_Sub_mesh = geompy.CreateGroup(Cut_Domain, geompy.ShapeType["EDGE"])
            geompy.UnionList(Body_Sub_mesh, [Edge_LowerSurface_LE, Edge_LowerSurface_TE, Edge_UpperSurface_LE, Edge_UpperSurface_TE])

            #FarField
            Auto_group_for_Sub_mesh_1_2 = geompy.CreateGroup(Cut_Domain, geompy.ShapeType["EDGE"])
            geompy.UnionList(Auto_group_for_Sub_mesh_1_2, [Edge_1, Edge_2, Edge_7, Edge_8])

            #Add to study
            geompy.addToStudy( O, 'O' )
            geompy.addToStudy( OX, 'OX' )
            geompy.addToStudy( OY, 'OY' )
            geompy.addToStudy( OZ, 'OZ' )
            geompy.addToStudy( Curve_UpperSurface_LE, 'Curve_UpperSurface_LE' )
            geompy.addToStudy( Curve_UpperSurface_TE, 'Curve_UpperSurface_TE' )
            geompy.addToStudy( Curve_LowerSurface_TE, 'Curve_LowerSurface_TE' )
            geompy.addToStudy( Curve_LowerSurface_LE, 'Curve_LowerSurface_LE' )
            geompy.addToStudyInFather( Cut_Domain, Edge_2, 'Edge_2' )
            geompy.addToStudyInFather( Cut_Domain, Edge_1, 'Edge_1' )
            geompy.addToStudy( Face_Domain, 'Face_Domain' )
            geompy.addToStudy( Face_Airfoil, 'Face_Airfoil' )
            geompy.addToStudyInFather( Cut_Domain, Edge_LowerSurface_LE, 'Edge_LowerSurface_LE' )
            geompy.addToStudyInFather( Cut_Domain, Edge_UpperSurface_LE, 'Edge_UpperSurface_LE' )
            geompy.addToStudy( Cut_Domain, 'Cut_Domain' )
            geompy.addToStudyInFather( Cut_Domain, Edge_LowerSurface_TE, 'Edge_LowerSurface_TE' )
            geompy.addToStudyInFather( Cut_Domain, Edge_UpperSurface_TE, 'Edge_UpperSurface_TE' )
            geompy.addToStudyInFather( Cut_Domain, Edge_7, 'Edge_7' )
            geompy.addToStudyInFather( Cut_Domain, Edge_8, 'Edge_8' )
            geompy.addToStudyInFather( Cut_Domain, Auto_group_for_Sub_mesh_1, 'Auto_group_for_Sub-mesh_1' )
            geompy.addToStudyInFather( Cut_Domain, Auto_group_for_Sub_mesh_1_1, 'Auto_group_for_Sub-mesh_1' )
            geompy.addToStudyInFather( Cut_Domain, Auto_group_for_Sub_mesh_2, 'Auto_group_for_Sub-mesh_2' )
            geompy.addToStudyInFather( Cut_Domain, Auto_group_for_Sub_mesh_1_2, 'Auto_group_for_Sub-mesh_1' )

            ###
            ### SMESH component
            ###

            import  SMESH, SALOMEDS
            from salome.smesh import smeshBuilder

            smesh = smeshBuilder.New(theStudy)

            #Set NETGEN
            NETGEN_1D_2D = smesh.CreateHypothesis('NETGEN_2D', 'NETGENEngine')
            NETGEN_2D_Parameters_1 = smesh.CreateHypothesis('NETGEN_Parameters_2D', 'NETGENEngine')
            NETGEN_2D_Parameters_1.SetMaxSize( FarField_MeshSize )
            NETGEN_2D_Parameters_1.SetSecondOrder( 0 )
            NETGEN_2D_Parameters_1.SetOptimize( 1 )
            NETGEN_2D_Parameters_1.SetFineness( 5 )
            NETGEN_2D_Parameters_1.SetGrowthRate( Growth_Rate )
            NETGEN_2D_Parameters_1.SetNbSegPerEdge( 3 )
            NETGEN_2D_Parameters_1.SetNbSegPerRadius( 5 )
            NETGEN_2D_Parameters_1.SetUseSurfaceCurvature( 1 )
            NETGEN_2D_Parameters_1.SetFuseEdges( 1 )
            NETGEN_2D_Parameters_1.SetQuadAllowed( 0 )
            Fluid = smesh.Mesh(Cut_Domain)
            status = Fluid.AddHypothesis(NETGEN_2D_Parameters_1)
            status = Fluid.AddHypothesis(NETGEN_1D_2D)
            NETGEN_2D_Parameters_1.SetMinSize( 1e-15 )

            #Set submeshes
            #Body
            Regular_1D = Fluid.Segment(geom=Body_Sub_mesh)
            Geometric_Progression_1 = Regular_1D.GeometricProgression(0.001,1.01,[])

            #UpperSurface
            #Regular_1D_1 = Fluid.Segment(geom=Auto_group_for_Sub_mesh_2)
            #status = Fluid.AddHypothesis(Geometric_Progression_1,Auto_group_for_Sub_mesh_2)

            #Set geometric mesh
            Geometric_Progression_1.SetStartLength( Airfoil_MeshSize )
            Geometric_Progression_1.SetCommonRatio( Ratio )
            Geometric_Progression_1.SetReversedEdges( [] )
            Geometric_Progression_1.SetObjectEntry( "0:1:1:14" )

            #Set farfield mesh
            Regular_1D_2 = Fluid.Segment(geom=Auto_group_for_Sub_mesh_1_2)
            Local_Length_1 = Regular_1D_2.LocalLength(FarField_MeshSize,None,1e-07)

            #Mesh
            isDone = Fluid.Compute()
            Body = Regular_1D.GetSubMesh()
            #UpperSurface = Regular_1D_1.GetSubMesh()
            FarField = Regular_1D_2.GetSubMesh()

            NumberOfNodes = Fluid.NbNodes()
            print(' Information about surface mesh:')
            print(' Number of nodes       :', NumberOfNodes)


            ## Set names of Mesh objects
            smesh.SetName(NETGEN_1D_2D, 'NETGEN 1D-2D')
            smesh.SetName(Regular_1D.GetAlgorithm(), 'Regular_1D')
            smesh.SetName(Geometric_Progression_1, 'Geometric Progression_1')
            smesh.SetName(NETGEN_2D_Parameters_1, 'NETGEN 2D Parameters_1')
            smesh.SetName(FarField, 'FarField')
            smesh.SetName(Local_Length_1, 'Local Length_1')
            smesh.SetName(Body, 'Body')
            #smesh.SetName(UpperSurface, 'UpperSurface')
            smesh.SetName(Fluid.GetMesh(), 'Fluid')

            fluid_path = salome_output_path + '/Parts_Parts_Auto1_Case_' + str(case) + '_DS_' + str(Domain_Length) + '_AOA_' + str(
                AOA) + '_Far_Field_Mesh_Size_' + str(FarField_MeshSize) + '_Airfoil_Mesh_Size_' + str(Airfoil_MeshSize) + '.dat'

            far_field_path = salome_output_path + '/PotentialWallCondition2D_Far_field_Auto1_Case_' + str(case) + '_DS_' + str(Domain_Length) + '_AOA_' + str(
                AOA) + '_Far_Field_Mesh_Size_' + str(FarField_MeshSize) + '_Airfoil_Mesh_Size_' + str(Airfoil_MeshSize) + '.dat'

            #upper_surface_path = salome_output_path + '/Body2D_UpperSurface_Case_' + str(case) + '_DS_' + str(Domain_Length) + '_AOA_' + str(
            #    AOA) + '_Far_Field_Mesh_Size_' + str(FarField_MeshSize) + '_Airfoil_Mesh_Size_' + str(Airfoil_MeshSize) + '.dat'

            #lower_surface_path = salome_output_path + '/Body2D_LowerSurface_Case_' + str(case) + '_DS_' + str(Domain_Length) + '_AOA_' + str(
            #    AOA) + '_Far_Field_Mesh_Size_' + str(FarField_MeshSize) + '_Airfoil_Mesh_Size_' + str(Airfoil_MeshSize) + '.dat'

            body_surface_path = salome_output_path + '/Body2D_Surface_Case_' + str(case) + '_DS_' + str(Domain_Length) + '_AOA_' + str(
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
                Fluid.ExportDAT( r'/' + body_surface_path, Body )
                pass
            except:
                print 'ExportPartToDAT() failed. Invalid file name?'

            # Saving file to open from salome's gui
            file_name = salome_output_path + "/generate_cosine.hdf"
            salome.myStudyManager.SaveAs(file_name, salome.myStudy, 0)

            '''
            if(case % 2 == 0):
                Airfoil_Refinement_Factor_Effective = Airfoil_Refinement_Factor
            else:
                Airfoil_Refinement_Factor_Effective = 0.2
            '''
            Airfoil_MeshSize *= Airfoil_Refinement_Factor
            #FarField_MeshSize /= FarField_Refinement_Factor
            case +=1
        AOA += AOA_Increment
    Domain_Length *= Domain_Size_Factor
    Domain_Width *= Domain_Size_Factor


if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser(True)
