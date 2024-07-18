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
