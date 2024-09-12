# imkernel Python 包开发手册

## 目录

imkernel包开发手册概要：

system.element.
system.method.create
### System
   #### 字段:element
   字段:method
   字段:procedure
   方法:
    - __init__()
# 单元模型
## 对象层
### 创建树结构
system.element.create(id,desc,parent_id,flag)
system.element.create('design_system', '1. 设计系统','blade_optimize_system')
### 展示树结构
system.element.print_tree()
### 展示所有叶子节点
- system.element.print_leaves()
### 获取element_name
- system.element.get_element_name()
### 根据id 获取指定 element 
- system.element.get_by_id(id:str)
## 参数层
### 添加参数组(行)  ['parameter_group_A','parameter_group_B','parameter_group_C']
- system.element.set_parameter_group(id:str,group_name_list:list)
- system.element.set_parameter_group(index:int,group_name_list:list)
- ~~system.element.add_parameter_group(id:str,group_name_list:list)~~
- ~~system.element.add_parameter_group(index:int,group_name_list:list)~~
### 添加参数  ['parameterA','parameterB','parameterC']
- system.element.set_parameters(id:str,parameter_list:list[list])
- system.element.set_parameters(index:int,parameter_list:list[list])
## 数据层



system.method.create(id,desc,parent_id)
system.method.create('design_system', '1. 设计系统','blade_optimize_system')

system.procedure.create(id,desc,parent_id)
system.procedure.create('design_system', '1. 设计系统','blade_optimize_system')


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
