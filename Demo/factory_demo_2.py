from imkernel.model import UnitCategory, Element, ElementParameter

main_object = Element("MainObject", UnitCategory.M)

# 创建嵌套对象
nested_object = Element("NestedObject", UnitCategory.P)
nested_object.add_parameter(ElementParameter("最底层参数-整数", value_type="int", value=42))

# 将嵌套对象添加到主对象

main_object.add_nested_object("nested", nested_object)

# 访问嵌套对象的参数
print(main_object.nested.nested_param)  # 输出: 42
