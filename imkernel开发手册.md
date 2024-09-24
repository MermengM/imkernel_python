# imkernel-python开发手册

# imkernel.core

> imkernel核心库，包含三维四层定义以及基础方法。

## 单元模型

### 对象层

##### 创建树结构

system.element.create(id,desc,parent_id,flag)
system.element.create('design_system', '1. 设计系统','blade_optimize_system')

##### 展示树结构

system.element.print_tree()

##### 展示树描述

system.element.print_tree_desc()

##### 获取element_name的dataframe

system.element.name()

##### 根据id 获取指定 element 

system.element.get_by_id(id:str)

##### 根据description获取指定 element 

system.element.get_by_description(description:str)

---

### 参数层

#### 参数组

##### 直接设置参数组

system.element.set_parameter_group(node: SystemNode, group_name_list: list[str])

##### 根据id设置参数组

示例： ['parameter_group_A','parameter_group_B','parameter_group_C']

system.element.set_parameter_group_by_id(id: str, group_name_list: list[str])

##### 展示参数组Dataframe

system.element.show_parameters_group()

#### 参数 

##### 直接设置参数

system.element.set_parameter(node: SystemNode, parameter_name_list_list: list[list[str]])

##### 根据id设置参数

示例： ['parameter_group_A','parameter_group_B','parameter_group_C']

system.element.set_parameter_by_id(id: str, parameter_name_list_list: list[list[str]])

##### 展示参数Dataframe

system.element.show_parameters()

---

### 数据层

#### 添加对象数据

示例：system.element.add_model_data(['CIMSH-System1', '331-blade_01', '331-blade-sur001', 'HEBUT-BL331-001', 'HEBUT-jindiao-001', 'HNU-cinema-001', 'visual_device-001'])

system.element.add_model_data(data_list: List[str])

#### 添加参数数据

system.element.add_parameter_data(data_index, element_id, parameter_group_name, data_list):

## 方法模型

### 对象层

##### 创建树结构

system.element.create(id,desc,parent_id,flag)
system.element.create('design_system', '1. 设计系统','blade_optimize_system')

##### 展示树结构

system.element.print_tree()

##### 展示树描述

system.element.print_tree_desc()

##### 获取element_name的dataframe

system.element.name()

##### 根据id 获取指定 element 

system.element.get_by_id(id:str)

##### 根据description获取指定 element 

system.element.get_by_description(description:str)

---

### 参数层

#### 参数组

##### 直接设置输入参数组

system.element.set_input_parameter_group(node: SystemNode, group_name_list: list[str])

##### 根据id设置输入参数组

示例： ['parameter_group_A','parameter_group_B','parameter_group_C']

system.element.set_input_parameter_group_by_id(id: str, group_name_list: list[str])

##### 直接设置输出参数组

system.element.set_output_parameter_group(node: SystemNode, group_name_list: list[str])

##### 根据id设置输出参数组

示例： ['parameter_group_A','parameter_group_B','parameter_group_C']

system.element.set_output_parameter_group_by_id(id: str, group_name_list: list[str])

##### 展示输入参数组Dataframe

system.element.show_input_parameters_group()

##### 展示输出参数组Dataframe

system.element.show_output_parameters_group()

##### 展示输入输出参数组Dataframe

system.element.show_parameters_group()

#### 参数 

##### 直接设置输入参数

system.element.set_input_parameter(node: SystemNode, parameter_name_list_list: list[list[str]])

##### 根据id设置输入参数

示例： ['parameter_group_A','parameter_group_B','parameter_group_C']

system.element.set_input_parameter_by_id(id: str, parameter_name_list_list: list[list[str]])

##### 直接设置输出参数

system.element.set_output_parameter(node: SystemNode, parameter_name_list_list: list[list[str]])

##### 根据id设置输出参数

示例： ['parameter_group_A','parameter_group_B','parameter_group_C']

system.element.set_output_parameter_by_id(id: str, parameter_name_list_list: list[list[str]])

##### 展示输入参数Dataframe

system.element.show_input_parameters()

##### 展示输出参数Dataframe

system.element.show_output_parameters()

##### 展示输入以及输出参数Dataframe

system.element.show_parameters()

---

### 数据层

##### 直接设置输入参数数据

system.method.set_input_parameter_data(node: SystemNode, parameter_name_list_list: list[list[str]])

##### 直接设置输出参数数据

示例： ['parameter_group_A','parameter_group_B','parameter_group_C']

system.method.set_output_parameter_data(id: str, parameter_name_list_list: list[list[str]])

##### 获取所有参数数据列表Dataframe

system.method.show_parameter_data():

##### 获取指定参数数据列表Dataframe

system.method.show_parameter_data(id:str):

### 分析

#### 运行指定方法模型 

system.method.run(id:str):

## 过程模型

### 对象层

##### 创建树结构

system.procedure.create(id: str, description: str = None, parent_id: str = None, is_tag: bool = False)

##### 关联对象模型和方法模型

system.procedure.relate(id: str, description: str = None, parent_id: str = None, is_tag: bool = False)

# imkernel.v3d

> 用于在jupyter中渲染三维图形

