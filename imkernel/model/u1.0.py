# class Element:
#     def __init__(self, name, category, attributes=None):
#         self.name = name
#         self.category = category
#         self.attributes = attributes or {}
#         self.children = []
#
#     def add_child(self, child):
#         self.children.append(child)
#
#     def add_attribute(self, key, value):
#         self.attributes[key] = value
#
#     def find_element(self, name):
#         if self.name == name:
#             return self
#         for child in self.children:
#             found = child.find_element(name)
#             if found:
#                 return found
#         return None
#
#     def __str__(self):
#         return self._str_helper()
#
#     def _str_helper(self, level=0):
#         indent = "  " * level
#         result = f"{indent}{self.name} ({self.category}):\n"
#         for key, value in self.attributes.items():
#             result += f"{indent}  {key}: {value}\n"
#         for child in self.children:
#             result += child._str_helper(level + 1)
#         return result
#
# class ElementTree:
#     def __init__(self):
#         self.root = Element("Root", "root")
#
#     def add_element(self, parent_name, name, category, attributes=None):
#         new_element = Element(name, category, attributes)
#         if parent_name == "Root":
#             self.root.add_child(new_element)
#         else:
#             parent = self.root.find_element(parent_name)
#             if parent:
#                 parent.add_child(new_element)
#             else:
#                 raise ValueError(f"Parent element '{parent_name}' not found")
#
#     def __str__(self):
#         return str(self.root)
#
# # 使用示例
# tree = ElementTree()
#
# # 添加顶层类别
# tree.add_element("Root", "Human", "category")
# tree.add_element("Root", "Machine", "category")
# tree.add_element("Root", "Material", "category")
#
# # 添加人员子类别
# tree.add_element("Human", "Men", "subcategory")
# tree.add_element("Human", "Women", "subcategory")
#
# # 添加具体的人员
# tree.add_element("Men", "John", "individual", {"age": 30, "height": 180})
# tree.add_element("Women", "Alice", "individual", {"age": 28, "profession": "engineer"})
#
# # 添加机器子类别
# tree.add_element("Machine", "Robots", "subcategory")
# tree.add_element("Machine", "Computers", "subcategory")
#
# # 添加具体的机器
# tree.add_element("Robots", "Robot001", "individual", {"model": "XR-100", "function": "assembly"})
# tree.add_element("Computers", "PC001", "individual", {"brand": "Dell", "CPU": "Intel i7"})
#
# # 添加物料子类别
# tree.add_element("Material", "Metals", "subcategory")
# tree.add_element("Material", "Plastics", "subcategory")
#
# # 添加具体的物料
# tree.add_element("Metals", "Steel", "type", {"density": 7.8, "melting_point": 1370})
# tree.add_element("Plastics", "PVC", "type", {"density": 1.4, "melting_point": 100})
#
# # 演示无限嵌套
# tree.add_element("Steel", "HighCarbonSteel", "subtype", {"carbon_content": "0.60-1.00%"})
# tree.add_element("HighCarbonSteel", "ToolSteel", "specific_type", {"hardness": "Very high"})
#
# # 打印整个结构
# print(tree)