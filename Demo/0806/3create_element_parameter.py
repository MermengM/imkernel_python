import pandas as pd

from imkernel.model import System
from imkernel.core import df_utils

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

method_parameter_df = pd.DataFrame(data=[
    ('方法参数', '叶片设计参数', '型线生成参数', "十一参数", "输入参数", "Chord_Length(截面弦长)"),
    ('方法参数', '叶片设计参数', '型线生成参数', "十一参数", "输入参数", "Upper_Max_Width(叶背最大厚度)"),
    ('方法参数', '叶片设计参数', '型线生成参数', "十一参数", "输入参数", "Upper_Max_Width_Loc(叶背最大厚度位置)"),
    ('方法参数', '叶片设计参数', '型线生成参数', "十一参数", "输入参数", "Upper_Angle(叶背与尾缘夹角)"),
    ('方法参数', '叶片设计参数', '型线生成参数', "十一参数", "输入参数", "Upper_tip_coeff(叶背-前缘外形因数)"),
    ('方法参数', '叶片设计参数', '型线生成参数', "十一参数", "输入参数", "Upper_aft_part_shape(扩散点位置)"),
    ('方法参数', '叶片设计参数', '型线生成参数', "十一参数", "输入参数", "Lower_max_width(叶盆最大厚度)"),
    ('方法参数', '叶片设计参数', '型线生成参数', "十一参数", "输入参数", "Lower_max_width_loc(叶盆最大厚度位置)"),
    ('方法参数', '叶片设计参数', '型线生成参数', "十一参数", "输入参数", "Lower_Angle(叶盆与尾缘夹角)"),
    ('方法参数', '叶片设计参数', '型线生成参数', "十一参数", "输入参数", "Lower_tip_coeff(叶背-前缘外形因数)"),
    ('方法参数', '叶片设计参数', '型线生成参数', "十一参数", "输入参数", "Lower_aft_part_shape(扩散点位置)"),
    ('方法参数', '叶片设计参数', '型线生成参数', "十一参数", "输入参数", "Tangent_Leading_Edge(前缘切向夹角)"),
    ('方法参数', '叶片设计参数', '型线生成参数', "采样点", "输入参数", "SectionPoints(点位x,y,z)"),
    ('方法参数', '叶片设计参数', '型线生成参数', "输出参数", "CurvePoints(点位x,y,z)"),
    ('方法参数', '叶片设计参数', '型线生成参数', "输出参数", "cpts(控制点坐标x,y,z)"),
    ('方法参数', '叶片设计参数', '曲面生成参数', "输入参数", "CurvePoints(弧线点x,y,z)"),
    ('方法参数', '叶片设计参数', '曲面生成参数', "输出参数", "未封闭曲面(.obj)"),
    ('方法参数', '叶片设计参数', '端面封闭参数', "输入参数", "未封闭曲面(.obj)"),
    ('方法参数', '叶片设计参数', '端面封闭参数', "输出参数", "封闭曲面(.obj)"),
    ('方法参数', '轨迹规划参数', '精加工算法参数', "输入参数", "cpts(控制点x,y,z)"),

])

# 方法模型
method_model = System()

method_object = System()
method_object.build_from_dataframes(method_df)

method_parameter = System()
method_parameter.build_from_dataframes(method_parameter_df)
method_parameter.print_tree()

elevent_input = df_utils.find_children(method_parameter_df, '十一参数')
method_parameter_1 = method_parameter.find_node_by_path(['方法参数', '叶片设计参数', '型线生成参数', '十一参数'])
method_parameter_1.print_tree()
method_model.build_from_dataframes(method_df)
method_model.print_tree()
elements_df = method_model.get_element_df()
print(1)
eleven_df = method_model
method_model.bind_method_parameter_to_object(['输入参数', 'Chord_Length(截面弦长)'], object_path=['叶片设计方法', '型线生成方法(Python型线程序)', '十一参数法'])
method_model.associate_parameter_to_object(parameter_info="Upper_Max_Width(叶背最大厚度)", object_path=['叶片设计方法', '型线生成方法(Python型线程序)', '十一参数法'])
method_model.associate_parameter_to_object(parameter_info="Upper_Max_Width_Loc(叶背最大厚度位置)", object_path=['叶片设计方法', '型线生成方法(Python型线程序)', '十一参数法'])
method_model.associate_parameter_to_object(parameter_info="Upper_Angle(叶背与尾缘夹角)", object_path=['叶片设计方法', '型线生成方法(Python型线程序)', '十一参数法'])
method_model.associate_parameter_to_object(parameter_info="Upper_tip_coeff(叶背-前缘外形因数)", object_path=['叶片设计方法', '型线生成方法(Python型线程序)', '十一参数法'])
method_model.associate_parameter_to_object(parameter_info="Upper_aft_part_shape(扩散点位置)", object_path=['叶片设计方法', '型线生成方法(Python型线程序)', '十一参数法'])
method_model.associate_parameter_to_object(parameter_info="Lower_max_width(叶盆最大厚度)", object_path=['叶片设计方法', '型线生成方法(Python型线程序)', '十一参数法'])
method_model.associate_parameter_to_object(parameter_info="Lower_max_width_loc(叶盆最大厚度位置)", object_path=['叶片设计方法', '型线生成方法(Python型线程序)', '十一参数法'])
method_model.associate_parameter_to_object(parameter_info="Lower_Angle(叶盆与尾缘夹角)", object_path=['叶片设计方法', '型线生成方法(Python型线程序)', '十一参数法'])
method_model.associate_parameter_to_object(parameter_info="Lower_tip_coeff(叶背-前缘外形因数)", object_path=['叶片设计方法', '型线生成方法(Python型线程序)', '十一参数法'])
method_model.associate_parameter_to_object(parameter_info="Lower_aft_part_shape(扩散点位置)", object_path=['叶片设计方法', '型线生成方法(Python型线程序)', '十一参数法'])
method_model.associate_parameter_to_object(parameter_info="Tangent_Leading_Edge(前缘切向夹角)", object_path=['叶片设计方法', '型线生成方法(Python型线程序)', '十一参数法'])
