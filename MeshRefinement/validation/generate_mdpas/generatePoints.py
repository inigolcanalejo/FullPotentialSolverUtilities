# -*- coding: utf-8 -*-

###
### This file is generated automatically by SALOME v8.4.0 with dump python functionality
###

import sys
import salome

salome.salome_init()
theStudy = salome.myStudy

import salome_notebook
notebook = salome_notebook.NoteBook(theStudy)
#sys.path.insert( 0, r'/home/inigo/simulations/naca0012/07_salome/00_Model/tests')

###
### GEOM component
###

import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS


geompy = geomBuilder.New(theStudy)

O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)
points = []
number_of_steps = 100
delta = 2*math.pi / number_of_steps

#alpha = 0.0
beta = 0.0
for step in range(number_of_steps):
  # print('')
  # print('step = ', step)
  if beta > 2*math.pi:
    EnvironmentError
  elif beta < math.pi:
    alpha = math.pi * (1 - math.cos(beta)) * 0.5
    xi = 1 - math.cos(beta)
  else:
    alpha = math.pi * (3 - math.cos(beta - math.pi)) * 0.5
    xi = 3 - math.cos(beta)
  x = (1 + math.cos(alpha)) / 2
  #print('alpha = ', alpha*180/math.pi)
  #print('xi = ', xi)
  #print('x = ', x)
  if alpha < math.pi:
    y = 0.6*(0.2969*math.sqrt(x) - 0.1260*x - 0.3516*x**2 + 0.2843*x**3 - 0.1036*x**4)
  else:
    y = -0.6*(0.2969*math.sqrt(x) - 0.1260*x - 0.3516*x**2 + 0.2843*x**3 - 0.1036*x**4)
  #print('y = ', y)
  vertex = geompy.MakeVertex(x, y, 0)
  points.append(vertex)
  beta += delta
  geompy.addToStudy( vertex, 'vertex_'+str(step) )


Curve_Airfoil = geompy.MakePolyline(points, True, False)
# Airfoil_divided = geompy.DivideEdge(Airfoil, -1, 0.5, 1)
# [Edge_LowerSurface, Edge_UpperSurface] = geompy.ExtractShapes(Airfoil_divided, geompy.ShapeType["EDGE"], True)
# Edge_LowerSurface_divided = geompy.DivideEdge(Edge_LowerSurface, -1, 0.5, 1)
# Edge_UpperSurface_divided = geompy.DivideEdge(Edge_UpperSurface, -1, 0.5, 1)
# [Curve_LowerSurface_LE, Curve_LowerSurface_TE] = geompy.ExtractShapes(Edge_LowerSurface_divided, geompy.ShapeType["EDGE"], True)
# [Curve_UpperSurface_LE, Curve_UpperSurface_TE] = geompy.ExtractShapes(Edge_UpperSurface_divided, geompy.ShapeType["EDGE"], True)
Face_Airfoil = geompy.MakeFaceWires([Curve_Airfoil], 1)
geompy.TranslateDXDYDZ(Face_Airfoil, -0.5, 0, 0)
geompy.Rotate(Face_Airfoil, OZ, -5*math.pi/180.0)
Face_Domain = geompy.MakeFaceHW(100, 100, 1)
Cut_1 = geompy.MakeCutList(Face_Domain, [Face_Airfoil], True)
[Wire_Airfoil,Wire_FarField] = geompy.ExtractShapes(Cut_1, geompy.ShapeType["WIRE"], True)
geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )
geompy.addToStudy( Curve_Airfoil, 'Curve_Airfoil' )
# geompy.addToStudy( Face_Domain, 'Face_Domain' )
# geompy.addToStudy( Face_Airfoil, 'Face_Airfoil' )
# geompy.addToStudy( Cut_1, 'Cut_1' )
# geompy.addToStudyInFather( Cut_1, Wire_FarField, 'Wire_FarField' )
# geompy.addToStudyInFather( Cut_1, Wire_Airfoil, 'Wire_Airfoil' )

###
### SMESH component
###

import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder

smesh = smeshBuilder.New(theStudy)

# Set NETGEN
Mesh_Domain = smesh.Mesh(Cut_1)
NETGEN_2D = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_2D)
NETGEN_2D_Parameters_1 = NETGEN_2D.Parameters()
NETGEN_2D_Parameters_1.SetMaxSize( 2.0 )
NETGEN_2D_Parameters_1.SetOptimize( 1 )
NETGEN_2D_Parameters_1.SetFineness( 5 )
NETGEN_2D_Parameters_1.SetGrowthRate( 0.05 )
NETGEN_2D_Parameters_1.SetNbSegPerEdge( 3 )
NETGEN_2D_Parameters_1.SetNbSegPerRadius( 5 )
NETGEN_2D_Parameters_1.SetMinSize( 1e-08 )
NETGEN_2D_Parameters_1.SetUseSurfaceCurvature( 1 )
NETGEN_2D_Parameters_1.SetQuadAllowed( 0 )
NETGEN_2D_Parameters_1.SetSecondOrder( 0 )
NETGEN_2D_Parameters_1.SetFuseEdges( 1 )

# Set submeshes
Regular_1D = Mesh_Domain.Segment(geom=Wire_FarField)
Local_Length_Farfield = Regular_1D.LocalLength(2,None,1e-07)

Regular_1D_1 = Mesh_Domain.Segment(geom=Wire_Airfoil)
Number_of_Segments_Airfoil = Regular_1D_1.NumberOfSegments(1)

isDone = Mesh_Domain.Compute()
Sub_mesh_Farfield = Regular_1D.GetSubMesh()
Sub_mesh_Airfoil = Regular_1D_1.GetSubMesh()


## Set names of Mesh objects
smesh.SetName(NETGEN_2D.GetAlgorithm(), 'NETGEN 2D')
smesh.SetName(Regular_1D.GetAlgorithm(), 'Regular_1D')
smesh.SetName(Local_Length_Farfield, 'Local Length_Farfield')
smesh.SetName(Number_of_Segments_Airfoil, 'Number of Segments_Airfoil')
smesh.SetName(NETGEN_2D_Parameters_1, 'NETGEN 2D Parameters_1')
smesh.SetName(Mesh_Domain.GetMesh(), 'Mesh_Domain')
smesh.SetName(Sub_mesh_Farfield, 'Sub-mesh_Farfield')
smesh.SetName(Sub_mesh_Airfoil, 'Sub-mesh_Airfoil')

salome.myStudyManager.SaveAs("/home/inigo/simulations/naca0012/07_salome/00_Model/tests/Study3.hdf", salome.myStudy, 0)




if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser(True)
