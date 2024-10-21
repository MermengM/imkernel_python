# 创建根节点
from imkernel.core.node import Node

root = Node("Root")

# 创建子节点
child1 = Node("Child 1", parent=root)
child2 = Node("Child 2", parent=root)

# 添加子节点
root.add_child(child1)
root.add_child(child2)

# 创建孙节点
grandchild = Node("Grandchild", parent=child1)
child1.add_child(grandchild)

# 打印节点信息
print(root)
print(child1)
print(child2)
print(grandchild)
