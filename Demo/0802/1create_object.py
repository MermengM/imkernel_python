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
Elements_df_new = system.get_element_df()
# 使用新的基于名称的方法设置和获取数据
system.set_node_data("ElevenParameters", "Chord_Length", "12332")
system.set_node_data("ElevenParameters", "Upper_Max_Width", 0.5)
system.set_node_data("ElevenParameters", "Upper_Max_Width_Loc", [1, 2, 3, 4])
a = system.get_node_data("ElevenParameters", "Chord_Length")
