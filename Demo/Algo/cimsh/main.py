import os
import tempfile

import CurveModeling as CM


def make_molded(
        Chord_Length: float = 50,
        Upper_Max_Width: float = 0.4149,
        Upper_Max_Width_Loc: float = 0.2098,
        Upper_Angle: float = 0.0582,
        Upper_tip_coeff: float = 0.4492,
        Upper_aft_part_shape: float = 0.3339,
        Lower_max_width: float = 0.234,
        Lower_max_width_loc: float = 0.7289,
        Lower_Angle: float = 0.2497,
        Lower_tip_coeff: float = 0.52,
        Lower_aft_part_shape: float = 0.8523,
        Tangent_Leading_Edge: float = 0.5,
        Z_height: int = 10,
        **kwargs,
):
    """
    型线生成算法
    @param parameters:输入参数（字典）
        "Chord_Length",adsa
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
        "Z_height"

    @return:点位数据（x，y，z）
    """
    # 处理输入参数
    try:
        true_order = {
            "Chord_Length": Chord_Length,
            "Upper_Max_Width": Upper_Max_Width,
            "Upper_Max_Width_Loc": Upper_Max_Width_Loc,
            "Upper_Angle": Upper_Angle,
            "Upper_tip_coeff": Upper_tip_coeff,
            "Upper_aft_part_shape": Upper_aft_part_shape,
            "Lower_max_width": Lower_max_width,
            "Lower_max_width_loc": Lower_max_width_loc,
            "Lower_Angle": Lower_Angle,
            "Lower_tip_coeff": Lower_tip_coeff,
            "Lower_aft_part_shape": Lower_aft_part_shape,
            "Tangent_Leading_Edge": Tangent_Leading_Edge,
            "Z_height": Z_height,
        }

        for param in true_order:
            if param is None or (isinstance(param, float) and not param > 0):
                raise Exception("参数格式不正确或者为空")

        # 使用临时文件来存储参数和点位数据
        with tempfile.NamedTemporaryFile(
                delete=False, mode="w", suffix=".txt"
        ) as input_file, tempfile.NamedTemporaryFile(
            delete=False, mode="w", suffix=".txt"
        ) as output_file:

            # 写入参数到临时输入文件
            for param in true_order:
                input_file.write(f"{param}: {true_order[param]}\n")

        input_file_path = input_file.name  # 保存输入文件路径
        output_file_path = output_file.name  # 保存输出文件路径

        # section = CM.psds.para metric_section(50,0.4149,0.2098,0.0582,0.4492,0.3339,0.2340,0.7289,0.2497,0.5200,0.8523,0.5000)
        model = CM.CurveModeling(300)
        # model.load_from_Parsection(section)
        model.load_parameter(input_file_path)
        model.calculate_origin_shape()
        # model.draw_origin_shape()
        num_in_each_span = [42, 111, 68, 79]
        span_to_repara = [0, 1, 1, 0]
        model.calculate_sampling_out(num_in_each_span, span_to_repara)

        model.save_sampling_points(output_file_path[:-4], Z_height)
        # model.set_Z_height(Z_height)
        # fitting3D = CM.LSPIA_fitting3D(model, 3, 250, 1e-5)
        # fitting3D.generate_init_controlpoints(4, 30)
        # fitting3D.Curvature_Preparation(0.05)
        # fitting3D.Incremental_LSPIA(2.5, 100, 5, 1e-5)
        # fitting3D.Curvature_Constrained_Refine(0.25, 5)
        # fitting3D.Common_LSPIA()
        # fitting3D.drawfittingCurve()
        # fitting3D.curve_save(rf"fitting_curve_3D_{index}")

        three_point_lines = []  # 用于存储点位

        with open(output_file_path, "r") as file:
            for line in file:
                # 去除两端空白并分割行为单独的元素
                parts = line.strip().split()
                # 检查该行是否恰好有三个元素
                if len(parts) == 3:
                    try:
                        # 尝试将这三个元素转换为浮点数
                        three_point_lines.append(
                            {
                                "x": float(parts[0]),
                                "y": float(parts[1]),
                                "z": float(parts[2]),
                            }
                        )
                    except ValueError:
                        # 如果转换失败（例如，某些元素不是数字），跳过这一行
                        pass

        return three_point_lines
    except Exception as e:
        raise Exception("算法运行错误")

#
# if __name__ == "__main__":
#     # Creating a list by calling make_molded 5 times with different index and Chord_Length
#     results = [make_molded(Z_height=20 * i, index=i + 1) for i in range(2)]
#     print(results)
