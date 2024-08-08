from imkernel.model import Element, UnitObject, UnitParameter, UnitData
import pandas as pd
from imkernel.core.df_utils import find_children, find_all_parents

# 创建单元对象dataframe
object_df = pd.DataFrame(data=[
    ('Blade', 'BladeCross', 'BladePolyLine', 'ElevenParameters'),
    ('Blade', 'BladeCross', 'BladePolyLine', 'SectionPoints'),
    ('Blade', 'BladeCross', 'BladePolyLine', 'CurvePonits'),
    ('Blade', 'BladeCross', 'BladePolyLine', 'cpts'),
    ('Blade', 'FinishingPoint'),
    ('Blade', 'ClosedBladeCross'),
    ('machine', 'BasicParameters'),
    ('machine', 'MachiningParameter'),
    ('cutter', 'BasicParameters'),
    ('cutter', 'P_Parameter')
])
object_df

# 单元对象修改
system = Element()
system.build_from_dataframes(object_df)
system.add_object_to_node("BladeCross", "6新增对象7")
BladePolyLine = system.find_node("BladeCross")
for x in BladePolyLine.children:
    print(x.name)

Elements_df_new = system.to_df()
Elements_df_new
# 单元对象查找
test_cases = ['Blade', 'BladePolyLine', 'machine', 'cutter', '不存在的节点']
test_cases2 = ['Blade', 'cpts', 'MachiningParameter', 'P_Parameter', '不存在的节点']

for case in test_cases:
    print(f"\n查找 '{case}' 的子节点:")
    result_child = find_children(object_df, case)
    if not result_child.empty:
        print(result_child)
    else:
        print("没有找到子节点")
for case in test_cases2:
    print(f"\n查找 '{case}' 的父节点:")
    result_parent = find_all_parents(object_df, case)

    if result_parent is not None:
        result_parent.to_string()
        print(result_parent)
    else:
        print("没有找到父节点")
