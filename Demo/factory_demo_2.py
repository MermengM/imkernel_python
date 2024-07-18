from imkernel.model import UnitCategory, UnitObject, UnitParameter

main_object = UnitObject("MainObject", UnitCategory.M)

# 创建嵌套对象
nested_object = UnitObject("NestedObject", UnitCategory.P)
nested_object.add_parameter(UnitParameter("最底层参数-整数", value_type="int", value=42))

# 将嵌套对象添加到主对象

main_object.add_nested_object("nested", nested_object)

# 访问嵌套对象的参数
print(main_object.nested.nested_param)  # 输出: 42
