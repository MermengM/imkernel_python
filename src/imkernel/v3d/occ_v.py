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
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.IFSelect import IFSelect_RetDone
from imkernel.v3d.occ_utils import shape_to_obj
from imkernel.v3d.vtk_utils import show_obj


def show_occ_shape(shape: TopoDS_Shape):
    # box = BRepPrimAPI_MakeBox(gp_Pnt(0, 0, 0), 100, 60, 40).Shape()
    obj_file_path = shape_to_obj(shape)
    if not obj_file_path:
        raise Exception("obj生成失败")
    show_obj(obj_file_path)


def show_stp_shape(stp_file_path: str):
    # 生成一个 step 模型类
    reader = STEPControl_Reader()
    # 加载一个文件并且返回一个状态枚举值
    status = reader.ReadFile(stp_file_path)
    # 如果正常执行且有模型
    try:
        if status == IFSelect_RetDone:  # check status
            # 执行步骤文件转换
            ok = reader.TransferRoot(1)
            # 返回转换后的形状
            shape = reader.Shape(1)
        else:
            print(f"文件{stp_file_path}加载失败，返回测试 Shape")
            shape = BRepPrimAPI_MakeBox(1, 1, 1).Shape()
        show_occ_shape(shape)
    except Exception as e:
        print(f"{e} 文件{stp_file_path}加载失败")
