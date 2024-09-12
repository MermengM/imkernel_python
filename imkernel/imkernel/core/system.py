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

    def create_node(self, id: str, description: str = None, parent_id: str = None, has_parameters: bool = True):
        self.tree_element.create_node(description, id, parent_id)
        self.tree_element_list.append(self.ElementObject(id, description, parent_id, has_parameters))


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
    element1 = ElementObject("001", "Hydrogen")
    element2 = ElementObject("002", "Helium")

    # 打印元素
    print(element1)  # 输出: Element(id='001', name='Hydrogen')
    print(element2)  # 输出: Element(id='002', name='Helium')

    # 访问属性
    print(element1.id)  # 输出: 001
    print(element1.name)  # 输出: Hydrogen
