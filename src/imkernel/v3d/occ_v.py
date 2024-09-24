import os
import tempfile

from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.gp import gp_Pnt
from loguru import logger

# OCC
from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
from OCC.Core.BRepTools import breptools
from OCC.Core.Message import Message_ProgressRange
from OCC.Core.RWMesh import (
    RWMesh_CoordinateSystem_negZfwd_posYup,
    RWMesh_CoordinateSystem_posYfwd_posZup,
)
from OCC.Core.RWObj import RWObj_CafWriter
from OCC.Core.TColStd import TColStd_IndexedDataMapOfStringString
from OCC.Core.TDocStd import TDocStd_Document
from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.UnitsMethods import unitsmethods
from OCC.Core.XCAFDoc import XCAFDoc_DocumentTool

from imkernel.v3d.occ_utils import shape_to_obj
from imkernel.v3d.vtk_utils import showObjFromFile


def show_occ_shape(shape: TopoDS_Shape):
    # box = BRepPrimAPI_MakeBox(gp_Pnt(0, 0, 0), 100, 60, 40).Shape()
    obj_file_path = shape_to_obj(shape)
    if not obj_file_path:
        raise Exception("obj生成失败")
    showObjFromFile(obj_file_path)
