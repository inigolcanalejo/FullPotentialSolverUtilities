# -*- coding: utf-8 -*-

###
### This file is generated automatically by SALOME v8.4.0 with dump python functionality
###
'''
run this script with:
salome -t python generateNacaWingInfinite.py
'''
# Indicate pah
script_path = '/home/inigo/simulations/wing/00_models/00_runSalome'
# Indicate angle of attack
AOA = 0
Domain_Length = 20
Domain_Height = Domain_Length
Domain_Width = 0.01

LE_Mesh_Size = 0.1
TE_Mesh_Size = 0.1
Far_Field_Mesh_Size = 0.5

import sys
import salome
import time as time

salome.salome_init()
theStudy = salome.myStudy

import salome_notebook
notebook = salome_notebook.NoteBook(theStudy)
sys.path.insert( 0, r'/home/inigo/simulations/wing/00_models/00_runSalome')

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

# Create naca0012 with center in origin
Curve_UpperSurface_LE = geompy.MakeCurveParametric("t - 0.5", "0", "0.6*(0.2969*sqrt(t) - 0.1260*t - 0.3516*t**2 + 0.2843*t**3 - 0.1036*t**4)", 0, 0.5, 999, GEOM.Interpolation, True)
Curve_UpperSurface_TE = geompy.MakeCurveParametric("t - 0.5", "0", "0.6*(0.2969*sqrt(t) - 0.1260*t - 0.3516*t**2 + 0.2843*t**3 - 0.1036*t**4)", 0.5, 1, 999, GEOM.Interpolation, True)
Curve_LowerSurface_TE = geompy.MakeCurveParametric("t - 0.5", "0", "-0.6*(0.2969*sqrt(t) - 0.1260*t - 0.3516*t**2 + 0.2843*t**3 - 0.1036*t**4)", 0.5, 1, 999, GEOM.Interpolation, True)
Curve_LowerSurface_LE = geompy.MakeCurveParametric("t - 0.5", "0", "-0.6*(0.2969*sqrt(t) - 0.1260*t - 0.3516*t**2 + 0.2843*t**3 - 0.1036*t**4)", 0, 0.5, 999, GEOM.Interpolation, True)

# Create face
Face_Airfoil = geompy.MakeFaceWires([Curve_UpperSurface_LE, Curve_UpperSurface_TE, Curve_LowerSurface_TE, Curve_LowerSurface_LE], 1)

# Rotate around center to AOA
AOA *=math.pi/180.0
geompy.Rotate(Face_Airfoil, OY, AOA)

# Create domain face
Face_Domain = geompy.MakeFaceHW(Domain_Length, Domain_Height, 3)

# Cut the airfoil from domain
Cut_Domain = geompy.MakeCutList(Face_Domain, [Face_Airfoil], True)

# Extrude volume
Extrusion_Domain = geompy.MakePrismVecH(Cut_Domain, OY, Domain_Width)

# Explode faces and edges
if Domain_Width > 5.1:
  [Face_Inlet,Face_Left,Face_LS_LE,Face_UP_LE,Face_Bottom,Face_Top,Face_LS_TE,Face_US_TE,Face_Right,Face_Outlet] = geompy.ExtractShapes(Extrusion_Domain, geompy.ShapeType["FACE"], True)
  [Edge_Left_LS_LE,Edge_LE,Edge_LS_Middle,Edge_Right_LS_LE] = geompy.ExtractShapes(Face_LS_LE, geompy.ShapeType["EDGE"], True)
  [Edge_Left_US_LE,geomObj_1,Edge_US_Middle,Edge_Right_US_LE] = geompy.ExtractShapes(Face_UP_LE, geompy.ShapeType["EDGE"], True)
  [Edge_Left_LS_TE,geomObj_1,Edge_TE,Edge_Right_LS_TE] = geompy.ExtractShapes(Face_LS_TE, geompy.ShapeType["EDGE"], True)
  [Edge_Left_US_TE,geomObj_1,geomObj_2,Edge_Right_US_TE] = geompy.ExtractShapes(Face_US_TE, geompy.ShapeType["EDGE"], True)
else:
  [Face_Inlet,Face_LS_LE,Face_UP_LE,Face_Left,Face_Bottom,Face_Top,Face_Right,Face_LS_TE,Face_US_TE,Face_Outlet] = geompy.ExtractShapes(Extrusion_Domain, geompy.ShapeType["FACE"], True)
  [Edge_LE,Edge_Left_LS_LE,Edge_Right_LS_LE,Edge_LS_Middle] = geompy.ExtractShapes(Face_LS_LE, geompy.ShapeType["EDGE"], True)
  [geomObj_1,Edge_Left_US_LE,Edge_Right_US_LE,Edge_US_Middle] = geompy.ExtractShapes(Face_UP_LE, geompy.ShapeType["EDGE"], True)
  [geomObj_1,Edge_Left_LS_TE,Edge_Right_LS_TE,Edge_TE] = geompy.ExtractShapes(Face_LS_TE, geompy.ShapeType["EDGE"], True)
  [geomObj_1,Edge_Left_US_TE,Edge_Right_US_TE,geomObj_2] = geompy.ExtractShapes(Face_US_TE, geompy.ShapeType["EDGE"], True)
  [Edge_Inlet_Left,Edge_Inlet_Down,Edge_Inlet_Up,Edge_Inlet_Right] = geompy.ExtractShapes(Face_Inlet, geompy.ShapeType["EDGE"], True)

Auto_group_for_Sub_mesh_Wing = geompy.CreateGroup(Extrusion_Domain, geompy.ShapeType["FACE"])
geompy.UnionList(Auto_group_for_Sub_mesh_Wing, [Face_LS_LE, Face_UP_LE, Face_LS_TE, Face_US_TE])
Auto_group_for_Sub_mesh_FarField_Edges = geompy.CreateGroup(Extrusion_Domain, geompy.ShapeType["EDGE"])
geompy.UnionList(Auto_group_for_Sub_mesh_FarField_Edges, [Edge_Inlet_Left,Edge_Inlet_Right])
Auto_group_for_Sub_mesh_FarField = geompy.CreateGroup(Extrusion_Domain, geompy.ShapeType["FACE"])
geompy.UnionList(Auto_group_for_Sub_mesh_FarField, [Face_Inlet, Face_Left, Face_Bottom, Face_Top, Face_Right, Face_Outlet])

# Generate wake
Vector_Wake_Direction = geompy.MakeVectorDXDYDZ(1, 0, 0)
Extrusion_Wake = geompy.MakePrismVecH(Edge_TE, Vector_Wake_Direction, Domain_Length*0.5)

# Add to study
geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )
geompy.addToStudy( Curve_UpperSurface_LE, 'Curve_UpperSurface_LE' )
geompy.addToStudy( Curve_UpperSurface_TE, 'Curve_UpperSurface_TE' )
geompy.addToStudy( Curve_LowerSurface_TE, 'Curve_LowerSurface_TE' )
geompy.addToStudy( Curve_LowerSurface_LE, 'Curve_LowerSurface_LE' )
geompy.addToStudy( Face_Airfoil, 'Face_Airfoil' )
geompy.addToStudy( Face_Domain, 'Face_Domain' )
geompy.addToStudy( Cut_Domain, 'Cut_Domain' )
geompy.addToStudy( Extrusion_Domain, 'Extrusion_Domain' )
geompy.addToStudyInFather( Extrusion_Domain, Face_Inlet, 'Face_Inlet' )
geompy.addToStudyInFather( Extrusion_Domain, Face_Left, 'Face_Left' )
geompy.addToStudyInFather( Extrusion_Domain, Face_LS_LE, 'Face_LS_LE' )
geompy.addToStudyInFather( Extrusion_Domain, Face_UP_LE, 'Face_UP_LE' )
geompy.addToStudyInFather( Extrusion_Domain, Face_Bottom, 'Face_Bottom' )
geompy.addToStudyInFather( Extrusion_Domain, Face_Top, 'Face_Top' )
geompy.addToStudyInFather( Extrusion_Domain, Face_LS_TE, 'Face_LS_TE' )
geompy.addToStudyInFather( Extrusion_Domain, Face_US_TE, 'Face_US_TE' )
geompy.addToStudyInFather( Extrusion_Domain, Face_Right, 'Face_Right' )
geompy.addToStudyInFather( Extrusion_Domain, Face_Outlet, 'Face_Outlet' )
geompy.addToStudyInFather( Face_LS_LE, Edge_Left_LS_LE, 'Edge_Left_LS_LE' )
geompy.addToStudyInFather( Face_LS_LE, Edge_LE, 'Edge_LE' )
geompy.addToStudyInFather( Face_LS_LE, Edge_LS_Middle, 'Edge_LS_Middle' )
geompy.addToStudyInFather( Face_LS_LE, Edge_Right_LS_LE, 'Edge_Right_LS_LE' )
geompy.addToStudyInFather( Face_UP_LE, Edge_Left_US_LE, 'Edge_Left_US_LE' )
geompy.addToStudyInFather( Face_LS_TE, Edge_Left_LS_TE, 'Edge_Left_LS_TE' )
geompy.addToStudyInFather( Face_UP_LE, Edge_US_Middle, 'Edge_US_Middle' )
geompy.addToStudyInFather( Face_UP_LE, Edge_Right_US_LE, 'Edge_Right_US_LE' )
geompy.addToStudyInFather( Face_US_TE, Edge_Left_US_TE, 'Edge_Left_US_TE' )
geompy.addToStudyInFather( Face_LS_TE, Edge_TE, 'Edge_TE' )
geompy.addToStudyInFather( Face_LS_TE, Edge_Right_LS_TE, 'Edge_Right_LS_TE' )
geompy.addToStudyInFather( Extrusion_Domain, Auto_group_for_Sub_mesh_Wing, 'Auto_group_for_Sub-mesh_Wing' )
geompy.addToStudyInFather( Extrusion_Domain, Auto_group_for_Sub_mesh_FarField, 'Auto_group_for_Sub-mesh_FarField' )
geompy.addToStudyInFather( Face_US_TE, Edge_Right_US_TE, 'Edge_Right_US_TE' )
geompy.addToStudy( Vector_Wake_Direction, 'Vector_Wake_Direction' )
geompy.addToStudy( Extrusion_Wake, 'Extrusion_Wake' )

###
### SMESH component
###

import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder

smesh = smeshBuilder.New(theStudy)
Mesh_Domain = smesh.Mesh(Extrusion_Domain)

# Set NETGEN 3D
NETGEN_3D = Mesh_Domain.Tetrahedron()
NETGEN_3D_Parameters_1 = NETGEN_3D.Parameters()
NETGEN_3D_Parameters_1.SetMaxSize( Far_Field_Mesh_Size )
NETGEN_3D_Parameters_1.SetOptimize( 1 )
NETGEN_3D_Parameters_1.SetFineness( 5 )
NETGEN_3D_Parameters_1.SetGrowthRate( 0.3 )
NETGEN_3D_Parameters_1.SetNbSegPerEdge( 6.92034e-310 )
NETGEN_3D_Parameters_1.SetNbSegPerRadius( 1.47958e-316 )
NETGEN_3D_Parameters_1.SetMinSize( 0.001 )
NETGEN_3D_Parameters_1.SetUseSurfaceCurvature( 0 )
NETGEN_3D_Parameters_1.SetSecondOrder( 100 )
NETGEN_3D_Parameters_1.SetFuseEdges( 80 )
NETGEN_3D_Parameters_1.SetQuadAllowed( 127 )

# Set TE and LE
Regular_1D = Mesh_Domain.Segment(geom=Edge_TE)
Sub_mesh_TE = Regular_1D.GetSubMesh()
Local_Length_TE = Regular_1D.LocalLength(TE_Mesh_Size,None,1e-07)
Regular_1D_1 = Mesh_Domain.Segment(geom=Edge_LE)
Local_Length_LE = Regular_1D_1.LocalLength(LE_Mesh_Size,None,1e-07)

# Set Inlet edges
Regular_1D_2 = Mesh_Domain.Segment(geom=Auto_group_for_Sub_mesh_FarField_Edges)
Local_Length_FarField = Regular_1D_2.LocalLength(Far_Field_Mesh_Size,None,1e-07)

# Set Wing
NETGEN_1D_2D = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_1D2D,geom=Auto_group_for_Sub_mesh_Wing)
Sub_mesh_Wing = NETGEN_1D_2D.GetSubMesh()
NETGEN_2D_Parameters_Wing = NETGEN_1D_2D.Parameters()
NETGEN_2D_Parameters_Wing.SetMaxSize( 1.73205 )
NETGEN_2D_Parameters_Wing.SetSecondOrder( 0 )
NETGEN_2D_Parameters_Wing.SetOptimize( 1 )
NETGEN_2D_Parameters_Wing.SetFineness( 5 )
NETGEN_2D_Parameters_Wing.SetGrowthRate( 0.3 )
NETGEN_2D_Parameters_Wing.SetNbSegPerEdge( 1 )
NETGEN_2D_Parameters_Wing.SetNbSegPerRadius( 2 )
NETGEN_2D_Parameters_Wing.SetMinSize( 0.001 )
NETGEN_2D_Parameters_Wing.SetUseSurfaceCurvature( 1 )
NETGEN_2D_Parameters_Wing.SetFuseEdges( 1 )
NETGEN_2D_Parameters_Wing.SetQuadAllowed( 0 )

# Set Far field
NETGEN_1D_2D_1 = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_1D2D,geom=Auto_group_for_Sub_mesh_FarField)
Sub_mesh_FarField = NETGEN_1D_2D_1.GetSubMesh()
NETGEN_2D_Parameters_FarField = NETGEN_1D_2D_1.Parameters()
NETGEN_2D_Parameters_FarField.SetMaxSize( Far_Field_Mesh_Size )
NETGEN_2D_Parameters_FarField.SetSecondOrder( 0 )
NETGEN_2D_Parameters_FarField.SetOptimize( 1 )
NETGEN_2D_Parameters_FarField.SetFineness( 5 )
NETGEN_2D_Parameters_FarField.SetGrowthRate( 0.3 )
NETGEN_2D_Parameters_FarField.SetNbSegPerEdge( 1 )
NETGEN_2D_Parameters_FarField.SetNbSegPerRadius( 2 )
NETGEN_2D_Parameters_FarField.SetMinSize( 0.01 )
NETGEN_2D_Parameters_FarField.SetUseSurfaceCurvature( 1 )
NETGEN_2D_Parameters_FarField.SetFuseEdges( 1 )
NETGEN_2D_Parameters_FarField.SetQuadAllowed( 0 )
isDone = Mesh_Domain.SetMeshOrder( [ [ Sub_mesh_Wing, Sub_mesh_FarField ] ])

print(' Starting meshing ')
start_time = time.time()
# Compute mesh
isDone = Mesh_Domain.Compute()
exe_time = time.time() - start_time
print(' Mesh execution tool ', str(round(exe_time, 2)), ' sec')
print(' Information about volume mesh:')
print(' Number of nodes       :', Mesh_Domain.NbNodes())
print(' Number of elements    :', Mesh_Domain.NbTetras())
# print(' Information about wing mesh:')
# print(' Number of nodes       :', Sub_mesh_Wing.NbNodes())
# print(' Number of elements    :', Sub_mesh_Wing.NbTetras())

# Export meshes into data files
try:
  Mesh_Domain.ExportDAT( r'/home/inigo/simulations/wing/00_models/00_runSalome/salome_output/Mesh_Domain.dat' )
  pass
except:
  print 'ExportDAT() failed. Invalid file name?'
try:
  Mesh_Domain.ExportDAT( r'/home/inigo/simulations/wing/00_models/00_runSalome/salome_output/Sub-mesh_TE.dat', Sub_mesh_TE )
  pass
except:
  print 'ExportPartToDAT() failed. Invalid file name?'
try:
  Mesh_Domain.ExportDAT( r'/home/inigo/simulations/wing/00_models/00_runSalome/salome_output/Sub-mesh_Wing.dat', Sub_mesh_Wing )
  pass
except:
  print 'ExportPartToDAT() failed. Invalid file name?'
try:
  Mesh_Domain.ExportDAT( r'/home/inigo/simulations/wing/00_models/00_runSalome/salome_output/Sub-mesh_FarField.dat', Sub_mesh_FarField )
  pass
except:
  print 'ExportPartToDAT() failed. Invalid file name?'
Sub_mesh_LE = Regular_1D_1.GetSubMesh()

# Mesh wake and export STL
Mesh_Wake_Surface = smesh.Mesh(Extrusion_Wake)
status = Mesh_Wake_Surface.AddHypothesis(NETGEN_2D_Parameters_FarField)
NETGEN_1D_2D_2 = Mesh_Wake_Surface.Triangle(algo=smeshBuilder.NETGEN_1D2D)
isDone = Mesh_Wake_Surface.Compute()
try:
  Mesh_Wake_Surface.ExportSTL( r'/home/inigo/simulations/wing/00_models/00_runSalome/case/wake_stl.stl', 1 )
  pass
except:
  print 'ExportSTL() failed. Invalid file name?'


## Set names of Mesh objects
smesh.SetName(Sub_mesh_FarField, 'Sub-mesh_FarField')
smesh.SetName(Sub_mesh_Wing, 'Sub-mesh_Wing')
smesh.SetName(NETGEN_3D.GetAlgorithm(), 'NETGEN 3D')
smesh.SetName(Regular_1D.GetAlgorithm(), 'Regular_1D')
smesh.SetName(NETGEN_1D_2D.GetAlgorithm(), 'NETGEN 1D-2D')
smesh.SetName(Mesh_Domain.GetMesh(), 'Mesh_Domain')
smesh.SetName(Local_Length_LE, 'Local Length_LE')
smesh.SetName(Local_Length_TE, 'Local Length_TE')
smesh.SetName(NETGEN_3D_Parameters_1, 'NETGEN 3D Parameters_1')
smesh.SetName(NETGEN_2D_Parameters_FarField, 'NETGEN 2D Parameters_FarField')
smesh.SetName(NETGEN_2D_Parameters_Wing, 'NETGEN 2D Parameters_Wing')
smesh.SetName(Sub_mesh_LE, 'Sub-mesh_LE')
smesh.SetName(Sub_mesh_TE, 'Sub-mesh_TE')


if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser(True)
