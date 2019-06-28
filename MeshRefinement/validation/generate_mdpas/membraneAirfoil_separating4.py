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
sys.path.insert( 0, r'/home/inigo/simulations/membranAirfoil/salome')

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
cad_model_moved_collapsed_igs_1 = geompy.ImportIGES("/home/inigo/simulations/membranAirfoil/cad_model_scaled_moved_collapsed.gid/cad_model_moved_collapsed.igs")
Face_Airfoil = geompy.MakeFaceWires([cad_model_moved_collapsed_igs_1], 1)
geompy.Rotate(Face_Airfoil, OZ, -5*math.pi/180.0)
Face_Domain = geompy.MakeFaceHW(25, 25, 1)
Cut_Domain = geompy.MakeCutList(Face_Domain, [Face_Airfoil], True)
[Inlet,Wall_Down,Lower_LE,Upper_LE,Lower_Middle,Upper_Middle,Lower_TE,Upper_TE,Wall_Up,Outlet] = geompy.ExtractShapes(Cut_Domain, geompy.ShapeType["EDGE"], True)
Group_FarField = geompy.CreateGroup(Cut_Domain, geompy.ShapeType["EDGE"])
geompy.UnionList(Group_FarField, [Inlet, Wall_Down, Wall_Up, Outlet])
Auto_group_for_Sub_mesh_1 = geompy.CreateGroup(Cut_Domain, geompy.ShapeType["EDGE"])
geompy.UnionList(Auto_group_for_Sub_mesh_1, [Upper_LE, Lower_TE])
Auto_group_for_Sub_mesh_2 = geompy.CreateGroup(Cut_Domain, geompy.ShapeType["EDGE"])
geompy.UnionList(Auto_group_for_Sub_mesh_2, [Lower_LE, Upper_TE])
Auto_group_for_Sub_mesh_3 = geompy.CreateGroup(Cut_Domain, geompy.ShapeType["EDGE"])
geompy.UnionList(Auto_group_for_Sub_mesh_3, [Lower_Middle, Upper_Middle])
geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )
geompy.addToStudy( cad_model_moved_collapsed_igs_1, 'cad_model_moved_collapsed.igs_1' )
geompy.addToStudy( Face_Airfoil, 'Face_Airfoil' )
geompy.addToStudy( Face_Domain, 'Face_Domain' )
geompy.addToStudy( Cut_Domain, 'Cut_Domain' )
geompy.addToStudyInFather( Cut_Domain, Inlet, 'Inlet' )
geompy.addToStudyInFather( Cut_Domain, Wall_Down, 'Wall_Down' )
geompy.addToStudyInFather( Cut_Domain, Lower_LE, 'Lower_LE' )
geompy.addToStudyInFather( Cut_Domain, Upper_LE, 'Upper_LE' )
geompy.addToStudyInFather( Cut_Domain, Lower_Middle, 'Lower_Middle' )
geompy.addToStudyInFather( Cut_Domain, Upper_Middle, 'Upper_Middle' )
geompy.addToStudyInFather( Cut_Domain, Lower_TE, 'Lower_TE' )
geompy.addToStudyInFather( Cut_Domain, Upper_TE, 'Upper_TE' )
geompy.addToStudyInFather( Cut_Domain, Wall_Up, 'Wall_Up' )
geompy.addToStudyInFather( Cut_Domain, Outlet, 'Outlet' )
geompy.addToStudyInFather( Cut_Domain, Group_FarField, 'Group_FarField' )
geompy.addToStudyInFather( Cut_Domain, Auto_group_for_Sub_mesh_1, 'Auto_group_for_Sub-mesh_1' )
geompy.addToStudyInFather( Cut_Domain, Auto_group_for_Sub_mesh_2, 'Auto_group_for_Sub-mesh_2' )
geompy.addToStudyInFather( Cut_Domain, Auto_group_for_Sub_mesh_3, 'Auto_group_for_Sub-mesh_3' )

###
### SMESH component
###

import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder

smesh = smeshBuilder.New(theStudy)
Mesh_Domain = smesh.Mesh(Cut_Domain)
NETGEN_1D_2D = Mesh_Domain.Triangle(algo=smeshBuilder.NETGEN_1D2D)
NETGEN_2D_Parameters_1 = NETGEN_1D_2D.Parameters()
NETGEN_2D_Parameters_1.SetMaxSize( 1 )
NETGEN_2D_Parameters_1.SetSecondOrder( 0 )
NETGEN_2D_Parameters_1.SetOptimize( 1 )
NETGEN_2D_Parameters_1.SetFineness( 5 )
NETGEN_2D_Parameters_1.SetGrowthRate( 0.1 )
NETGEN_2D_Parameters_1.SetNbSegPerEdge( 3 )
NETGEN_2D_Parameters_1.SetNbSegPerRadius( 5 )
NETGEN_2D_Parameters_1.SetMinSize( 1e-10 )
NETGEN_2D_Parameters_1.SetUseSurfaceCurvature( 1 )
NETGEN_2D_Parameters_1.SetFuseEdges( 1 )
NETGEN_2D_Parameters_1.SetQuadAllowed( 0 )
Regular_1D = Mesh_Domain.Segment(geom=Group_FarField)
FarField_Mesh = Regular_1D.GetSubMesh()
Local_Length_FarField = Regular_1D.LocalLength(1,None,1e-07)
Start_and_End_Length_BigToSmall = smesh.CreateHypothesis('StartEndLength')
Start_and_End_Length_BigToSmall.SetStartLength( 0.0001 )
Start_and_End_Length_BigToSmall.SetEndLength( 0.001 )
Start_and_End_Length_BigToSmall.SetReversedEdges( [] )
Start_and_End_Length_BigToSmall.SetObjectEntry( 'Upper_LE' )
Regular_1D_1 = Mesh_Domain.Segment(geom=Auto_group_for_Sub_mesh_1)
Sub_mesh_1 = Regular_1D_1.GetSubMesh()
Start_and_End_Length_BigToSmall_1 = Regular_1D_1.StartEndLength(0.001,0.0001,[])
Start_and_End_Length_BigToSmall_1.SetObjectEntry( 'Cut_Domain' )
Regular_1D_2 = Mesh_Domain.Segment(geom=Auto_group_for_Sub_mesh_2)
Sub_mesh_2 = Regular_1D_2.GetSubMesh()
Start_and_End_Length_SmallToBig = Regular_1D_2.StartEndLength(0.0001,0.001,[])
Start_and_End_Length_SmallToBig.SetObjectEntry( 'Cut_Domain' )
Regular_1D_3 = Mesh_Domain.Segment(geom=Auto_group_for_Sub_mesh_3)
Sub_mesh_3 = Regular_1D_3.GetSubMesh()
Local_Length_Middle = Regular_1D_3.LocalLength(0.001,None,1e-07)
isDone = Mesh_Domain.Compute()
Compound_Mesh_Airfoil = smesh.Concatenate([Sub_mesh_1, Sub_mesh_2, Sub_mesh_3], 1, 1, 1e-05)
try:
  Mesh_Domain.ExportDAT( r'/home/inigo/simulations/membranAirfoil/salome/dat_files/FarField_Mesh.dat', FarField_Mesh )
  pass
except:
  print 'ExportPartToDAT() failed. Invalid file name?'
try:
  Compound_Mesh_Airfoil.ExportDAT( r'/home/inigo/simulations/membranAirfoil/salome/dat_files/Compound_Mesh_Airfoil.dat' )
  pass
except:
  print 'ExportDAT() failed. Invalid file name?'
try:
  Mesh_Domain.ExportDAT( r'/home/inigo/simulations/membranAirfoil/salome/dat_files/Mesh_Domain.dat' )
  pass
except:
  print 'ExportDAT() failed. Invalid file name?'


## Set names of Mesh objects
smesh.SetName(NETGEN_1D_2D.GetAlgorithm(), 'NETGEN 1D-2D')
smesh.SetName(Regular_1D.GetAlgorithm(), 'Regular_1D')
smesh.SetName(Local_Length_FarField, 'Local Length_FarField')
smesh.SetName(Start_and_End_Length_BigToSmall, 'Start and End Length_BigToSmall')
smesh.SetName(NETGEN_2D_Parameters_1, 'NETGEN 2D Parameters_1')
smesh.SetName(Local_Length_Middle, 'Local Length_Middle')
smesh.SetName(Start_and_End_Length_BigToSmall_1, 'Start and End Length_BigToSmall')
smesh.SetName(Start_and_End_Length_SmallToBig, 'Start and End Length_SmallToBig')
smesh.SetName(Mesh_Domain.GetMesh(), 'Mesh_Domain')
smesh.SetName(Compound_Mesh_Airfoil.GetMesh(), 'Compound_Mesh_Airfoil')
smesh.SetName(Sub_mesh_2, 'Sub-mesh_2')
smesh.SetName(Sub_mesh_1, 'Sub-mesh_1')
smesh.SetName(FarField_Mesh, 'FarField_Mesh')
smesh.SetName(Sub_mesh_3, 'Sub-mesh_3')


if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser(True)
