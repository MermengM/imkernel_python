from imkernel import imkernel as kernel


if __name__ == "__main__":
    # 创建Element实例
    s = kernel.System()
    s.element.create("blade_optimize_system", "0. 叶片铣削设计制造系统")
    s.element.create("design_system", "1. 设计系统", "blade_optimize_system", True)
    s.element.create("blade", "1.1 叶片", "design_system")
    s.element.create("curved_surface", "1.1.1 曲面", "blade")
    s.element.create("manufacture_test_system", "2. 制造检测系统", "blade_optimize_system", True)
    s.element.create("physical_blade", "2.1 叶片实物", "manufacture_test_system")
    s.element.create("milling_machine", "2.2 铣床", "manufacture_test_system")
    s.element.create("test_device", "2.3 检测设备", "manufacture_test_system", True)
    s.element.create("visual_inspect_device", "2.3.1 视觉检测装置", "test_device")

    s.element.change_print_format("description")
    print(s.element)

    print(s.element.get_element_id())

    s.element.set_parameter_group("blade_optimize_system", [])
    s.element.set_parameter_group("blade", ["blade_CAD"])
    s.element.set_parameter_group("curved_surface", ["eleven_parameter"])
    s.element.set_parameter_group("physical_blade", ["path_parameter"])
    s.element.set_parameter_group("milling_machine", ["technological_parameter"])
    s.element.set_parameter_group("visual_inspect_device", [])

    s.element.set_parameter("blade_optimize_system", [])
    s.element.set_parameter("blade", [["obj_file"]])
    s.element.set_parameter(
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
    s.element.set_parameter("physical_blade", [["Cutter_diameter", "Cutting_depth", "Residual_height"]])
    s.element.set_parameter("milling_machine", [["Cutter_length", "Cutter_angle", "Feed_speed", "Spindle_speed"]])
    s.element.set_parameter("visual_inspect_device", [])

    alist = s.element.tree_element.get_no_tag_nodes()
    for node in alist:
        print(node.parameter_list)
