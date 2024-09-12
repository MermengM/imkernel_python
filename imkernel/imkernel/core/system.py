
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
class System:
    def __init__(
            self,
            element=None,
            method=None,
            procedure=None,
            element_data=None,
            method_parameter=None,
            method_data=None,
            procedure_parameter=None,

    ):
        self.element = {
            "element": "单元模型",
            "method": "方法模型",
            "procedure": "过程模型"}
        self.element_parameter = element if element is not None else []
        self.element_parameter_name = []
        self.element_data = {}
        self.method_parameter = method_parameter if method_parameter is not None else []
        self.method_data = {}
        self.procedure_parameter = procedure_parameter if procedure_parameter is not None else []
        self.dataframes = {
            'element_parameter': self.element_parameter,
            'method_parameter': self.method_parameter,
            'procedure_parameter': self.procedure_parameter
        }
        #
        # # 验证输入的DataFrame
        # for name, df in self.dataframes.items():
        #     if df is not None and not isinstance(df, pd.DataFrame):
        #         raise TypeError(f"{name} 必须是dataframe")

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