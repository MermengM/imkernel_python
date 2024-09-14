from typing import Optional, Union, List, Dict

from .tree_base import TreeBase
from .node_base import NodeBase
from enum import Enum


class ModelType(Enum):
    """模型类型枚举"""

    # 单元模型
    Element = "Element"
    # 方法模型
    Method = "Method"
    # 过程模型
    Procedure = "Procedure"


class SystemNode(NodeBase):
    """
    系统基类对象，继承自NodeBase，增加了模型类型、标签标识和参数列表等属性。
    """

    def __init__(self, model_type: ModelType, id: str, description: str = None, is_tag: bool = False) -> None:
        """
        初始化 BaseSystemObject

        :param model_type: 模型类型，表示系统对象所属的类型。
        :param id: 标识符，继承自 NodeBase 的 identification。
        :param description: 描述，继承自 NodeBase 的 desc。
        :param is_tag: 是否为标签，默认值为 False。
        """
        super().__init__(identification=id, desc=description)
        self.model_type: ModelType = model_type  # 模型类型
        self.is_tag: bool = is_tag  # 是否为标签
        # 列表中的每个元素是一个字典，字典的 key 表示参数组名称，value 是参数组包含的具体参数
        self.parameter_list: List[Dict[str, List[str]]] = []


class IndustryTree(TreeBase):
    def __init__(self):
        super().__init__()
        self.roots: Dict[str, SystemNode] = {}  # 用于存储森林中的根节点
        self.nodes: Dict[str, SystemNode] = {}  # 用于存储所有节点

    def add_node(self, node: SystemNode, parent_id: str = None) -> None:
        """
        添加节点
        :param node: SystemNode 类型的节点
        :param parent_id: 父节点ID（可选）
        """
        super().add_node(node, parent_id)  # 调用父类方法

    def set_node_tag(self, node_id: Union[str, List[str]], tag: bool) -> None:
        """
        设置节点的标签状态
        :param node_id: 节点ID(或节点ID列表)
        :param tag: 标签状态(True 或 False)
        """
        if isinstance(node_id, str):
            self.nodes[node_id].is_tag = tag
        elif isinstance(node_id, list):
            for node_id_ in node_id:
                self.nodes[node_id_].is_tag = tag

    def get_no_tag_nodes(self) -> List[SystemNode]:
        """
        获取所有未被标记为标签的节点
        :return: 未被标记为标签的节点列表
        """
        return [node for node in self.nodes.values() if not node.is_tag]

    def find_node_by_description(self, description: str) -> List[SystemNode]:
        """
        根据描述查找节点
        :param description: 描述
        :return: 节点列表
        """
        return [node for node in self.nodes.values() if description in node.desc]

    def find_node_by_id(self, node_id: str) -> Optional[SystemNode]:
        """
        根据节点ID查找节点
        :param node_id: 节点ID
        :return: 节点或None
        """
        return self.nodes.get(node_id)


class BaseIndustryModel:
    """
    三维四层统一模型基类
    """

    def __init__(self, model_type: ModelType):
        self.tree = IndustryTree()
        self.model_type = model_type

    def __str__(self):
        return f"{self.tree},{self.model_type}"

    def create(self, id: str, description: str = None, parent_id: str = None, is_tag: bool = False):
        """
        创建对象节点
        """
        self.tree.add_node(SystemNode(model_type=self.model_type, id=id, description=description, is_tag=is_tag), parent_id)

    def print_tree(self):
        """
        打印Id树
        """
        print(self.tree.print_id())

    def print_tree_desc(self):
        """
        打印描述树
        """
        print(self.tree.print_desc())

    def get_by_id(self, id: str) -> Optional[NodeBase]:
        return self.tree.find_node_by_id(id)

    def get_by_description(self, desc: str) -> list[SystemNode]:
        return self.tree.find_node_by_description(desc)

    def get_ids(self) -> list[str]:
        return [node.id for node in self.tree.get_no_tag_nodes()]

    def get_descriptions(self) -> list[str]:
        return [node.description for node in self.tree.get_no_tag_nodes()]

    def set_parameter_group(self, id: str, group_name_list: list[str]):
        node = self.tree.find_node_by_id(id)
        for group_name in group_name_list:
            node.parameter_list.append({"group_name": group_name, "parameters": []})

    def set_parameter(self, id: str, parameter_name_list_list: list[list[str]]):
        node = self.tree.find_node_by_id(id)
        for index, group_name in enumerate(node.parameter_list):
            group_name["parameters"] = parameter_name_list_list[index]


class Element(BaseIndustryModel):
    def __init__(self):
        super().__init__(ModelType.Element)


class Method(BaseIndustryModel):
    def __init__(self):
        super().__init__(ModelType.Method)


class Procedure(BaseIndustryModel):
    def __init__(self):
        super().__init__(ModelType.Procedure)


#
# class Element:
#     # 单元对象的结构
#
#     class ElementTree(TreeBase):
#         def __init__(self, print_format="id"):
#             super().__init__()
#             self.print_format = print_format
#
#         def _format_node(self, node: BaseSystemObject) -> str:
#             """
#             限定不同参数条件下树的输出格式
#             :param node:节点对象
#             """
#             if self.print_format == "id":
#                 return node.id
#             if self.print_format == "description":
#                 return node.description
#             if self.print_format == "is_tag":
#                 return node.is_tag
#             if self.print_format == "data":
#                 return node.data
#             return node.id
#
#         def set_node_tag(self, node_id: Union[str, List[str]], tag: bool):
#             if isinstance(node_id, str):
#                 self.nodes[node_id].is_tag = tag
#             elif isinstance(node_id, list):
#                 for node_id_ in node_id:
#                     self.nodes[node_id_].is_tag = tag
#
#         def get_no_tag_nodes(self) -> list[BaseSystemObject]:
#             """
#             获取所有非分组标签节点
#             """
#             return [node for node in self.nodes.values() if node.is_tag is False]
#
#         def find_node_by_description(self, description: str) -> list[BaseSystemObject]:
#             matched_nodes = []
#             for node in self.nodes.values():
#                 if description in node.description:
#                     matched_nodes.append(node)
#             return matched_nodes
#
#     def __init__(self):
#         self.tree_element = Element.ElementTree()
#
#     def __str__(self) -> str:
#         """
#         重载默认输出
#         """
#         return self.tree_element.__str__()
#
#     # region 单元层
#     def create(self, id: str, description: str = None, parent_id: str = None, is_tag: bool = False):
#         """
#         创建单元对象节点
#         :param id:唯一标识符
#         :param description:中文描述
#         :param parent_id:父节点唯一标识符号（留空则为添加根节点）
#         :param is_tag:是否是分组标签（分组标签不会在列表中显示/没有参数）
#         """
#         self.tree_element.add_node(BaseSystemObject(industry_model_type=IndustryModelType.Element, id=id, description=description, is_tag=is_tag), parent_id)
#
#     def change_print_format(self, print_format: str):
#         """
#         设置打印格式
#         :param print_format:打印格式，可选值：id, description, is_tag, data
#         """
#         self.tree_element.print_format = print_format
#
#     def print_tree(self):
#         """
#         输出单元模型树结构（字符串形式）
#         """
#         print(self.tree_element.__str__())
#
#     def get_element_id(self) -> list[str]:
#         """
#         展示所有单元对象唯一标识符（除分组节点）
#         """
#         node_description_list: list[str] = []
#         for node in self.tree_element.get_no_tag_nodes():
#             node_description_list.append(node.id)
#         return node_description_list
#
#     def get_element_description(self) -> list[str]:
#         """
#         展示所有单元对象介绍（除分组节点）
#         """
#         node_description_list: list[str] = []
#         for node in self.tree_element.get_no_tag_nodes():
#             node_description_list.append(node.description)
#         return node_description_list
#
#     def get_by_id(self, id: str) -> Optional[NodeBase]:
#         """
#         根据id 获取指定 element
#         :param id:唯一标识符
#         """
#         node: Optional[NodeBase] = self.tree_element.find_node_by_id(id)
#         return node
#
#     def get_by_description(self, description: str) -> list[BaseSystemObject]:
#         """
#         根据 description 获取指定 element
#         :param description:描述
#         """
#         nodes: list[BaseSystemObject] = self.tree_element.find_node_by_description(description=description)
#         return nodes
#
#     # endregion
#
#     # region 参数层
#     def set_parameter_group(self, id: str, group_name_list: list[str]):
#         """
#         根据id设置参数组
#         :param id:
#         :param group_name_list:
#         """
#         node: Element.ElementObject = self.tree_element.find_node_by_id(id)
#         for group_name in group_name_list:
#             node.parameter_list.append({"group_name": group_name, "parameters": []})
#
#     #     示例： ['parameter_group_A', 'parameter_group_B', 'parameter_group_C']
#
#     def set_parameter(self, id: str, parameter_name_list_list: list[list[str]]):
#         """
#         根据id设置详细参数
#         :param id:
#         :param parameter_name_list_list:
#         """
#         node: Element.ElementObject = self.tree_element.find_node_by_id(id)
#         for index, group_name in enumerate(node.parameter_list):
#             group_name["parameters"] = parameter_name_list_list[index]
#
#     # endregion


class System:
    def __init__(self):
        self.element = Element()
        self.method = Method()
        self.procedure = Procedure()
