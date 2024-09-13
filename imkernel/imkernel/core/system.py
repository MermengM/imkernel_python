from tree_base import TreeBase
from node_base import NodeBase


class Element:
    # 单元对象的结构
    class ElementObject(NodeBase):
        def __init__(self, id: str, description: str = None, is_tag: bool = True) -> None:
            super().__init__(id=id, data=None)
            self.id = id
            self.description = description
            self.is_tag = is_tag

    class ElementTree(TreeBase):
        def __init__(self, print_format="id"):
            super().__init__()
            self.print_format = print_format

        def _format_node(self, node: "Element.ElementObject") -> str:
            """
            限定不同参数条件下树的输出格式
            :param node:节点对象
            """
            if self.print_format == "id":
                return node.id
            if self.print_format == "description":
                return node.description
            if self.print_format == "is_tag":
                return node.is_tag
            if self.print_format == "data":
                return node.data
            return node.id

        def set_node_tag(self, node_id: str | list[str], tag: bool):
            if isinstance(node_id, str):
                self.nodes[node_id].is_tag = tag
            elif isinstance(node_id, list):
                for node_id_ in node_id:
                    self.nodes[node_id_].is_tag = tag

        def get_no_tag_nodes(self) -> list["Element.ElementObject"]:
            """
            获取所有非分组标签节点
            """
            return [node for node in self.nodes.values() if node.is_tag is False]

        def find_node_by_description(self, description: str) -> list["Element.ElementObject"]:
            matched_nodes = []
            for node in self.nodes.values():
                if description in node.description:
                    matched_nodes.append(node)
            return matched_nodes

    def __init__(self):
        self.tree_element = Element.ElementTree()

    def __str__(self) -> str:
        """
        重载默认输出
        """
        return self.tree_element.__str__()

    # region 单元层
    def create(self, id: str, description: str = None, parent_id: str = None, is_tag: bool = False):
        """
        创建单元对象节点
        :param id:唯一标识符
        :param description:中文描述
        :param parent_id:父节点唯一标识符号（留空则为添加根节点）
        :param is_tag:是否是分组标签（分组标签不会在列表中显示/没有参数）
        """
        self.tree_element.add_node(self.ElementObject(id=id, description=description, is_tag=is_tag), parent_id)

    def change_print_format(self, print_format: str):
        """
        设置打印格式
        :param print_format:打印格式，可选值：id, description, is_tag, data
        """
        self.tree_element.print_format = print_format

    def print_tree(self):
        """
        输出单元模型树结构（字符串形式）
        """
        print(self.tree_element.__str__())

    def get_element_id(self):
        """
        展示所有单元对象唯一标识符（除分组节点）
        """
        node_description_list = []
        for node in self.tree_element.get_no_tag_nodes():
            node_description_list.append(node.id)
        return node_description_list

    def get_element_description(self):
        """
        展示所有单元对象介绍（除分组节点）
        """
        node_description_list = []
        for node in self.tree_element.get_no_tag_nodes():
            node_description_list.append(node.description)
        return node_description_list

    def get_by_id(self, id: str):
        """
        根据id 获取指定 element
        :param id:唯一标识符
        """
        node = self.tree_element.find_node_by_id(id)
        return node

    def get_by_description(self, description: str):
        """
        根据 description 获取指定 element
        :param description:描述
        """
        nodes = self.tree_element.find_node_by_description(description=description)
        return nodes

    # endregion

    # region 参数层
    def set_parameter_group(self, id: str, group_name_list: list):
        """
        根据id设置参数组
        :param id:
        :param group_name_list:
        """

        raise Exception("TODO")

    #     示例： ['parameter_group_A', 'parameter_group_B', 'parameter_group_C']
    # endregion


class Method:
    def __init__(self):
        pass


class Procedure:
    def __init__(self):
        pass


class System:
    def __init__(self):
        self.element = Element()
        self.method = Method()
        self.procedure = Procedure()


if __name__ == "__main__":
    # 创建Element实例
    s = System()
    s.element.create("blade_optimize_system", "0. 叶片铣削设计制造系统")
    s.element.create("design_system", "1. 设计系统", "blade_optimize_system", True)
    s.element.create("blade", "1.1 叶片", "design_system")
    s.element.create("curved_surface", "1.1.1 曲面", "blade")
    s.element.create("manufacture_test_system", "2. 制造检测系统", "blade_optimize_system", True)
    s.element.create("physical_blade", "2.1 叶片实物", "manufacture_test_system")
    s.element.create("milling_machine", "2.2 铣床", "manufacture_test_system")
    s.element.create("test_device", "2.3 检测设备", "manufacture_test_system", True)
    s.element.create("visual_inspect_device", "2.3.1 视觉检测装置", "test_device")

    print(s.element)

    s.element.change_print_format("description")
    print(s.element)

    list = s.element.get_by_description("1")
    for elementObject in list:
        print(elementObject.description)

    print(s.element.get_element_id())
