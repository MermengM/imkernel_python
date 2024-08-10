from imkernel.model.new_model import BaseNode, Element, UnitObject, UnitParameter, UnitData
import pandas as pd

method_df = pd.DataFrame(data=[
    ('叶片设计方法', '型线生成方法(Python型线程序)', '十一参数法'),
    ('叶片设计方法', '型线生成方法(Python型线程序)', '采样点法'),
    ('叶片设计方法', '曲面生成法(PeriodicTsplineSkinningLib.dll)'),
    ('叶片设计方法', '端面封闭生成法(Fill_empty_obj2stl.py)'),
    ('轨迹规划方法', '精加工算法'),
    ('加工规划方法', 'NC代码生成方法(FiveAxisSolver.dll)'),
    ('检测方法', '采样算法'),
    ('检测方法', '配准算法'),
    ('人工智能优化方法', '复杂型面加工特征参数优化迭代算法'),
    ('人工智能优化方法', '面向复杂型面的铣削参数优化方法')
])
# 方法模型
CIMSH_Method = Element()
CIMSH_Method.add_object_from_dataframe(method_df)
CIMSH_Method.to_df()

# 单个参数
CIMSH_Method.bind_method_parameter_to_object(
    ['输入参数', 'Chord_Length(截面弦长)'],
    object_path=['叶片设计方法', '型线生成方法(Python型线程序)', '十一参数法']
)

# 批量参数
all_parameters = [
    ['时间参数', 'Chord_Length(截面弦长)'],
    ['输入参数', 'Upper_Max_Width(叶背最大厚度)'],
    ['输入参数', 'Upper_Max_Width_Loc(叶背最大厚度位置)'],
    ['输入参数', 'Upper_Angle(叶背与尾缘夹角)'],
    ['输入参数', 'Upper_tip_coeff(叶背-前缘外形因数)'],
    ['输入参数', 'Upper_aft_part_shape(扩散点位置)'],
    ['输入参数', 'Lower_max_width(叶盆最大厚度)'],
    ['输入参数', 'Lower_max_width_loc(叶盆最大厚度位置)'],
    ['输入参数', 'Lower_Angle(叶盆与尾缘夹角)'],
    ['输入参数', 'Lower_tip_coeff(叶背-前缘外形因数)'],
    ['输入参数', 'Lower_aft_part_shape(扩散点位置)'],
    ['输入参数', 'Tangent_Leading_Edge(前缘切向夹角)']
]

# 使用组合后的列表一次性绑定所有参数
CIMSH_Method.bind_method_parameter_to_object(
    param_info=all_parameters,
    object_path=['叶片设计方法', '型线生成方法(Python型线程序)', '十一参数法']
)
CIMSH_Method_df = CIMSH_Method.to_df()
CIMSH_Method_df
# 添加一套数据
system.set_node_data("Chord_Length", 0.5)
system.set_node_data("Upper_Max_Width", 0.5)
system.set_node_data("Upper_Max_Width_Loc", 0.5)
system.set_node_data("Upper_Angle", 0.5)
system.set_node_data("Upper_tip_coeff", 0.5)
system.set_node_data("Upper_aft_part_shape", 0.5)
system.set_node_data("Lower_max_width", 0.5)
system.set_node_data("Lower_max_width_loc", 0.5)
system.set_node_data("Lower_Angle", 0.5)
system.set_node_data("Lower_tip_coeff", 0.5)
system.set_node_data("Lower_aft_part_shape", 0.5)
system.set_node_data("Tangent_Leading_Edge", 0.5)
system.set_node_data("A", 0.5)
system.print_tree()
