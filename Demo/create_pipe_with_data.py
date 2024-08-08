from imkernel.model import Element, UnitCategory, ElementParameter

pipe = Element("管件名称", UnitCategory.M)
# 给管件添加 “名称” 参数
pipe.add_parameter(ElementParameter("名称", value_type="string"))
# 给管件 “名称” 参数赋值
pipe.名称 = "管件001"

# 给管件添加 “类型” 参数，并且直接赋值 “弯管”
pipe.add_parameter(ElementParameter("类型", value_type="string", value="弯管"))

# 给管件添加 “文件路径” 参数
pipe.add_parameter(ElementParameter("文件路径", value_type="string", value="/path/to/file"))
# 给管件 “文件路径” 参数赋值
pipe.文件路径 = r"C:\SHUSHE\IM\Workspace3\steps\pipe-01.STEP"

# 获取指定参数
pipe_type = pipe.类型
print(pipe_type.value)
print("*" * 30)

# 添加XYZ参数
XYZ = Element("XYZ", UnitCategory.M)
XYZ.add_parameter(ElementParameter("X", value_type="float", value=0.0))
XYZ.add_parameter(ElementParameter("Y", value_type="float", value=0.0))
XYZ.add_parameter(ElementParameter("Z", value_type="float", value=0.0))
pipe.add_parameter(XYZ)

# XYZ赋值
pipe.XYZ = [[1, 2, 3], [2, 3, 4]]

YBC = Element("YBC", UnitCategory.M)
pipe_xyz = pipe.XYZ
print(pipe_xyz.value)
print("*" * 30)

YBC.add_parameter(ElementParameter("Y", value_type="float", value=0.0))
YBC.add_parameter(ElementParameter("B", value_type="float", value=0.0))
YBC.add_parameter(ElementParameter("C", value_type="float", value=0.0))

pipe.add_parameter(YBC)
print(pipe.XYZ)
print(pipe.YBC)

print(pipe)

# factory_model = UnitModel("工厂")
# factory_model.add_object(pipe)
# print(factory_model)
# pipe_df = unit_to_nested_dataframe(pipe)
# print(pipe_df)
# # 访问XYZ的X值
# x_value = pipe_df["XYZ"].iloc[0]["X"].iloc[0]
#
# # 修改XYZ的Y值
# pipe_df.at[0, "XYZ"].at[0, "Y"] = 5.0
