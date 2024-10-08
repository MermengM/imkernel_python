from typing import Optional

from .node_base import NodeBase


class TreeBase:
    def __init__(self):
        self.roots: dict[str, NodeBase] = {}  # 用于存储森林中的根节点
        self.nodes: dict[str, NodeBase] = {}  # 用于存储所有节点

    def add_node(self, node: NodeBase, parent_id: str = None) -> None:
        # 如果没有 parent_id，则该节点是根节点
        if parent_id is None:
            if node.id in self.roots:
                raise ValueError(f"根节点 {node.id} 已存在")
            self.roots[node.id] = node
        else:
            parent_node = self.nodes.get(parent_id)
            if parent_node:
                parent_node.add_child(node)
            else:
                raise ValueError(f"根节点 {parent_id} 未找到")

        # 添加到节点字典中
        self.nodes[node.id] = node

    def remove_node(self, node: NodeBase) -> None:
        if node.id in self.nodes:
            del self.nodes[node.id]
            if node.parent:
                node.parent.remove_child(node)
            # 如果删除的是根节点，更新根节点列表
            if node.id in self.roots:
                del self.roots[node.id]
            for child in list(node.children):  # 创建一个子节点列表的副本
                self.remove_node(child)
        else:
            raise Exception(f"未找到名为{node.id}的节点")

    def find_node_by_id(self, node_id) -> Optional[NodeBase]:
        return self.nodes.get(node_id)

    def _format_node(self, node: NodeBase, format_type) -> str:
        if format_type == "id":
            return node.id
        elif format_type == "desc":
            return node.desc

    def _print_tree(self, node: NodeBase, prefix: str = "", is_last: bool = True, format_type: str = 'id') -> str:
        """Helper method to print the tree structure"""
        connector = "└── " if is_last else "├── "
        result = prefix + connector + f"{self._format_node(node, format_type)}\n"
        prefix += "    " if is_last else "│   "
        children = node.children
        for i, child in enumerate(children):
            result += self._print_tree(child, prefix, i == len(children) - 1, format_type=format_type)
        return result

    def _print_tree_with_type(self, format_type: str = "id"):
        tree_str = ""
        for i, root in enumerate(self.roots.values()):
            tree_str += f"{self._format_node(root, format_type)}\n"
            children = root.children
            for j, child in enumerate(children):
                tree_str += self._print_tree(child, "", j == len(children) - 1, format_type=format_type)
            if i < len(self.roots) - 1:
                tree_str += "\n"  # 在根节点之间添加空行
        return tree_str

    def print_id(self):
        """
        返回Id树
        :return:
        """
        return self._print_tree_with_type(format_type="id")

    def print_desc(self):
        """
        返回描述树
        :return:
        """
        return self._print_tree_with_type(format_type="desc")

    def __str__(self) -> str:
        return self.print_id()
