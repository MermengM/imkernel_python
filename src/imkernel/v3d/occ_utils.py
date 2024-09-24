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


def shape_to_obj(shape: TopoDS_Shape):
    # 创建固定的临时目录
    temp_dir = os.path.join(tempfile.gettempdir(), 'imkernel', 'occ_temp')
    os.makedirs(temp_dir, exist_ok=True)

    # 设置固定的文件名
    file_name = os.path.join(temp_dir, 'shape_to_obj_temp.obj')

    # 如果文件已存在，先删除
    if os.path.exists(file_name):
        os.remove(file_name)
    # 构建 Doc
    doc = TDocStd_Document("")
    shape_tool = XCAFDoc_DocumentTool.ShapeTool(doc.Main())

    # 构建网格形状
    breptools.Clean(shape)
    msh_algo = BRepMesh_IncrementalMesh(shape, True)
    msh_algo.Perform()

    shape_tool.AddShape(shape)

    # 元数据
    a_file_info = TColStd_IndexedDataMapOfStringString()

    rwobj_writer = RWObj_CafWriter(file_name)

    # apply a scale factor of 0.001 to mimic conversion from m to mm
    # 单位转换从 m 到 mm
    csc = rwobj_writer.ChangeCoordinateSystemConverter()
    system_unit_factor = unitsmethods.GetCasCadeLengthUnit() * 0.001
    csc.SetInputLengthUnit(system_unit_factor)
    csc.SetOutputLengthUnit(system_unit_factor)
    csc.SetInputCoordinateSystem(RWMesh_CoordinateSystem_posYfwd_posZup)
    csc.SetOutputCoordinateSystem(RWMesh_CoordinateSystem_negZfwd_posYup)

    rwobj_writer.SetCoordinateSystemConverter(csc)

    rwobj_writer.Perform(doc, a_file_info, Message_ProgressRange())
    # 检查文件是否成功创建
    if os.path.exists(file_name) and os.path.getsize(file_name) > 0:
        logger.success(f"导出成功：{file_name}")
        return file_name
    else:
        logger.error(f"导出失败：{file_name}")
        return None


if __name__ == "__main__":
    # 创建一个简单的盒子 shape
    box = BRepPrimAPI_MakeBox(gp_Pnt(0, 0, 0), 100, 60, 40).Shape()
    shape_to_obj(box)
