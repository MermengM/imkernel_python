from typing import Optional, Union, List, Dict

import pandas as pd

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


class ElementNode(NodeBase):
    """
    单元对象，继承自NodeBase，增加了模型类型、标签标识和参数列表等属性。
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


class MethodNode(NodeBase):
    """
    方法对象，继承自NodeBase，增加了模型类型、标签标识和参数列表等属性。
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
        self.program: list[str] = []
        # 列表中的每个元素是一个字典，字典的 key 表示参数组名称，value 是参数组包含的具体参数
        self.input_parameter_list: List[Dict[str, List[str]]] = []
        self.output_parameter_list: List[Dict[str, List[str]]] = []


class ProcedureNode(NodeBase):
    """
    过程对象，继承自NodeBase，增加了模型类型、标签标识和参数列表等属性。
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
        self.roots: Dict[str, Union[ElementNode, MethodNode, ProcedureNode]] = {}  # 用于存储森林中的根节点
        self.nodes: Dict[str, Union[ElementNode, MethodNode, ProcedureNode]] = {}  # 用于存储所有节点

    def add_node(self, node: Union[ElementNode, MethodNode, ProcedureNode], parent_id: str = None) -> None:
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

    def get_no_tag_nodes(self) -> List[Union[ElementNode, MethodNode, ProcedureNode]]:
        """
        获取所有未被标记为标签的节点
        :return: 未被标记为标签的节点列表
        """
        return [node for node in self.nodes.values() if not node.is_tag]

    def find_node_by_description(self, description: str) -> List[Union[ElementNode, MethodNode, ProcedureNode]]:
        """
        根据描述查找节点
        :param description: 描述
        :return: 节点列表
        """
        return [node for node in self.nodes.values() if description in node.desc]

    def find_node_by_id(self, node_id: str) -> Optional[Union[ElementNode, MethodNode, ProcedureNode]]:
        """
        根据节点ID查找节点
        :param node_id: 节点ID
        :return: 节点或None
        """
        return self.nodes.get(node_id)


class ElementTree(IndustryTree):
    def __init__(self):
        super().__init__()


class MethodTree(IndustryTree):
    def __init__(self):
        super().__init__()


class ProcedureTree(IndustryTree):
    def __init__(self):
        super().__init__()


class IndustryModel:
    """
    三维四层统一模型基类
    """

    def __init__(self, model_type: ModelType):
        if model_type == ModelType.Element:
            self.tree = ElementTree()
        elif model_type == ModelType.Method:
            self.tree = MethodTree()
        elif model_type == ModelType.Procedure:
            self.tree = ProcedureTree()
        else:
            raise ValueError("类型错误")

        self.model_type = model_type

    def __str__(self):
        return f"{self.tree},{self.model_type}"

    def create(self, id: str, description: str = None, parent_id: str = None, is_tag: bool = False):
        """
        创建对象节点
        """
        if self.model_type == ModelType.Element:
            self.tree.add_node(ElementNode(model_type=self.model_type, id=id, description=description, is_tag=is_tag), parent_id)
        elif self.model_type == ModelType.Method:
            self.tree.add_node(MethodNode(model_type=self.model_type, id=id, description=description, is_tag=is_tag), parent_id)
        elif self.model_type == ModelType.Procedure:
            self.tree.add_node(ProcedureNode(model_type=self.model_type, id=id, description=description, is_tag=is_tag), parent_id)
        else:
            raise ValueError("类型错误")

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

    def name(self):
        """
        获取name的dataframe
        :return:
        """
        return pd.DataFrame(self._get_id_list(), columns=["element_name"])

    def get_by_id(self, id: str) -> Optional[Union[ElementNode, MethodNode, ProcedureNode, None]]:
        """
        根据ID查找节点
        :param id:
        :return:
        """
        return self.tree.find_node_by_id(id)

    def get_by_description(self, desc: str) -> List[Union[ElementNode, MethodNode, ProcedureNode]]:
        """
        根据描述查找节点
        :param desc:
        :return:
        """
        return self.tree.find_node_by_description(desc)

    def _get_id_list(self) -> list[str]:
        return [node.id for node in self.tree.get_no_tag_nodes()]

    # region 参数层
    @staticmethod
    def set_parameter_group(node: Union[ElementNode, MethodNode, ProcedureNode], group_name_list: list[str]):
        """
        设置节点参数组，避免重复添加
        :param node: 节点
        :param group_name_list: 参数组名称列表
        """
        # 遍历 group_name_list 并检查是否已经存在该参数组
        for group_name in group_name_list:
            # 检查是否已存在具有相同 group_name 的参数组
            if not any(group_name == param_group["group_name"] for param_group in node.parameter_list):
                # 如果不存在，则添加新的参数组
                node.parameter_list.append({"group_name": group_name, "parameters": []})

    def set_parameter_group_by_id(self, id: str, group_name_list: list[str]):
        """
        根据Id设置参数组
        :param id:
        :param group_name_list:
        """
        node = self.tree.find_node_by_id(id)
        self.set_parameter_group(node, group_name_list)

    # 给 set_parameter_group_by_id 取别名
    parameter_group = set_parameter_group_by_id

    @staticmethod
    def set_parameter(node: Union[ElementNode, MethodNode, ProcedureNode], parameter_name_list_list: list[list[str]]):
        """
        设置节点参数
        :param node:节点
        :param parameter_name_list_list:
        """

        for index, group_name in enumerate(parameter_name_list_list):
            # 检查 index 是否在 node.parameter_list 范围内
            if index < len(node.parameter_list):
                node.parameter_list[index]["parameters"] = group_name
            else:
                # 如果超出范围，则跳过
                print(f"Index {index} exceeds the length of parameter_list. Skipping.")

    def set_parameter_by_id(self, id: str, parameter_name_list_list: list[list[str]]):
        """
        根据节点Id设置参数
        :param id:
        :param parameter_name_list_list:
        """
        node = self.tree.find_node_by_id(id)
        self.set_parameter(node, parameter_name_list_list)

    # 给 set_parameter_group_by_id 取别名
    parameter = set_parameter_by_id

    def _get_all_parameter_group_name_list(self) -> list[str]:
        """
        组合单元对象+参数组1、2、3、4...
        :return:
        """
        output_list = []
        for node_id, node in self.tree.nodes.items():
            node: Union[ElementNode, MethodNode, ProcedureNode]
            if not node.is_tag:
                output_list.append([node_id] + [p["group_name"] for p in node.parameter_list])
        return output_list

    def _get_all_parameter_name_list(self) -> list[str]:
        """
        组合单元对象+参数1、2、3、4...
        :return:
        """
        output_list = []
        for node_id, node in self.tree.nodes.items():
            node: Union[ElementNode, MethodNode, ProcedureNode]
            if not node.is_tag:
                output_list.append([node_id] + [p["parameters"] for p in node.parameter_list])
        return output_list

    def show_parameters_group(self):
        input_list = self._get_all_parameter_group_name_list()
        max_len = max(len(sublist) for sublist in input_list)

        normalized_list = [sublist + [""] * (max_len - len(sublist)) for sublist in input_list]

        df = pd.DataFrame(normalized_list)

        # 设置列名
        columns = ["element_type"] + [f"parameter_type_{i}" for i in range(1, df.shape[1])]
        df.columns = columns

        return df

    def show_parameters(self):
        input_list = self._get_all_parameter_name_list()
        max_len = max(len(sublist) for sublist in input_list)

        normalized_list = [sublist + [""] * (max_len - len(sublist)) for sublist in input_list]

        df = pd.DataFrame(normalized_list)

        # 设置列名
        columns = ["element_type"] + [f"parameter_index_{i}" for i in range(1, df.shape[1])]
        df.columns = columns

        return df

    # endregion 参数层


class Element(IndustryModel):
    def __init__(self):
        super().__init__(ModelType.Element)


class Method(IndustryModel):
    def __init__(self):
        super().__init__(ModelType.Method)

    def set_program(self, id: str, program: list[str]):
        node: MethodNode = self.tree.find_node_by_id(id)
        node.program = program

    def get_program(self):
        columns = ["id", "program"]
        program_list = [(node.id, node.program) for node in self.tree.get_no_tag_nodes()]
        df = pd.DataFrame(program_list, columns=columns)
        return df

    @staticmethod
    def set_input_parameter_group(node: MethodNode, group_name_list: list[str]):
        """
        设置节点参数组，避免重复添加
        :param node: 节点
        :param group_name_list: 参数组名称列表
        """
        # 遍历 group_name_list 并检查是否已经存在该参数组
        for group_name in group_name_list:
            # 检查是否已存在具有相同 group_name 的参数组
            if not any(group_name == param_group["group_name"] for param_group in node.input_parameter_list):
                # 如果不存在，则添加新的参数组
                node.input_parameter_list.append({"group_name": group_name, "parameters": []})

    @staticmethod
    def set_output_parameter_group(node: MethodNode, group_name_list: list[str]):
        """
        设置节点参数组，避免重复添加
        :param node: 节点
        :param group_name_list: 参数组名称列表
        """
        # 遍历 group_name_list 并检查是否已经存在该参数组
        for group_name in group_name_list:
            # 检查是否已存在具有相同 group_name 的参数组
            if not any(group_name == param_group["group_name"] for param_group in node.output_parameter_list):
                # 如果不存在，则添加新的参数组
                node.output_parameter_list.append({"group_name": group_name, "parameters": []})

    def set_input_parameter_group_by_id(self, id: str, group_name_list: list[str]):
        """
        根据Id设置参数组
        :param id:
        :param group_name_list:
        """
        node = self.tree.find_node_by_id(id)
        self.set_input_parameter_group(node, group_name_list)

    # 给 set_parameter_group_by_id 取别名
    input_parameter_group = set_input_parameter_group_by_id

    def set_output_parameter_group_by_id(self, id: str, group_name_list: list[str]):
        """
        根据Id设置参数组
        :param id:
        :param group_name_list:
        """
        node = self.tree.find_node_by_id(id)
        self.set_output_parameter_group(node, group_name_list)

    # 给 set_parameter_group_by_id 取别名
    output_parameter_group = set_output_parameter_group_by_id

    @staticmethod
    def set_input_parameter(node: MethodNode, parameter_name_list_list: list[list[str]]):
        """
        设置节点参数
        :param node:节点
        :param parameter_name_list_list:
        """

        for index, group_name in enumerate(parameter_name_list_list):
            # 检查 index 是否在 node.parameter_list 范围内
            if index < len(node.input_parameter_list):
                node.input_parameter_list[index]["parameters"] = group_name
            else:
                # 如果超出范围，则跳过
                print(f"Index {index} exceeds the length of parameter_list. Skipping.")

    @staticmethod
    def set_output_parameter(node: MethodNode, parameter_name_list_list: list[list[str]]):
        """
        设置节点参数
        :param node:节点
        :param parameter_name_list_list:
        """

        for index, group_name in enumerate(parameter_name_list_list):
            # 检查 index 是否在 node.parameter_list 范围内
            if index < len(node.output_parameter_list):
                node.output_parameter_list[index]["parameters"] = group_name
            else:
                # 如果超出范围，则跳过
                print(f"Index {index} exceeds the length of parameter_list. Skipping.")

    def set_input_parameter_by_id(self, id: str, parameter_name_list_list: list[list[str]]):
        """
        根据节点Id设置参数
        :param id:
        :param parameter_name_list_list:
        """
        node = self.tree.find_node_by_id(id)
        self.set_input_parameter(node, parameter_name_list_list)

    # 给 set_parameter_group_by_id 取别名
    input_parameter = set_input_parameter_by_id

    def set_output_parameter_by_id(self, id: str, parameter_name_list_list: list[list[str]]):
        """
        根据节点Id设置参数
        :param id:
        :param parameter_name_list_list:
        """
        node = self.tree.find_node_by_id(id)
        self.set_output_parameter(node, parameter_name_list_list)

    # 给 set_parameter_group_by_id 取别名
    output_parameter = set_output_parameter_by_id

    def _get_all_input_parameter_group_name_list(self) -> list[str]:
        """
        组合单元对象+参数组1、2、3、4...
        :return:
        """
        output_list = []
        for node_id, node in self.tree.nodes.items():
            node: MethodNode
            if not node.is_tag:
                output_list.append([node_id] + [p["group_name"] for p in node.input_parameter_list])
        return output_list

    def _get_all_output_parameter_group_name_list(self) -> list[str]:
        """
        组合单元对象+参数组1、2、3、4...
        :return:
        """
        output_list = []
        for node_id, node in self.tree.nodes.items():
            node: MethodNode
            if not node.is_tag:
                output_list.append([node_id] + [p["group_name"] for p in node.output_parameter_list])
        return output_list

    def _get_all_input_parameter_name_list(self) -> list[str]:
        """
        组合单元对象+参数1、2、3、4...
        :return:
        """
        output_list = []
        for node_id, node in self.tree.nodes.items():
            node: MethodNode
            if not node.is_tag:
                output_list.append([node_id] + [p["parameters"] for p in node.input_parameter_list])
        return output_list

    def _get_all_output_parameter_name_list(self) -> list[str]:
        """
        组合单元对象+参数1、2、3、4...
        :return:
        """
        output_list = []
        for node_id, node in self.tree.nodes.items():
            node: MethodNode
            if not node.is_tag:
                output_list.append([node_id] + [p["parameters"] for p in node.output_parameter_list])
        return output_list

    def show_input_parameters_group(self):
        input_list = self._get_all_input_parameter_group_name_list()
        max_len = max(len(sublist) for sublist in input_list)

        normalized_list = [sublist + [""] * (max_len - len(sublist)) for sublist in input_list]

        df = pd.DataFrame(normalized_list)

        # 设置列名
        columns = ["element_type"] + [f"parameter_type_{i}" for i in range(1, df.shape[1])]
        df.columns = columns

        return df

    def show_output_parameters_group(self):
        input_list = self._get_all_output_parameter_group_name_list()
        max_len = max(len(sublist) for sublist in input_list)

        normalized_list = [sublist + [""] * (max_len - len(sublist)) for sublist in input_list]

        df = pd.DataFrame(normalized_list)

        # 设置列名
        columns = ["element_type"] + [f"parameter_type_{i}" for i in range(1, df.shape[1])]
        df.columns = columns

        return df

    def show_parameters_group(self):
        input_list = self._get_all_input_parameter_group_name_list()
        output_list = self._get_all_output_parameter_group_name_list()
        max_input_len = max(len(sublist) for sublist in input_list)
        max_output_len = max(len(sublist) for sublist in output_list)

        normalized_list = []
        for i, itemIter in enumerate(input_list):
            rowData = []
            for j in range(max_input_len):
                if j < len(input_list[i]):
                    rowData.append(input_list[i][j])
                else:
                    rowData.append("")
            for k in range(max_output_len):
                if k == 0:
                    pass
                elif k < len(output_list[i]):
                    rowData.append(output_list[i][k])
                else:
                    rowData.append("")
            normalized_list.append(rowData)

        df = pd.DataFrame(normalized_list)
        # 设置列名
        columns = ["element_type"] + [f"input_{i}" for i in range(1, max_input_len)] + [f"output_{i}" for i in range(1, max_output_len)]
        df.columns = columns
        return df

    def show_input_parameters(self):
        input_list = self._get_all_input_parameter_name_list()
        max_len = max(len(sublist) for sublist in input_list)

        normalized_list = [sublist + [""] * (max_len - len(sublist)) for sublist in input_list]

        df = pd.DataFrame(normalized_list)

        # 设置列名
        columns = ["element_type"] + [f"parameter_index_{i}" for i in range(1, df.shape[1])]
        df.columns = columns

        return df

    def show_output_parameters(self):
        input_list = self._get_all_output_parameter_name_list()
        max_len = max(len(sublist) for sublist in input_list)

        normalized_list = [sublist + [""] * (max_len - len(sublist)) for sublist in input_list]

        df = pd.DataFrame(normalized_list)

        # 设置列名
        columns = ["element_type"] + [f"parameter_index_{i}" for i in range(1, df.shape[1])]
        df.columns = columns

        return df

    def show_parameters(self):
        input_list = self._get_all_input_parameter_name_list()
        output_list = self._get_all_output_parameter_name_list()
        max_input_len = max(len(sublist) for sublist in input_list)
        max_output_len = max(len(sublist) for sublist in output_list)

        normalized_list = []
        for i, itemIter in enumerate(input_list):
            rowData = []
            for j in range(max_input_len):
                if j < len(input_list[i]):
                    rowData.append(input_list[i][j])
                else:
                    rowData.append("")
            for k in range(max_output_len):
                if k == 0:
                    pass
                elif k < len(output_list[i]):
                    rowData.append(output_list[i][k])
                else:
                    rowData.append("")
            normalized_list.append(rowData)

        df = pd.DataFrame(normalized_list)
        # 设置列名
        columns = ["element_type"] + [f"input_{i}" for i in range(1, max_input_len)] + [f"output_{i}" for i in range(1, max_output_len)]
        df.columns = columns
        return df


class Procedure(IndustryModel):
    def __init__(self):
        super().__init__(ModelType.Procedure)


class System:
    def __init__(self):
        self.element = Element()
        self.method = Method()
        self.procedure = Procedure()
