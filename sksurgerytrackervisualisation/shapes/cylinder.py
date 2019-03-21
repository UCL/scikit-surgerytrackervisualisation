# -*- coding: utf-8 -*-

"""
VTK pipeline to represent a surface model via a vtkPolyData.
"""

import os
import vtk
from vtk.util import numpy_support
import sksurgeryvtk.models.vtk_surface_model as vbs
import sksurgeryvtk.utils.matrix_utils as mu

# pylint: disable=no-member


class VTKCylinderModel(vbs.VTKSurfaceModel):
    """
    Class to create a VTK surface model of a cylinder.
    """
    def __init__(self, height, radius, colour, name, visibility=True, opacity=1.0):
        """
        Creates a new surface model.
        
        :param height: the height of the cylinder
        :param diameter: the radius of the cylinder
        :param name: a name for the model
        :param colour: (R,G,B) where each are floats [0-1]
        :param visibility: boolean, True|False
        :param opacity: float [0,1]
        """

        print ("calling super")
        super(VTKCylinderModel, self).__init__(None,colour, visibility, opacity)

        self.name = name

        print ("called super")
        cyl = vtk.vtkCylinderSource()
        cyl.SetResolution(88)
        cyl.SetRadius(radius)
        cyl.SetHeight(height)
        cyl.Update()
        self.source = cyl.GetOutput()
        
        #this is from super init, have to redo as we now have data
        self.normals = None
        if self.source.GetPointData().GetNormals() is None:
            self.normals = vtk.vtkPolyDataNormals()
            self.normals.SetInputData(self.source)
            self.normals.SetAutoOrientNormals(True)
            self.normals.SetFlipNormals(False)
        self.transform = vtk.vtkTransform()
        self.transform.Identity()
        self.transform_filter = vtk.vtkTransformPolyDataFilter()
        if self.normals is None:
            self.transform_filter.SetInputData(self.source)
        else:
            self.transform_filter.SetInputConnection(
                self.normals.GetOutputPort())
        self.transform_filter.SetTransform(self.transform)
        self.mapper = vtk.vtkPolyDataMapper()
        self.mapper.SetInputConnection(self.transform_filter.GetOutputPort())
        self.mapper.Update()
        self.actor.SetMapper(self.mapper)


        
