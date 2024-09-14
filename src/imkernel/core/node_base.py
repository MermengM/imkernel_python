from typing import Optional


class NodeBase:
    """
    树节点基类
    """

    def __init__(self, identification: str, desc: str = None, data=None):
        """
        初始化
        :param identification:标识符
        :param desc:描述
        :param data:扩展数据字段
        """
        self.id = identification
        self.desc = desc
        self.data = data
        self.parent: Optional["NodeBase"] = None
        self.children: list["NodeBase"] = []

    def add_child(self, child_node: "NodeBase") -> None:
        """
        添加子节点
        :param child_node:
        """
        child_node.parent = self
        self.children.append(child_node)

    def remove_child(self, child_node: "NodeBase") -> None:
        """
        移除子节点
        :param child_node:
        """
        self.children.remove(child_node)
        child_node.parent = None

    def __str__(self) -> str:
        return f"NodeBase(id={self.id}, desc={self.desc},data={self.data})"
