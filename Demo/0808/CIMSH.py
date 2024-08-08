import pandas as pd

from imkernel.model import Element

Blade = pd.DataFrame(data=[
    ('Blade', 'BladeCross', 'BladePolyLine'),
])
Machine = pd.DataFrame(data=[
    ('machine', 'BasicParameters'),
    ('machine', 'MachiningParameter'),
])
Cutter = pd.DataFrame(data=[
    ('cutter', 'BasicParameters'),
    ('cutter', 'PerformanceParameter'),
])

CIMSH_Element = Element()
CIMSH_Element.add_object_from_dataframe([Blade, Machine, Cutter])
CIMSH_Element.print()
CIMSH_Element_DF = CIMSH_Element.to_df()
CIMSH_Element_DF

# 新增单元对象到指定节点
# 单层添加
CIMSH_Element.add_object_to_node("BladeCross", "BladePolyLineTest")
# 多层添加
CIMSH_Element.add_nested_objects("BladePolyLineTest", ['A', 'B', 'C'])

CIMSH_Element.print()
CIMSH_Element_DF = CIMSH_Element.to_df()
CIMSH_Element_DF

# 移除指定单元对象
CIMSH_Element.remove_node("BladePolyLineTest")
CIMSH_Element.print()
CIMSH_Element_DF = CIMSH_Element.to_df()
CIMSH_Element_DF

# 根据单元对象名查找

# 机器
machine_node_df = CIMSH_Element.find_node_to_df("machine")
machine_node_df

# 根节点
Element_node_df = CIMSH_Element.find_node_to_df("Element")
Element_node_df

# 单元参数

Parameter_df = pd.DataFrame(data=[
    ('BladeDesginParameters', 'ElevenParameters', 'Chord_Length'),
    ('BladeDesginParameters', 'ElevenParameters', 'Upper_Max_Width'),
    ('BladeDesginParameters', 'ElevenParameters', 'Upper_Max_Width_Loc'),
    ('BladeDesginParameters', 'ElevenParameters', 'Upper_Angle'),
    ('BladeDesginParameters', 'ElevenParameters', 'Upper_tip_coeff'),
    ('BladeDesginParameters', 'ElevenParameters', 'Upper_aft_part_shape'),
    ('BladeDesginParameters', 'ElevenParameters', 'Lower_max_width'),
    ('BladeDesginParameters', 'ElevenParameters', 'Lower_max_width_loc'),
    ('BladeDesginParameters', 'ElevenParameters', 'Lower_Angle'),
    ('BladeDesginParameters', 'ElevenParameters', 'Lower_tip_coeff'),
    ('BladeDesginParameters', 'ElevenParameters', 'Lower_aft_part_shape'),
    ('BladeDesginParameters', 'ElevenParameters', 'Tangent_Leading_Edge'),
    ('BladeDesginParameters', 'cpts', 'x'),
    ('BladeDesginParameters', 'cpts', 'y'),
    ('BladeDesginParameters', 'cpts', 'z'),
    ('BladeDesginParameters', 'CurvePonits', 'x'),
    ('BladeDesginParameters', 'CurvePonits', 'y'),
    ('BladeDesginParameters', 'CurvePonits', 'z'),
    ('BladeDesginParameters', 'SectionPoints', 'x'),
    ('BladeDesginParameters', 'SectionPoints', 'y'),
    ('BladeDesginParameters', 'SectionPoints', 'z'),
    ('FinishingPoint', 'x'),
    ('FinishingPoint', 'y'),
    ('FinishingPoint', 'z'),
    ('FinishingPoint', 'i'),
    ('FinishingPoint', 'j'),
    ('FinishingPoint', 'k'),
    ('BladeMachiningParameters', 'machine', 'BasicParameters', 'Type'),
    ('MachiningParameters', 'machine', 'MachiningParameters', 'Speed'),
    ('MachiningParameters', 'cutter', 'MachiningParameters', 'Speed'),
    ('BasicParameters', 'B'),
    ('BasicParameters', 'C'),
])

# 单元参数
CIMSH_Element_Parameter = Element()
CIMSH_Element_Parameter.add_object_from_dataframe(Parameter_df)
CIMSH_Element_Parameter.print()
CIMSH_Element_Parameter_DF = CIMSH_Element_Parameter.to_df()
CIMSH_Element_Parameter_DF

# 单元参数查找
ElevenParameters_df = CIMSH_Element_Parameter.find_node_to_df("ElevenParameters")
ElevenParameters_df

# 单元参数关联到单元对象
# 单个参数关联
CIMSH_Element.bind_parameter_to_object(parameter_info="Chord_Length", object_path=['Blade', 'BladeCross', 'BladePolyLine'])

# 使用参数列表关联
eleven_parameters = [
    "Upper_Max_Width",
    "Upper_Max_Width_Loc",
    "Upper_Angle",
    "Upper_tip_coeff",
    "Upper_aft_part_shape",
    "Lower_max_width",
    "Lower_max_width_loc",
    "Lower_Angle",
    "Lower_tip_coeff",
    "Lower_aft_part_shape",
    "Tangent_Leading_Edge"
]
CIMSH_Element.bind_parameter_to_object(
    parameter_info=eleven_parameters,
    object_path=['Blade', 'BladeCross', 'BladePolyLine']
)
# 添加 x y z
CIMSH_Element.bind_parameter_to_object(
    parameter_info=['x','y','z'],
    object_path=['Blade', 'BladeCross', 'BladePolyLine']
)

df = CIMSH_Element.to_df()
CIMSH_Element
