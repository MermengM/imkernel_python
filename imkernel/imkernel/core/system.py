
class Node:
    def __init__(self, tag=None, identifier=None, data=None):
        self.tag = tag
        self.identifier = identifier
        self.data = data
        self._predecessor = None
        self._successors = []

    def set_predecessor(self, predecessor):
        self._predecessor = predecessor

    def add_successor(self, successor):
        self._successors.append(successor)

    def is_leaf(self):
        return len(self._successors) == 0

    def __repr__(self):
        return f"Node(tag={self.tag}, id={self.identifier})"


class ElementObject:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name

    def __str__(self):
        return f"Element(id='{self.id}', name='{self.name}')"

    def __repr__(self):
        return self.__str__()
class Element:
    def __init__(self):
        pass

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
if __name__ == '__main__':
    # 创建Element实例
    element1 = ElementObject("001", "Hydrogen")
    element2 = ElementObject("002", "Helium")

    # 打印元素
    print(element1)  # 输出: Element(id='001', name='Hydrogen')
    print(element2)  # 输出: Element(id='002', name='Helium')

    # 访问属性
    print(element1.id)  # 输出: 001
    print(element1.name)  # 输出: Hydrogen