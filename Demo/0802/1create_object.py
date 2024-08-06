from imkernel.model import System, UnitObject, UnitParameter, UnitData
import pandas as pd

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
system = System()
system.build_from_dataframes(object_df)
system.add_object_to_node("BladeCross", "新增对象7")
BladePolyLine = system.find_node("BladeCross")
for x in BladePolyLine.children:
    print(x.name)

Elements_df_new = system.get_element_df()
Elements_df_new
