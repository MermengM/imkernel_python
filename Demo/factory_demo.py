# 从imkernel.model模块导入所需的类
from imkernel.model import UnitCategory, UnitModel, Element, ElementParameter

# 创建一个名为"工厂模型"的UnitModel实例
factory = UnitModel(name="工厂模型")

# 创建一个名为"OperatorA"的UnitObject实例，类别为UnitCategory.H
operator_a = Element("OperatorA", UnitCategory.H)
# 将operator_a添加到工厂模型中
factory.add_object(operator_a)

# 为operator_a添加参数 [1,2,3,4,5,6,7,8,9]
operator_a.add_parameter(ElementParameter("input1"))
operator_a.add_parameter(ElementParameter("input2"))
operator_a.add_parameter(ElementParameter("output34"))
operator_a.add_parameter(ElementParameter("param4"))
operator_a.add_parameter(ElementParameter("param5"))
# 为operator_a的参数赋值
operator_a.input1 = 10
operator_a.input2 = "Hello"[1][2]
operator_a.output34 = [1, 2, 3]
operator_a.param4 = {"key": "value"}
operator_a.param5 = True
operator_a.New = True  # 添加一个新的属性
print(operator_a)

#
# # 创建另一个名为"OperatorB"的UnitObject实例，类别也为UnitCategory.H
# operator_b = UnitObject("OperatorB", UnitCategory.H)
#
# # 为operator_b添加参数
# operator_b.add_parameter(UnitParameter("inputA"))
# operator_b.add_parameter(UnitParameter("inputB"))
# operator_b.add_parameter(UnitParameter("outputC"))
# operator_b.add_parameter(UnitParameter("paramD"))
# operator_b.add_parameter(UnitParameter("paramE"))
#
# # 打印operator_a的信息
# print(operator_a)
#
# # 打印operator_b的信息
# print(operator_b)
#
# # 打印整个工厂模型的信息
# print(factory)
#
# # 打印工厂模型中所有类别为UnitCategory.H的对象
# print(factory.get_objects_by_unit_category(UnitCategory.H))
#
# # 打印工厂模型中所有类别为UnitCategory.M的对象（可能为空）
# print(factory.get_objects_by_unit_category(UnitCategory.M))
#
# # 打印工厂模型中所有类别为UnitCategory.P的对象（可能为空）
# print(factory.get_objects_by_unit_category(UnitCategory.P))
