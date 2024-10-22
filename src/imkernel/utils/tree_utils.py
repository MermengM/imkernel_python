import treelib
from treelib import Tree
import numpy as np
import pandas as pd


def get_paths_dict(tree: treelib.Tree):
    """
    获取从根节点到叶子节点的路径，并将ID替换为TAG，返回一个字典。

    参数:
    tree (Tree): treelib中的树结构。

    返回:
    dict: 包含从根节点到叶子节点路径的字典，路径以节点TAG表示。
    """
    # 获取所有从根节点到叶子节点的路径
    paths = tree.paths_to_leaves()
    # 将路径从ID转换为TAG，并构建字典
    paths_dict = {}
    for i, path in enumerate(paths):
        # 使用tag替代id
        tag_path = [tree.get_node(node_id).tag for node_id in path]
        paths_dict[f"path_{i + 1}"] = tag_path
    return paths_dict


def dict_to_df(paths_dict, names, columns):
    """
    根据获取的路径，返回df。

    参数：
    paths_dict：路径
    names：多级索引的列名
    columns：值的列名

    返回：
    df
    """
    # 转换为多级索引
    multi_index = pd.MultiIndex.from_tuples([tuple(path) for path in paths_dict.values()],
                                            names=names)
    # 创建DataFrame，值为NaN
    df = pd.DataFrame(np.nan, index=multi_index, columns=columns)
    return df


def tree_to_df(tree, index_num=None, columns_num=None, index_levels=None, columns=None):
    """
    获取从根节点到叶子节点的路径，并将ID替换为TAG，返回一个df。
    根据路径字典生成df，多级索引的层数可以根据用户输入的index_num选择。
    未选择的层级将作为值保留，columns_num决定列的数量。

    :arg:
    tree (Tree): treelib中的树结构。
    index_num: 选择的多级索引层数，默认为路径的最大层数
    columns_num: DataFrame列的数量，默认为None
    index_levels: 多级索引的列名，默认使用 ['level_1', 'level_2', ..., 'level_n']
    columns: 除未选择层级外的其他列名，默认为 ['column_1', 'column_2', ..., 'column_n']

    返回:
    df: 包含从根节点到叶子节点路径的DataFrame，路径以节点TAG表示。

    如果index_num超过路径层次或其他参数不匹配则报错。
    """
    # 获取所有从根节点到叶子节点的路径
    paths = tree.paths_to_leaves()

    # 检查路径的最大层数
    max_depth = max(len(path) for path in paths)

    # 如果没有指定index_num，默认使用最大深度
    if index_num is None:
        index_num = max_depth

    # 如果指定的index_num超过了路径的最大深度，报错
    if index_num > max_depth:
        raise ValueError(f"输入的index_num超过了路径的层次，路径最大层次为 {max_depth}")

    # 检查 index_levels 的长度是否匹配 index_num
    if index_levels is not None and len(index_levels) != index_num:
        raise ValueError(f"提供的index_levels长度 ({len(index_levels)}) 不等于index_num ({index_num})")

    # 如果没有指定index_levels，默认使用 ['level_1', 'level_2', ..., 'level_n']
    if index_levels is None:
        index_levels = [f'level_{i + 1}' for i in range(index_num)]

    # 如果columns为None且columns_num为NaN，默认columns_num为2
    if columns_num is None and columns is None:
        columns_num = 2

    # 如果传入了columns且columns_num为NaN，则columns_num等于columns的长度
    if columns is not None and columns_num is None:
        columns_num = len(columns)

    # 如果用户提供的columns长度大于columns_num，报错
    if columns is not None and len(columns) > columns_num:
        raise ValueError(f"提供的columns长度 ({len(columns)}) 超过了columns_num ({columns_num})")

    # 如果columns不够columns_num长度，补齐
    if columns is None:
        columns = [f'column_{i + 1}' for i in range(columns_num)]
    elif len(columns) < columns_num:
        columns += [f'column_{i + 1}' for i in range(len(columns), columns_num)]

    # 将路径从ID转换为TAG，并构建字典
    paths_dict = {}
    for i, path in enumerate(paths):
        # 使用tag替代id
        tag_path = [tree.get_node(node_id).tag for node_id in path]
        paths_dict[f"path_{i + 1}"] = tag_path

    # 切割路径为多级索引部分和剩余层级部分
    truncated_paths = [tuple(path[:index_num]) for path in paths_dict.values()]
    remaining_levels = [path[index_num:] for path in paths_dict.values()]

    # 转换为多级索引
    multi_index = pd.MultiIndex.from_tuples(truncated_paths, names=index_levels)

    # 将剩余层级转为DataFrame列，值为剩下的路径层级
    remaining_columns = pd.DataFrame(remaining_levels, index=multi_index,
                                     columns=[f"level_{i + 1}" for i in range(index_num, max_depth)])

    # 创建DataFrame，值为NaN，并结合剩余层级的列
    df = pd.DataFrame(np.nan, index=multi_index, columns=columns)

    # 将剩余的层级与空的DataFrame合并
    df = pd.concat([df, remaining_columns], axis=1)
    # 替换 NaN 为 None
    df = df.map(lambda x: None if pd.isna(x) else x)

    return df


def df_to_tree(df) -> treelib.Tree:
    """
    将 DataFrame 的 MultiIndex 转换为树结构，并将行的值作为叶子节点添加到树中。
    Args:
        df(pd.DataFrame):包含 MultiIndex 的 DataFrame，其索引层次及对应的行值将被转换为树结构。

    Returns:
        返回由 DataFrame 的 MultiIndex 构建的树结构，并将行的值作为叶节点附加。

    """
    # 初始化树
    tree = Tree()

    # 遍历 DataFrame 的 MultiIndex，并附加行值作为叶节点
    for idx_tuple, row_values in df.iterrows():
        current_parent = None  # 没有根节点，直接从第一个索引级别开始
        for i, level in enumerate(idx_tuple):
            if pd.notna(level):  # 确保不处理 None 或 NaN 值
                # 如果 current_parent 为空，说明这是树的顶层节点
                if current_parent is None:
                    if not tree.contains(level):
                        tree.create_node(level, level)  # 顶层节点
                else:
                    if not tree.contains(level):
                        tree.create_node(level, level, parent=current_parent)  # 子节点
                current_parent = level

        # 将行的所有值作为叶节点添加到树中
        for i, value in enumerate(row_values):
            if value is not None:
                tree.create_node(tag=value, identifier=value, parent=current_parent)

    return tree
