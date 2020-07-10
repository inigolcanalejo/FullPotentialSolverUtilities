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

coordinates_file_name = 'airfoilCoordinates/k1.dat'

upper_points = []
lower_points = []

with open(coordinates_file_name, 'r') as coordinates_file:
    airfoil_name = coordinates_file.readline()
    coordinates_number = coordinates_file.readline()
    upper_surface_coord_number = int(coordinates_number.split()[0])
    lower_surface_coord_number = int(coordinates_number.split()[1])
    print('Airfoil: ', airfoil_name)
    print('Number of upper points: ',  upper_surface_coord_number)
    print('Number of lower points: ', lower_surface_coord_number)
    vertex_id = 0
    lower_surface = False
    empty_line = coordinates_file.readline()
    line = coordinates_file.readline()
    while line:
        if '0.' in line:
            x = float(line.split()[0])
            y = float(line.split()[1])
            vertex = geompy.MakeVertex(x, y, 0)

            # geompy.addToStudy( vertex, 'vertex_'+str(vertex_id) )
            vertex_id += 1
            if lower_surface:
                lower_points.append(vertex)
            else:
                upper_points.append(vertex)
        # Lower surface starts when empty line is reached
        if not line.strip():
            lower_surface = True
        line = coordinates_file.readline()

if len(upper_points) != upper_surface_coord_number or len(lower_points) != lower_surface_coord_number:
    print('Warning: number of points different than prescribed in input file:')
    print('Number of upper points (input): ',  upper_surface_coord_number)
    print('Number of upper points: ',  len(upper_points))
    print('Number of lower points (input): ', lower_surface_coord_number)
    print('Number of lower points: ', len(lower_points))

Upper_Airfoil = geompy.MakePolyline(upper_points, False)
Lower_Airfoil = geompy.MakePolyline(lower_points, False)

geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )
geompy.addToStudy( Upper_Airfoil, 'Upper_Airfoil' )
geompy.addToStudy( Lower_Airfoil, 'Lower_Airfoil' )

salome.myStudyManager.SaveAs("/home/inigo/simulations/naca0012/07_salome/00_model_read_points/readPoints.hdf", salome.myStudy, 0)




if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser(True)