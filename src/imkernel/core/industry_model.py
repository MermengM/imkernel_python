# import inspect
# import pandas as pd
# from loguru import logger
# import copy
# from .utils import get_algorithm_by_path
#
#
# class industry_model:
#     def __init__(
#             self,
#             element_parameter=None,
#             element_data=None,
#             method_parameter=None,
#             method_data=None,
#             procedure_parameter=None,
#
#     ):
#         self.param_type_messages = {
#             "element": "单元模型",
#             "method": "方法模型",
#             "procedure": "过程模型"}
#         self.element_parameter = element_parameter if element_parameter is not None else []
#         self.element_parameter_name = []
#         self.element_data = {}
#         self.method_parameter = method_parameter if method_parameter is not None else []
#         self.method_data = {}
#         self.procedure_parameter = procedure_parameter if procedure_parameter is not None else []
#         self.dataframes = {
#             'element_parameter': self.element_parameter,
#             'method_parameter': self.method_parameter,
#             'procedure_parameter': self.procedure_parameter
#         }
#         #
#         # # 验证输入的DataFrame
#         # for name, df in self.dataframes.items():
#         #     if df is not None and not isinstance(df, pd.DataFrame):
#         #         raise TypeError(f"{name} 必须是dataframe")
#
#     def _get_element_parameter(self, parameter_group_name: str = None):
#         """
#         获取指定单元参数（组）
#         @param parameter_group_name: 参数组名称
#         @return:
#         @return:
#         """
#         parameter_list = []
#         if not parameter_group_name:
#             parameter_list = copy.deepcopy(self.element_parameter)
#         else:
#             parameter_list = [copy.deepcopy(x) for x in self.element_parameter if x[0] == parameter_group_name]
#
#         if not parameter_list:
#             raise Exception(f"未找到名为{parameter_group_name}的参数")
#
#         return parameter_list
#
#     def get_element_parameter_df(self, parameter_group_name: str = None, with_data=False):
#         """
#         获取当前模型中所有的单元参数（组）
#         @param parameter_group_name: 参数组名称
#         @param with_data: 带上数据
#         @return:
#         @return:
#         """
#         parameter_list = self._get_element_parameter(parameter_group_name)
#
#         columns = ['element']
#         max_params = max(len(item) - 1 for item in parameter_list)
#         columns.extend([f'parameter{i + 1}' for i in range(max_params)])
#         # 添加数据
#         if with_data:
#             for p_group in parameter_list:
#                 for i, p in enumerate(p_group):
#                     data = self.element_data.get(p, f"None")
#                     p_group[i] = f"{p} = {data}"
#
#         df = pd.DataFrame(parameter_list, columns=columns)
#
#         return df
#
#     def add_element(self, parameter_list: list, data_list: list):
#         """
#         添加单元模型
#         @param parameter_list: 参数列表
#         @param data_list: 列表/参数值列表
#         """
#         data_list = data_list[0]
#
#         # 检查 parameter_list 和 data_list 的长度是否匹配
#         if len(parameter_list) != len(data_list):
#             raise ValueError("参数和数据列表长度不匹配")
#
#         # 遍历 parameter_list 并检查是否已存在，然后添加到 self.element_data
#         for index, key in enumerate(parameter_list):
#             if key in self.element_data:
#                 logger.error(f"键 '{key}' 已经存在")
#             else:
#                 self.element_data[key] = data_list[index]
#
#     def set_element_data(self, para_name: str, data_list: list):
#         """
#         添加单元模型数据
#         @param para_name: 参数名
#         @param data_list: 参数值列表
#         """
#         # 获取self.element_data 指定key 的 对象 而不是值
#         if para_name not in self.element_data:
#             raise Exception(f"未找到单元参数{para_name}")
#
#         self.element_data[para_name] = data_list
#
#     def _get_method_parameter(self, parameter_group_name: str = None):
#         """
#         获取指定单元参数方法参数（组）
#         @param parameter_group_name: 参数组名称
#         @return:
#         @return:
#         """
#         parameter_list = []
#         if not parameter_group_name:
#             parameter_list = copy.deepcopy(self.method_parameter)
#         else:
#             parameter_list = [copy.deepcopy(x) for x in self.method_parameter if x[0] == parameter_group_name]
#
#         if not parameter_list:
#             raise Exception(f"未找到名为{parameter_group_name}的参数")
#         return parameter_list
#
#     def get_method_parameter_df(self, parameter_group_name: str = None, with_data=False):
#         """
#         获取当前模型中所有的方法参数（组）
#         @param parameter_group_name: 参数组名称
#         @param with_data: 带上数据
#         @return:
#         @return:
#         """
#         parameter_list = self._get_method_parameter(parameter_group_name)
#
#         columns = ['element']
#         max_params = max(len(item) - 1 for item in parameter_list)
#         columns.extend([f'parameter{i + 1}' for i in range(max_params)])
#         # 添加数据
#         if with_data:
#             for p_group in parameter_list:
#                 for i, p in enumerate(p_group):
#                     data = self.method_data.get(p, f"None")
#                     p_group[i] = f"{p} = {data}"
#
#         df = pd.DataFrame(parameter_list, columns=columns)
#
#         return df
#
#     def add_method(self, parameter_list: list, data_list: list):
#         """
#         添加方法模型
#         @param parameter_list: 参数列表
#         @param data_list: 列表/参数值列表
#         """
#         data_list = data_list[0]
#
#         # 检查 parameter_list 和 data_list 的长度是否匹配
#         if len(parameter_list) != len(data_list):
#             raise ValueError("参数和数据列表长度不匹配")
#
#         # 遍历 parameter_list 并检查是否已存在，然后添加到 self.element_data
#         for index, key in enumerate(parameter_list):
#             if key in self.method_data:
#                 pass
#                 # logger.error(f"键 '{key}' 已经存在")
#             self.method_data[key] = data_list[index]
#
#     def set_method_data(self, para_name: str, data_list: list):
#         """
#         添加方法模型数据
#         @param para_name: 参数名
#         @param data_list: 参数值列表
#         """
#         # 获取self.element_data 指定key 的 对象 而不是值
#         para_name = f"method_{para_name}"
#         if para_name not in self.method_data:
#             raise Exception(f"未找到方法参数{para_name}")
#
#         self.method_data[para_name] = data_list
#
#     def _get_procedure_parameter(self, procedure_name: str = None):
#         """
#         获取当前模型中所有的过程参数（组）
#         @param procedure_name:流程名
#         @return:
#         """
#         procedure_list = []
#         if not procedure_name:
#             procedure_list = copy.deepcopy(self.procedure_parameter)
#         else:
#             procedure_list = [copy.deepcopy(x) for x in self.procedure_parameter if x[0] == procedure_name]
#
#         if not procedure_list:
#             raise Exception(f"未找到名为{procedure_name}的流程")
#
#         return procedure_list
#
#     def get_procedure_parameter_df(self, procedure_name: str = None, with_data=False):
#         """
#         获取当前模型中所有的过程参数（组）
#         @param procedure_name:流程名
#         @param with_data:带上数据
#         @return:
#         """
#         procedure_list = self._get_procedure_parameter(procedure_name)
#
#         columns = ['procedure', 'element', 'method']
#         # 添加数据
#         if with_data:
#             for p_group in procedure_list:
#                 element_name = p_group[1]
#                 method_name = p_group[2]
#                 # 处理单元模型
#                 element_parameter = self._get_element_parameter(element_name)
#                 p_group[1] = f"{p_group[1]}={element_parameter}"
#                 # 处理方法模型
#                 method_parameter = self._get_method_parameter(method_name)
#                 p_group[2] = f"{p_group[2]}={method_parameter}"
#
#         df = pd.DataFrame(procedure_list, columns=columns)
#
#         return df
#
#     def run_procedure(self, procedure_name: str):
#         """
#         运行指定流程
#         @param procedure_name:流程名
#         """
#         # 获取流程信息
#         # procedure	element	method
#         procedure_info = next((item for item in self.procedure_parameter if item[0] == procedure_name), None)
#         if procedure_info is None:
#             raise Exception(f"流程{procedure_name}不存在!")
#         else:
#             print(f"开始运行流程模型：{procedure_name}")
#
#         procedure_element_name = procedure_info[1]
#         procedure_method_name = procedure_info[2]
#
#         print(f"算法模型：{procedure_method_name}")
#         print(f"单元模型：{procedure_element_name}")
#
#         # 获取单元参数信息
#         # element parameter1 parameter2	parameter3 parameter4 parameter5 ....
#         element_parameter_info = next((item for item in self.element_parameter if item[0] == procedure_element_name), None)
#
#         # 获取算法参数信息
#         # method EXE_file input	output1	output2 ....
#         method_parameter_info = next((item for item in self.method_parameter if item[0] == procedure_method_name), None)
#         if not method_parameter_info:
#             raise Exception(f"算法{procedure_method_name}匹配不到对应参数。")
#         elif len(method_parameter_info) < 4:
#             raise Exception(f"算法{procedure_method_name}参数数量不足!")
#
#         # 根据单元参数获取单元数据
#         element_data_info = []
#         for element_par_name in element_parameter_info:
#             element_par = self.element_data[element_par_name]
#             element_data_info.append(element_par)
#
#         # 根据方法参数获取方法数据
#         method_data_info = []
#         for method_par_name in method_parameter_info:
#             method_par = self.method_data[method_par_name]
#             method_data_info.append(method_par)
#
#         # 处理输入参数
#         input_parameter_name = method_parameter_info[2]
#         if input_parameter_name.startswith('method_'):
#             # 从input_parameter_name中删除 method_ 获取实际参数名
#             input_parameter_name = input_parameter_name.replace('method_', '')
#
#         # 检查键是否存在于 self.element_data 中
#         if input_parameter_name not in self.element_data:
#             raise KeyError(f"参数 '{input_parameter_name}'不存在，请检查")
#         print(f"输入参数：{input_parameter_name}")
#         print(f"输入参数值：{self.element_data[input_parameter_name]}")
#         # print(f"输出参数：{input_parameter_name}")
#         # real_input=method_data_info[2]
#         real_input = [self.element_data[input_parameter_name]]
#
#         # 处理输出参数
#         real_output = method_data_info[3]
#         print(f"尝试导入方法体")
#         # 获取算法
#         function = get_algorithm_by_path(method_data_info[1][0], method_data_info[0][0])
#         if not function:
#             raise Exception(f"未能导入{method_data_info[1][0]}")
#         print(f"成功导入算法: {method_data_info[0][0]}")
#
#         result = function(*real_input)
#         # print(f"算法运行完毕，结果如下：\n{result}")
#         # logger.info(result)
#         return result
#
#     def run_method(self, method_name: str):
#         """
#         运行指定方法模型
#         :param method_name: 算法名
#         :return:
#         """
#         # 获取流程信息
#         # procedure	element	method
#         method_parameter_info = next((item for item in self.method_parameter if item[0] == method_name), None)
#         if method_parameter_info is None:
#             raise Exception(f"算法{method_name}不存在!")
#         else:
#             print(f"开始运行算法模型：{method_name}")
#
#         # 根据方法参数获取方法数据
#         method_data_info = []
#         for method_par_name in method_parameter_info:
#             method_par = self.method_data[method_par_name]
#             method_data_info.append(method_par)
#
#         # 处理输入参数
#         input_parameter_name = method_parameter_info[2]
#         input_parameter_data = method_data_info[2]
#         if input_parameter_name.startswith('method_'):
#             # 从input_parameter_name中删除 method_ 获取实际参数名
#             input_parameter_name = input_parameter_name.replace('method_', '')
#
#         print(f"输入参数：{input_parameter_name}")
#         print(f"输入参数值：{input_parameter_data}")
#         # print(f"输出参数：{input_parameter_name}")
#         # real_input=method_data_info[2]
#         real_input = input_parameter_data
#
#         # 处理输出参数
#         real_output = method_data_info[3]
#         print(f"尝试导入方法体")
#         # 获取算法
#         function = get_algorithm_by_path(method_data_info[1][0], method_data_info[0][0])
#         if not function:
#             raise Exception(f"未能导入{method_data_info[1][0]}")
#         print(f"成功导入算法: {method_data_info[0][0]}")
#
#         result = function(real_input)
#         # print(f"算法运行完毕，结果如下：\n{result}")
#         # logger.info(result)
#         return result
#
#     def _get_parameter(self, param_type: str, parameter_group_name: str = None):
#         """
#         获取指定类型的参数（组）
#         @param param_type: 参数类型 ('element', 'method', 'procedure')
#         @param parameter_group_name: 参数组名称
#         @return:
#         """
#         if param_type == "element":
#             parameter_list = copy.deepcopy(self.element_parameter)
#         elif param_type == "method":
#             parameter_list = copy.deepcopy(self.method_parameter)
#         elif param_type == "procedure":
#             parameter_list = copy.deepcopy(self.procedure_parameter)
#         else:
#             raise ValueError(f"未知的参数类型: {param_type}")
#
#         if parameter_group_name:
#             parameter_list = [x for x in parameter_list if x[0] == parameter_group_name]
#
#         if not parameter_list:
#             friendly_type = self.param_type_messages.get(param_type, param_type)
#
#             raise Exception(f"未找到名为{parameter_group_name}的{friendly_type}参数")
#
#         return parameter_list
#
#     def _get_vector(self, param_type: str, parameter_group_name: str = None):
#         """
#         获取指定类型的参数（组）
#         @param param_type: 参数类型 ('element', 'method', 'procedure')
#         @param parameter_group_name: 参数组名称
#         @return:
#         """
#         if param_type == "element":
#             vector_dict = copy.deepcopy(self.element_data)
#         elif param_type == "method":
#             vector_dict = copy.deepcopy(self.method_data)
#         elif param_type == "procedure":
#             # parameter_list = copy.deepcopy(self.procedure_parameter)
#             raise ValueError(f"暂无")
#         else:
#             raise ValueError(f"未知的参数类型: {param_type}")
#
#         if parameter_group_name:
#             if parameter_group_name in vector_dict:
#                 vector_dict = vector_dict[parameter_group_name]
#
#         if not vector_dict:
#             friendly_type = self.param_type_messages.get(param_type, param_type)
#
#             raise Exception(f"未找到名为{parameter_group_name}的{friendly_type}向量")
#
#         return vector_dict
#
#
# def get_parameter_df(model, para_type: str, para_name: str = None, with_data=False):
#     """
#     获取当前模型中指定类型的参数（组）
#     @param para_type: 参数类型 ('element', 'method', 'procedure')
#     @param para_name: 参数组名称
#     @param with_data: 是否带上数据
#     @return: DataFrame
#     """
#     parameter_list = model._get_parameter(para_type, para_name)
#
#     if para_type in ['element', 'method']:
#         columns = ['element']
#         max_params = max(len(item) - 1 for item in parameter_list)
#         columns.extend([f'parameter{i + 1}' for i in range(max_params)])
#         if with_data:
#             data_dict = model.element_data if para_type == 'element' else model.method_data
#             for p_group in parameter_list:
#                 for i, p in enumerate(p_group):
#                     data = data_dict.get(p, f"None")
#                     p_group[i] = f"{p} = {data}"
#     elif para_type == 'procedure':
#         columns = ['procedure', 'element', 'method']
#         if with_data:
#             for p_group in parameter_list:
#                 element_name = p_group[1]
#                 method_name = p_group[2]
#                 # 处理单元模型
#                 element_parameter = model._get_parameter('element', element_name)
#                 p_group[1] = f"{element_name}={element_parameter}"
#                 # 处理方法模型
#                 method_parameter = model._get_parameter('method', method_name)
#                 p_group[2] = f"{method_name}={method_parameter}"
#     else:
#         raise ValueError(f"未知的参数类型: {para_type}")
#
#     df = pd.DataFrame(parameter_list, columns=columns)
#
#     return df
#
#
# def get_vector_df(model, para_type: str, para_name: str = None):
#     """
#     获取当前模型中指定类型的参数向量
#     @param para_type: 参数类型 ('element', 'method', 'procedure')
#     @param para_name: 参数组名称
#     @param with_data: 是否带上数据
#     @return: DataFrame
#     """
#
#     parameter_dict = model._get_vector(para_type, para_name)
#
#     # 创建DataFrame
#     df = pd.DataFrame(parameter_dict)
#
#     # 设置列名
#     num_columns = df.shape[1]
#     df.columns = [f'Param_{i + 1}' for i in range(num_columns)]
#
#     # 添加行索引
#     df.index.name = 'Row'
#     df.index = df.index + 1  # 使行索引从1开始
#
#     # 设置显示选项
#     pd.set_option('display.max_columns', None)  # 显示所有列
#     pd.set_option('display.width', None)  # 自动调整显示宽度
#     pd.set_option('display.precision', 4)  # 设置浮点数精度
#
#     return df
#
#
# def get_specific_variable(variable_name):
#     # 获取调用此函数的帧
#     frame = inspect.currentframe().f_back
#
#     # 获取该帧的局部和全局变量
#     variables = {**frame.f_locals, **frame.f_globals}
#
#     # 查找特定名称的变量
#     if variable_name in variables:
#         return {variable_name: variables[variable_name]}
#     else:
#         return None
#
#
# def run_method(method_data_list):
#     """
#     运行指定数据
#     :param method_data_list: 数据
#     :return:
#     """
#     method_data_list = method_data_list[0]
#     # print(method_data_list)
#
#     algo_name = method_data_list[0][0]
#     algo_file = method_data_list[1][0]
#     input_parameter = method_data_list[2]
#
#     # print(f"尝试导入方法体")
#     # 获取算法
#     function = get_algorithm_by_path(algo_file,algo_name )
#     if not function:
#         raise Exception(f"未能导入{algo_file}")
#     print(f"算法运行中")
#
#     result = function(input_parameter)
#     # print(f"算法运行完毕，结果如下：\n{result}")
#     print(f"算法运行完毕")
#     # logger.info(result)
#     return result
