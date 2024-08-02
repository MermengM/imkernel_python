from abc import ABC, abstractmethod
from typing import List, Union, Optional
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

    def add_object_to_node(self, parent_node_name: str, new_object_name: str) -> Optional[UnitObject]:

        parent_node = self.find_node(parent_node_name)

        if parent_node is None:
            logger.error(f"父对象 '{parent_node_name}' 未找到.")
            return None

        # 检查是否已存在相同名称的对象
        for child in parent_node.children:
            if child.name == new_object_name and isinstance(child, UnitObject):
                logger.warning(f" '{new_object_name}'已经在 '{parent_node_name}' 下存在.")
                return child

        # Create and add the new UnitObject
        new_object_id = self.generate_unique_id()
        new_object = UnitObject(new_object_name, new_object_id)
        self.add_node(parent_node, new_object, new_object_name)

        logger.info(f"增加 '{new_object_name}' (ID: {new_object_id}) 到 '{parent_node_name}'.")
        return new_object

    def remove_node(self, node: BaseNode) -> None:
        if node.parent:
            node.parent.remove_child(node)
        self.data_manager.clear_node_data(node)

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
    def get_object_df(self):
        paths = []
        self._collect_paths(self.root, [], paths, include_parameters=False)
        return self._create_df_from_paths(paths)

    def get_data_df(self) -> pd.DataFrame:
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

    def get_parameter_df(self):
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

    def get_element_df(self):
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
    # region 参数Parameter操作
    def get_parameters_by_node_name(self, node_name: str) -> List[str]:
        node = self.find_node(node_name)
        if node:
            parameters = self._get_all_parameters(node)
            return [param.name for param in parameters]
        else:
            return []

    def get_parameters_dict_by_node_name(self, node_name: str) -> Dict[str, Any]:
        node = self.find_node(node_name)
        if node:
            parameters = self._get_all_parameters(node)
            return {param.name: self.get_node_data(node_name, param.name) for param in parameters}
        else:
            return {}

    def get_parameters_for_object(self, object_name: str) -> List[str]:
        """
        获取指定 UnitObject 下的所有参数名称列表。

        :param object_name: UnitObject 的名称
        :return: 参数名称列表
        """
        node = self.find_node(object_name)
        if node is None or not isinstance(node, UnitObject):
            raise ValueError(f"未找到名为 '{object_name}' 的 UnitObject")

        parameters = []
        for child in node.children:
            if isinstance(child, UnitParameter):
                parameters.append(child.name)
        return parameters

    def get_parameters_df_for_object(self, object_name: str) -> Optional[pd.DataFrame]:
        """
        获取指定 UnitObject 下的所有参数，并以 DataFrame 形式返回。

        :param object_name: UnitObject 的名称
        :return: 包含参数信息的 DataFrame，如果没有参数则返回 None
        """
        parameters = self.get_parameters_for_object(object_name)
        if not parameters:
            return None

        data = []
        for param in parameters:
            value = self.get_node_data(object_name, param)
            data.append({"Parameter": param, "Value": value})

        return pd.DataFrame(data)

    # endregion
    # region Data操作
    def set_node_data(self, node_name: str, key: str, value: Any) -> None:
        node = self.find_node(node_name)
        if node:
            self.data_manager.set_data(node, key, value)
        else:
            raise ValueError(f"Node not found: {node_name}")

    def add_node_data(self, node_name: str, value_dict: Dict[str, Any]) -> None:
        node = self.find_node(node_name)
        if node:
            for x in value_dict:
                for key, value in x.items():
                    current_value = self.data_manager.get_data(node, key)
                    if current_value is None:
                        new_value = value
                    elif isinstance(current_value, list):
                        new_value = current_value + [value]
                    else:
                        new_value = [current_value, value]
                    self.data_manager.set_data(node, key, new_value)
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

    def set_multiple_node_data(self, node_name: str, param_list: List[Dict[str, Any]]):
        for param_dict in param_list:
            for key, value in param_dict.items():
                try:
                    self.set_node_data(node_name, key, value)
                except Exception as e:
                    print(f"无法设置参数 {key} 的值: {str(e)}")

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

    def build_from_dataframes(self, elements_df: pd.DataFrame | None = None, parameter_df: pd.DataFrame | None = None):
        if elements_df is None and parameter_df is None:
            raise ValueError("请提供参数！")

        if elements_df is not None:
            self.build_object_structure(elements_df)

        if parameter_df is not None:
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

    def get_system_df(self):
        # 获取元素结构
        element_df = self.get_element_df()
        # 初始化一个空的列表来存储所有数据
        # 这里可以进一步处理 element_df，并结合其他数据生成系统 DataFrame
        return element_df  # 目前返回 element_df 作为示例

    def get_element_df_new(self) -> pd.DataFrame:
        paths = []
        self._collect_paths_with_data_new(self.root, [], paths)
        return self._create_df_from_paths_1(paths)

    def _collect_paths_with_data_new(self, node: BaseNode, current_path: List[str], paths: List[Dict[str, Any]]):
        current_path.append(node.name)
        node_data = self.data_manager.get_all_data(node)  # 获取当前节点的数据

        # 保存路径和数据
        paths.append({'path': current_path.copy(), 'data': node_data})

        for child in node.children:
            self._collect_paths_with_data_new(child, current_path, paths)

        current_path.pop()  # 回溯，移除当前节点

    def _create_df_from_paths_1(self, paths: List[Dict[str, Any]]) -> pd.DataFrame:
        max_length = max(len(p['path']) for p in paths)
        df = pd.DataFrame(columns=[f'Level {i + 1}' for i in range(max_length)] + ['Data'])

        # 创建 DataFrame 行
        for path_info in paths:
            row = path_info['path'] + [None] * (max_length - len(path_info['path']))  # 填充 None
            row_data = path_info['data']

            # 如果有数据，填充到对应的行
            if row_data:
                for key, value in row_data.items():
                    new_row = row.copy()  # 复制当前行
                    new_row[-1] = value  # 将值放入最后一列
                    # 只添加非空的数据行
                    if key:
                        new_row.insert(-1, key)  # 插入参数名称
                        df.loc[len(df)] = new_row  # 添加新行

        return df

    def get_full_system_df(self) -> pd.DataFrame:
        paths = []
        self._collect_full_paths_with_data(self.root, [], paths)
        return self._create_full_df_from_paths_2(paths)

    def _collect_full_paths_with_data(self, node: BaseNode, current_path: List[str], paths: List[Dict[str, Any]]):
        current_path.append(node.name)
        node_data = self.data_manager.get_all_data(node)  # 获取当前节点的数据

        # 保存路径和数据
        paths.append({'path': current_path.copy(), 'data': node_data})

        for child in node.children:
            self._collect_full_paths_with_data(child, current_path, paths)

        # 添加空行以保持结构
        if not node.children:
            paths.append({'path': current_path.copy(), 'data': None})  # 添加空行

        current_path.pop()  # 回溯，移除当前节点

    def _create_full_df_from_paths_2(self, paths: List[Dict[str, Any]]) -> pd.DataFrame:
        max_length = max(len(p['path']) for p in paths)
        df = pd.DataFrame(columns=[f'Level {i + 1}' for i in range(max_length)] + ['Data'])

        # 创建 DataFrame 行
        for path_info in paths:
            row = path_info['path'] + [None] * (max_length - len(path_info['path']))  # 填充 None
            row_data = path_info['data']

            # 填充数据
            if row_data:
                for key, value in row_data.items():
                    new_row = row.copy()
                    new_row[-1] = value  # 将值放入最后一列
                    new_row.insert(-1, key)  # 插入参数名称
                    df.loc[len(df)] = new_row  # 添加新行
            else:
                new_row = row + [None]  # 空值行填充
                df.loc[len(df)] = new_row  # 添加空行

        return df
