import pandas as pd

from imkernel.model import System

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

# 单元模型创建
system = System()
system.build_from_dataframes(object_df, parameter_df)
elements_df = system.get_element_df()
elements_df

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
# 输出十一参数数据
ElevenParameters_df = system.get_parameters_df_for_object('ElevenParameters')
ElevenParameters_df1 = system.get_parameters_for_object('ElevenParameters')
tttt = system.get_parameters_by_node_name('ElevenParameters')
elevenParameters_input_dict = system.get_parameters_dict_by_node_name('ElevenParameters')

# 算法

from algo import make_molded

result = make_molded(**elevenParameters_input_dict)
system.add_node_data("CurvePonits", result)
# x = system.get_parameters_dict_by_node_name("CurvePonits")
# print(x)
result_df = system.get_element_df()
all_df = system.get_element_df()
system.print_tree()

print(1)
