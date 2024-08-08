from abc import ABC, abstractmethod
from typing import List, Union, Optional, Tuple
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


class RootNode(BaseNode):
    def __init__(self, name: str, id: str):
        super().__init__(name, id)

    def get_type(self) -> str:
        return "Element"


class UnitObject(BaseNode):
    def __init__(self, name: str, id: str):
        super().__init__(name, id)

    def get_type(self) -> str:
        return "UnitObject"


class UnitParameter(BaseNode):
    def __init__(self, name: str, id: str):
        super().__init__(name, id)
        self.data = None

    def get_type(self) -> str:
        return "UnitParameter"

    def set_data(self, value: Any):
        if self.data is None:
            self.data = UnitData(f"{value}", f"{self.id}_data", value)
            self.add_child(self.data)
        else:
            self.data.value = value

    def get_data(self) -> Any:
        return self.data.value if self.data else None


# region UnitData
class UnitData(BaseNode):
    def __init__(self, name: str, id: str, value: Any = None):
        super().__init__(name, id)
        self.value = value

    def get_type(self) -> str:
        return "UnitData"


# endregion
class Element:
    def __init__(self):
        self.root = RootNode("Element", "0")
        self.node_counter = 1

    def generate_unique_id(self) -> str:
        self.node_counter += 1
        return str(self.node_counter)

    def add_node(self, parent: BaseNode, node: BaseNode, name: str) -> BaseNode:
        parent.add_child(node)
        return node

    def add_object_to_node(self, parent_node_name: str, new_object_name: str) -> Optional[UnitObject]:
        """
        在指定的父节点下添加一个新的UnitObject对象。

        :param parent_node_name: 父节点的名称。
        :param new_object_name: 要添加的新对象的名称。
        :return: 添加的UnitObject对象，如果父节点不存在或新对象已存在，则返回None。
        """
        # 寻找指定名称的父节点
        parent_node = self.find_node(parent_node_name)

        # 如果找不到父节点，则记录错误并返回None
        if parent_node is None:
            logger.error(f"父对象 '{parent_node_name}' 未找到.")
            return None

        # 检查父节点下是否已经存在同名的UnitObject对象
        existing_object = next((child for child in parent_node.children
                                if child.name == new_object_name and isinstance(child, UnitObject)), None)

        # 如果已经存在同名对象，则记录警告并返回该对象
        if existing_object:
            logger.warning(f" '{new_object_name}'已经在 '{parent_node_name}' 下存在.")
            return existing_object

        # 生成新对象的唯一ID，并创建UnitObject对象
        new_object_id = self.generate_unique_id()
        new_object = UnitObject(new_object_name, new_object_id)

        # 将新对象添加到父节点中
        self.add_node(parent_node, new_object, new_object_name)

        # 记录新增对象的信息并返回新对象
        logger.info(f"增加 '{new_object_name}' (ID: {new_object_id}) 到 '{parent_node_name}'.")
        return new_object

        # region Data操作

    def add_nested_objects(self, parent_node_name: str, object_path: List[str]) -> Optional[UnitObject]:
        """
        在指定的父节点下添加嵌套的UnitObject对象结构。

        :param parent_node_name: 父节点的名称。
        :param object_path: 描述对象路径的字符串列表。
        :return: 添加的最底层UnitObject对象，如果父节点不存在则返回None。
        """
        parent_node = self.find_node(parent_node_name)

        if parent_node is None:
            logger.error(f"父对象 '{parent_node_name}' 未找到.")
            return None

        current_node = parent_node
        last_added_object = None

        for obj_name in object_path:
            existing_object = next((child for child in current_node.children
                                    if child.name == obj_name and isinstance(child, UnitObject)), None)

            if existing_object:
                logger.info(f"'{obj_name}' 已经在 '{current_node.name}' 下存在.")
                current_node = existing_object
            else:
                new_object_id = self.generate_unique_id()
                new_object = UnitObject(obj_name, new_object_id)
                self.add_node(current_node, new_object, obj_name)
                logger.info(f"增加 '{obj_name}' (ID: {new_object_id}) 到 '{current_node.name}'.")
                current_node = new_object

            last_added_object = current_node

        return last_added_object

    def remove_node(self, node_name: str) -> bool:
        node_to_remove = self.find_node(node_name)

        if node_to_remove is None:
            logger.error(f"节点 '{node_name}' 未找到.")
            return False

        if node_to_remove == self.root:
            logger.error("不能删除根节点.")
            return False

        parent = self.find_parent(node_to_remove)

        if parent is None:
            logger.error(f"无法找到节点 '{node_name}' 的父节点.")
            return False

        parent.children.remove(node_to_remove)
        logger.info(f"已删除节点 '{node_name}' 及其所有子节点.")
        return True

    def find_parent(self, node: BaseNode) -> Optional[BaseNode]:
        def dfs(current_node: BaseNode) -> Optional[BaseNode]:
            for child in current_node.children:
                if child == node:
                    return current_node
                result = dfs(child)
                if result:
                    return result
            return None

        return dfs(self.root)
    def set_node_data(self, node_name: str, value: Any) -> None:
        node = self.find_node(node_name)
        if node and isinstance(node, UnitParameter):
            node.set_data(value)
        else:
            raise ValueError(f"Node not found or not a UnitParameter: {node_name}")

    def get_node_data(self, node_name: str) -> Any:
        node = self.find_node(node_name)
        if node and isinstance(node, UnitParameter):
            return node.get_data()
        else:
            raise ValueError(f"Node not found or not a UnitParameter: {node_name}")

    def delete_node_data(self, node_name: str) -> None:
        node = self.find_node(node_name)
        if node and isinstance(node, UnitParameter):
            node.set_data(None)
        else:
            raise ValueError(f"Node not found or not a UnitParameter: {node_name}")

    def get_all_node_data(self, node_name: str) -> Dict[str, Any]:
        node = self.find_node(node_name)
        if node:
            data = {}
            for child in node.children:
                if isinstance(child, UnitParameter):
                    data[child.name] = child.get_data()
            return data
        else:
            raise ValueError(f"Node not found: {node_name}")

    def set_multiple_node_data(self, node_name: str, param_list: List[Dict[str, Any]]):
        node = self.find_node(node_name)
        if node:
            for param_dict in param_list:
                for key, value in param_dict.items():
                    param_node = self.find_node(key, node)
                    if param_node and isinstance(param_node, UnitParameter):
                        param_node.set_data(value)
                    else:
                        print(f"无法设置参数 {key} 的值")
        else:
            raise ValueError(f"Node not found: {node_name}")

    # endregion Data操作

    # def remove_node(self, node: BaseNode) -> None:
    #     if node.parent:
    #         node.parent.remove_child(node)

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

    def find_node_to_df(self, node_name: str) -> Union[pd.DataFrame, None]:
        """
        查找指定名称的节点，并将该节点及其所有子节点的信息转换为DataFrame。

        :param node_name: 要查找的节点名称
        :return: 包含节点路径信息的DataFrame，如果节点未找到则返回None
        """
        node = self.find_node(node_name)
        if node is None:
            logger.error(f"节点 '{node_name}' 未找到.")
            return None

        def collect_paths(node: BaseNode, current_path: List[str], paths: List[List[str]]):
            new_path = current_path + [node.name]

            if isinstance(node, UnitParameter):
                new_path.append(str(node.get_data()))
                paths.append(new_path)
            elif not node.children:
                paths.append(new_path)
            else:
                for child in node.children:
                    collect_paths(child, new_path, paths)

        paths = []
        collect_paths(node, [], paths)
        return self._create_df_from_paths_for_node(paths)

    def _create_df_from_paths_for_node(self, paths: List[List[str]]) -> pd.DataFrame:
        max_length = max(len(path) for path in paths)
        padded_paths = [path + [None] * (max_length - len(path)) for path in paths]
        df = pd.DataFrame(padded_paths)
        df = df.dropna(axis=1, how='all')
        return df
    # region 转换器

    def to_df(self):
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
            value = self.get_node_data(object_name)
            data.append({"Parameter": param, "Value": value})

        return pd.DataFrame(data)

    # endregion

    # region show方法
    def print(self):
        self._print_tree_recursive(self.root, 0)

    def _print_tree_recursive(self, node, level):
        indent = "  " * level
        node_type = type(node).__name__
        node_data = self.get_all_node_data(node.name)
        data_str = f" - Data: {node_data}" if node_data else ""
        print(f"{indent}{node.name} ({node_type}){data_str}")

        for child in node.children:
            self._print_tree_recursive(child, level + 1)

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

    # endregion
    def add_object_from_dataframe(self, elements_df):
        if elements_df is not None:
            if isinstance(elements_df, pd.DataFrame):
                self.build_object_structure(elements_df)
            elif isinstance(elements_df, list):
                for df in elements_df:
                    if isinstance(df, pd.DataFrame):
                        self.build_object_structure(df)
                    else:
                        raise TypeError(f"请传入Dataframe, 而不是 {type(df)}")
            else:
                raise TypeError(f"请传入Dataframe, 而不是 {type(elements_df)}")

    def add_parameter_from_dataframe(self,elements_df: pd.DataFrame):
        if elements_df is not None:
            self.build_object_structure(elements_df)
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
            self._add_parameter_from_row(row)

    def bind_method_parameter_to_object(self, param_info: Union[List[str], List[List[str]]], object_path: List[str]) -> bool:
        """
        将一个或多个参数绑定到指定对象。

        参数:
        - param_info: 单个参数信息列表 ['参数类型', '参数名称'] 或这样的列表的列表。
        - object_path: 用于定位对象的路径列表。

        返回:
        - 所有参数成功绑定返回True，任何参数绑定失败则返回False。
        """
        object_node = self.find_node_by_path(object_path)

        if object_node is None or not isinstance(object_node, UnitObject):
            logger.error(f"未找到对象或对象类型错误: {' > '.join(object_path)}")
            return False

        # 确保param_info是一个二维列表
        if isinstance(param_info[0], str):
            param_info = [param_info]

        success = True
        for param_type, param_name in param_info:
            if param_type not in ['输入参数', '输出参数']:
                logger.error(f"参数类型错误: {param_type}")
                success = False
                continue

            # 查找或创建参数类型对象（输入参数或输出参数）
            type_node = next((child for child in object_node.children if child.name == param_type), None)
            if type_node is None:
                type_node = UnitObject(param_type, self.generate_unique_id())
                object_node.add_child(type_node)

            # 创建新的参数节点
            param_id = self.generate_unique_id()
            new_param = UnitParameter(param_name, param_id)

            # 将新参数添加到对应的参数类型节点下
            type_node.add_child(new_param)
            logger.info(f"成功将{param_type} '{param_name}' 绑定到对象 '{object_node.name}'")

        return success

    def bind_parameter_to_object(self, parameter_info: Union[str, List[str]], object_path: List[str]) -> bool:
        """
        将一个或多个参数关联到指定对象。

        通过提供的对象路径找到对象节点，并根据参数信息创建一个或多个新的参数节点，
        然后将它们关联到找到的对象上。

        参数:
        - parameter_info: 包含参数名称的字符串，或参数名称列表。
        - object_path: 用于定位对象的路径列表。

        返回:
        - 所有参数成功关联返回True，任何参数关联失败则返回False。
        """
        object_node = self.find_node_by_path(object_path)

        if object_node is None or not isinstance(object_node, UnitObject):
            logger.error(f"未找到对象或对象类型错误: {' > '.join(object_path)}")
            return False

        # 确保parameter_info是一个列表
        if isinstance(parameter_info, str):
            parameter_info = [parameter_info]

        success = True
        for param_name in parameter_info:
            # 创建新的参数节点
            param_id = self.generate_unique_id()
            new_param = UnitParameter(param_name, param_id)

            # 将新参数添加到对象节点
            object_node.add_child(new_param)
            logger.info(f"成功将参数 '{param_name}' 关联到对象 '{object_node.name}'")

        return success
    def find_node_by_path(self, path: List[str]) -> Optional[BaseNode]:
        current_node = self.root
        for name in path:
            found = False
            for child in current_node.children:
                if child.name == name:
                    current_node = child
                    found = True
                    break
            if not found:
                return None
        return current_node

    def _add_parameter_from_row(self, row):
        valid_values = [value for value in reversed(row) if pd.notna(value)][:2]

        if len(valid_values) < 2:
            logger.info(f"没有足够列，跳过这一行： {row}")
            return

        parameter_name, object_name = valid_values

        matched_nodes = self._find_matching_nodes(object_name)

        if matched_nodes:
            for matched_node in matched_nodes:
                logger.info(f"对象：'{matched_node.name}' 匹配到参数： '{parameter_name}'")
                param_node = UnitParameter(parameter_name, self.generate_unique_id())
                self.add_node(matched_node, param_node, param_node.name)
        else:
            logger.warning(f"找不到满足 '{parameter_name}' 的对象：'{object_name}' ")

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
        element_df = self.to_df()
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
