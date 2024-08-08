from imkernel.model import Element, UnitCategory

pipe = Element("管件名称", UnitCategory.M)

# pipe.add_parameter(ElementParameter("名称", value_type="string", value="管件名称"))
# pipe.add_parameter(ElementParameter("类型", value_type="string", value="管件类型"))
# pipe.add_parameter(ElementParameter("文件路径", value_type="string", value="/path/to/file"))
#
# XYZ = Element("XYZ", UnitCategory.M)
# XYZ.add_parameter(ElementParameter("X", value_type="float", value=0.0))
# XYZ.add_parameter(ElementParameter("Y", value_type="float", value=0.0))
# XYZ.add_parameter(ElementParameter("Z", value_type="float", value=0.0))
# pipe.add_parameter(XYZ)
# YBC = Element("YBC", UnitCategory.M)
# YBC.add_parameter(ElementParameter("Y", value_type="float", value=0.0))
# YBC.add_parameter(ElementParameter("B", value_type="float", value=0.0))
# YBC.add_parameter(ElementParameter("C", value_type="float", value=0.0))
# pipe.add_parameter(YBC)
print(pipe)
