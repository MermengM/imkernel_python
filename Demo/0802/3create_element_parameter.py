import pandas as pd

from imkernel.model import Element
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

# 单元模型
system = Element()
system.build_from_dataframes(object_df)
elements_df = system.to_df()
elements_df

system.bind_parameter_to_object(parameter_info="Chord_Length", object_path=['Blade', 'BladeCross', 'BladePolyLine', 'ElevenParameters'])
system.bind_parameter_to_object(parameter_info="Upper_Max_Width", object_path=['Blade', 'BladeCross', 'BladePolyLine', 'ElevenParameters'])
system.bind_parameter_to_object(parameter_info="Upper_Max_Width_Loc", object_path=['Blade', 'BladeCross', 'BladePolyLine', 'ElevenParameters'])
system.bind_parameter_to_object(parameter_info="Upper_Angle", object_path=['Blade', 'BladeCross', 'BladePolyLine', 'ElevenParameters'])
system.bind_parameter_to_object(parameter_info="Upper_tip_coeff", object_path=['Blade', 'BladeCross', 'BladePolyLine', 'ElevenParameters'])
system.bind_parameter_to_object(parameter_info="Upper_aft_part_shape", object_path=['Blade', 'BladeCross', 'BladePolyLine', 'ElevenParameters'])
system.bind_parameter_to_object(parameter_info="Lower_max_width", object_path=['Blade', 'BladeCross', 'BladePolyLine', 'ElevenParameters'])
system.bind_parameter_to_object(parameter_info="Lower_max_width_loc", object_path=['Blade', 'BladeCross', 'BladePolyLine', 'ElevenParameters'])
system.bind_parameter_to_object(parameter_info="Lower_Angle", object_path=['Blade', 'BladeCross', 'BladePolyLine', 'ElevenParameters'])
system.bind_parameter_to_object(parameter_info="Lower_max_width_loc", object_path=['Blade', 'BladeCross', 'BladePolyLine', 'ElevenParameters'])
system.bind_parameter_to_object(parameter_info="Lower_tip_coeff", object_path=['Blade', 'BladeCross', 'BladePolyLine', 'ElevenParameters'])
system.bind_parameter_to_object(parameter_info="Lower_aft_part_shape", object_path=['Blade', 'BladeCross', 'BladePolyLine', 'ElevenParameters'])
system.bind_parameter_to_object(parameter_info="Tangent_Leading_Edge", object_path=['Blade', 'BladeCross', 'BladePolyLine', 'ElevenParameters'])

system.print_tree()
