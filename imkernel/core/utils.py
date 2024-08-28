import importlib.util
import sys
import nbformat
from nbformat.v4 import new_notebook, new_code_cell
from IPython.display import FileLink
import json
import os
import pandas as pd
from treelib import Tree
import nbformat
from nbformat.v4 import new_notebook, new_code_cell


def search_node(tree: Tree, node_identifier):
    """
    寻找节点的层级关系并输出
    :param tree: 树对象
    :param node_identifier: 节点标识符
    :return: 节点层级关系字符串
    """
    #
    node = tree.get_node(node_identifier)
    if node is None:
        # 如果通过 id 找不到,尝试通过 tag 遍历所有节点，并返回列表
        matching_nodes = list(tree.filter_nodes(lambda n: n.tag == node_identifier))
        if matching_nodes:
            node = matching_nodes[0]
        else:
            pass

    # 获取节点的所有祖先
    hierarchy = []
    current = node
    while current is not None:
        hierarchy.insert(0, current.tag)
        current = tree.parent(current.identifier)
    if not hierarchy:
        raise Exception(f"找不到节点{node_identifier}")

    return ' -> '.join(hierarchy)


def get_root_path():
    interpreter_path = sys.executable
    current_dir = os.path.dirname(interpreter_path)
    parent_dir = os.path.dirname(current_dir)
    root_dir = os.path.dirname(parent_dir)
    return root_dir


def get_algorithm_by_path(algo_file, algo_name):
    """

    @rtype: object
    """
    try:
        # print(f"正在尝试导入算法文件: {algo_file}")
        spec = importlib.util.spec_from_file_location(name=algo_name, location=algo_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # print(f"成功导入模块")

        algo_func = getattr(module, algo_name)
        # print(f"成功获取算法函数: {algo_name}")

        # print(f"算法信息:")
        # print(f"  - 函数名称: {algo_func.__name__}")
        # print(f"  - 函数文档: {algo_func.__doc__}")

        return algo_func
    except Exception as e:
        print(f"导入算法时发生错误: {e}")
        return None


def points_to_df(points):
    all_df_list = []
    # 遍历最外层列表
    for group in points:
        # 如果组内元素是字典，直接创建DataFrame
        if isinstance(group[0], dict):
            df = pd.DataFrame(group)
            all_df_list.append(df)
        # 如果组内元素是列表，先展平再创建DataFrame
        elif isinstance(group[0], list):
            flat_group = [item for sublist in group for item in sublist]
            df = pd.DataFrame(flat_group)
            all_df_list.append(df)
    return all_df_list


def dict_to_tree(tree, dictionary, parent=None):
    for key, value in dictionary.items():
        node_id = tree.size() + 1
        tree.create_node(tag=key, identifier=node_id, parent=parent)
        if isinstance(value, dict):
            dict_to_tree(tree, value, node_id)
        else:
            raise Exception("请输入字典")


def merge_tree(tree, param_mapping, parameter_dict):
    def add_parameters(node_id, param_list):
        for param in param_list:
            if param in parameter_dict:
                # Add the parameter as a new node
                tree.create_node(tag=param, identifier=f"{node_id}_{param}", parent=node_id)

                # Add each value of the parameter as a child node
                for i, value in enumerate(parameter_dict[param]):
                    tree.create_node(tag=value, identifier=f"{node_id}_{param}_{i}", parent=f"{node_id}_{param}")
            else:
                print(f"参数'{param}'未找到")

    for node_id, param_list in param_mapping.items():
        if tree.get_node(node_id):
            add_parameters(node_id, param_list)
        else:
            print(f"节点 '{node_id}' 未找到")
            


def save_model(notebook_path):
    # 打开并读取原始notebook文件
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # 合并所有代码单元格的内容
    merged_content = ""
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            merged_content += cell['source']
            merged_content += "\n\n"

    # 创建一个新的Jupyter Notebook对象
    new_nb = new_notebook()

    # 创建一个新的代码单元格，并将merged_content写入该单元格
    first_cell = new_code_cell(source=merged_content)

    # 将该单元格添加到新notebook中
    new_nb['cells'].append(first_cell)

    # 生成新的notebook文件路径，添加 "_分析" 后缀
    dir_name, base_name = os.path.split(notebook_path)
    name, ext = os.path.splitext(base_name)
    new_notebook_path = os.path.join(dir_name, f"{name}_分析{ext}")

    # 将新的notebook保存到指定路径
    with open(new_notebook_path, 'w', encoding='utf-8') as f:
        nbformat.write(new_nb, f)
     # 创建一个FileLink对象并显示下载链接
    display(FileLink(new_notebook_path, result_html_prefix="导出到: "))
    # 返回一个FileLink对象，Jupyter Notebook中会显示下载链接
    return  new_notebook_path

def merge_method_tree(tree, param_mapping, parameter_dict):
    def add_method_parameters(node_id, method_name):
        if method_name in parameter_dict:
            method_data = parameter_dict[method_name]

            # Create a node for the method
            method_node_id = f"{node_id}_{method_name}"
            tree.create_node(tag=method_name, identifier=method_node_id, parent=node_id)

            # Add Input and Output nodes
            for io_type in ["Input", "Output"]:
                if io_type in method_data:
                    io_node_id = f"{method_node_id}_{io_type}"
                    tree.create_node(tag=io_type, identifier=io_node_id, parent=method_node_id)

                    # Add parameters as child nodes
                    if isinstance(method_data[io_type], list):
                        for i, param in enumerate(method_data[io_type]):
                            tree.create_node(tag=param, identifier=f"{io_node_id}_{i}", parent=io_node_id)
                    elif isinstance(method_data[io_type], dict):
                        for sub_key, sub_list in method_data[io_type].items():
                            sub_node_id = f"{io_node_id}_{sub_key}"
                            tree.create_node(tag=sub_key, identifier=sub_node_id, parent=io_node_id)
                            for i, param in enumerate(sub_list):
                                tree.create_node(tag=param, identifier=f"{sub_node_id}_{i}", parent=sub_node_id)
        else:
            print(f"方法 '{method_name}' 未在参数字典中找到")

    for node_id, method_list in param_mapping.items():
        if tree.get_node(node_id):
            for method_name in method_list:
                add_method_parameters(node_id, method_name)
        else:
            print(f"节点 '{node_id}' 未在树中找到")


def save_model(notebook_path, new_notebook_path):
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(notebook_path, as_version=4)

    merged_content = ""
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            for x in cell['source']:
                merged_content += x
            merged_content += "\n\n"
    # 创建一个新的Jupyter Notebook对象
    nb = new_notebook()

    # 创建一个新的代码单元格，并将merged_content写入该单元格
    first_cell = new_code_cell(source=merged_content)

    # 将该单元格添加到notebook中
    nb['cells'].append(first_cell)

    # 将notebook保存到指定路径
    with open(new_notebook_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)

    return new_notebook_path
