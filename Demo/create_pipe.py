from imkernel.model import UnitObject, UnitCategory, UnitParameter

pipe = UnitObject("管件名称", UnitCategory.M)
pipe.add_parameter(UnitParameter("名称", value_type="string", value="管件名称"))
pipe.名称 = "管件001"
pipe.add_parameter(UnitParameter("类型", value_type="string", value="管件类型"))
pipe.类型 = "类型"
pipe.add_parameter(UnitParameter("文件路径", value_type="string", value="/path/to/file"))
pipe.文件路径 = r"C:\SHUSHE\IM\Workspace3\steps\pipe-01.STEP"
pipe.add_parameter(UnitParameter("fit_length", value_type="float", value=100.0))

XYZ = UnitObject("XYZ", UnitCategory.M)
XYZ.add_parameter(UnitParameter("X", value_type="float", value=0.0))
XYZ.add_parameter(UnitParameter("Y", value_type="float", value=0.0))
XYZ.add_parameter(UnitParameter("Z", value_type="float", value=0.0))
pipe.add_parameter(XYZ)

pipe.XYZ = [[1, 2, 3], [2, 3, 4]]
YBC = UnitObject("YBC", UnitCategory.M)
aa = pipe.类型
print(aa.value)
XY = pipe.XYZ
print(XY.value)
YBC.add_parameter(UnitParameter("Y", value_type="float", value=0.0))
YBC.add_parameter(UnitParameter("B", value_type="float", value=0.0))
YBC.add_parameter(UnitParameter("C", value_type="float", value=0.0))

pipe.add_parameter(YBC)
print(pipe.XYZ)

print(pipe.YBC)
print(pipe)


def unit_object_to_dict(unit_obj):
    result = {}
    for param_name, param in unit_obj._parameters.items():
        if isinstance(param, UnitParameter):
            result[param_name] = param.value
        elif isinstance(param, UnitObject):
            result[param_name] = unit_object_to_dict(param)
    return result


import pandas as pd


def unit_object_to_records(unit_obj):
    main_records = []
    nested_dfs = {}

    for param_name, param in unit_obj._parameters.items():
        if not param.is_object:
            main_records.append({
                'parameter': param_name,
                'value': param.value,
                'type': param.value_type
            })
        elif param.is_object:
            if isinstance(param.value, list) and all(isinstance(item, list) for item in param.value):
                # 对于 XYZ 这样的列表参数
                nested_dfs[param_name] = pd.DataFrame(param.value, columns=['X', 'Y', 'Z'])
            elif isinstance(param.value, UnitObject):
                # 对于 YBC 这样的对象参数
                nested_dfs[param_name] = pd.DataFrame(
                    [{p: getattr(param.value, p).value for p in param.value._parameters}])
            elif param.value is None:
                # 处理值为 None 的对象参数
                nested_dfs[param_name] = pd.DataFrame()

            main_records.append({
                'parameter': param_name,
                'value': f'DataFrame:{param_name}',
                'type': 'object'
            })

    main_df = pd.DataFrame(main_records)
    return main_df, nested_dfs


main_df, nested_dfs = unit_object_to_records(pipe)
print(main_df)
print(nested_dfs)
