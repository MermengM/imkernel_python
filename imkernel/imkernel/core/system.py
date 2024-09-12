from treelib import Tree, Node


class Element:
    # 单元对象的结构
    class ElementObject:
        def __init__(self, id: str, description: str = None, parent_id: str = None, has_parameters: bool = True) -> None:
            self.id = id
            self.description = description
            self.parent_id = parent_id
            self.has_parameters = has_parameters

    def __init__(self):
        self.tree_element = Tree()
        self.tree_element_list = []

    def __str__(self) -> str:
        """
        重载默认输出
        """
        return self.tree_element.__str__()

    # region 单元层
    def create_node(self, id: str, description: str = None, parent_id: str = None, has_parameters: bool = True):
        self.tree_element.create_node(description, id, parent_id)
        self.tree_element_list.append(self.ElementObject(id, description, parent_id, has_parameters))

    def create(self, id: str, description: str = None, parent_id: str = None, is_tag: bool = False):
        """
        创建单元对象节点
        :param id:唯一标识符
        :param description:中文描述
        :param parent_id:父节点唯一标识符号（留空则为添加根节点）
        :param is_tag:是否是分组标签（分组标签不会在列表中显示/没有参数）
        """
        self.tree_element.create_node(description, id, parent_id)

    def print_tree(self):
        """
        输出单元模型树结构（字符串形式）
        """
        print(self.tree_element.__str__())

    def print(self):
        """
        输出单元模型树结构（字符串形式）
        """
        raise Exception("TODO")

    def get_element_name(self):
        """
        展示所有单元对象唯一标识符（除分组节点）
        """
        raise Exception("TODO")

    def get_element_description(self):
        """
        展示所有单元对象介绍（除分组节点）
        """
        raise Exception("TODO")

    def get_by_id(self, id: str):
        """
        根据id 获取指定 element
        :param id:唯一标识符
        """
        node = self.tree_element.get_node(id)
        raise Exception("TODO")

    def get_by_name(self, id: str):
        """
        根据id 获取指定 element
        :param id:唯一标识符
        """
        node = self.tree_element.get_node(id)
        raise Exception("TODO")

    def get_by_description(self, description: str):
        """
        根据 description 获取指定 element
        :param description:描述
        """
        node = self.tree_element.get_node(id)
        raise Exception("TODO")

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
    s.element.create('1', '测试1', )
    s.element.create('2', '测试2', '1')
    s.element.create('3', '测试3', '2')
    s.element.create('4', '测试4', '1')
    print(s.element)
    s.element.get_by_id(6)
