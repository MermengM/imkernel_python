class NodeBase:
    def __init__(self, id: str, data=None):
        self.id: str = id
        self.data = data
        self.parent: NodeBase = None
        self.children: list[NodeBase] = []

    def add_child(self, child_node: "NodeBase") -> None:
        child_node.parent = self
        self.children.append(child_node)

    def remove_child(self, child_node: "NodeBase") -> None:
        self.children.remove(child_node)
        child_node.parent = None

    def __str__(self) -> str:
        return f"NodeBase(id={self.id}, data={self.data})"
