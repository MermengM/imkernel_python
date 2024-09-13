import importlib.util
import sys
import json
import os
import pandas as pd
from treelib import Tree
from nbformat.v4 import new_notebook, new_code_cell


def get_root_path():
    interpreter_path = sys.executable
    current_dir = os.path.dirname(interpreter_path)
    parent_dir = os.path.dirname(current_dir)
    root_dir = os.path.dirname(parent_dir)
    return root_dir


def get_algorithm_by_path(algo_file, algo_name):
    """
    通过文件路径获取算法函数。
    @param algo_file:算法文件的路径
    @param algo_name:算法函数的名称
    @return:algo_func: 算法函数，如果获取失败则返回None。

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
    return new_notebook_path


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


def remove_empty_members(input_list):
    if not isinstance(input_list, list):
        return input_list

    result = []
    for item in input_list:
        if isinstance(item, list):
            cleaned_item = remove_empty_members(item)
            if cleaned_item:  # 如果清理后的子列表非空，则添加
                result.append(cleaned_item)
        elif item not in [None, '', []]:  # 如果项目非空，则添加
            result.append(item)

    return result


def runMethod(index: int, method_input_data, method_program, method_parameter, method_parameter_arrayindex):
    """
    运行方法模型
    :param method: 方法模型列表
    :return:
    """

    # print(f"方法：{method_program[index]}")
    # print(f"参数层：{method_parameter[index]}")
    # print(f"向量：{method_parameter_arrayindex[index]}")
    # print(f"数据层：{method_input_data[index]}")

    # 组合方法
    full_path = method_program[index]

    method_body, method_name = os.path.split(full_path[0])

    real_input = method_input_data[index]

    # print(f"尝试导入方法体")
    # 获取算法
    function = get_algorithm_by_path(method_body, method_name)
    if not function:
        raise Exception(f"未能导入{method_name}")
    # print(f"成功导入算法: {method_name}")

    format_input = remove_empty_members(real_input)

    result = function(*format_input)
    print(f"算法运行完毕")
    # logger.info(result)
    return result
