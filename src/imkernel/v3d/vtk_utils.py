import re
import numpy as np
import pyvista as pv
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.gp import gp_Pnt
from vtk import vtkTransform
import datetime
import asyncio
from IPython.display import display, HTML, clear_output

pv.global_theme.trame.jupyter_extension_enabled = True
pv.set_jupyter_backend("client")


def showObjFromFile(file_path: str, color: str = None):
    """
    从Obj显示文件
    :param file_path:
    :param color:
    """

    # Set up the plotter

    # Read the OBJ file
    mesh = pv.read(file_path)

    # Create a plotter and add the mesh
    plotter = pv.Plotter()
    plotter.add_mesh(mesh, color=color)

    # Show the plot
    plotter.show()


def showPointsFromFile(file_path: str, color: str = None, handle_type: str = "txt"):
    """
    从文件显示点
    :param file_path:
    :param color:
    :param handle_type:
    """
    if handle_type == "txt":
        points_data = handle_txt(file_path)
    else:
        points_data = handle_cpt(file_path)

    plotter = pv.Plotter()
    plotter.add_points(points=points_data, color=color)
    plotter.show()


def showLineFromFile(file_path: str, color: str = None, line_width: float = 1.0, handle_type: str = "cpt"):
    if handle_type == "txt":
        line_data = handle_txt(file_path)
    else:
        line_data = handle_cpt(file_path)
    mesh = pv.MultipleLines(points=line_data)
    plotter = pv.Plotter()
    plotter.add_mesh(mesh, line_width=line_width, color=color)
    plotter.camera.azimuth = 45
    plotter.camera.zoom(0.8)
    plotter.show()


def showOneLineFromList(line_data_list, color: str = None, line_width: float = 1.0):
    plotter = pv.Plotter()
    points = []
    for oneXYZ in line_data_list:
        points.append([oneXYZ["x"], oneXYZ["y"], oneXYZ["z"]])
    line_data = np.array(points, dtype=np.float32)
    mesh = pv.MultipleLines(points=line_data)
    plotter.add_mesh(mesh, line_width=line_width, color=color)
    plotter.show()


def showMultiLineFromList(lines_data_list, color: str = None, line_width: float = 1.0):
    plotter = pv.Plotter()
    for oneLine in lines_data_list:
        line_data = np.array(oneLine, dtype=np.float32)
        mesh = pv.MultipleLines(points=line_data)
        plotter.add_mesh(mesh, line_width=line_width, color=color)
    plotter.show()


def showMultiLineFromListDict(lines_data_list, color: str = None, line_width: float = 1.0):
    plotter = pv.Plotter()
    for oneLine in lines_data_list:
        points = []
        for oneXYZ in oneLine:
            points.append([oneXYZ["x"], oneXYZ["y"], oneXYZ["z"]])
        line_data = np.array(points, dtype=np.float32)
        mesh = pv.MultipleLines(points=line_data)
        plotter.add_mesh(mesh, line_width=line_width, color=color)
    plotter.show()


def showModel(file_path: str, color: str = None):
    reader = pv.get_reader(file_path)
    mesh = reader.read()
    plotter = pv.Plotter()
    plotter.add_mesh(mesh, color=color)
    plotter.show()


def showAnimation(NC_file_path: str, file_paths: str = None, blade_file_path: str = None, output_path: str = None, pop_window=True):
    # 初始化 Plotter
    if pop_window:
        plotter = pv.Plotter()
    else:
        plotter = pv.Plotter(off_screen=True)

    # 定义文件路径和颜色
    if file_paths:
        pass
        # file_paths = [
        #     f"{machine_file_path}\\Mach_X_Axis_0.STL",
        #     f"{machine_file_path}\\Mach_Z_Axis_0.STL",
        #     f"{machine_file_path}\\Mach_Spindle_0.STL",
        #     f"{machine_file_path}\\Mach_Y_Axis_0.STL",
        #     f"{machine_file_path}\\Mach_B_Axis_0.STL",
        #     f"{machine_file_path}\\Mach_C_Axis_0.STL",
        # ]
    else:
        file_paths = [
            "machineModel\\Mach_X_Axis_0.STL",
            "machineModel\\Mach_Z_Axis_0.STL",
            "machineModel\\Mach_Spindle_0.STL",
            "machineModel\\Mach_Y_Axis_0.STL",
            "machineModel\\Mach_B_Axis_0.STL",
            "machineModel\\Mach_C_Axis_0.STL",
        ]
    colors = ["red", "orange", "yellow", "green", "blue", "purple"]
    # 创造actor list
    actors = []
    print(f"开始生成动画{datetime.datetime.now()}")
    # 添加机床模型
    for i, file_path in enumerate(file_paths):
        reader = pv.get_reader(file_path)
        mesh = reader.read()  # 读取机床模型
        actor = plotter.add_mesh(mesh, color=colors[i], opacity=0.7)  # 添加机床模型到plotter上，0.7表示模型的透明度
        actor.RotateX(90)
        actors.append(actor)

    # 单独添加叶片
    if not blade_file_path:
        print(f"blade_file_path{blade_file_path}不存在")
    else:
        reader = pv.get_reader(blade_file_path)
    blade = reader.read()
    actor_blade = plotter.add_mesh(blade)
    actor_blade.RotateX(180)  # 调整叶片的位置

    # 添加圆柱体模拟刀片
    cylinder = pv.Cylinder(center=(-224, 95, -290), direction=(0, 0, 1), radius=1.0, height=20.0)  # 数值为测试数值，是手动调节的位置等信息
    actor_addcylinder = plotter.add_mesh(cylinder)

    # 显示坐标轴
    plotter.add_axes(interactive=True)  # 使用互动的全局坐标轴
    # 设置视角
    plotter.view_vector((0, 1, 0), (0, 0, -1))

    # 使用非阻塞模式显示初始场景
    if pop_window:
        plotter.show(auto_close=False, interactive_update=True, jupyter_backend="client")

    # 设置初始的位置坐标
    # 定义NC代码中，要匹配的正则表达式模式，筛选出符合条件的行
    pattern = r"X(-?\d+\.?\d*)Y(-?\d+\.?\d*)Z(-?\d+\.?\d*)B(-?\d+\.?\d*)C(-?\d+\.?\d*)"
    # 存储每行状态的的图片
    frames = []
    with open(NC_file_path, "r") as file:
        lines = file.readlines()
        for index, line in enumerate(lines, 1):
            if index % 1000 == 0:
                print(f"第d{index}行：{line}")
            # 对行进行匹配
            match = re.search(pattern, line)
            if match:
                values = list(map(float, match.groups()))
                # 上半部分，初始偏移量
                offsetTrans = vtkTransform()
                offsetTrans.Translate(200, -95, 200)
                # 上半部分，需要进行X轴平移的物体
                XTrans = vtkTransform()
                XTrans.DeepCopy(offsetTrans)
                XTrans.Translate(values[0], 0, 0)
                actors[0].SetUserTransform(XTrans)
                # 上半部分，需要进行Z轴平移的物体
                ZTrans = vtkTransform()
                ZTrans.DeepCopy(XTrans)
                ZTrans.Translate(0, 0, values[2])
                actors[1].SetUserTransform(ZTrans)
                actors[2].SetUserTransform(ZTrans)
                actor_addcylinder.SetUserTransform(ZTrans)
                # 下半部分，Y轴平移的物体
                YTrans = vtkTransform()
                YTrans.Translate(0, values[1], 0)
                actors[3].SetUserTransform(YTrans)
                # 下半部分，B旋转的物体
                BTrans = vtkTransform()
                BTrans.DeepCopy(YTrans)
                BTrans.RotateY(values[3])
                actors[4].SetUserTransform(BTrans)
                # 下半部分，C旋转的物体
                CTrans = vtkTransform()
                CTrans.DeepCopy(BTrans)
                CTrans.RotateZ(values[4])
                actors[5].SetUserTransform(CTrans)
                actor_blade.SetUserTransform(CTrans)

                #  更新画布
                if not pop_window:
                    plotter.iren.initialize()
                plotter.update()
                # 动画播放设置时间间隔
                # time.sleep(0.1)
                # 锁定摄像机的视角
                # plotter.reset_camera()
                # 捕获当前帧
                image = plotter.screenshot()
                frames.append(image)

    # 在动画结束后，窗口保持打开状态
    # plotter.show(auto_close=False)

    # 关闭 plotter
    plotter.close()
    # 保存为 mp4
    # output_file = output_path if output_path else "machine.mp4"
    # print(f"动画生成完成! 尝试保存到{output_file}")
    # # imageio.mimsave(output_file, frames, fps=60, codec="libx264")
    # # 提示完成全部操作
    # print(f"动画保存到d{output_file}")


async def showAnimationAsync(NC_file_path: str, file_paths: str = None, blade_file_path: str = None, output_path: str = None):
    # 初始化 Plotter
    plotter = pv.Plotter()

    # 定义文件路径和颜色
    if not file_paths:
        print("请提供机床模型文件")
        return

    colors = ["red", "orange", "yellow", "green", "blue", "purple"]
    # 创造actor list
    actors = []

    # 添加机床模型
    for i, file_path in enumerate(file_paths):
        reader = pv.get_reader(file_path)
        mesh = reader.read()  # 读取机床模型
        actor = plotter.add_mesh(mesh, color=colors[i], opacity=0.7)  # 添加机床模型到plotter上，0.7表示模型的透明度
        actor.RotateX(90)
        actors.append(actor)

    # 单独添加叶片
    if not blade_file_path:
        print(f"叶片文件{blade_file_path}不存在")
        return
    else:
        reader = pv.get_reader(blade_file_path)

    blade = reader.read()
    actor_blade = plotter.add_mesh(blade)
    actor_blade.RotateX(180)  # 调整叶片的位置

    # 添加圆柱体模拟刀片
    cylinder = pv.Cylinder(center=(-224, 95, -290), direction=(0, 0, 1), radius=1.0, height=20.0)  # 数值为测试数值，是手动调节的位置等信息
    actor_addcylinder = plotter.add_mesh(cylinder)

    # 显示坐标轴
    plotter.add_axes(interactive=True)  # 使用互动的全局坐标轴
    # 设置视角
    plotter.view_vector((0, 1, 0), (0, 0, -1))

    plotter.show(jupyter_backend='client', auto_close=False)
    plotter.iren.initialize()
    plotter.iren.start()
    plotter.render()

    print(f"开始计算动画{datetime.datetime.now()}")
    # 设置初始的位置坐标
    # 定义NC代码中，要匹配的正则表达式模式，筛选出符合条件的行
    pattern = r"X(-?\d+\.?\d*)Y(-?\d+\.?\d*)Z(-?\d+\.?\d*)B(-?\d+\.?\d*)C(-?\d+\.?\d*)"

    with open(NC_file_path, "r") as file:
        lines = file.readlines()
        for index, line in enumerate(lines, 1):
            if index % 10 == 0:
                # 对行进行匹配
                match = re.search(pattern, line)
                if match:
                    values = list(map(float, match.groups()))
                    # 上半部分，初始偏移量
                    offsetTrans = vtkTransform()
                    offsetTrans.Translate(200, -95, 200)
                    # 上半部分，需要进行X轴平移的物体
                    XTrans = vtkTransform()
                    XTrans.DeepCopy(offsetTrans)
                    XTrans.Translate(values[0], 0, 0)
                    actors[0].SetUserTransform(XTrans)
                    # 上半部分，需要进行Z轴平移的物体
                    ZTrans = vtkTransform()
                    ZTrans.DeepCopy(XTrans)
                    ZTrans.Translate(0, 0, values[2])
                    actors[1].SetUserTransform(ZTrans)
                    actors[2].SetUserTransform(ZTrans)
                    actor_addcylinder.SetUserTransform(ZTrans)
                    # 下半部分，Y轴平移的物体
                    YTrans = vtkTransform()
                    YTrans.Translate(0, values[1], 0)
                    actors[3].SetUserTransform(YTrans)
                    # 下半部分，B旋转的物体
                    BTrans = vtkTransform()
                    BTrans.DeepCopy(YTrans)
                    BTrans.RotateY(values[3])
                    actors[4].SetUserTransform(BTrans)
                    # 下半部分，C旋转的物体
                    CTrans = vtkTransform()
                    CTrans.DeepCopy(BTrans)
                    CTrans.RotateZ(values[4])
                    actors[5].SetUserTransform(CTrans)
                    actor_blade.SetUserTransform(CTrans)

                    plotter.update()
                    await asyncio.sleep(0.1)


async def showAnimationWithInfoAsync(NC_file_path: str, file_paths: str = None, blade_file_path: str = None, line_skip=10):
    # 清除所有之前的输出
    clear_output(wait=True)

    # 关闭所有之前的 plotter
    pv.close_all()
    # 初始化 Plotter
    plotter = pv.Plotter()

    # 定义文件路径和颜色
    if not file_paths:
        print("请提供机床模型文件")
        return

    colors = ["red", "orange", "yellow", "green", "blue", "purple"]
    # 创造actor list
    actors = []

    # 添加机床模型
    for i, file_path in enumerate(file_paths):
        reader = pv.get_reader(file_path)
        mesh = reader.read()  # 读取机床模型
        actor = plotter.add_mesh(mesh, color=colors[i], opacity=0.7)  # 添加机床模型到plotter上，0.7表示模型的透明度
        actor.RotateX(90)
        actors.append(actor)

    # 单独添加叶片
    if not blade_file_path:
        print(f"叶片文件{blade_file_path}不存在")
        return
    else:
        reader = pv.get_reader(blade_file_path)

    blade = reader.read()
    actor_blade = plotter.add_mesh(blade)
    actor_blade.RotateX(180)  # 调整叶片的位置

    # 添加圆柱体模拟刀片
    cylinder = pv.Cylinder(center=(-224, 95, -290), direction=(0, 0, 1), radius=1.0, height=20.0)  # 数值为测试数值，是手动调节的位置等信息
    actor_addcylinder = plotter.add_mesh(cylinder)

    # 显示坐标轴
    plotter.add_axes(interactive=True)  # 使用互动的全局坐标轴
    # 设置视角
    plotter.view_vector((0, 1, 0), (0, 0, -1))

    plotter.show(jupyter_backend='client', auto_close=False)
    plotter.iren.initialize()
    plotter.iren.start()
    plotter.render()

    print(f"开始计算动画{datetime.datetime.now()}")

    # 创建一个用于显示NC代码信息的输出区域
    output = display(HTML(""), display_id=True)

    # 用于存储最近的5行NC代码信息
    recent_lines = []

    pattern = r"X(-?\d+\.?\d*)Y(-?\d+\.?\d*)Z(-?\d+\.?\d*)B(-?\d+\.?\d*)C(-?\d+\.?\d*)"

    with open(NC_file_path, "r") as file:
        lines = file.readlines()
        for index, line in enumerate(lines, 1):
            if index % line_skip == 0:
                match = re.search(pattern, line)

                if match:
                    values = list(map(float, match.groups()))
                    # 上半部分，初始偏移量
                    offsetTrans = vtkTransform()
                    offsetTrans.Translate(225, -95, 200)
                    # 上半部分，需要进行X轴平移的物体
                    XTrans = vtkTransform()
                    XTrans.DeepCopy(offsetTrans)
                    XTrans.Translate(values[0], 0, 0)
                    actors[0].SetUserTransform(XTrans)
                    # 上半部分，需要进行Z轴平移的物体
                    ZTrans = vtkTransform()
                    ZTrans.DeepCopy(XTrans)
                    ZTrans.Translate(0, 0, values[2])
                    actors[1].SetUserTransform(ZTrans)
                    actors[2].SetUserTransform(ZTrans)
                    actor_addcylinder.SetUserTransform(ZTrans)
                    # 下半部分，Y轴平移的物体
                    YTrans = vtkTransform()
                    YTrans.Translate(0, values[1], 0)
                    actors[3].SetUserTransform(YTrans)
                    # 下半部分，B旋转的物体
                    BTrans = vtkTransform()
                    BTrans.DeepCopy(YTrans)
                    BTrans.RotateY(values[3])
                    actors[4].SetUserTransform(BTrans)
                    # 下半部分，C旋转的物体
                    CTrans = vtkTransform()
                    CTrans.DeepCopy(BTrans)
                    CTrans.RotateZ(values[4])
                    actors[5].SetUserTransform(CTrans)
                    actor_blade.SetUserTransform(CTrans)

                    # 更新最近的NC代码信息
                    recent_lines.append(f"第{index}行: {line.strip()}")
                    if len(recent_lines) > 5:
                        recent_lines.pop(0)

                    # 更新显示的NC代码信息
                    output.update(HTML("<pre>" + "\n".join(recent_lines) + "</pre>"))

                    plotter.update()
                    await asyncio.sleep(0.1)

    # 清除输出
    clear_output()


class showMultiModel:
    def __init__(self):
        self.plotter = pv.Plotter()
        self.actors = {}

    def addPointsFromFile(self, file_path: str, color: str = None, handle_type: str = "txt"):
        if handle_type == "txt":
            points_data = handle_txt(file_path)
        elif handle_type == "cpt":
            points_data = handle_cpt(file_path)
        actor = self.plotter.add_points(points=points_data, color=color)
        self.actors[file_path] = actor

    def addLinesFromFile(self, file_path: str, color: str = None, line_width: float = 1.0, handle_type: str = "cpt"):
        if handle_type == "txt":
            line_data = handle_txt(file_path)
        elif handle_type == "cpt":
            line_data = handle_cpt(file_path)
        mesh = pv.MultipleLines(points=line_data)
        actor = self.plotter.add_mesh(mesh, line_width=line_width, color=color)
        self.actors[file_path] = actor

    def showOneLineFromList(self, line_data_list, color: str = None, line_width: float = 1.0):
        points = []
        for oneXYZ in line_data_list:
            points.append([oneXYZ["x"], oneXYZ["y"], oneXYZ["z"]])
        line_data = np.array(points, dtype=np.float32)
        mesh = pv.MultipleLines(points=line_data)
        actor = self.plotter.add_mesh(mesh, line_width=line_width, color=color)
        self.actors[line_data_list] = actor
        self.plotter.show()

    # 暂时不支持移除全部型线模型
    def showMultiLineFromList(self, lines_data_list, color: str = None, line_width: float = 1.0):
        for oneLine in lines_data_list:
            points = []
            for oneXYZ in oneLine:
                points.append([oneXYZ["x"], oneXYZ["y"], oneXYZ["z"]])
            line_data = np.array(points, dtype=np.float32)
            mesh = pv.MultipleLines(points=line_data)
            self.plotter.add_mesh(mesh, line_width=line_width, color=color)
        self.plotter.show()

    def addModel(self, file_path: str, color: str = None):
        reader = pv.get_reader(file_path)
        mesh = reader.read()
        actor = self.plotter.add_mesh(mesh, color=color)
        self.actors[file_path] = actor

    def removeModel(self, file_path: str):
        if file_path in self.actors:
            self.plotter.remove_actor(self.actors[file_path])
            del self.actors[file_path]

    def show(self):
        self.plotter.show()


# 检查字符串是否为数字（包括负数和小数）
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


# 读取文件中的点数据并处理非点位信息
def handle_txt(file_path):
    points = []
    with open(file_path, "r") as file:
        data = file.readlines()
        for line in data:
            elements = line.split()
            # 检查每一项是否都是数字，并且数量大于等于三个
            if len(elements) >= 3 and all(is_number(e) for e in elements):
                # 取前三个数字
                points.append([float(elements[0]), float(elements[1]), float(elements[2])])
    return np.array(points, dtype=np.float32)


def handle_cpt(file_path):
    points = []
    with open(file_path, "r") as file:
        data = file.readlines()
        for line in data:
            elements = line.split()
            # 检查每一项是否都是数字，并且数量大于等于三个
            if len(elements) == 3 and all(is_number(e) for e in elements):
                # 取前三个数字
                points.append([float(elements[0]), float(elements[1]), float(elements[2])])
    return np.array(points, dtype=np.float32)


def showPcd(pcd_path):
    multiModel = showMultiModel()
    multiModel.addPointsFromFile(file_path=r"E:\imkernel_python_release\imkernel\ShowModel\target.pcd", color="yellow")
    multiModel.addPointsFromFile(file_path=r"E:\imkernel_python_release\imkernel\ShowModel\final.pcd", color="lightgreen")
    multiModel.show()


def showMolded(molded_list):
    multiModel = showMultiModel()
    for x in molded_list:
        multiModel.addPointsFromFile(file_path=x, color=None)
    multiModel.show()


import pandas as pd
import matplotlib.pyplot as plt


def showScatter_plot(file_path):
    df = pd.read_csv(file_path, index_col=0)
    # 获取最后两列的数据
    mrr = df.iloc[:, -2]
    failure_rate = df.iloc[:, -1]
    failure_mrr = df.iloc[:, -2:]

    # 绘制散点图
    plt.figure(figsize=(10, 6))
    plt.scatter(mrr, failure_rate, color='blue')
    plt.title('Scatter Plot of MRR vs. Failure Rate')
    plt.xlabel('MRR')
    plt.ylabel('Failure Rate')
    plt.grid(True)

    print("Optimize output")
    print(failure_mrr)

    plt.legend()
    plt.show()


if __name__ == '__main__':
    showObjFromFile(r'C:\SHUSHE\Python\imkernel_python\src\imkernel\3DV\1.obj')
