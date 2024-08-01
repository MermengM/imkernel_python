import numpy as np
from imkernel.model.new_model import BaseNode, System, UnitObject, UnitParameter, UnitData
import pandas as pd

# 创建DataFrame
Elements_df = pd.DataFrame(data=[
    ('Blade', 'BladeCross', 'BladePolyLine', 'ElevenParameters'),
    ('Blade', 'BladeCross', 'BladePolyLine', 'SectionPoints'),
    ('Blade', 'BladeCross', 'BladePolyLine', 'CurvePonits'),
    ('Blade', 'BladeCross', 'BladePolyLine', 'cpts'),
    ('Blade', 'FinishingPoint'),
    ('Blade', 'ClosedBladeCross'),
    ('machine', 'BasicParameters'),
    ('machine', 'MachiningParameter'),
    ('cutter', 'BasicParameters'),
    ('cutter', 'P_Parameter'),
    ('cutter', 'NoneTest')
])

# 创建DataFrame
parameter_pd = pd.DataFrame(data=[
    ('DesginParameters', 'ElevenParameters', 'Chord_Length'),
    ('DesginParameters', 'ElevenParameters', 'Upper_Max_Width'),
    ('DesginParameters', 'ElevenParameters', 'Upper_Max_Width_Loc'),
    ('DesginParameters', 'ElevenParameters', 'Upper_Angle'),
    ('DesginParameters', 'ElevenParameters', 'Upper_tip_coeff'),
    ('DesginParameters', 'ElevenParameters', 'Upper_aft_part_shape'),
    ('DesginParameters', 'ElevenParameters', 'Lower_max_width'),
    ('DesginParameters', 'ElevenParameters', 'Lower_max_width_loc'),
    ('DesginParameters', 'ElevenParameters', 'Lower_Angle'),
    ('DesginParameters', 'ElevenParameters', 'Lower_tip_coef'),
    ('DesginParameters', 'ElevenParameters', 'Lower_aft_part_shape'),
    ('DesginParameters', 'ElevenParameters', 'Tangent_Leading_Edge'),
    ('SectionPoints', 'x'),
    ('SectionPoints', 'y'),
    ('SectionPoints', 'z'),
    ('CurvePonits', 'x'),
    ('CurvePonits', 'y'),
    ('CurvePonits', 'z'),
    ('FinishingPoint', 'x'),
    ('FinishingPoint', 'y'),
    ('FinishingPoint', 'z'),
    ('FinishingPoint', 'i'),
    ('FinishingPoint', 'j'),
    ('FinishingPoint', 'k'),
    ('BasicParameters', 'A'),
    ('BasicParameters', 'B'),
    ('BasicParameters', 'C'),
])

# 创建System实例并从DataFrame构建树形结构
system = System()
system.build_from_dataframes(Elements_df, parameter_pd)

# 使用新的基于名称的方法设置和获取数据
system.set_node_data("ElevenParameters", "Chord_Length", "12332")
system.set_node_data("ElevenParameters", "Upper_Max_Width", 0.5)
system.set_node_data("ElevenParameters", "Upper_Max_Width_Loc", [1, 2, 3, 4])
a = system.get_node_data("ElevenParameters", "Chord_Length")
# 打印完整树形结构
print("Complete Tree:")
system.print_tree()

# 获取并打印只包含UnitObject的树
print("\nObject Tree:")
print(system.get_object_tree())

# 获取并打印只包含UnitParameter的树
print("\nParameter Tree:")
print(system.get_parameter_tree())

# 生成对象 DataFrame
objects_df = system.generate_objects_df()
print("Objects DataFrame:")
print(objects_df)
print()

# 生成参数 DataFrame
parameters_df = system.generate_parameters_df()
print("Parameters DataFrame:")
print(parameters_df)
print()

# 生成所有元素的 DataFrame
elements_df = system.generate_elements_df()
print("All Elements DataFrame:")
print(elements_df)

# Get all data as a DataFrame
data_df = system.get_all_data_as_dataframe()

# Display the DataFrame
print(data_df)
