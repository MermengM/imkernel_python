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

    def add_node(self, parent: BaseNode, child: BaseNode):
        parent.add_child(child)

    def remove_node(self, node: BaseNode):
        if node.parent:
            node.parent.remove_child(node)

    def find_node_by_id(self, id: str) -> Union[BaseNode, None]:
        return self._find_node_by_id_recursive(self.root, id)

    def _find_node_by_id_recursive(self, node: BaseNode, id: str) -> Union[BaseNode, None]:
        if node.id == id:
            return node
        for child in node.children:
            result = self._find_node_by_id_recursive(child, id)
            if result:
                return result
        return None

    def print_tree(self):
        self._print_tree_recursive(self.root, 0)

    def _print_tree_recursive(self, node: BaseNode, level: int):
        print("  " * level + f"{node.name} ({node.get_type()})")
        for child in node.children:
            self._print_tree_recursive(child, level + 1)

    # region show方法
    def get_object_tree(self) -> Dict[str, Any]:
        return self._get_tree_recursive(self.root, lambda node: isinstance(node, UnitObject))

    def get_parameter_tree(self) -> Dict[str, Any]:
        return self._get_tree_recursive(self.root, lambda node: isinstance(node, UnitParameter))

    def get_data_tree(self) -> Dict[str, Any]:
        return self._get_tree_recursive(self.root, lambda node: isinstance(node, UnitData))

    def _get_tree_recursive(self, node: BaseNode, filter_func) -> Dict[str, Any]:
        result = {}
        if filter_func(node):
            result[node.name] = {}
            for child in node.children:
                child_result = self._get_tree_recursive(child, filter_func)
                if child_result:
                    result[node.name].update(child_result)
        else:
            for child in node.children:
                child_result = self._get_tree_recursive(child, filter_func)
                if child_result:
                    result.update(child_result)
        return result

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
            child = self.find_or_create_child(current_node, item, f"{index}.{i}", UnitObject)
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
            logger.info(f"Skipping row {index} due to insufficient valid values: {row}")
            return

        parameter_name, object_name = valid_values

        matched_nodes = self._find_matching_nodes(object_name)

        if matched_nodes:
            for matched_node in matched_nodes:
                logger.info(f"Matched parameter '{parameter_name}' to object '{matched_node.name}'")
                param_node = UnitParameter(parameter_name, f"{index}.{len(row) - 1}")
                self.add_node(matched_node, param_node)
        else:
            logger.warning(f"Could not find matching object '{object_name}' for parameter '{parameter_name}'")

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
        self.add_node(parent, new_child)
        return new_child
