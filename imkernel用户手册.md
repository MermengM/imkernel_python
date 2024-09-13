# imkernel Python 包使用手册

## 目录

1. [简介](#简介)
2. [安装](#安装)
3. [基本结构](#基本结构)
4. [使用示例](#使用示例)
5. [API 参考](#api-参考)
6. [常见问题](#常见问题)

## 简介

imkernel 是一个 Python 包,用于...（在此处添加包的主要功能和用途）

## 安装

使用 pip 安装 imkernel:

```bash
pip install imkernel
```

## 基本结构

imkernel 包主要包含以下模块:

- `core`: 核心功能模块，提供基础功能和工具。
- `ShowModel` 三维展示模块

## 类

### industry_model

#### `class industry_model`

工业模型类，用于管理单元模型、方法模型、过程模型。

**主要方法**:

- `__init__(self, element_parameter=None, element_data=None, method_parameter=None, method_data=None, procedure_parameter=None)`

  初始化工业模型。

- `get_element_parameter_df(self, parameter_group_name: str = None, with_data=False)`

  获取元素参数的DataFrame。

- `add_element(self, parameter_list: list, data_list: list)`

  添加元素到模型中。

- `add_method(self, parameter_list: list, data_list: list)`

  添加方法到模型中。

- `get_method_parameter_df(self, parameter_group_name: str = None, with_data=False)`

  获取方法参数的DataFrame。


- `get_procedure_parameter_df(self, procedure_name: str = None, with_data=False)`

  获取流程参数的DataFrame。

- `run_procedure(self, procedure_name: str)`

  运行指定的流程。

## API 参考

### core

- `search_node(tree: Tree,node_identifier:str) -> str`

### ShowModel

- ...

## 使用示例

---

### `search_node` 方法

该方法用于在树结构中查找节点的层级关系，并返回层级关系字符串。

#### 功能描述

- **输入**:
    - `tree`: `treelib` 库中的 `Tree` 对象。
    - `node_identifier`: 节点标识符，可以是节点的 `id` 或 `tag`。

- **输出**:
    - 返回节点的层级关系字符串，格式如 `Root -> Child -> Node`。

#### 示例用法

```python
from treelib import Tree
from src.core import search_node

# 创建示例树结构
tree = Tree()
tree.create_node("Root", "root")
tree.create_node("Child", "child", parent="root")
tree.create_node("Node", "node", parent="child")

# 查找节点并获取层级关系
hierarchy = search_node(tree, "node")
print(hierarchy)  # 输出: Root -> Child -> Node
```

---

## `get_algorithm_by_path` 方法

该方法用于动态导入指定路径的 Python 脚本，并获取其中的指定函数。

### 功能描述

- **输入**:
    - `algo_file`: 算法文件的路径。
    - `algo_name`: 算法函数的名称。

- **输出**:
    - 返回指定的算法函数对象。
    - 如果导入失败，返回 `None`。

- **功能**:
    - 动态加载 Python 脚本。
    - 获取并返回指定名称的函数。

### 示例用法

```python
from src.core import get_algorithm_by_path

# 指定算法文件路径和函数名称
algo_file = r"E:\path\to\algorithm.py"
algo_name = "my_algorithm_function"

# 获取算法函数
algorithm_function = get_algorithm_by_path(algo_file, algo_name)

if algorithm_function:
    # 使用获取的函数
    result = algorithm_function()
    print("Result:", result)
```

### 注意事项

- 确保 `algo_file` 路径正确且文件存在。
- 确保 `algo_name` 在指定文件中定义。
- 处理可能的异常或错误日志。

---

## 常见问题
