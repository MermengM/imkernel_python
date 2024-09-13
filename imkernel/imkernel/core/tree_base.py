from .node_base import NodeBase


class TreeBase:
    def __init__(self):
        self.roots: dict[str, NodeBase] = {}  # 用于存储森林中的根节点
        self.nodes: dict[str, NodeBase] = {}  # 用于存储所有节点

    def add_node(self, node: NodeBase, parent_id: str = None) -> None:
        # 如果没有 parent_id，则该节点是根节点
        if parent_id is None:
            if node.id in self.roots:
                raise ValueError(f"Node with id {node.id} already exists as a root.")
            self.roots[node.id] = node
        else:
            parent_node = self.nodes.get(parent_id)
            if parent_node:
                parent_node.add_child(node)
            else:
                raise ValueError(f"Parent node with id {parent_id} not found.")

        # 添加到节点字典中
        self.nodes[node.id] = node

    def remove_node(self, node_id: str) -> None:
        node = self.nodes.pop(node_id, None)
        if node:
            if node.parent:
                node.parent.remove_child(node)
            # 如果删除的是根节点，更新根节点列表
            if node.id in self.roots:
                del self.roots[node.id]
            for child in node.children:
                self.remove_node(child.id)

    def find_node_by_id(self, node_id) -> NodeBase | None:
        return self.nodes.get(node_id)

    def _format_node(self, node: NodeBase) -> str:
        return node.id

    def _print_tree(self, node: NodeBase, prefix: str = "", is_last: bool = True) -> str:
        """Helper method to print the tree structure"""
        connector = "└── " if is_last else "├── "
        result = prefix + connector + f"{self._format_node(node)}\n"
        prefix += "    " if is_last else "│   "
        children = node.children
        for i, child in enumerate(children):
            result += self._print_tree(child, prefix, i == len(children) - 1)
        return result

    def __str__(self) -> str:
        tree_str = ""
        for root in self.roots.values():
            tree_str += self._print_tree(root)
        return tree_str


# 示例
if __name__ == "__main__":
    tree = TreeBase(print_format="name")
    root1 = NodeBase("blade_optimize_system", {"name": "0.叶片铣削设计制造系统"})
    child1 = NodeBase("design_system", {"name": "1.设计系统"})
    child2 = NodeBase("blade", {"name": "1.1.叶片"})
    child3 = NodeBase("curved_surface", {"name": "1.1.1.曲面"})
    child4 = NodeBase("manufacture_test_system", {"name": "2.制造检测系统"})
    child5 = NodeBase("physical_blade", {"name": "2.1.叶片实物"})
    child6 = NodeBase("milling_machine", {"name": "2.2.铣床"})
    child7 = NodeBase("test_device", {"name": "2.3.检测设备"})
    child8 = NodeBase("visual_inspect_device", {"name": "2.3.1.视觉检测装置"})

    tree.add_node(root1)
    tree.add_node(child1, "blade_optimize_system")
    tree.add_node(child2, "design_system")
    tree.add_node(child3, "blade")
    tree.add_node(child4, "blade_optimize_system")
    tree.add_node(child5, "manufacture_test_system")
    tree.add_node(child6, "manufacture_test_system")
    tree.add_node(child7, "manufacture_test_system")
    tree.add_node(child8, "test_device")

    print(tree)
