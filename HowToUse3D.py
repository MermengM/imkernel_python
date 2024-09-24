from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.gp import gp_Pnt
from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_FACE
from OCC.Core.TopoDS import topods_Face
from OCC.Core.BRep import BRep_Tool

import vtk
from vtk.util.numpy_support import numpy_to_vtk

import numpy as np

# 创建一个简单的盒子 shape
box = BRepPrimAPI_MakeBox(gp_Pnt(0, 0, 0), 100, 60, 40).Shape()

# 创建网格
mesh = BRepMesh_IncrementalMesh(box, 0.1)
mesh.Perform()

# 创建 VTK 数据结构
points = vtk.vtkPoints()
polygons = vtk.vtkCellArray()

# 遍历所有面
explorer = TopExp_Explorer(box, TopAbs_FACE)
while explorer.More():
    face = topods_Face(explorer.Current())
    location = vtk.vtkTransform()
    facing = BRep_Tool.Triangulation(face, location)

    if facing is not None:
        tab = facing.Nodes()
        tri = facing.Triangles()
        for i in range(1, facing.NbTriangles() + 1):
            trian = tri.Value(i)
            for j in range(1, 4):
                pnt = tab.Value(trian.Value(j))
                points.InsertNextPoint(pnt.X(), pnt.Y(), pnt.Z())
            polygon = vtk.vtkTriangle()
            polygon.GetPointIds().SetId(0, 3 * (i - 1))
            polygon.GetPointIds().SetId(1, 3 * (i - 1) + 1)
            polygon.GetPointIds().SetId(2, 3 * (i - 1) + 2)
            polygons.InsertNextCell(polygon)
    explorer.Next()

# 创建 PolyData
polydata = vtk.vtkPolyData()
polydata.SetPoints(points)
polydata.SetPolys(polygons)

# 创建 Mapper
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputData(polydata)

# 创建 Actor
actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(0.3, 0.5, 0.8)  # 设置颜色为蓝色

# 创建 Renderer
renderer = vtk.vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(1, 1, 1)  # 设置背景为白色

# 创建 RenderWindow
render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(600, 400)  # 设置窗口大小

# 创建 RenderWindowInteractor
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# 初始化并开始交互
interactor.Initialize()
render_window.Render()

# 在 Jupyter 中显示
from IPython.display import Image
import tempfile

# 将渲染结果保存为图像
_, temp_file = tempfile.mkstemp(suffix='.png')
vtk.vtkWindowToImageFilter().SetInput(render_window).Update()
vtk.vtkPNGWriter().SetFileName(temp_file).SetInputConnection(vtk.vtkWindowToImageFilter().GetOutputPort()).Write()

# 显示图像
Image(filename=temp_file)
