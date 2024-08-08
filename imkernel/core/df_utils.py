import pandas as pd


def find_children(df, parent):
    """
    根据输入的父节点字符串，查找其所有的直接子节点，并在结果前面加上父节点列

    :param df: 包含层级结构的DataFrame
    :param parent: 要查找子节点的父节点字符串
    :return: 包含父节点和子节点的DataFrame
    """
    # 查找所有包含父节点的行
    parent_rows = df[df.apply(lambda row: parent in row.values, axis=1)]

    if parent_rows.empty:
        print(f"未找到节点: {parent}")
        return pd.DataFrame()

    # 获取父节点所在的列索引
    parent_col_index = parent_rows.apply(lambda row: row.tolist().index(parent), axis=1).iloc[0]

    # 查找直接子节点
    children = df[df.iloc[:, parent_col_index] == parent].iloc[:, parent_col_index:]

    # 移除全为NaN的列
    children = children.dropna(axis=1, how='all')

    # 重命名列名，使其更有描述性
    new_columns = ['父节点'] + [f'子节点{i + 1}' for i in range(len(children.columns) - 1)]
    children.columns = new_columns

    return children


def find_all_parents(df, child):
    """
    根据输入的子节点字符串，查找其所有父节点直到顶级节点

    :param df: 包含层级结构的DataFrame
    :param child: 要查找父节点的子节点字符串
    :return: 包含所有父节点和当前节点的平铺DataFrame，当前节点在最后一列
    """
    parents = []
    current_node = child

    while True:
        # 查找包含当前节点的行
        node_rows = df[df.apply(lambda row: current_node in row.values, axis=1)]

        if node_rows.empty:
            print(f"未找到节点: {current_node}")
            break

        # 获取当前节点所在的列索引
        node_col_index = node_rows.apply(lambda row: row.tolist().index(current_node), axis=1).iloc[0]

        if node_col_index == 0:
            # 如果当前节点在第一列，说明已经到达顶级节点
            break

        # 获取父节点（当前节点左侧的列）
        parent = node_rows.iloc[0, node_col_index - 1]
        parents.append(parent)

        # 更新当前节点为其父节点，继续循环
        current_node = parent

    # 创建结果DataFrame
    parents.reverse()  # 反转列表，使顶级节点在前
    result = parents + [child]
    columns = [f'父节点_{i + 1}' for i in range(len(parents))] + ['当前节点']
    result_df = pd.DataFrame([result], columns=columns)

    return result_df
