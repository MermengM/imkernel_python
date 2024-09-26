# 创建Element实例
from imkernel import Model

CIMSH = Model()
# create(id, description, parent_id, is_tag)
CIMSH.element.create("blade_optimize_system", "0. 叶片铣削设计制造系统")
CIMSH.element.create("design_system", "1. 设计系统", "blade_optimize_system", True)
CIMSH.element.create("blade", "1.1 叶片", "design_system")
CIMSH.element.create("curved_surface", "1.1.1 曲面", "blade")
CIMSH.element.create('molded_line', '1.1.1.1 型线', 'curved_surface')
CIMSH.element.create("manufacture_test_system", "2. 制造检测系统", "blade_optimize_system", True)
CIMSH.element.create("blade_reality", "2.1 叶片实物", "manufacture_test_system")
CIMSH.element.create("milling_machine", "2.2 铣床", "manufacture_test_system")
CIMSH.element.create("test_device", "2.3 检测设备", "manufacture_test_system", True)
CIMSH.element.create("visual_inspect_device", "2.3.1 视觉检测装置", "test_device")
# CIMSH.element.print_tree()
a = CIMSH.element.name()

CIMSH.element.parameter_group("blade_optimize_system", ['feature', 'label'])
CIMSH.element.parameter_group("blade", ['CAD_file'])
CIMSH.element.parameter_group("curved_surface", ['CAD_file', 'control_point'])
CIMSH.element.parameter_group("molded_line", ['eleven_parameter', 'sampling_point', 'control_point', 'point'])
CIMSH.element.parameter_group("blade_reality", ['milling_tool_path', 'path_parameter', 'point_cloud', 'profile_error'])
CIMSH.element.parameter_group("milling_machine", ['technological_parameter', 'NC_code'])
CIMSH.element.parameter_group("visual_inspect_device", [])

CIMSH.element.parameter("blade_optimize_system", [[f"feature {i}" for i in range(0, 3)], [f"label {j}" for j in range(0, 2)]])
CIMSH.element.parameter("blade", [['obj_file']])
CIMSH.element.parameter("curved_surface", [['obj_file'], ['X', 'Y', 'Z']])
CIMSH.element.parameter("molded_line", [["Chord_Length", "Upper_Max_Width", "Upper_Max_Width_Loc", 'Upper_Angle', "Upper_tip_coeff", "Upper_aft_part_shape",
                                         "Lower_max_width", "Lower_max_width_loc", "Lower_Angle", "Lower_tip_coeff", "Lower_aft_part_shape",
                                         "Tangent_Leading_Edge", 'spanwise_length'], ['X', 'Y', 'Z'], ['X', 'Y', 'Z'], ['X', 'Y', 'Z']])
CIMSH.element.parameter("blade_reality", [['X', 'Y', 'Z', 'I', 'J', 'K'], ['Cutter_diameter', 'Cutting_depth', 'Residual_height'], ['txt_file'], ['profile_error']])
CIMSH.element.parameter("milling_machine", [['Cutter_length', 'Cutter_angle', 'Feed_speed', 'Spindle_speed'], ['txt_file']])
CIMSH.element.parameter("visual_inspect_device", [])

CIMSH.element.show_parameters_group()
CIMSH.element.show_parameters()
CIMSH.element.add_model_data(['CIMSH-System1', '331-blade_01', '331-blade-sur001', 'HEBUT-BL331-001', 'HEBUT-jindiao-001', 'HNU-cinema-001', 'visual_device-001'])
CIMSH.element.add_model_data(['CIMSH-System2', '331-blade_01', '331-blade-sur001', 'HEBUT-BL331-001', 'HEBUT-jindiao-001', 'HNU-cinema-001', 'visual_device-001'])
CIMSH.element.add_model_data(['CIMSH-System3', '331-blade_01', '331-blade-sur001', 'HEBUT-BL331-001', 'HEBUT-jindiao-001', 'HNU-cinema-001', 'visual_device-001'])
ddf = CIMSH.element.get_all_data_df()
CIMSH.element.add_parameter_data(0, 'molded_line', 'eleven_parameter', [1, 2, 3, 4, 5, 6, 7, 8])
CIMSH.element.add_parameter_data(1, 'molded_line', 'eleven_parameter', [1, 2, 3, 4, 5, 6, 7, 8])
CIMSH.element.add_parameter_data(0, 'molded_line', 'sampling_point', [[1, 2, 3], [1, 2, 3]])
CIMSH.element.add_parameter_data(1, 'molded_line', 'sampling_point', [[1, 2, 3], [1, 2, 3]])
CIMSH.element.add_parameter_data(0, 'molded_line', 'control_point', [[1, 2, 3], [1, 2, 3]])
CIMSH.element.add_parameter_data(1, 'molded_line', 'control_point', [[1, 2, 3], [1, 2, 3]])
aaa = CIMSH.element.get_all_data_parameter_df()
print(CIMSH)
# 创建Element实例
CIMSH = Model()
# create(id, description, parent_id, is_tag)
CIMSH.method.create("blade_design_milling_optimization", "叶片设计铣削优化方法集", None, True)
# 创建叶片设计方法
CIMSH.method.create("blade_design", "1 叶片设计", "blade_design_milling_optimization", True)
CIMSH.method.create("molded_line_generate", "1.1 型线生成", "blade_design", True)
CIMSH.method.create("method_eleven_parameter", "1.1.1 曲面生成十一参数法", "molded_line_generate")
CIMSH.method.create("method_sampling_point", "1.1.2 曲面生成采样点法", "molded_line_generate")
CIMSH.method.create("curved_surface_generate", "1.2 曲面生成", "blade_design", True)
CIMSH.method.create("method_curved_surface_generate", "1.2.1 曲面生成方法", "curved_surface_generate")
CIMSH.method.create("blade_generate", "1.3 叶片生成", "blade_design", True)
CIMSH.method.create("method_blade_generate", "1.3.1 叶片生成方法", "blade_generate")
# 创建叶片制造和检测方法
CIMSH.method.create("blade_milling_inspect", "2 叶片加工检测", "blade_design_milling_optimization", True)
CIMSH.method.create("blade_milling", "2.1 叶片铣削加工", "blade_milling_inspect", True)
CIMSH.method.create("method_path_plan", "2.1.1 加工路径规划方法", "blade_milling")
CIMSH.method.create("method_technological_design", "2.1.2 加工工艺设计方法", "blade_milling")
CIMSH.method.create("method_blade_milling", "2.1.3 加工铣削方法", "blade_milling")
CIMSH.method.create("blade_inspect", "2.2 叶片产品检测", "blade_milling_inspect", True)
CIMSH.method.create("method_blade_routine_test", "2.2.1 常规检测方法", "blade_inspect")
CIMSH.method.create("method_blade_viaual_inspect", "2.2.2 视觉检测方法", "blade_inspect")
# 创建数据工程方法
CIMSH.method.create("blade_data_engineering", "3 叶片数据工程", "blade_design_milling_optimization", True)
CIMSH.method.create("blade_data_collect", "3.1 叶片数据采集", "blade_data_engineering", True)
CIMSH.method.create("experiment_data_collect", "3.1.1 试验数据采集", "blade_data_collect", True)
CIMSH.method.create("method_experiment_design", "3.1.1.1 试验设计", "experiment_data_collect")
CIMSH.method.create("method_experiment_data_collect", "3.1.1.2 试验数据采集", "experiment_data_collect")
CIMSH.method.create("actual_data_collect", "3.1.2 实际数据采集", "blade_data_collect", True)
CIMSH.method.create("method_actual_data_collect", "3.1.2.1 实际数据采集方法", "actual_data_collect")
CIMSH.method.create("blade_data_processing", "3.2 叶片数据治理", "blade_data_engineering", True)
CIMSH.method.create("blade_data_filter", "3.2.1 叶片数据筛选", "blade_data_engineering", True)
CIMSH.method.create("method_AI_filter_model_train", "3.2.1.1 筛选模型训练方法", "blade_data_filter")
CIMSH.method.create("method_AI_data_filter", "3.2.1.2 AI数据筛选方法", "blade_data_filter")
# 创建AI叶片优化方法
CIMSH.method.create("blade_AI_optimization_AI", "4. 叶片AI优化", "blade_design_milling_optimization", True)
CIMSH.method.create("method_AI_model_train", "4.2.1 AI模型训练方法", "blade_AI_optimization_AI")
CIMSH.method.create("method_AI_parameter_recommand", "4.2.2 AI参数推荐方法", "blade_AI_optimization_AI")

# CIMSH.method.print_tree()
CIMSH.method.print_tree_desc()
CIMSH.method.set_program("method_eleven_parameter", [r"E:\imkernel_python_release\CIMSH\algo\MoldedWire\main.py\make_molded"])
CIMSH.method.set_program("method_sampling_point", [r"E:\imkernel_python_release\CIMSH\algo\MoldedWire\main.py\sampling_point"])
CIMSH.method.set_program("method_curved_surface_generate", [r"E:\imkernel_python_release\CIMSH\algo\QuMianJianMo\main.py\jian_mo"])
CIMSH.method.set_program("method_blade_generate", [r"E:\imkernel_python_release\CIMSH\algo\DuanMianFengBi\main.py\fill_empty"])
CIMSH.method.set_program("method_path_plan", [r"E:\imkernel_python_release\CIMSH\algo\ToolPath\main.py\ToolPath"])
CIMSH.method.set_program("method_technological_design", [r"E:\imkernel_python_release\CIMSH\algo\NCGenerate\main.py\NC_Generate"])
CIMSH.method.set_program("method_blade_viaual_inspect", [r"E:\imkernel_python_release\CIMSH\algo\Detection\main.py\DetectionAlgorithm"])
CIMSH.method.set_program("method_AI_filter_model_train", [r"E:\imkernel_python_release\CIMSH\algo\p_filter_gf\main0.py\feature_filter"])
CIMSH.method.set_program("method_AI_data_filter", [r"E:\imkernel_python_release\CIMSH\algo\p_filter_gf\main0.py\data_filtering_model"])
CIMSH.method.set_program("method_AI_parameter_recommand", [r"E:\imkernel_python_release\CIMSH\algo\p_optim_gf\source_code\main.py\feature_optim"])
CIMSH.method.get_program()
CIMSH.method.input_parameter_group("method_eleven_parameter", ["eleven_parameter"])
CIMSH.method.input_parameter_group("method_sampling_point", ["molded_line_sampling_point"])
CIMSH.method.input_parameter_group("method_curved_surface_generate", ["molded_line_control_point"])
CIMSH.method.input_parameter_group("method_blade_generate", ["curved_surface_CAD"])
CIMSH.method.input_parameter_group("method_path_plan", ["curved_surface_control_point", "path_parameter"])
CIMSH.method.input_parameter_group("method_technological_design", ["milling_tool_path", "technological_parameter"])
CIMSH.method.input_parameter_group("method_blade_milling", ["NC_code", "blade_blank_set"])
CIMSH.method.input_parameter_group("method_blade_routine_test", ["blade_product_set", "blade_test_taget"])
CIMSH.method.input_parameter_group("method_blade_viaual_inspect", ["blade_product_set", "blade_CAD"])
CIMSH.method.input_parameter_group("method_experiment_design", ["feature_dataset_ranged", "DOE_parameter"])
CIMSH.method.input_parameter_group("method_experiment_data_collect", ["blade_product_set", "feature_dataset"])
CIMSH.method.input_parameter_group("method_actual_data_collect", ["blade_product_set", "feature_dataset"])
CIMSH.method.input_parameter_group("method_AI_filter_model_train", ["feature_label_dataset"])
CIMSH.method.input_parameter_group("method_AI_data_filter", ["feature_label_dataset"])
CIMSH.method.input_parameter_group("method_AI_model_train", ["filtered_feature_label_dataset"])
CIMSH.method.input_parameter_group("method_AI_parameter_recommand", ["model_weight", "designate_parameter"])

CIMSH.method.output_parameter_group("method_eleven_parameter", ["molded_line_control_point", "molded_line_point"])
CIMSH.method.output_parameter_group("method_sampling_point", ["molded_line_control_point", "molded_line_point"])
CIMSH.method.output_parameter_group("method_curved_surface_generate", ["curved_surface_control_point", "curved_surface_CAD"])
CIMSH.method.output_parameter_group("method_blade_generate", ["blade_CAD"])
CIMSH.method.output_parameter_group("method_path_plan", ["milling_tool_path"])
CIMSH.method.output_parameter_group("method_technological_design", ["NC_code"])
CIMSH.method.output_parameter_group("method_blade_milling", ["blade_product_set", "machine_parameter"])
CIMSH.method.output_parameter_group("method_blade_routine_test", ["blade_test_actual", "test_error"])
CIMSH.method.output_parameter_group("method_blade_viaual_inspect", ["blade_point_cloud", "profile_error"])
CIMSH.method.output_parameter_group("method_experiment_design", ["feature_dataset"])
CIMSH.method.output_parameter_group("method_experiment_data_collect", ["feature_label_dataset"])
CIMSH.method.output_parameter_group("method_actual_data_collect", ["feature_label_dataset"])
CIMSH.method.output_parameter_group("method_AI_filter_model_train", ["data_filtering_model_weight"])
CIMSH.method.output_parameter_group("method_AI_data_filter", ["filtered_feature_label_dataset"])
CIMSH.method.output_parameter_group("method_AI_model_train", ["model_weight"])
CIMSH.method.output_parameter_group("method_AI_parameter_recommand", ["recommand_parameter"])
gname = CIMSH.method.get_group_name_df()
CIMSH.method.show_parameters_group()
CIMSH.method.input_parameter(
    "method_eleven_parameter",
    [
        [
            "Chord_Length",
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
            "Tangent_Leading_Edge",
            "spanwise_length",
        ]
    ],
)
CIMSH.method.input_parameter("method_sampling_point", [["X", "Y", "Z"]])
CIMSH.method.input_parameter("method_curved_surface_generate", ["cpt_text"])
CIMSH.method.input_parameter("method_blade_generate", ["obj_file"])
CIMSH.method.input_parameter("method_path_plan", [["cpt_file"], ["Cutter_diameter", "Cutting_depth", "Residual_height"]])
CIMSH.method.input_parameter("method_technological_design", [["X", "Y", "Z", "I", "J", "K"], ["Cutter_length", "Cutter_angle", "Feed_speed", "Spindle_speed"]])
CIMSH.method.input_parameter("method_blade_milling", [["txt_file", "Bar_code"]])
CIMSH.method.input_parameter("method_blade_routine_test", ["Bar_code", ["Profile", "Average_roughness", "Qualified_or_not", "Processing_time"]])
CIMSH.method.input_parameter("method_blade_viaual_inspect", [["Bar_code"], ["obj_file"]])
CIMSH.method.input_parameter("method_experiment_design", [["feature1", "feature2", ""], ["doe1", "doe2"]])
CIMSH.method.input_parameter("method_experiment_data_collect", ["Bar_code", ["feature1", "feature2", ""]])
CIMSH.method.input_parameter("method_actual_data_collect", ["Bar_code", ["feature1", "feature2", ""]])
CIMSH.method.input_parameter("method_AI_filter_model_train", [["dataset"]])
CIMSH.method.input_parameter("method_AI_data_filter", [["dataset"], ["wgt_file"]])
CIMSH.method.input_parameter("method_AI_model_train", [["dataset"]])
CIMSH.method.input_parameter("method_AI_parameter_recommand", [["dataset"], ["wgt_file"]])

CIMSH.method.output_parameter("method_eleven_parameter", [["X", "Y", "Z"], ["X", "Y", "Z"]])
CIMSH.method.output_parameter("method_sampling_point", [["X", "Y", "Z"], ["X", "Y", "Z"]])
CIMSH.method.output_parameter("method_curved_surface_generate", [["obj_file"], ["X", "Y", "Z"]])
CIMSH.method.output_parameter("method_blade_generate", [["obj_file"]])
CIMSH.method.output_parameter("method_path_plan", [["X", "Y", "Z", "I", "J", "K"], "xyzijk_file"])
CIMSH.method.output_parameter("method_technological_design", [["txt_file"]])
CIMSH.method.output_parameter("method_blade_milling", ["Bar_code", ["Brand", "Type"]])
CIMSH.method.output_parameter(
    "method_blade_routine_test",
    [
        ["Profile", "Average_roughness", "Qualified_or_not", "Processing_time"],
        ["Profile_error", "Average_roughness_error", "Qualified_or_not", "Processing_time_error"],
    ],
)
CIMSH.method.output_parameter("method_blade_viaual_inspect", ["Profile_error"])
CIMSH.method.output_parameter("method_experiment_design", [["feature1", "feature2", ""]])
CIMSH.method.output_parameter("method_experiment_data_collect", [[["feature1", "feature2", ""], ["label1", "label2", ""]]])
CIMSH.method.output_parameter("method_actual_data_collect", [[["feature1", "feature2", ""], ["label1", "label2", ""]]])
CIMSH.method.output_parameter("method_AI_filter_model_train", [["wgt_file"]])
CIMSH.method.output_parameter("method_AI_data_filter", [["filtered_feature"]])
CIMSH.method.output_parameter("method_AI_model_train", [["wgt_file"]])
CIMSH.method.output_parameter("method_AI_parameter_recommand", [["optimized_data"]])

CIMSH.method.show_parameters()
CIMSH.method.input_parameter_data('method_eleven_parameter', [[[50, 0.4149, 0.2098, 0.0582, 0.4492, 0.3339, 0.234, 0.7289, 0.2497, 0.52, 0.8523, 0.5, 0],
                                                               [50, 0.4149, 0.2098, 0.0582, 0.4492, 0.3339, 0.234, 0.7289, 0.2497, 0.52, 0.8523, 0.5, 20],
                                                               [50, 0.4149, 0.2098, 0.0582, 0.4492, 0.3339, 0.234, 0.7289, 0.2497, 0.52, 0.8523, 0.5, 50],
                                                               [50, 0.4149, 0.2098, 0.0582, 0.4492, 0.3339, 0.234, 0.7289, 0.2497, 0.52, 0.8523, 0.5, 80],
                                                               [50, 0.4149, 0.2098, 0.0582, 0.4492, 0.3339, 0.234, 0.7289, 0.2497, 0.52, 0.8523, 0.5, 100]], []])
CIMSH.method.output_parameter_data('method_eleven_parameter', [[312, 41, 124], [214, 124, 4]])
CIMSH.method.run('method_eleven_parameter')
CIMSH.method.show_parameters()
aaa = CIMSH.method.show_parameter_data('method_eleven_parameter')
print(CIMSH)

# create(id, description, parent_id, is_tag)
CIMSH.procedure.create("blade_design_milling_optimization", "叶片设计铣削优化", None, True)
# 创建叶片设计流程
CIMSH.procedure.create("blade_design", "1 叶片设计", "blade_design_milling_optimization", True)
CIMSH.procedure.create("molded_line_generate", "1.1 型线生成", "blade_design")
CIMSH.procedure.create("curved_surface_generate", "1.2 曲面生成", "blade_design")
CIMSH.procedure.create("blade_generate", "1.3 叶片生成", "blade_design")
# 创建叶片制造和检测流程
CIMSH.procedure.create("blade_manufacture", "2 叶片制造", "blade_design_milling_optimization", True)
CIMSH.procedure.create("path_plan", "2.1 路径规划", "blade_manufacture")
CIMSH.procedure.create("technological_design", "2.2 工艺设计", "blade_manufacture")
CIMSH.procedure.create("milling", "2.3 加工铣削", "blade_manufacture")
CIMSH.procedure.create("blade_inspect", "3. 叶片检测", "blade_design_milling_optimization", True)
CIMSH.procedure.create("blade_routine_test", "3.1 常规检测", "blade_inspect", True)
CIMSH.procedure.create("blade_visual_inspect", "3.2 视觉检测", "blade_inspect")
# 创建数据工程流程
CIMSH.procedure.create("blade_data_engineering", "4 叶片数据工程", "blade_design_milling_optimization", True)
CIMSH.procedure.create("experiment_design", "4.1 叶片试验设计", "blade_data_engineering")
CIMSH.procedure.create("blade_data_collect", "4.2 叶片数据采集", "blade_data_engineering", True)
CIMSH.procedure.create("experiment_data_collect", "4.2.1 试验数据采集", "blade_data_collect")
CIMSH.procedure.create("factory_data_collect", "4.2.2 工厂数据采集", "blade_data_collect", True)
CIMSH.procedure.create("blade_data_filter", "4.3 叶片数据筛选", "blade_data_engineering", True)
CIMSH.procedure.create("AI_filter_model_train", "4.3.1 筛选模型训练", "blade_data_filter")
CIMSH.procedure.create("AI_data_filter", "4.3.2 AI数据筛选", "blade_data_filter")
# 创建AI叶片优化流程
CIMSH.procedure.create("blade_AI_optimization", "5. 叶片AI优化", "blade_design_milling_optimization", True)
CIMSH.procedure.create("AI_optimization_model_train", "5.1 AI优化模型训练", "blade_AI_optimization")
CIMSH.procedure.create("AI_optimization_recommand", "5.2 AI优化参数推荐", "blade_AI_optimization")

CIMSH.procedure.print_tree()
print(CIMSH.procedure.name())

CIMSH.procedure.relate("molded_line_generate", "method_eleven_parameter", "curved_surface")
CIMSH.procedure.relate("curved_surface_generate", "method_curved_surface_generate", "curved_surface")
CIMSH.procedure.relate("blade_generate", "method_blade_generate", "blade")
CIMSH.procedure.relate("path_plan", "method_path_plan", "physical_blade")
CIMSH.procedure.relate("technological_design", "method_technological_design", "milling_machine")
CIMSH.procedure.relate("milling", None, "milling_machine")
CIMSH.procedure.relate("blade_visual_inspect", "method_blade_viaual_inspect", "visual_inspect_device")
CIMSH.procedure.relate("experiment_design", "method_experiment_design", "blade_optimize_system")
CIMSH.procedure.relate("experiment_data_collect", None, "blade_optimize_system")
CIMSH.procedure.relate("AI_filter_model_train", "method_AI_filter_model_train", "blade_optimize_system")
CIMSH.procedure.relate("AI_data_filter", "method_AI_data_filter", "blade_optimize_system")
CIMSH.procedure.relate("AI_optimization_model_train", "method_AI_optimization_model_train", "blade_optimize_system")
CIMSH.procedure.relate("AI_optimization_recommand", "method_AI_optimization_recommand", "blade_optimize_system")
a = CIMSH.procedure.show_relation()
print(CIMSH.procedure.show_relation())
