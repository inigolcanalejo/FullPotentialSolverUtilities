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

# Create origin and axis
O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)

# Read cad file
cad_model_moved_collapsed_igs_1 = geompy.ImportIGES("/home/inigo/simulations/membranAirfoil/cad_model_scaled_moved_collapsed.gid/cad_model_moved_collapsed.igs")

# Create airfoil face
Face_Airfoil = geompy.MakeFaceWires([cad_model_moved_collapsed_igs_1], 1)

# Rotate around center to AOA
geompy.Rotate(Face_Airfoil, OZ, -5*math.pi/180.0)

# Create domain
Face_Domain = geompy.MakePlane(O, OZ, 25)

# Cut the airfoil from the domain
Cut_1 = geompy.MakeCutList(Face_Domain, [Face_Airfoil], True)

# Explode edges
[Wire_Far_Field,Wire_Airfoil] = geompy.ExtractShapes(Cut_1, geompy.ShapeType["WIRE"], True)
[Lower_Front,Upper_Front,Lower_Middle,Upper_Middle] = geompy.ExtractShapes(Wire_Far_Field, geompy.ShapeType["EDGE"], True)
[Lower_Front,Upper_Front,Lower_Middle,Upper_Middle,Lower_Back,Upper_Back] = geompy.ExtractShapes(Wire_Airfoil, geompy.ShapeType["EDGE"], True)
Auto_group_for_Sub_mesh_1 = geompy.CreateGroup(Cut_1, geompy.ShapeType["EDGE"])
geompy.UnionList(Auto_group_for_Sub_mesh_1, [Lower_Middle, Upper_Middle])

# Add to study
geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )
geompy.addToStudy( cad_model_moved_collapsed_igs_1, 'cad_model_moved_collapsed.igs_1' )
geompy.addToStudy( Face_Airfoil, 'Face_Airfoil' )
geompy.addToStudy( Face_Domain, 'Face_Domain' )
geompy.addToStudy( Cut_1, 'Cut_1' )
geompy.addToStudyInFather( Cut_1, Wire_Far_Field, 'Wire_Far_Field' )
geompy.addToStudyInFather( Cut_1, Wire_Airfoil, 'Wire_Airfoil' )
geompy.addToStudyInFather( Wire_Airfoil, Lower_Front, 'Lower_Front' )
geompy.addToStudyInFather( Wire_Airfoil, Upper_Front, 'Upper_Front' )
geompy.addToStudyInFather( Wire_Airfoil, Lower_Middle, 'Lower_Middle' )
geompy.addToStudyInFather( Wire_Airfoil, Upper_Middle, 'Upper_Middle' )
geompy.addToStudyInFather( Wire_Airfoil, Lower_Back, 'Lower_Back' )
geompy.addToStudyInFather( Wire_Airfoil, Upper_Back, 'Upper_Back' )
geompy.addToStudyInFather( Cut_1, Auto_group_for_Sub_mesh_1, 'Auto_group_for_Sub-mesh_1' )

###
### SMESH component
###

import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder

smesh = smeshBuilder.New(theStudy)

# Set NETGEN
Mesh_1 = smesh.Mesh(Cut_1)
NETGEN_1D_2D = Mesh_1.Triangle(algo=smeshBuilder.NETGEN_1D2D)
NETGEN_2D_Parameters_1 = NETGEN_1D_2D.Parameters()
NETGEN_2D_Parameters_1.SetSecondOrder( 0 )
NETGEN_2D_Parameters_1.SetOptimize( 1 )
NETGEN_2D_Parameters_1.SetUseSurfaceCurvature( 1 )
NETGEN_2D_Parameters_1.SetFuseEdges( 1 )
NETGEN_2D_Parameters_1.SetQuadAllowed( 0 )

# Set submeshes
# Upper front
Regular_1D = Mesh_1.Segment(geom=Upper_Front)
status = Mesh_1.RemoveHypothesis(Regular_1D,Upper_Front)
#Mesh_1.GetMesh().RemoveSubMesh( smeshObj_1 ) ### smeshObj_1 has not been yet created
Regular_1D_1 = Mesh_1.Segment(geom=Upper_Front)

# Lower front
Start_and_End_Length_1 = Regular_1D.StartEndLength(0.001,0.0001,[])
Regular_1D_2 = Mesh_1.Segment(geom=Lower_Front)
Start_and_End_Length_2 = Regular_1D_2.StartEndLength(0.0001,0.001,[])

# Middle
Regular_1D_3 = Mesh_1.Segment(geom=Auto_group_for_Sub_mesh_1)
Middle_Length_1 = Regular_1D_3.LocalLength(0.001,None,1e-07)
Regular_1D_4 = Mesh_1.Segment(geom=Lower_Back)
status = Mesh_1.AddHypothesis(Start_and_End_Length_1,Lower_Back)
Regular_1D_5 = Mesh_1.Segment(geom=Upper_Back)
status = Mesh_1.AddHypothesis(Start_and_End_Length_2,Upper_Back)
Middle_Length_1.SetLength( 0.001 )
Middle_Length_1.SetPrecision( 1e-07 )
Regular_1D_6 = Mesh_1.Segment(geom=Wire_Far_Field)
FarField_Length_1 = Regular_1D_6.LocalLength(1,None,1e-07)
Start_and_End_Length_1.SetStartLength( 0.001 )
Start_and_End_Length_1.SetEndLength( 0.0001 )
Start_and_End_Length_1.SetReversedEdges( [] )
Start_and_End_Length_1.SetObjectEntry( 'Cut_1' )
Start_and_End_Length_2.SetStartLength( 0.0001 )
Start_and_End_Length_2.SetEndLength( 0.001 )
Start_and_End_Length_2.SetReversedEdges( [] )
Start_and_End_Length_2.SetObjectEntry( 'Cut_1' )
NETGEN_2D_Parameters_1.SetMaxSize( 1 )
NETGEN_2D_Parameters_1.SetFineness( 5 )
NETGEN_2D_Parameters_1.SetGrowthRate( 0.1 )
NETGEN_2D_Parameters_1.SetNbSegPerEdge( 3 )
NETGEN_2D_Parameters_1.SetNbSegPerRadius( 5 )
NETGEN_2D_Parameters_1.SetMinSize( 1e-10 )
isDone = Mesh_1.Compute()
Upper_Front_1 = Regular_1D_1.GetSubMesh()
Lower_Front_1 = Regular_1D_2.GetSubMesh()
Middle = Regular_1D_3.GetSubMesh()
Lower_Back_1 = Regular_1D_4.GetSubMesh()
Upper_Back_1 = Regular_1D_5.GetSubMesh()
Sub_mesh_1 = Regular_1D_6.GetSubMesh()


## Set names of Mesh objects
smesh.SetName(Sub_mesh_1, 'Sub-mesh_1')
smesh.SetName(NETGEN_2D_Parameters_1, 'NETGEN 2D Parameters_1')
smesh.SetName(Start_and_End_Length_1, 'Start and End Length_1')
smesh.SetName(Upper_Front_1, 'Upper_Front')
smesh.SetName(Start_and_End_Length_2, 'Start and End Length_2')
smesh.SetName(Regular_1D.GetAlgorithm(), 'Regular_1D')
smesh.SetName(Lower_Front_1, 'Lower_Front')
smesh.SetName(Middle_Length_1, 'Middle Length_1')
smesh.SetName(NETGEN_1D_2D.GetAlgorithm(), 'NETGEN 1D-2D')
smesh.SetName(FarField_Length_1, 'FarField_Length_1')
smesh.SetName(Lower_Back_1, 'Lower_Back')
smesh.SetName(Upper_Back_1, 'Upper_Back')
smesh.SetName(Mesh_1.GetMesh(), 'Mesh_1')
smesh.SetName(Middle, 'Middle')


if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser(True)
