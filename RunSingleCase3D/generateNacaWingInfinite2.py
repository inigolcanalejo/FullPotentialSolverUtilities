# -*- coding: utf-8 -*-

###
### This file is generated automatically by SALOME v8.4.0 with dump python functionality
###
'''
run this script with:
salome -t python generateNacaWingInfinite2.py
'''
# Indicate pah
import os
script_path = os.path.dirname(os.path.realpath(__file__))

# Indicate angle of attack
AOA = 5
Domain_Length = 100
Domain_Height = Domain_Length
Domain_Width = 0.1

Airfoil_Mesh_Size = 0.001
Biggest_Airfoil_Mesh_Size = 0.05
LE_Mesh_Size = Airfoil_Mesh_Size
TE_Mesh_Size = Airfoil_Mesh_Size
Far_Field_Mesh_Size = Domain_Length/50.0
Growth_Rate_Wing = 0.3
Growth_Rate_Far_Field = 0.05
Growth_Rate_Domain = 0.3

import sys
import salome
import time as time

salome.salome_init()
theStudy = salome.myStudy

import salome_notebook
notebook = salome_notebook.NoteBook(theStudy)

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
AOArad = AOA*math.pi/180.0
geompy.Rotate(Face_Airfoil, OY, AOArad)

# Create domain face
Face_Domain = geompy.MakeFaceHW(Domain_Length, Domain_Height, 3)

# Cut the airfoil from domain
Cut_Domain = geompy.MakeCutList(Face_Domain, [Face_Airfoil], True)

# Extrude volume
Extrusion_Domain = geompy.MakePrismVecH(Cut_Domain, OY, Domain_Width)

# Explode faces and edges
if Domain_Width > 8.9:
  [Face_Inlet,Face_Left,Face_LS_LE,Face_UP_LE,Face_Bottom,Face_Top,Face_LS_TE,Face_US_TE,Face_Right,Face_Outlet] = geompy.ExtractShapes(Extrusion_Domain, geompy.ShapeType["FACE"], True)
  # Wing
  [Edge_Left_LS_LE,Edge_LE,Edge_LS_Middle,Edge_Right_LS_LE] = geompy.ExtractShapes(Face_LS_LE, geompy.ShapeType["EDGE"], True)
  [Edge_Left_US_LE,geomObj_1,Edge_US_Middle,Edge_Right_US_LE] = geompy.ExtractShapes(Face_UP_LE, geompy.ShapeType["EDGE"], True)
  [Edge_Left_LS_TE,geomObj_1,Edge_TE,Edge_Right_LS_TE] = geompy.ExtractShapes(Face_LS_TE, geompy.ShapeType["EDGE"], True)
  [Edge_Left_US_TE,geomObj_1,geomObj_2,Edge_Right_US_TE] = geompy.ExtractShapes(Face_US_TE, geompy.ShapeType["EDGE"], True)
  # Far field
  [Edge_Inlet_Left,Edge_Inlet_Down,Edge_Inlet_Up,Edge_Inlet_Right] = geompy.ExtractShapes(Face_Inlet, geompy.ShapeType["EDGE"], True)
  [geomObj_1,Edge_Bottom_Left,Edge_Bottom_Right,geomObj_2] = geompy.ExtractShapes(Face_Bottom, geompy.ShapeType["EDGE"], True)
  [geomObj_1,Edge_Top_Left,Edge_Top_Right,geomObj_2] = geompy.ExtractShapes(Face_Top, geompy.ShapeType["EDGE"], True)
  [Edge_Outlet_Left,Edge_Oulet_Down,Edge_Outlet_Top,Edge_Outlet_Right] = geompy.ExtractShapes(Face_Outlet, geompy.ShapeType["EDGE"], True)
elif Domain_Width > 4.9:
  [Face_Inlet,Face_LS_LE,Face_UP_LE,Face_Left,Face_Bottom,Face_Top,Face_LS_TE,Face_Right,Face_US_TE,Face_Outlet] = geompy.ExtractShapes(Extrusion_Domain, geompy.ShapeType["FACE"], True)
  # Wing
  [Edge_Left_LS_LE,Edge_LE,Edge_Right_LS_LE,Edge_LS_Middle] = geompy.ExtractShapes(Face_LS_LE, geompy.ShapeType["EDGE"], True)
  [Edge_Left_US_LE,geomObj_1,Edge_Right_US_LE,Edge_US_Middle] = geompy.ExtractShapes(Face_UP_LE, geompy.ShapeType["EDGE"], True)
  [geomObj_1,Edge_Left_LS_TE,Edge_Right_LS_TE,Edge_TE] = geompy.ExtractShapes(Face_LS_TE, geompy.ShapeType["EDGE"], True)
  [Edge_Left_US_TE,geomObj_1,geomObj_2,Edge_Right_US_TE] = geompy.ExtractShapes(Face_US_TE, geompy.ShapeType["EDGE"], True)
  # Far field
  [Edge_Inlet_Left,Edge_Inlet_Down,Edge_Inlet_Up,Edge_Inlet_Right] = geompy.ExtractShapes(Face_Inlet, geompy.ShapeType["EDGE"], True)
  [geomObj_1,Edge_Bottom_Left,Edge_Bottom_Right,geomObj_2] = geompy.ExtractShapes(Face_Bottom, geompy.ShapeType["EDGE"], True)
  [geomObj_1,Edge_Top_Left,Edge_Top_Right,geomObj_2] = geompy.ExtractShapes(Face_Top, geompy.ShapeType["EDGE"], True)
  [Edge_Outlet_Left,Edge_Oulet_Down,Edge_Outlet_Top,Edge_Outlet_Right] = geompy.ExtractShapes(Face_Outlet, geompy.ShapeType["EDGE"], True)
elif Domain_Width > 0.9:
  [Face_Inlet,Face_LS_LE,Face_UP_LE,Face_Left,Face_Bottom,Face_Top,Face_Right,Face_LS_TE,Face_US_TE,Face_Outlet] = geompy.ExtractShapes(Extrusion_Domain, geompy.ShapeType["FACE"], True)
  # Wing
  [Edge_LE,Edge_Left_LS_LE,Edge_Right_LS_LE,Edge_LS_Middle] = geompy.ExtractShapes(Face_LS_LE, geompy.ShapeType["EDGE"], True)
  [geomObj_1,Edge_Left_US_LE,Edge_Right_US_LE,Edge_US_Middle] = geompy.ExtractShapes(Face_UP_LE, geompy.ShapeType["EDGE"], True)
  [geomObj_1,Edge_Left_LS_TE,Edge_Right_LS_TE,Edge_TE] = geompy.ExtractShapes(Face_LS_TE, geompy.ShapeType["EDGE"], True)
  [geomObj_1,Edge_Left_US_TE,Edge_Right_US_TE,geomObj_2] = geompy.ExtractShapes(Face_US_TE, geompy.ShapeType["EDGE"], True)
  # Far field
  [Edge_Inlet_Left,Edge_Inlet_Down,Edge_Inlet_Up,Edge_Inlet_Right] = geompy.ExtractShapes(Face_Inlet, geompy.ShapeType["EDGE"], True)
  [geomObj_1,Edge_Bottom_Left,Edge_Bottom_Right,geomObj_2] = geompy.ExtractShapes(Face_Bottom, geompy.ShapeType["EDGE"], True)
  [geomObj_1,Edge_Top_Left,Edge_Top_Right,geomObj_2] = geompy.ExtractShapes(Face_Top, geompy.ShapeType["EDGE"], True)
  [Edge_Outlet_Left,Edge_Oulet_Down,Edge_Outlet_Top,Edge_Outlet_Right] = geompy.ExtractShapes(Face_Outlet, geompy.ShapeType["EDGE"], True)
else:
  [Face_Inlet,Face_LS_LE,Face_UP_LE,Face_Bottom,Face_Left,Face_Right,Face_Top,Face_LS_TE,Face_US_TE,Face_Outlet] = geompy.ExtractShapes(Extrusion_Domain, geompy.ShapeType["FACE"], True)
  # Wing
  [Edge_LE,Edge_Left_LS_LE,Edge_Right_LS_LE,Edge_LS_Middle] = geompy.ExtractShapes(Face_LS_LE, geompy.ShapeType["EDGE"], True)
  [geomObj_1,Edge_Left_US_LE,Edge_Right_US_LE,Edge_US_Middle] = geompy.ExtractShapes(Face_UP_LE, geompy.ShapeType["EDGE"], True)
  [geomObj_1,Edge_Left_LS_TE,Edge_Right_LS_TE,Edge_TE] = geompy.ExtractShapes(Face_LS_TE, geompy.ShapeType["EDGE"], True)
  [geomObj_1,Edge_Left_US_TE,Edge_Right_US_TE,geomObj_2] = geompy.ExtractShapes(Face_US_TE, geompy.ShapeType["EDGE"], True)
  # Far field
  [Edge_Inlet_Down,Edge_Inlet_Left,Edge_Inlet_Right,Edge_Inlet_Up] = geompy.ExtractShapes(Face_Inlet, geompy.ShapeType["EDGE"], True)
  [geomObj_1,Edge_Bottom_Left,Edge_Bottom_Right,geomObj_2] = geompy.ExtractShapes(Face_Bottom, geompy.ShapeType["EDGE"], True)
  [geomObj_1,Edge_Top_Left,Edge_Top_Right,geomObj_2] = geompy.ExtractShapes(Face_Top, geompy.ShapeType["EDGE"], True)
  [Edge_Oulet_Down,Edge_Outlet_Left,Edge_Outlet_Right,Edge_Outlet_Top] = geompy.ExtractShapes(Face_Outlet, geompy.ShapeType["EDGE"], True)


Auto_group_for_Sub_mesh_Wing = geompy.CreateGroup(Extrusion_Domain, geompy.ShapeType["FACE"])
geompy.UnionList(Auto_group_for_Sub_mesh_Wing, [Face_LS_LE, Face_UP_LE, Face_LS_TE, Face_US_TE])
Auto_group_for_Sub_mesh_FarField = geompy.CreateGroup(Extrusion_Domain, geompy.ShapeType["FACE"])
geompy.UnionList(Auto_group_for_Sub_mesh_FarField, [Face_Inlet, Face_Left, Face_Bottom, Face_Top, Face_Right, Face_Outlet])

Auto_group_for_Sub_mesh_FarFieldEdges = geompy.CreateGroup(Extrusion_Domain, geompy.ShapeType["EDGE"])
geompy.UnionList(Auto_group_for_Sub_mesh_FarFieldEdges, [Edge_Inlet_Left, Edge_Inlet_Right, Edge_Bottom_Left, Edge_Bottom_Right, Edge_Top_Left, Edge_Top_Right, Edge_Outlet_Left, Edge_Outlet_Right])
Auto_group_for_Sub_mesh_FarFieldWidth = geompy.CreateGroup(Extrusion_Domain, geompy.ShapeType["EDGE"])
geompy.UnionList(Auto_group_for_Sub_mesh_FarFieldWidth, [Edge_Inlet_Down, Edge_Inlet_Up, Edge_Oulet_Down, Edge_Outlet_Top])

Auto_group_for_Sub_mesh_LE_Airfoils = geompy.CreateGroup(Extrusion_Domain, geompy.ShapeType["EDGE"])
geompy.UnionList(Auto_group_for_Sub_mesh_LE_Airfoils, [Edge_Left_LS_LE, Edge_Right_LS_LE, Edge_Left_US_LE, Edge_Right_US_LE])
Auto_group_for_Sub_mesh_TE_Airfoils = geompy.CreateGroup(Extrusion_Domain, geompy.ShapeType["EDGE"])
geompy.UnionList(Auto_group_for_Sub_mesh_TE_Airfoils, [Edge_Left_LS_TE, Edge_Right_LS_TE, Edge_Left_US_TE, Edge_Right_US_TE])
Auto_group_for_Sub_mesh_MiddleEdges = geompy.CreateGroup(Extrusion_Domain, geompy.ShapeType["EDGE"])
geompy.UnionList(Auto_group_for_Sub_mesh_MiddleEdges, [Edge_LS_Middle, Edge_US_Middle])

# Generate wake
Vector_Wake_Direction = geompy.MakeVectorDXDYDZ(1, 0, 0)
Extrusion_Wake = geompy.MakePrismVecH(Edge_TE, Vector_Wake_Direction, Domain_Length*0.5)

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
NETGEN_3D_Parameters_1.SetGrowthRate( Growth_Rate_Domain )
NETGEN_3D_Parameters_1.SetNbSegPerEdge( 6.92034e-310 )
NETGEN_3D_Parameters_1.SetNbSegPerRadius( 1.47958e-316 )
NETGEN_3D_Parameters_1.SetMinSize( Airfoil_Mesh_Size )
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

# Set Airfoils
Regular_1D_5 = Mesh_Domain.Segment(geom=Auto_group_for_Sub_mesh_MiddleEdges)
Local_Length_Width2 = Regular_1D_5.LocalLength(Biggest_Airfoil_Mesh_Size,None,1e-07)

Regular_1D_6 = Mesh_Domain.Segment(geom=Auto_group_for_Sub_mesh_LE_Airfoils)
Start_and_End_Length_LE = Regular_1D_6.StartEndLength(Airfoil_Mesh_Size,Biggest_Airfoil_Mesh_Size,[])
Start_and_End_Length_LE.SetObjectEntry( 'Extrusion_Domain' )
Regular_1D_7 = Mesh_Domain.Segment(geom=Auto_group_for_Sub_mesh_TE_Airfoils)
Start_and_End_Length_TE = Regular_1D_7.StartEndLength(Biggest_Airfoil_Mesh_Size,Airfoil_Mesh_Size,[])
Start_and_End_Length_TE.SetObjectEntry( 'Extrusion_Domain' )

# Far Field edges
Regular_1D_2 = Mesh_Domain.Segment(geom=Auto_group_for_Sub_mesh_FarFieldEdges)
Local_Length_FarField = Regular_1D_2.LocalLength(Far_Field_Mesh_Size,None,1e-07)
Regular_1D_3 = Mesh_Domain.Segment(geom=Auto_group_for_Sub_mesh_FarFieldWidth)
Local_Length_Width = Regular_1D_3.LocalLength(Domain_Width,None,1e-07)

# Set Wing
#NETGEN_1D_2D = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_1D2D,geom=Auto_group_for_Sub_mesh_Wing)
NETGEN_1D_2D = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_2D,geom=Auto_group_for_Sub_mesh_Wing)
Sub_mesh_Wing = NETGEN_1D_2D.GetSubMesh()
NETGEN_2D_Parameters_Wing = NETGEN_1D_2D.Parameters()
NETGEN_2D_Parameters_Wing.SetMaxSize( Biggest_Airfoil_Mesh_Size )
NETGEN_2D_Parameters_Wing.SetSecondOrder( 0 )
NETGEN_2D_Parameters_Wing.SetOptimize( 1 )
NETGEN_2D_Parameters_Wing.SetFineness( 5 )
NETGEN_2D_Parameters_Wing.SetGrowthRate( Growth_Rate_Wing )
NETGEN_2D_Parameters_Wing.SetNbSegPerEdge( 3 )
NETGEN_2D_Parameters_Wing.SetNbSegPerRadius( 5 )
NETGEN_2D_Parameters_Wing.SetMinSize( Airfoil_Mesh_Size )
NETGEN_2D_Parameters_Wing.SetUseSurfaceCurvature( 1 )
NETGEN_2D_Parameters_Wing.SetFuseEdges( 1 )
NETGEN_2D_Parameters_Wing.SetQuadAllowed( 0 )

# Set Far field
#NETGEN_1D_2D_1 = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_1D2D,geom=Auto_group_for_Sub_mesh_FarField)
NETGEN_1D_2D_1 = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_2D,geom=Auto_group_for_Sub_mesh_FarField)
Sub_mesh_FarField = NETGEN_1D_2D_1.GetSubMesh()
NETGEN_2D_Parameters_FarField = NETGEN_1D_2D_1.Parameters()
NETGEN_2D_Parameters_FarField.SetMaxSize( Far_Field_Mesh_Size )
NETGEN_2D_Parameters_FarField.SetSecondOrder( 0 )
NETGEN_2D_Parameters_FarField.SetOptimize( 1 )
NETGEN_2D_Parameters_FarField.SetFineness( 5 )
NETGEN_2D_Parameters_FarField.SetGrowthRate( Growth_Rate_Far_Field )
NETGEN_2D_Parameters_FarField.SetNbSegPerEdge( 1 )
NETGEN_2D_Parameters_FarField.SetNbSegPerRadius( 2 )
NETGEN_2D_Parameters_FarField.SetMinSize( Airfoil_Mesh_Size )
NETGEN_2D_Parameters_FarField.SetUseSurfaceCurvature( 1 )
NETGEN_2D_Parameters_FarField.SetFuseEdges( 1 )
NETGEN_2D_Parameters_FarField.SetQuadAllowed( 0 )
isDone = Mesh_Domain.SetMeshOrder( [ [ Sub_mesh_Wing, Sub_mesh_FarField ] ])

print(' Starting meshing ')
start_time = time.time()
# Compute mesh
isDone = Mesh_Domain.Compute()
exe_time = time.time() - start_time
NumberOfNodes = Mesh_Domain.NbNodes()
NumberOfElements = Mesh_Domain.NbTetras()
print(' Mesh execution tool ', str(round(exe_time, 2)), ' sec')
print(' Information about volume mesh:')
print(' Number of nodes       :', NumberOfNodes)
print(' Number of elements    :', NumberOfElements)

# Export meshes into data files
try:
  Mesh_Domain.ExportDAT( script_path + '/salome_output/Mesh_Domain.dat' )
  pass
except:
  print 'ExportDAT() failed. Invalid file name?'
try:
  Mesh_Domain.ExportDAT( script_path + '/salome_output/Sub-mesh_TE.dat', Sub_mesh_TE )
  pass
except:
  print 'ExportPartToDAT() failed. Invalid file name?'
try:
  Mesh_Domain.ExportDAT( script_path + '/salome_output/Sub-mesh_Wing.dat', Sub_mesh_Wing )
  pass
except:
  print 'ExportPartToDAT() failed. Invalid file name?'
try:
  Mesh_Domain.ExportDAT( script_path + '/salome_output/Sub-mesh_FarField.dat', Sub_mesh_FarField )
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
  Mesh_Wake_Surface.ExportSTL( script_path + '/case/wake_stl.stl', 1 )
  pass
except:
  print 'ExportSTL() failed. Invalid file name?'

with open('case/results_3d.dat', 'a+') as file:
  file.write('\n{0:6.0f} {1:10.0f} {2:10.0e} {3:10.0e} {4:10.0e} {5:10.2f} {6:15.1e} {7:15.1e} {8:10.1f}'.format(
    AOA, Domain_Length, Domain_Width, Airfoil_Mesh_Size,Biggest_Airfoil_Mesh_Size, Growth_Rate_Wing,
    NumberOfNodes/1000.0, NumberOfElements/1000.0, exe_time/60.0))
  file.flush()