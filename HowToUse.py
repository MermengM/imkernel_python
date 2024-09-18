from imkernel import System

# 创建Element实例
s = System()
s.element.create("blade_optimize_system", "0. 叶片铣削设计制造系统")
s.element.create("design_system", "1. 设计系统", "blade_optimize_system", True)
s.element.create("blade", "1.1 叶片", "design_system")
s.element.create("curved_surface", "1.1.1 曲面", "blade")
s.element.create("manufacture_test_system", "2. 制造检测系统", "blade_optimize_system", True)
s.element.create("physical_blade", "2.1 叶片实物", "manufacture_test_system")
s.element.create("milling_machine", "2.2 铣床", "manufacture_test_system")
s.element.create("test_device", "2.3 检测设备", "manufacture_test_system", True)
s.element.create("visual_inspect_device", "2.3.1 视觉检测装置", "test_device")
s.element.create("AAAA", "-0.视觉检测装置", )
s.element.create("BBBB", "-0.视觉检测装置", 'AAAA')
s.element.print_tree()
# s.element.print_tree_desc()


print(s.element.name())
print(s.element.get_by_id('test_device'))
#
# print(s.element.get_element_id())
#
s.element.parameter_group("blade_optimize_system", [])
s.element.parameter_group("blade", ["blade_CAD", 89, 68, 1])
s.element.parameter_group("curved_surface", ["eleven_parameter", 0])
s.element.parameter_group("physical_blade", ["path_parameter", 1, 2])
s.element.parameter_group("milling_machine", ["technological_parameter"])
s.element.parameter_group("visual_inspect_device", [])
print(s)
#
s.element.parameter("blade_optimize_system", [])
s.element.parameter("blade", [["obj_file"], 0, 0])
s.element.parameter(
    "curved_surface",
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
s.element.parameter("physical_blade", [["Cutter_diameter", "Cutting_depth", "Residual_height"]])
s.element.parameter("milling_machine", [["Cutter_length", "Cutter_angle", "Feed_speed", "Spindle_speed"]])
s.element.parameter("visual_inspect_device", [])

a = s.element.show_parameters()
g = s.element.show_parameters_group()
print(s)
# alist = s.element.tree_element.get_no_tag_nodes()
# for node in alist:
#     print(node.parameter_list)
