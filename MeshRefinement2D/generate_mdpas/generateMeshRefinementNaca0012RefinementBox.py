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

Ratio = 1.001
Growth_Rate = 0.1
Growth_Rate_Refinement_Box = 0.1
#Initial_Airfoil_MeshSize = 0.01
Refinement_Box_Size_Length = 1.05
Refinement_Box_Size_Width = 0.2
Refinement_Box_Mesh_Size = 0.002

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
    FarField_MeshSize = int(Domain_Length / 100.0)
    AOA = Initial_AOA
    for j in range(Number_Of_AOAS):
        Airfoil_MeshSize = Initial_Airfoil_MeshSize
        #Refinement_Box_Mesh_Size = Airfoil_MeshSize
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

            #Create refinement box
            Face_Refinement_Box = geompy.MakeFaceHW(Refinement_Box_Size_Length, Refinement_Box_Size_Width, 1)

            #Cut the airfoil from the refinement box
            Cut_Refinement_Box = geompy.MakeCutList(Face_Refinement_Box, [Face_Airfoil], True)

            #Create domain
            Face_Domain = geompy.MakeFaceHW(Domain_Length, Domain_Width, 1)

            #Cut the Face_Refinement_Box from the domain
            Cut_Domain = geompy.MakeCutList(Face_Domain, [Face_Refinement_Box], True)

            # Make partition
            Partition_Domain = geompy.MakePartition([Cut_Refinement_Box, Cut_Domain], [], [], [], geompy.ShapeType["FACE"], 0, [], 0)

            # Explode faces
            [Outer_Box,Inner_Box] = geompy.ExtractShapes(Partition_Domain, geompy.ShapeType["FACE"], True)

            #Explode edges
            #[Inlet,Top,Box_Inlet,Box_Top,Box_Bottom,Box_Outlet,Bottom,Outlet] = geompy.ExtractShapes(Outer_Box, geompy.ShapeType["EDGE"], True)
            #[Box_Inlet_2,Edge_UpperSurface_LE,Edge_LowerSurface_LE,Box_Top_2,Edge_UpperSurface_TE,Box_Bottom_2,Edge_LowerSurface_TE,Outlet_2] = geompy.ExtractShapes(Inner_Box, geompy.ShapeType["EDGE"], True)
            if Refinement_Box_Size_Length > 4.5:
                [Inlet,Bottom,Box_Inlet,Edge_UpperSurface_LE,Edge_LowerSurface_LE,Box_Top,Edge_LowerSurface_TE,Box_Bottom,Edge_UpperSurface_TE,Box_Outlet,Top,Outlet] = geompy.ExtractShapes(Partition_Domain, geompy.ShapeType["EDGE"], True)
            else:
                [Inlet,Bottom,Box_Inlet,Edge_UpperSurface_LE,Edge_LowerSurface_LE,Box_Top,Box_Bottom,Edge_LowerSurface_TE,Edge_UpperSurface_TE,Box_Outlet,Top,Outlet] = geompy.ExtractShapes(Partition_Domain, geompy.ShapeType["EDGE"], True)


            #Body
            Body_Sub_mesh = geompy.CreateGroup(Partition_Domain, geompy.ShapeType["EDGE"])
            geompy.UnionList(Body_Sub_mesh, [Edge_LowerSurface_LE, Edge_LowerSurface_TE, Edge_UpperSurface_LE, Edge_UpperSurface_TE])

            #FarField
            Far_Field_Sub_Mesh = geompy.CreateGroup(Partition_Domain, geompy.ShapeType["EDGE"])
            geompy.UnionList(Far_Field_Sub_Mesh, [Inlet, Bottom, Top, Outlet])

            # Refinement box
            Refinement_Box_Sub_Mesh = geompy.CreateGroup(Partition_Domain, geompy.ShapeType["EDGE"])
            geompy.UnionList(Refinement_Box_Sub_Mesh, [Box_Inlet, Box_Bottom, Box_Top, Box_Outlet])

            #Add to study
            geompy.addToStudy( O, 'O' )
            geompy.addToStudy( OX, 'OX' )
            geompy.addToStudy( OY, 'OY' )
            geompy.addToStudy( OZ, 'OZ' )

            geompy.addToStudy( Curve_UpperSurface_LE, 'Curve_UpperSurface_LE' )
            geompy.addToStudy( Curve_UpperSurface_TE, 'Curve_UpperSurface_TE' )
            geompy.addToStudy( Curve_LowerSurface_TE, 'Curve_LowerSurface_TE' )
            geompy.addToStudy( Curve_LowerSurface_LE, 'Curve_LowerSurface_LE' )

            geompy.addToStudy( Face_Airfoil, 'Face_Airfoil' )
            geompy.addToStudy( Cut_Refinement_Box, 'Cut_Refinement_Box' )

            geompy.addToStudy( Face_Domain, 'Face_Domain' )
            geompy.addToStudy( Cut_Domain, 'Cut_Domain' )
            geompy.addToStudy( Partition_Domain, 'Partition_Domain' )

            geompy.addToStudyInFather( Partition_Domain, Outer_Box, 'Outer_Box' )
            geompy.addToStudyInFather( Partition_Domain, Inner_Box, 'Inner_Box' )

            geompy.addToStudyInFather( Partition_Domain, Inlet, 'Inlet' )
            geompy.addToStudyInFather( Partition_Domain, Bottom, 'Bottom' )
            geompy.addToStudyInFather( Partition_Domain, Box_Inlet, 'Box_Inlet' )
            geompy.addToStudyInFather( Partition_Domain, Edge_LowerSurface_LE, 'Edge_LowerSurface_LE' )
            geompy.addToStudyInFather( Partition_Domain, Edge_UpperSurface_LE, 'Edge_UpperSurface_LE' )
            geompy.addToStudyInFather( Partition_Domain, Box_Bottom, 'Box_Bottom' )
            geompy.addToStudyInFather( Partition_Domain, Edge_LowerSurface_TE, 'Edge_LowerSurface_TE' )
            geompy.addToStudyInFather( Partition_Domain, Box_Top, 'Box_Top' )
            geompy.addToStudyInFather( Partition_Domain, Edge_UpperSurface_TE, 'Edge_UpperSurface_TE' )
            geompy.addToStudyInFather( Partition_Domain, Box_Outlet, 'Box_Outlet' )
            geompy.addToStudyInFather( Partition_Domain, Top, 'Top' )
            geompy.addToStudyInFather( Partition_Domain, Outlet, 'Outlet' )

            geompy.addToStudyInFather( Partition_Domain, Body_Sub_mesh, 'Body_Sub_mesh' )
            geompy.addToStudyInFather( Partition_Domain, Far_Field_Sub_Mesh, 'Far_Field_Sub_Mesh' )
            geompy.addToStudyInFather( Partition_Domain, Refinement_Box_Sub_Mesh, 'Refinement_Box_Sub_Mesh' )

            ###
            ### SMESH component
            ###

            import  SMESH, SALOMEDS
            from salome.smesh import smeshBuilder

            smesh = smeshBuilder.New(theStudy)

            #Set NETGEN
            NETGEN_2D_Fluid = smesh.CreateHypothesis('NETGEN_2D', 'NETGENEngine')
            NETGEN_2D_Parameters_Fluid = smesh.CreateHypothesis('NETGEN_Parameters_2D', 'NETGENEngine')
            NETGEN_2D_Parameters_Fluid.SetMaxSize( FarField_MeshSize )
            NETGEN_2D_Parameters_Fluid.SetSecondOrder( 0 )
            NETGEN_2D_Parameters_Fluid.SetOptimize( 1 )
            NETGEN_2D_Parameters_Fluid.SetFineness( 4 )
            NETGEN_2D_Parameters_Fluid.SetGrowthRate( Growth_Rate_Refinement_Box )
            NETGEN_2D_Parameters_Fluid.SetNbSegPerEdge( 3 )
            NETGEN_2D_Parameters_Fluid.SetNbSegPerRadius( 5 )
            NETGEN_2D_Parameters_Fluid.SetUseSurfaceCurvature( 1 )
            NETGEN_2D_Parameters_Fluid.SetFuseEdges( 1 )
            NETGEN_2D_Parameters_Fluid.SetQuadAllowed( 0 )
            Fluid = smesh.Mesh(Partition_Domain)
            status = Fluid.AddHypothesis(NETGEN_2D_Parameters_Fluid)
            status = Fluid.AddHypothesis(NETGEN_2D_Fluid)
            NETGEN_2D_Parameters_Fluid.SetMinSize( Refinement_Box_Mesh_Size )

            #Set submeshes
            # Body
            Regular_1D_Body = Fluid.Segment(geom=Body_Sub_mesh)
            Local_Length_Body = Regular_1D_Body.LocalLength(Airfoil_MeshSize,None,1e-07)

            # Regular_1D_Body = Fluid.Segment(geom=Body_Sub_mesh)
            # Geometric_Progression_1 = Regular_1D_Body.GeometricProgression(0.001,1.01,[])

            # #Set geometric mesh
            # Geometric_Progression_1.SetStartLength( Airfoil_MeshSize )
            # Geometric_Progression_1.SetCommonRatio( Ratio )
            # Geometric_Progression_1.SetReversedEdges( [] )
            # Geometric_Progression_1.SetObjectEntry( "0:1:1:14" )

            # Refinement box edges
            Regular_1D_Box = Fluid.Segment(geom=Refinement_Box_Sub_Mesh)
            Local_Length_Box = Regular_1D_Box.LocalLength(Refinement_Box_Mesh_Size,None,1e-07)

            #Set farfield mesh
            Regular_1D_Far_Field = Fluid.Segment(geom=Far_Field_Sub_Mesh)
            Local_Length_Far_Field = Regular_1D_Far_Field.LocalLength(FarField_MeshSize,None,1e-07)

            NETGEN_2D_Refinement_Box = Fluid.Triangle(algo=smeshBuilder.NETGEN_2D,geom=Inner_Box)
            NETGEN_2D_Parameters_Box = NETGEN_2D_Refinement_Box.Parameters()
            NETGEN_2D_Parameters_Box.SetMaxSize( Refinement_Box_Mesh_Size )
            NETGEN_2D_Parameters_Box.SetOptimize( 1 )
            NETGEN_2D_Parameters_Box.SetFineness( 5 )
            NETGEN_2D_Parameters_Fluid.SetGrowthRate( Growth_Rate_Refinement_Box )
            NETGEN_2D_Parameters_Box.SetMinSize( Airfoil_MeshSize )
            NETGEN_2D_Parameters_Box.SetUseSurfaceCurvature( 1 )
            NETGEN_2D_Parameters_Box.SetQuadAllowed( 0 )
            NETGEN_2D_Parameters_Box.SetSecondOrder( 0 )
            NETGEN_2D_Parameters_Box.SetFuseEdges( 1 )

            NETGEN_2D_Outer_Box = Fluid.Triangle(algo=smeshBuilder.NETGEN_2D,geom=Outer_Box)
            NETGEN_2D_Parameters_Outer_Box = NETGEN_2D_Outer_Box.Parameters()
            NETGEN_2D_Parameters_Outer_Box.SetMaxSize( FarField_MeshSize )
            NETGEN_2D_Parameters_Outer_Box.SetOptimize( 1 )
            NETGEN_2D_Parameters_Outer_Box.SetFineness( 4 )
            NETGEN_2D_Parameters_Fluid.SetGrowthRate( Growth_Rate_Refinement_Box )
            NETGEN_2D_Parameters_Outer_Box.SetMinSize( Airfoil_MeshSize )
            NETGEN_2D_Parameters_Outer_Box.SetUseSurfaceCurvature( 1 )
            NETGEN_2D_Parameters_Outer_Box.SetQuadAllowed( 0 )
            NETGEN_2D_Parameters_Outer_Box.SetSecondOrder( 0 )
            NETGEN_2D_Parameters_Outer_Box.SetFuseEdges( 1 )

            #Mesh
            isDone = Fluid.Compute()
            Body = Regular_1D_Body.GetSubMesh()
            FarField = Regular_1D_Far_Field.GetSubMesh()
            Sub_mesh_Box_Edges = Regular_1D_Box.GetSubMesh()
            Sub_mesh_Refinement_Box = NETGEN_2D_Refinement_Box.GetSubMesh()
            Sub_mesh_Outer_Box = NETGEN_2D_Outer_Box.GetSubMesh()

            NumberOfNodes = Fluid.NbNodes()
            print(' Information about surface mesh:')
            print(' Number of nodes       :', NumberOfNodes)

            ## Set names of Mesh objects
            smesh.SetName(Fluid.GetMesh(), 'Fluid')
            smesh.SetName(NETGEN_2D_Fluid, 'NETGEN_2D_Fluid')
            smesh.SetName(NETGEN_2D_Parameters_Fluid, 'NETGEN_2D_Parameters_Fluid')

            smesh.SetName(Body, 'Body')
            # smesh.SetName(Local_Length_Body, 'Local_Length_Body')
            smesh.SetName(Sub_mesh_Box_Edges, 'Sub_mesh_Box_Edges')
            smesh.SetName(Local_Length_Box, 'Local_Length_Box')
            smesh.SetName(FarField, 'FarField')
            smesh.SetName(Local_Length_Far_Field, 'Local_Length_Far_Field')

            smesh.SetName(Sub_mesh_Refinement_Box, 'Sub_mesh_Refinement_Box')
            smesh.SetName(NETGEN_2D_Refinement_Box, 'NETGEN_2D_Refinement_Box')
            smesh.SetName(NETGEN_2D_Parameters_Box, 'NETGEN_2D_Parameters_Box')

            smesh.SetName(Sub_mesh_Outer_Box, 'Sub_mesh_Outer_Box')
            smesh.SetName(NETGEN_2D_Outer_Box, 'NETGEN_2D_Outer_Box')
            smesh.SetName(NETGEN_2D_Parameters_Outer_Box, 'NETGEN_2D_Parameters_Outer_Box')

            fluid_path = salome_output_path + '/Parts_Parts_Auto1_Case_' + str(case) + '_DS_' + str(Domain_Length) + '_AOA_' + str(
                AOA) + '_Far_Field_Mesh_Size_' + str(FarField_MeshSize) + '_Airfoil_Mesh_Size_' + str(Airfoil_MeshSize) + '.dat'

            far_field_path = salome_output_path + '/PotentialWallCondition2D_Far_field_Auto1_Case_' + str(case) + '_DS_' + str(Domain_Length) + '_AOA_' + str(
                AOA) + '_Far_Field_Mesh_Size_' + str(FarField_MeshSize) + '_Airfoil_Mesh_Size_' + str(Airfoil_MeshSize) + '.dat'

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
            file_name = salome_output_path + "/generate_naca0012_with_refinement_box.hdf"
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
