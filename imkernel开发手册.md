# imkernel-python开发手册

# 单元模型

## 对象层

#### 创建树结构

system.element.create(id,desc,parent_id,flag)
system.element.create('design_system', '1. 设计系统','blade_optimize_system')

#### 展示树结构

system.element.print_tree()

#### 展示树描述

system.element.print_tree_desc()

#### 获取element_name的dataframe

system.element.name()

#### 根据id 获取指定 element 

system.element.get_by_id(id:str)

#### 根据description获取指定 element 

system.element.get_by_description(description:str)

---



## 参数层

### 参数组

#### 直接设置参数组

system.element.set_parameter_group(node: SystemNode, group_name_list: list[str])
#### 根据id设置参数组

示例： ['parameter_group_A','parameter_group_B','parameter_group_C']

system.element.set_parameter_group_by_id(id: str, group_name_list: list[str])

### 参数 

#### 直接设置参数

system.element.set_parameter(node: SystemNode, parameter_name_list_list: list[list[str]])

#### 根据id设置参数

示例： ['parameter_group_A','parameter_group_B','parameter_group_C']

system.element.set_parameter_by_id(id: str, parameter_name_list_list: list[list[str]])

#### 根据索引设置参数

system.element.set_parameter(index:int,group_name_list:list[list])

#### 根据索引添加参数

system.element.add_parameter(index:int,group_name_list:list[list])

---

## 数据层

system.method.create(id,desc,parent_id)
system.method.create('design_system', '1. 设计系统','blade_optimize_system')

system.procedure.create(id,desc,parent_id)
system.procedure.create('design_system', '1. 设计系统','blade_optimize_system')

# 方法模型

# 过程模型




2. Matplotlib
   方法:
    - __init__()
    - activate()
    - deactivate()
    - execute()
    - get_info()

3. ShowModel
   方法:
    - __init__()
    - process_message()
    - send_response()
    - log_message()
