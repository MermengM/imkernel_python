from abc import ABC, abstractmethod
from typing import List, Union
from typing import Dict, Any
import pandas as pd
from loguru import logger


class BaseNode(ABC):
    def __init__(self, name: str, id: str):
        self.name = name
        self.id = id
        self.parent = None
        self.children = []

    def add_child(self, child: 'BaseNode'):
        child.parent = self
        self.children.append(child)

    def remove_child(self, child: 'BaseNode'):
        if child in self.children:
            self.children.remove(child)
            child.parent = None

    @abstractmethod
    def get_type(self) -> str:
        pass

    def get_path(self) -> List[str]:
        if self.parent is None:
            return [self.name]
        return self.parent.get_path() + [self.name]


class DataManager:
    def __init__(self):
        self.data_store: Dict[str, Dict[str, Any]] = {}

    def set_data(self, node: BaseNode, key: str, value: Any) -> None:
        node_path = ":".join(node.get_path())
        if node_path not in self.data_store:
            self.data_store[node_path] = {}
        self.data_store[node_path][key] = value

    def get_data(self, node: BaseNode, key: str) -> Any:
        node_path = ":".join(node.get_path())
        return self.data_store.get(node_path, {}).get(key)

    def delete_data(self, node: BaseNode, key: str) -> None:
        node_path = ":".join(node.get_path())
        if node_path in self.data_store and key in self.data_store[node_path]:
            del self.data_store[node_path][key]

    def get_all_data(self, node: BaseNode) -> Dict[str, Any]:
        node_path = ":".join(node.get_path())
        return self.data_store.get(node_path, {})

    def clear_node_data(self, node: BaseNode) -> None:
        node_path = ":".join(node.get_path())
        if node_path in self.data_store:
            del self.data_store[node_path]


class RootNode(BaseNode):
    def __init__(self, name: str, id: str):
        super().__init__(name, id)

    def get_type(self) -> str:
        return "Root"


class UnitObject(BaseNode):
    def __init__(self, name: str, id: str):
        super().__init__(name, id)

    def get_type(self) -> str:
        return "UnitObject"


class UnitParameter(BaseNode):
    def __init__(self, name: str, id: str):
        super().__init__(name, id)

    def get_type(self) -> str:
        return "UnitParameter"


class UnitData(BaseNode):
    def __init__(self, name: str, id: str, value: any = None):
        super().__init__(name, id)
        self.value = value

    def get_type(self) -> str:
        return "UnitData"


class System:
    def __init__(self):
        self.root = RootNode("Root", "0")
        self.node_counter = 1
        self.data_manager = DataManager()

    def generate_unique_id(self) -> str:
        self.node_counter += 1
        return str(self.node_counter)

    # def add_node(self, parent: BaseNode, child: BaseNode):
    #     parent.add_child(child)

    def add_node(self, parent: BaseNode, node: BaseNode, name: str) -> BaseNode:
        parent.add_child(node)
        return node

    def remove_node(self, node: BaseNode) -> None:
        if node.parent:
            node.parent.remove_child(node)
        self.data_manager.clear_node_data(node)

    def _find_matching_nodes(self, object_name: str):
        def search(node, results):
            if node.name == object_name and isinstance(node, UnitObject):
                results.append(node)
            for child in node.children:
                search(child, results)

        results = []
        search(self.root, results)
        return results

    def find_or_create_child(self, parent: BaseNode, name: str, id: str, node_class) -> BaseNode:
        for child in parent.children:
            if child.name == name and isinstance(child, node_class):
                return child
        new_child = node_class(name, id)
        self.add_node(parent, new_child, new_child.name)
        return new_child

    def find_node(self, name: str, start_node: BaseNode = None) -> Union[BaseNode, None]:
        if start_node is None:
            start_node = self.root

        if start_node.name == name:
            return start_node

        for child in start_node.children:
            result = self.find_node(name, child)
            if result:
                return result

        return None

    # region 转换器
    def generate_objects_df(self):
        paths = []
        self._collect_paths(self.root, [], paths, include_parameters=False)
        return self._create_df_from_paths(paths)

    def get_all_data_as_dataframe(self) -> pd.DataFrame:
        data_list = []
        self._collect_all_data(self.root, [], data_list)
        return pd.DataFrame(data_list, columns=['对象', '参数名', '参数值'])

    def _collect_all_data(self, node: BaseNode, current_path: List[str], data_list: List[Dict[str, Any]]):
        node_path = ":".join(current_path + [node.name])
        node_data = self.data_manager.get_all_data(node)

        for key, value in node_data.items():
            data_list.append({
                '对象': node_path,
                '参数名': key,
                '参数值': value
            })

        for child in node.children:
            self._collect_all_data(child, current_path + [node.name], data_list)

    # def generate_parameters_df(self):
    #     param_data = []
    #     self._collect_parameters(self.root, [], param_data)
    #     df = pd.DataFrame(param_data, columns=['单元对象', '参数名'])
    #     return df
    #
    # def _collect_parameters(self, node, current_path, param_data):
    #     if isinstance(node, UnitParameter):
    #         parent_name = current_path[-1] if current_path else 'Root'
    #         param_data.append((parent_name, node.name))
    #     else:
    #         for child in node.children:
    #             self._collect_parameters(child, current_path + [node.name], param_data)

    def generate_parameters_df(self):
        param_data = []
        self._collect_parameters(self.root, [], param_data)
        df = pd.DataFrame(param_data, columns=['单元对象', '单元参数'])
        return df

    def _collect_parameters(self, node, current_path, param_data):
        if isinstance(node, UnitParameter):
            object_path = ' > '.join(current_path) if current_path else 'Root'
            param_data.append((object_path, node.name))
        else:
            for child in node.children:
                self._collect_parameters(child, current_path + [node.name], param_data)

    def generate_elements_df(self):
        paths = []
        for child in self.root.children:
            self._collect_paths(child, [], paths, include_parameters=True)
        return self._create_df_from_paths(paths)

    def _collect_paths(self, node, current_path, paths, include_parameters=True):
        current_path = current_path + [node.name]

        if not node.children or (isinstance(node, UnitParameter) and not include_parameters):
            paths.append(current_path)
        else:
            for child in node.children:
                if include_parameters or not isinstance(child, UnitParameter):
                    self._collect_paths(child, current_path, paths, include_parameters)

    def _create_df_from_paths(self, paths):
        max_length = max(len(path) for path in paths)
        padded_paths = [path + [None] * (max_length - len(path)) for path in paths]
        df = pd.DataFrame(padded_paths)
        df = df.dropna(axis=1, how='all')
        return df

    # endregion

    # region Data操作
    def set_node_data(self, node_name: str, key: str, value: Any) -> None:
        node = self.find_node(node_name)
        if node:
            self.data_manager.set_data(node, key, value)
        else:
            raise ValueError(f"Node not found: {node_name}")

    def get_node_data(self, node_name: str, key: str) -> Any:
        node = self.find_node(node_name)
        if node:
            return self.data_manager.get_data(node, key)
        else:
            raise ValueError(f"节点: {node_name}未找到")

    def delete_node_data(self, node_name: str, key: str) -> None:
        node = self.find_node(node_name)
        if node:
            self.data_manager.delete_data(node, key)
        else:
            raise ValueError(f"节点: {node_name}未找到")

    def get_all_node_data(self, node_name: str) -> Dict[str, Any]:
        node = self.find_node(node_name)
        if node:
            return self.data_manager.get_all_data(node)
        else:
            raise ValueError(f"节点: {node_name}未找到")

    # endregion Data操作

    # region show方法
    def print_tree(self):
        self._print_tree_recursive(self.root, 0)

    def _print_tree_recursive(self, node, level):
        indent = "  " * level
        node_type = type(node).__name__
        node_data = self.get_all_node_data(node.name)
        data_str = f" - Data: {node_data}" if node_data else ""
        print(f"{indent}{node.name} ({node_type}){data_str}")

        for child in node.children:
            self._print_tree_recursive(child, level + 1)

    def get_object_tree(self) -> str:
        return self._get_tree_recursive(self.root, lambda node: isinstance(node, UnitObject), 0)

    def get_parameter_tree(self) -> str:
        return self._get_parameter_tree_recursive(self.root, 0)

    def _get_parameter_tree_recursive(self, node: BaseNode, level: int) -> str:
        result = ""
        has_parameters = False

        # 检查当前节点或其子节点是否有参数
        if isinstance(node, UnitParameter):
            has_parameters = True
        else:
            for child in node.children:
                if self._has_parameters(child):
                    has_parameters = True
                    break

        if has_parameters:
            if isinstance(node, UnitObject):
                result += "  " * level + f"({node.id}) {node.name} ({node.get_type()})\n"
                level += 1
            elif isinstance(node, UnitParameter):
                result += "  " * level + f"({node.id}) {node.name} ({node.get_type()})\n"

            for child in node.children:
                result += self._get_parameter_tree_recursive(child, level)

        return result

    def _has_parameters(self, node: BaseNode) -> bool:
        if isinstance(node, UnitParameter):
            return True
        return any(self._has_parameters(child) for child in node.children)

    def get_data_tree(self) -> str:
        return self._get_tree_recursive(self.root, lambda node: isinstance(node, UnitData), 0)

    def _get_tree_recursive(self, node: BaseNode, filter_func, level: int) -> str:
        result = ""
        if filter_func(node):
            result += "  " * level + f"({node.id}){node.name} ({node.get_type()})\n"
            for child in node.children:
                result += self._get_tree_recursive(child, filter_func, level + 1)
        else:
            for child in node.children:
                result += self._get_tree_recursive(child, filter_func, level)
        return result

    def _get_all_parameters(self, node: BaseNode) -> List[UnitParameter]:
        parameters = []
        if isinstance(node, UnitParameter):
            parameters.append(node)
        for child in node.children:
            parameters.extend(self._get_all_parameters(child))
        return parameters

    def build_from_dataframes(self, elements_df: pd.DataFrame, parameter_df: pd.DataFrame):
        self.build_object_structure(elements_df)
        self.add_parameters(parameter_df)

    def build_object_structure(self, df: pd.DataFrame):
        for index, row in df.iterrows():
            self._add_node_from_row(row, index)

    def _add_node_from_row(self, row, index):
        current_node = self.root
        for i, item in enumerate(row):
            if pd.isna(item):
                break
            child = self.find_or_create_child(current_node, item, self.generate_unique_id(), UnitObject)
            current_node = child

    def add_parameters(self, df: pd.DataFrame):
        for index, row in df.iterrows():
            self._add_parameter_from_row(row, index)

    def _add_parameter_from_row(self, row, index):
        # 从右向左遍历行，跳过 None 值
        valid_values = []
        for value in reversed(row):
            if pd.notna(value):
                valid_values.append(value)
            if len(valid_values) == 2:
                break

        if len(valid_values) < 2:
            logger.info(f"没有足够列，跳过第 {index} 行： {row}")
            return

        parameter_name, object_name = valid_values

        matched_nodes = self._find_matching_nodes(object_name)

        if matched_nodes:
            for matched_node in matched_nodes:
                logger.info(f"对象：'{matched_node.name}' 匹配到参数： '{parameter_name}'")
                param_node = UnitParameter(parameter_name, self.generate_unique_id())
                self.add_node(matched_node, param_node, param_node.name)
        else:
            logger.warning(f"找不到满足 '{parameter_name}' 的对象：'{object_name}'  ")

    def _find_matching_nodes(self, object_name):
        def search(node, results):
            if node.name == object_name and isinstance(node, UnitObject):
                results.append(node)
            for child in node.children:
                search(child, results)

        results = []
        search(self.root, results)
        return results

    def find_or_create_child(self, parent: BaseNode, name: str, id: str, node_class) -> BaseNode:
        for child in parent.children:
            if child.name == name and isinstance(child, node_class):
                return child
        new_child = node_class(name, id)
        self.add_node(parent, new_child, new_child.name)
        return new_child
