import pandas as pd
from imkernel.core.df_utils import find_children, find_all_parents
from imkernel.model import Element

parameter_df = pd.DataFrame(data=[
    ('DesginParameters', 'ElevenParameters', 'Chord_Length'),
    ('DesginParameters', 'ElevenParameters', 'Upper_Max_Width'),
    ('DesginParameters', 'ElevenParameters', 'Upper_Max_Width_Loc'),
    ('DesginParameters', 'ElevenParameters', 'Upper_Angle'),
    ('DesginParameters', 'ElevenParameters', 'Upper_tip_coeff'),
    ('DesginParameters', 'ElevenParameters', 'Upper_aft_part_shape'),
    ('DesginParameters', 'ElevenParameters', 'Lower_max_width'),
    ('DesginParameters', 'ElevenParameters', 'Lower_max_width_loc'),
    ('DesginParameters', 'ElevenParameters', 'Lower_Angle'),
    ('DesginParameters', 'ElevenParameters', 'Lower_tip_coeff'),
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

# 单元参数修改
system = Element()
system.build_from_dataframes(parameter_df)
system.add_object_to_node("ElevenParameters", "新增参数")
Elements_df_new = system.to_df()
Elements_df_new
# 单元参数查找
test_cases = ['DesginParameters', 'ElevenParameters', 'SectionPoints', 'BasicParameters', '不存在的节点']
test_cases2 = ['Blade', 'cpts', 'MachiningParameter', 'P_Parameter', '不存在的节点']

for case in test_cases:
    print(f"\n查找 '{case}' 的子节点:")
    result_child = find_children(parameter_df, case)
    if not result_child.empty:
        print(result_child)
    else:
        print("没有找到子节点")
for case in test_cases2:
    print(f"\n查找 '{case}' 的父节点:")
    result_parent = find_all_parents(parameter_df, case)
    if result_parent is not None:
        print(result_parent)
    else:
        print("没有找到父节点")
