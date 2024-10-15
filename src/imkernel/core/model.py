import json
import os
from typing import Optional, Union, List, Dict, Any
from abc import ABC, abstractmethod
import pandas as pd
import time
import copy

from . import get_algorithm_by_path
from .tree_base import TreeBase
from .node_base import NodeBase
from enum import Enum

from .utils import remove_empty_members


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

    def find_parameters_by_group(self, parameter_group_name):
        # 遍历 parameter_list
        for group in self.parameter_list:
            # 检查 group_name 是否等于指定的 parameter_group_name
            if group['group_name'] == parameter_group_name:
                return group
        # 如果找不到匹配的 group_name，返回 None
        return None

    def get_parameter_list_name(self):
        """
        参数组名
        :return:
        """
        rlist = []
        for x in self.parameter_list:
            rlist.append(x.get('group_name'))
        return rlist

    def get_data_list(self):
        """
        获取单元节点所有data信息
        :return:
        """
        rlist = []
        for x in self.parameter_list:
            rlist.append(x.get('parameter_data'))
        return rlist

    def get_data_by_index(self, index: int):
        """
        获取单元节点指定索引data信息
        :param index:
        """
        combined_dict = {}
        for item in self.parameter_list:
            group_name = item['group_name']
            parameter_data_dict: Dict = item['parameter_data']
            data = parameter_data_dict.get(str(index))
            combined_dict[group_name] = data

        return combined_dict

    def set_parameter_data_by_group_name_index(self, data_index: int, parameter_group_name: str, data_list):
        """
        增加参数数据
        :param data_index:data索引
        :param element_id:单元唯一标识符
        :param parameter_group_name:参数组名称
        :param data_list: 需要增加的参数数据列表
        """
        pg = self.find_parameters_by_group(parameter_group_name)
        if pg is None:
            return
            # raise KeyError(f"{self.id}下没有{parameter_group_name}")

        # 如果 pg['parameter_data'] 还不是字典，先初始化为空字典
        if 'parameter_data' not in pg:
            pg['parameter_data'] = {}

        # 根据 data_index 将 data_list 存储到字典中
        pg['parameter_data'][str(data_index)] = data_list


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

    def get_parameter_data_list(self) -> list:
        """
        获取当前节点所有参数数据列表
        """
        input_data_list = [p.get('parameter_data', []) for p in self.input_parameter_list]
        return input_data_list

    def set_parameter_data_list(self, parameter_data_list: List[List[Any]]) -> None:
        """
        设置当前节点所有参数数据列表

        :param parameter_data_list: 要设置的参数数据列表，应该是一个二维列表，
                                    其中每个子列表对应一个参数组的数据
        """
        output_len = len(self.output_parameter_list)
        if len(parameter_data_list) != len(self.output_parameter_list):
            raise ValueError("参数数据列表长度与输出参数列表长度不匹配")

        for i, data in enumerate(parameter_data_list):
            if 'parameter_data' not in self.output_parameter_list[i]:
                self.output_parameter_list[i]['parameter_data'] = []
            self.output_parameter_list[i]['parameter_data'] = data


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
        self.element_node: Optional[list[ElementNode]] = None
        self.method_node: Optional[MethodNode] = None
        # self.relative_method: MethodNode = None
        # self.relative_element: ElementNode = None
        # 列表中的每个元素是一个字典，字典的 key 表示参数组名称，value 是参数组包含的具体参数
        self.parameter_list: List[Dict[str, List[str]]] = []


class IndustryTree(TreeBase):
    def __init__(self):
        super().__init__()
        self.roots: Dict[str, Union[ElementNode, MethodNode, ProcedureNode]] = {}  # 用于存储森林中的根节点
        self.nodes: Dict[str, Union[ElementNode, MethodNode, ProcedureNode]] = {}  # 用于存储所有节点

    def create_node(self, node: Union[ElementNode, MethodNode, ProcedureNode], parent_id: str = None) -> None:
        """
        添加节点
        :param node: SystemNode 类型的节点
        :param parent_id: 父节点ID（可选）
        """
        super().create_node(node, parent_id)  # 调用父类方法

    def remove_node(self, node: Union[ElementNode, MethodNode, ProcedureNode]):
        """
        删除指定节点
        :param node: 要删除的节点
        """
        super().remove_node(node)

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

    def get_no_tag_nodes_id_list(self) -> List[str]:
        """
        获取所有未被标记为标签的节点ID列表
        :return: 未被标记为标签的节点列表
        """
        return [node.id for node in self.nodes.values() if not node.is_tag]

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

    def _format_node(self, node: NodeBase, format_type, addition_string="√") -> str:
        """
        重写基类_format_node方法
        :param node:
        :param format_type:
        :return:
        """
        node_info = ""
        if format_type == "id":
            node_info = node.id
        elif format_type == "desc":
            node_info = node.desc

        # 是分组标签节点（不参与运算）
        if node.is_tag:
            pass
        else:
            node_info += addition_string
        return node_info

    def _tree_to_dict(self, format_type: str = "id"):
        def node_to_dict(node):
            node_dict = {
                "name": self._format_node(node, format_type, addition_string="")
            }
            if node.children:
                node_dict["children"] = [node_to_dict(child) for child in node.children]
            return node_dict

        roots = self.roots.values()  # 假设树有一个roots属性，是一个包含所有根节点的列表
        return [node_to_dict(root) for root in roots]


class ElementTree(IndustryTree):
    def __init__(self):
        super().__init__()

    def find_node_by_id(self, node_id: str) -> Optional[ElementNode]:
        """
        根据节点ID查找节点
        :param node_id: 节点ID
        :return: 节点或None
        """
        return self.nodes.get(node_id)


class MethodTree(IndustryTree):
    def __init__(self):
        super().__init__()
        self.roots: Dict[str, MethodNode] = {}
        self.nodes: Dict[str, MethodNode] = {}

    def find_node_by_id(self, node_id: str) -> Optional[MethodNode]:
        """
        根据节点ID查找节点
        :param node_id: 节点ID
        :return: 节点或None
        """
        return self.nodes.get(node_id)


class ProcedureTree(IndustryTree):
    def __init__(self):
        super().__init__()

    def get_no_tag_nodes(self) -> List[ProcedureNode]:
        """
        获取所有未被标记为标签的节点
        :return: 未被标记为标签的节点列表
        """
        return [node for node in self.nodes.values() if not node.is_tag]

    def find_node_by_id(self, node_id: str) -> Optional[ProcedureNode]:
        """
        根据节点ID查找节点
        :param node_id: 节点ID
        :return: 节点或None
        """
        return self.nodes.get(node_id)


def process_function_result(func_result):
    if isinstance(func_result, tuple):
        # if len(func_result) == 1:
        #     # 当返回的 tuple 长度为 1 时的处理
        #     return func_result[0]  # 返回 tuple 中的单个元素
        return func_result
    else:
        # 当返回值不是 tuple 时的处理
        return [func_result]


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
        self.model_data = []

    def __str__(self):
        return f"{self.tree},{self.model_type}"

    def create(self, id: str, description: str = None, parent_id: str = None, is_tag: bool = False):
        """
        创建对象节点
        """
        if self.model_type == ModelType.Element:
            self.tree.create_node(ElementNode(model_type=self.model_type, id=id, description=description, is_tag=is_tag), parent_id)
        elif self.model_type == ModelType.Method:
            self.tree.create_node(MethodNode(model_type=self.model_type, id=id, description=description, is_tag=is_tag), parent_id)
        elif self.model_type == ModelType.Procedure:
            self.tree.create_node(ProcedureNode(model_type=self.model_type, id=id, description=description, is_tag=is_tag), parent_id)
        else:
            raise ValueError("类型错误")

    def delete(self, id: str):
        """
        删除对象节点
        :param id: 要删除的节点ID
        """
        node = self.get_by_id(id)
        if node is None:
            print(f"对象 '{id}' 未找到。")
            return
        self.tree.remove_node(node)

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

    def get_group_name_df(self):
        """
        获取group_name的dataframe
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

    def get_by_id_no_tag(self, id: str) -> Optional[Union[ElementNode, MethodNode, ProcedureNode, None]]:
        """
        根据ID查找节点（非tag节点）
        :param id:
        :return:
        """
        node = self.tree.find_node_by_id(id)
        if not node or node.is_tag:
            return None
        return node

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
                node.parameter_list[index]["parameter_data"] = {}
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

    def get_parameter_group_name_list_by_element_id(self, element_id: str) -> list[str]:
        """
        根据id获取参数组列表
        :return:
        """
        output_list = []

        for node_id, node in self.tree.nodes.items():
            node: Union[ElementNode, MethodNode, ProcedureNode]
            if not node.is_tag and node_id == element_id:
                output_list = [p["group_name"] for p in node.parameter_list]
        return output_list

    # endregion 参数层

    # region 数据层
    def add_model_data(self, data_list: List[str]):
        """
        增加模型数据
        :param data_list:数据列表
        """
        raise NotImplementedError("暂不支持")
        pass

    @abstractmethod
    def add_parameter_data(self, param):
        """
        增加参数数据
        :param param:
        """
        raise NotImplementedError("暂未实现")
        pass

    def get_all_data_df(self) -> pd.DataFrame:
        """
        获取所有数据
        :param data_list:数据列表
        """
        nodes_id_list = self.tree.get_no_tag_nodes_id_list()
        data = self.model_data

        # 创建 DataFrame
        df = pd.DataFrame(data, columns=nodes_id_list)
        # 设置索引
        df.index = [f'model[{i}]' for i in range(len(df))]
        return df

    # endregion 数据层
    data = add_model_data
    parameter = set_parameter_by_id
    parameter_group = set_parameter_group_by_id


def filter_and_extract(data_list, index):
    def process_item(item):
        if isinstance(item, list):
            return [process_item(sub_item) for sub_item in item]
        elif isinstance(item, dict):
            return item.get(index, [])
        return []

    return process_item(data_list)


class Element(IndustryModel):
    def __init__(self):
        super().__init__(ModelType.Element)

    def get_parameter_data_by_index(self, index: int) -> dict:
        data_list = []
        for node in self.tree.get_no_tag_nodes():
            para_list = []
            for para in node.parameter_list:
                para_list.append(para.get('parameter_data'))
            data_list.append(para_list)

        filtered_list = filter_and_extract(data_list, str(index))

        return filtered_list
        # real_data_list = data_list[c_index]

    def get_group_name_df(self):
        """
        获取name的dataframe
        :return:
        """
        return pd.DataFrame(self._get_id_list(), columns=["element type"])

    # region 数据层
    def add_model_data(self, data_list: List[str]):
        """
        增加对象层数据
        :param data_list:数据列表
        """
        nodes = self.tree.get_no_tag_nodes()
        if len(nodes) == len(data_list):
            self.model_data.append(data_list)
        else:
            raise ValueError(f"对象数量为{len(nodes)}，与输入数量不匹配")

    def add_parameter_data(self, data_index: int, element_id: str, parameter_group_name: str, data_list):
        """
        增加参数数据
        :param data_index:data索引
        :param element_id:单元唯一标识符
        :param parameter_group_name:参数组名称
        :param data_list: 需要增加的参数数据列表
        """
        if data_index + 1 <= len(self.model_data):
            data = self.model_data[data_index]
            # 在这里添加后续的处理逻辑
        else:
            raise KeyError(f"第{data_index}条数据不存在")
        element = self.tree.find_node_by_id(element_id)
        if not element:
            raise KeyError(f"未找到{element_id}")
        pg = element.find_parameters_by_group(parameter_group_name)
        if pg is None:
            raise KeyError(f"{element.id}下没有{parameter_group_name}")

        # 如果 pg['parameter_data'] 还不是字典，先初始化为空字典
        if 'parameter_data' not in pg:
            pg['parameter_data'] = {}

        # 根据 data_index 将 data_list 存储到字典中
        pg['parameter_data'][str(data_index)] = data_list

    def set_parameter_data_by_id_index(self, data_index: int, element_id: str, parameter_group_name: str, data_list):
        """
        增加参数数据
        :param data_index:data索引
        :param element_id:单元唯一标识符
        :param parameter_group_name:参数组名称
        :param data_list: 需要增加的参数数据列表
        """
        if data_index + 1 <= len(self.model_data):
            data = self.model_data[data_index]
            # 在这里添加后续的处理逻辑
        else:
            raise KeyError(f"第{data_index}条数据不存在")
        element: ElementNode = self.tree.find_node_by_id(element_id)
        if not element:
            raise KeyError(f"未找到{element_id}")
        element.set_parameter_data_by_group_name_index(data_index=data_index, parameter_group_name=parameter_group_name, data_list=data_list)

    # endregion 数据层
    name = get_group_name_df

    def get_all_data_df(self) -> pd.DataFrame:
        """
        获取所有数据并返回DataFrame，修改索引格式为element
        """
        # 调用父类的方法获取DataFrame
        df = super().get_all_data_df()

        # 修改索引
        df.index = [f'element[{i}]' for i in range(len(df))]
        return df

    def get_all_parameter_data_df(self) -> pd.DataFrame:
        """
        获取所有数据并返回DataFrame，修改索引格式为element
        """

        def calc_row(dataa_list):
            max_length = 0
            for sublist in dataa_list:
                for dic in sublist:
                    if isinstance(dic, dict):
                        max_length = max(max_length, len(dic))
                    else:
                        print("Error: Element is not a dictionary:", dic)
            return max_length

        nodes_id_list = self.tree.get_no_tag_nodes_id_list()

        dataa_list = []
        for node in self.tree.get_no_tag_nodes():
            para_list = []
            for para in node.parameter_list:
                para_list.append(para.get('parameter_data'))
            dataa_list.append(para_list)

        max_le = calc_row(dataa_list)
        new_dict = {}
        for x in range(0, max_le):
            new_dict[x] = []
        for column in dataa_list:
            for index in new_dict:
                # Check if the key exists and append the value or None
                #     new_dict[index].append(add_list)
                l = []
                for dic in column:
                    l.append(dic.get(str(index), None))
                new_dict[index].append(l)

        # 转置字典以创建 DataFrame
        df = pd.DataFrame.from_dict(new_dict, orient='index')
        df.columns = nodes_id_list
        df.index = [f'element [{i}]' for i in df.index]  # 设置索引
        return df

    def get_parameter_data(self, element_data_index: int, element_id_or_index: Union[str, int], para_id_or_index: Optional[Union[str, int]] = None):
        """
        根据单元索引+参数Id/参数索引获取指定参数值
        :param element_data_index:单元模型整体数据索引
        :param element_id_or_index:单元模型ID/索引
        """
        # 单元模型表头列表
        element_id_list = self.tree.get_no_tag_nodes_id_list()
        element_id_index = -1
        # 索引
        if isinstance(element_id_or_index, int):
            # 有效
            if element_id_or_index < len(element_id_list):
                element_id_index = element_id_or_index
            else:
                raise Exception(f"索引{element_id_or_index}超出范围")
        elif isinstance(element_id_or_index, str):
            element_id_index = element_id_list.index(element_id_or_index)
            if element_id_index < 0:
                raise Exception(f"参数{element_id_or_index}不存在")
        # 获取指定单元ID
        element_id = element_id_list[element_id_index]
        # 获取指定索引的参数值列表
        element_data_list = self.get_parameter_data_by_index(element_data_index)
        data_list = element_data_list[element_id_index]
        # 如果参数索引为空，直接返回参数组数据
        if para_id_or_index is None:
            return data_list
        # 参数索引不为空，进一步索引

        # 指定单元模型参数组列表
        para_group_list = self.get_parameter_group_name_list_by_element_id(element_id)
        para_group_index = -1
        # 索引
        if isinstance(para_id_or_index, int):
            # 有效
            if para_id_or_index < len(para_group_list):
                para_group_index = para_id_or_index
            else:
                raise Exception(f"索引{para_id_or_index}超出范围")
        # 参数名
        elif isinstance(para_id_or_index, str):
            para_group_index = para_group_list.index(para_id_or_index)
            if para_group_index < 0:
                raise Exception(f"参数{para_id_or_index}不存在")
        # 获取指定参数组名称
        para_group_name = para_group_list[para_group_index]
        para_data_list = data_list[para_group_index]
        return para_data_list

    def get_parameter_group_data_df(self, element_data_index: int, id: str):
        """
        根据单元索引+参数Id获取指定单元所有参数组数据
        :param element_data_index:单元索引
        :param id:参数Id
        """
        # 表头列表
        nodes_id_list = self.tree.get_no_tag_nodes_id_list()
        # 索引
        c_index = nodes_id_list.index(id)
        if c_index < 0:
            raise Exception(f"参数{id}不存在")

        # 获取指定索引的参数值列表
        data_list = self.get_parameter_data_by_index(element_data_index)
        dataa_list = data_list[c_index]

        # 参数组列表
        p_g_list = self.get_parameter_group_name_list_by_element_id(id)
        # 将p_g_list作为key，real_data_list作为value拼接成字典
        result_dict = dict(zip(p_g_list, dataa_list))

        # 找到最长列表的长度
        max_length = max(len(v) for v in result_dict.values())

        # 填充短列表
        for k, v in result_dict.items():
            if len(v) < max_length:
                result_dict[k] = v + [None] * (max_length - len(v))
        df = pd.DataFrame(result_dict)
        return df

    def get_parameter_name_data(self, index, element_id, element_name_index):
        template = {
            'name': '',
            'data': ''
        }
        name_list = self._get_all_parameter_name_list()[element_name_index]
        name_list = name_list[1:]
        data_list = self.get_parameter_data(index, element_id)

        combined_templates = []

        for name, data in zip(name_list, data_list):
            new_template = copy.deepcopy(template)
            new_template['name'] = name
            new_template['data'] = data
            combined_templates.append(new_template)

        return combined_templates

    def get_parameter_group_name_data(self, element_name, element_data_index, element_name_index):
        template = {
            'name': self.get_parameter_group_name_list_by_element_id(element_name),
            'parameters': self.get_parameter_name_data(element_data_index, element_name, element_name_index),
        }
        # template = {
        #     'name': '',
        #     'parameter_groups': ''
        # }
        r_list = []
        # for element_data_index in self.tree.get():
        #     new_template = copy.deepcopy(template)
        #     print(self.model_data[int(element_data_index)][element_name_index])
        #     new_template['name'] = self.model_data[int(element_data_index)][element_name_index]
        #     new_template['parameter_groups'] = self.get_parameter_group_name_data(element_name, element_data_index, element_name_index)
        #     r_list.append(new_template)
        # return r_list
        return template

    def get_element_data(self, element_name, element_name_index):
        template = {
            'name': '',
            'parameter_groups': ''
        }
        r_list = []
        for element_data_index in range(len(self.model_data)):
            new_template = copy.deepcopy(template)
            print(self.model_data[int(element_data_index)][element_name_index])
            new_template['name'] = self.model_data[int(element_data_index)][element_name_index]
            new_template['parameter_groups'] = self.get_parameter_group_name_data(element_name, element_data_index, element_name_index)
            r_list.append(new_template)
        return r_list

    def model_to_dict(self):
        template = {
            'element_index': 0,
            'name': '0',
            'data': [

            ]
        }

        json_list = []

        element_name_list = self.tree.get_no_tag_nodes_id_list()
        for i, element_name in enumerate(element_name_list):
            new_template = copy.deepcopy(template)
            new_template['element_index'] = i
            new_template['name'] = element_name
            new_template['data'] = self.get_element_data(element_name, i)
            json_list.append(new_template)
        return json_list

    def to_json(self):
        """
        获取单元模型所有数据（json)
        :param data_list:数据列表
        """
        r_json = {
            'tree': self.tree._tree_to_dict(),
            'model': self.model_to_dict()

        }
        return r_json


class Method(IndustryModel):
    def __init__(self):
        super().__init__(ModelType.Method)

    # region 对象层

    def get_group_name_df(self):
        """
        获取对象层节点所有id的dataframe
        :return:
        """
        return pd.DataFrame(self._get_id_list(), columns=["method type"])

    def set_program(self, id: str, program: list[str]):
        node: MethodNode = self.tree.find_node_by_id(id)
        node.program = program

    def get_program_by_id(self, id: str):

        node: MethodNode = self.tree.find_node_by_id(id)
        if node is not None:
            return node.program
        else:
            raise Exception("未找到节点")

    def get_program(self):
        columns = ["id", "program"]
        program_list = [(node.id, node.program) for node in self.tree.get_no_tag_nodes()]
        df = pd.DataFrame(program_list, columns=columns)
        return df

    # endregion 对象层

    # region 参数层
    @staticmethod
    def set_input_parameter_group(node: MethodNode, group_name_list: list[str]):
        """
        设置方法模型输入参数组
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
        设置方法模型输出参数组
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
        根据Id设置方法模型输入参数组
        :param id:
        :param group_name_list:
        """
        node = self.tree.find_node_by_id(id)
        self.set_input_parameter_group(node, group_name_list)

    def set_output_parameter_group_by_id(self, id: str, group_name_list: list[str]):
        """
        根据Id设置方法模型输出参数组
        :param id:
        :param group_name_list:
        """
        node = self.tree.find_node_by_id(id)
        self.set_output_parameter_group(node, group_name_list)

    @staticmethod
    def set_input_parameter(node: MethodNode, parameter_name_list_list: list[list[str]]):
        """
        设置节点输入参数
        :param node:节点
        :param parameter_name_list_list:
        """

        for index, group_name in enumerate(parameter_name_list_list):
            # 检查 index 是否在 node.parameter_list 范围内
            if index < len(node.input_parameter_list):
                node.input_parameter_list[index]["parameters"] = group_name
            else:
                # 如果超出范围，则跳过
                print(f" {index} 超过索引")

    @staticmethod
    def set_output_parameter(node: MethodNode, parameter_name_list_list: list[list[str]]):
        """
        设置节点输出参数
        :param node:节点
        :param parameter_name_list_list:
        """

        for index, group_name in enumerate(parameter_name_list_list):
            # 检查 index 是否在 node.parameter_list 范围内
            if index < len(node.output_parameter_list):
                node.output_parameter_list[index]["parameters"] = group_name
            else:
                # 如果超出范围，则跳过
                print(f"索引 {index} 超出范围")

    def set_input_parameter_by_id(self, id: str, parameter_name_list_list: list[list[str]]):
        """
        根据节点Id设置输入参数
        :param id:
        :param parameter_name_list_list:
        """
        node = self.tree.find_node_by_id(id)
        self.set_input_parameter(node, parameter_name_list_list)

    def set_output_parameter_by_id(self, id: str, parameter_name_list_list: list[list[str]]):
        """
        根据节点Id设置输出参数
        :param id:
        :param parameter_name_list_list:
        """
        node = self.tree.find_node_by_id(id)
        self.set_output_parameter(node, parameter_name_list_list)

    def _get_all_input_parameter_group_name_list(self) -> list[str]:
        """
        获取所有输入参数组名称
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
        获取所有输出参数组名称
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
        获取所有输入参数名称
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
        获取所有输出参数名称
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

    # endregion 参数层
    # region 数据层
    def get_parameter_data(self, method_id_or_index: Union[str, int], para_id_or_index: Optional[Union[str, int]] = None):
        """
        获取方法模型的参数数据
        :param method_id_or_index:模型ID/索引
        :param para_id_or_index:模型参数名/索引
        """
        # 方法模型表头列表
        method_id_list = self.tree.get_no_tag_nodes_id_list()
        method_id_index = -1
        # 索引
        if isinstance(method_id_or_index, int):
            # 有效
            if method_id_or_index < len(method_id_list):
                method_id_index = method_id_or_index
            else:
                raise Exception(f"索引{method_id_or_index}超出范围")
        elif isinstance(method_id_or_index, str):
            method_id_index = method_id_list.index(method_id_or_index)
            if method_id_index < 0:
                raise Exception(f"参数{method_id_or_index}不存在")
        # 获取指定单元ID
        method_id = method_id_list[method_id_index]
        data_list = self._get_all_parameter_data_list(2, 2)
        target_data_list = [x for x in data_list if x[0] == method_id_or_index]

        if len(target_data_list) == 0:
            raise Exception(f"{method_id_or_index}不存在")
        elif len(target_data_list) > 1:
            raise Exception(f"{method_id_or_index}不存在")
        target_data_list = target_data_list[0]

        # 如果参数索引为空，直接返回参数组数据
        return_list = target_data_list[1:]
        if para_id_or_index is None:
            return return_list
        # 参数索引不为空，进一步索引

        # 指定单元模型参数组列表
        para_group_index = -1
        # 索引
        if isinstance(para_id_or_index, int):
            # 有效
            if para_id_or_index < len(return_list):
                para_group_index = para_id_or_index
            else:
                raise Exception(f"索引{para_id_or_index}超出范围")
        # 参数名
        elif isinstance(para_id_or_index, str):
            raise Exception(f"当前版本仅接受索引(0,1,2...)取值")
        # 获取指定参数组名称
        return return_list[para_group_index]

    def get_all_data_df(self) -> pd.DataFrame:
        """
        获取所有数据并返回DataFrame，修改索引格式为element
        """
        # 调用父类的方法获取DataFrame
        raise NotImplementedError("暂不支持该方法")

    @staticmethod
    def _add_parameter_data(node: MethodNode, type: str, id: str, data_list):
        """
        增加参数数据
        :param node:方法节点
        :param type:输入输出标识符
        :param id:唯一标识符
        :param data_list: 需要增加的参数数据列表
        """

        if not node:
            raise KeyError(f"未找到{id}")
        parameter_list = []
        if type == "input":
            parameter_list = node.input_parameter_list
        elif type == "output":
            parameter_list = node.output_parameter_list
        else:
            raise TypeError("类型不正确，请指定input/output")
        for index, par_dict in enumerate(parameter_list):
            par_dict['parameter_data'] = data_list[index] if index < len(data_list) else None

    def set_input_parameter_data(self, id: str, data_list):
        """
        设置参数输入数据
        :param id:唯一标识符
        :param data_list: 需要设置的参数数据列表
        """
        node = self.tree.find_node_by_id(id)
        self._add_parameter_data(node=node, id=id, type="input", data_list=data_list)

    def set_output_parameter_data(self, id: str, data_list):
        """
        设置参数输出数据
        :param id:唯一标识符
        :param data_list: 需要设置的参数数据列表
        """
        node = self.tree.find_node_by_id(id)
        self._add_parameter_data(node=node, id=id, type="output", data_list=data_list)

    def _get_all_parameter_data_list(self, max_input_len: int, max_output_len: int):
        """
        获取所有参数数据列表
        :param max_output_len:
        :param max_input_len:
        """
        result_list = []
        for node_id, node in self.tree.nodes.items():
            node: MethodNode
            if not node.is_tag:
                add_list = [node_id]
                input_list = [p.get('parameter_data', []) for p in node.input_parameter_list]
                output_list = [p.get('parameter_data', []) for p in node.output_parameter_list]
                # 调整 input_list 长度为 max_input_len
                if len(input_list) > max_input_len:
                    input_list = input_list[:max_input_len]
                elif len(input_list) < max_input_len:
                    input_list.extend([[] for _ in range(max_input_len - len(input_list))])

                # 调整 output_list 长度为 max_output_len
                if len(output_list) > max_output_len:
                    output_list = output_list[:max_output_len]
                elif len(output_list) < max_output_len:
                    output_list.extend([[] for _ in range(max_output_len - len(output_list))])

                add_list.extend(input_list)
                add_list.extend(output_list)
                result_list.append(add_list)
        return result_list

    def get_parameter_data_by_index(self, index: int) -> dict:
        data_list = []
        for node in self.tree.get_no_tag_nodes():
            node: MethodNode
            para_list = []
            for para in node.input_parameter_list:
                para_list.append(para.get('parameter_data'))
            data_list.append(para_list)

        filtered_list = filter_and_extract(data_list, str(index))

        return filtered_list
        # real_data_list = data_list[c_index]

    def get_parameter_data_df(self, id: str = None):
        """
        展示方法parameter data
        :param id:
        :return:
        """
        max_input_len = 2
        max_output_len = 2
        if id is None or id.strip() == "":
            # 获取所有
            method_name_list = self.tree.get_no_tag_nodes_id_list()
            output_list = self._get_all_parameter_data_list(max_input_len, max_output_len)
            df = pd.DataFrame(output_list)
            # 设置列名
            columns = ["method_name"] + [f"input_{i}" for i in range(0, max_input_len)] + [f"output_{i}" for i in range(0, max_output_len)]
            df.columns = columns
        else:
            node = self.tree.find_node_by_id(id)
            if not node or node.is_tag:
                raise Exception(f"未找到{id}")
            output_list = []
            all_output_list = self._get_all_parameter_data_list(max_input_len, max_output_len)
            for row in all_output_list:
                if row and str(row[0]) == str(id):
                    output_list = row
            df = pd.DataFrame([output_list])
            # 设置列名
            columns = ["method_name"] + [f"input_{i}" for i in range(0, max_input_len)] + [f"output_{i}" for i in range(0, max_output_len)]
            df.columns = columns
        return df

    # endregion 数据层
    # region 分析方法

    def run(self, id: str):
        """
        使用方法模型数据运行方法
        :param id: 方法名
        """

        node: MethodNode = self.tree.find_node_by_id(id)
        if node.is_tag or node is None:
            raise Exception("节点不存在")
        program = self.get_program_by_id(node.id)

        if program is None:
            raise Exception("程序未指定")
        # 分割py路径，函数名称
        method_body, method_name = os.path.split(program[0])
        if not method_body or not method_name:
            raise Exception("方法体/方法获取失败")
        input_par_list = [p.get('parameters', []) for p in node.input_parameter_list]
        # input_data_list = [p.get('parameter_data', []) for p in node.input_parameter_list]
        input_data_list = node.get_parameter_data_list()
        print(f"方法体：{method_body}，方法：{method_name}")
        print(f"参数：{input_par_list}")
        print(f"参数值：{input_data_list}")

        # print(f"尝试导入方法体")
        # 获取算法
        function = get_algorithm_by_path(method_body, method_name)
        if not function:
            raise Exception(f"未能导入{method_name}")
        # print(f"成功导入算法: {method_name}")

        # format_input = remove_empty_members(input_data_list)

        # 开始计时
        start_time = time.time()
        func_result = function(*input_data_list)
        format_result = process_function_result(func_result)

        # 结束计时
        end_time = time.time()

        # 计算耗时
        execution_time = end_time - start_time

        node.set_parameter_data_list(format_result)

        print(f"算法运行完毕，耗时：{execution_time:.4f}秒")
        # logger.info(result)
        return func_result

    # endregion
    name = get_group_name_df
    input_parameter_group = set_input_parameter_group_by_id
    output_parameter_group = set_output_parameter_group_by_id
    input_parameter = set_input_parameter_by_id
    output_parameter = set_output_parameter_by_id
    input_parameter_data = set_input_parameter_data
    output_parameter_data = set_output_parameter_data

    def to_json(self):
        """
        获取方法模型所有数据（json)
        :param data_list:数据列表
        """
        r_json = {'tree': self.tree._tree_to_dict()}
        return r_json


class Procedure(IndustryModel):
    def __init__(self, model):
        super().__init__(ModelType.Procedure)
        self.model: Model = model

    def get_all_data_df(self) -> pd.DataFrame:
        """
        获取所有数据并返回DataFrame，修改索引格式为element
        """
        # 调用父类的方法获取DataFrame
        df = super().get_all_data_df()

        # 修改索引
        df.index = [f'procedure[{i}]' for i in range(len(df))]
        return df

    def get_group_name_df(self):
        """
        获取name的dataframe
        :return:
        """
        return pd.DataFrame(self._get_id_list(), columns=["procedure name"])

    def relate(self, procedure_name: str, element_id: Optional[Union[list[str], str]], method_id: Optional[str]):
        procedure_node: ProcedureNode = self.get_by_id_no_tag(procedure_name)
        element_node_list = []
        if procedure_node is None:
            raise Exception(f"流程模型{procedure_name}未找到")
        if isinstance(element_id, list):
            # 关联多个单元模型
            for element in element_id:
                e_node: ElementNode = self.model.element.get_by_id_no_tag(element)
                if e_node is None:
                    raise Exception(f"单元模型{element_id}未找到")
                element_node_list.append(e_node)
        elif isinstance(element_id, str):
            e_node: ElementNode = self.model.element.get_by_id_no_tag(element_id)
            if e_node is None:
                raise Exception(f"单元模型{element_id}未找到")
            element_node_list.append(e_node)
        m_node: MethodNode = self.model.method.get_by_id_no_tag(method_id)
        if m_node is None:
            raise Exception(f"方法模型{method_id}未找到")
        # program = self.get_program_by_id(p_node.id)
        #
        # procedure_node: MethodNode =  .get_by_id(procedure_name)
        #
        procedure_node.element_node = element_node_list
        procedure_node.method_node = m_node

    def show_relation(self):
        relation_list: list[list] = []
        for node in self.tree.get_no_tag_nodes():
            node: ProcedureNode
            relation_list.append([
                node.id,
                [x.id for x in node.element_node] if node.element_node else None,
                node.method_node.id if node.method_node else None
            ])
        df = pd.DataFrame(relation_list, columns=["procedure name", "element name", "method name"])
        return df

    def run(self, id: str, element_index: int):
        """
        运行指定流程
        :param id:唯一标识符
        :param element_index:
        """

        procedure_node: ProcedureNode = self.tree.find_node_by_id(id)
        if procedure_node.is_tag or procedure_node is None:
            raise Exception("过程模型不存在")
        element_node_list = procedure_node.element_node
        method_node = procedure_node.method_node
        if element_node_list is None or method_node is None:
            raise Exception("未绑定单元/方法模型")

        program = method_node.program

        if program is None:
            raise Exception("程序未指定")
        # 分割py路径，函数名称
        method_body, method_name = os.path.split(program[0])
        if not method_body or not method_name:
            raise Exception("方法体/方法获取失败")

        # 处理输入输出参数
        method_input_group_name = [p.get('group_name', []) for p in method_node.input_parameter_list]
        method_input = [p.get('parameters', []) for p in method_node.input_parameter_list]
        method_output_group_name = [p.get('group_name', []) for p in method_node.output_parameter_list]
        method_output = [p.get('parameters', []) for p in method_node.output_parameter_list]
        element_input_group_name = [element_node.get_parameter_list_name() for element_node in element_node_list]
        element_input = [element_node.get_data_list() for element_node in element_node_list]
        print(min([len(e) for e in element_input]))
        # 获取数据
        if element_index > min([len(e) for e in element_input]):
            raise Exception(f"数据索引{element_index}超出范围")
        # real_data = element_input[element_index]

        # 将所有单元模型的参数组字典合并为一个列表
        real_data_list = {k: v for d in [e.get_data_by_index(element_index) for e in element_node_list] for k, v in d.items()}

        # 使用字典推导式创建新的字典，只包含指定的键
        matched_input_data = {key: real_data_list[key] for key in method_input_group_name if key in real_data_list}
        print(f"方法体：{method_body}，方法：{method_name}")
        print(f"方法模型输入参数组：{method_input_group_name}")
        print(f"方法模型输出参数组：{method_output_group_name}")
        print(f"单元模型参数组：{[k for k, v in real_data_list.items()]}")
        print(f"匹配到{len(matched_input_data)}条输入参数组：{[k for k, v in matched_input_data.items()]}")

        # 提取 matched_data 的值到一个列表
        real_input_list = list(matched_input_data.values())

        # print(f"参数：{input_par_list}")
        # print(f"参数值：{input_data_list}")

        print(f"尝试导入方法体")
        # 获取算法
        function = get_algorithm_by_path(method_body, method_name)
        if not function:
            raise Exception(f"未能导入{method_name}")
        print(f"成功导入算法: {method_name}")

        # format_input = remove_empty_members(real_input_list)

        # 开始计时
        start_time = time.time()
        func_result = function(*real_input_list)
        format_result = process_function_result(func_result)

        # 结束计时
        end_time = time.time()

        # 计算耗时
        execution_time = end_time - start_time

        print(f"算法运行完毕，耗时：{execution_time:.4f}秒")
        matched_output_data = dict(zip(method_output_group_name, format_result))
        print(f"匹配到{len(matched_output_data)}条输出参数组：{[k for k, v in matched_output_data.items()]}")
        # print(f"算法运行匹配结果：{matched_output_data}")
        for group_name, data in matched_output_data.items():
            for element_node in element_node_list:
                element_node.set_parameter_data_by_group_name_index(data_index=element_index, parameter_group_name=group_name, data_list=data)

        # logger.info(result)
        return func_result

    def to_json(self):
        """
        获取过程模型所有数据（json)
        :param data_list:数据列表
        """
        r_json = {'tree': self.tree._tree_to_dict()}
        return r_json

    name = get_group_name_df


class Model:
    def __init__(self):
        self.element = Element()
        self.method = Method()
        self.procedure = Procedure(self)

    def to_json(self):
        r_json = {
            "element": self.element.to_json(),
            "method": self.method.to_json(),
            "procedure": self.procedure.to_json(),

        }
        return json.dumps(r_json)
