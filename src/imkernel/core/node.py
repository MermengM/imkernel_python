from typing import Optional

from imkernel.utils import idgen


class Node:
    """
    树节点基类
    """

    def __init__(self, id, name, node_type, parent: Optional['Node'] = None):
        self.id = id
        self.name = name
        self.node_type = node_type
        self.parent = parent
        self.parent_id = parent.id if parent else None
        self.children = []

    def add_child(self, child: 'Node'):
        child.parent = self
        child.parent_id = self.id
        self.children.append(child)

    def remove_child(self, child: 'Node'):
        if child in self.children:
            self.children.remove(child)
            child.parent = None
            child.parent_id = None

    def print_tree(self, level=0, prefix="", is_last=True):
        # 准备当前节点的前缀
        current_prefix = prefix
        if level > 0:
            current_prefix += "└── " if is_last else "├── "

        # 打印当前节点
        print(current_prefix + self.name)

        # 准备子节点的前缀
        child_prefix = prefix
        if level > 0:
            child_prefix += "    " if is_last else "│   "

        # 递归处理子节点
        for i, child in enumerate(self.children):
            is_last_child = (i == len(self.children) - 1)
            child.print_tree(level + 1, child_prefix, is_last_child)

    def __str__(self):
        return f"Node(id={self.id}, data={self.name}, parent_id={self.parent_id})"

    def __repr__(self):
        return self.__str__()
