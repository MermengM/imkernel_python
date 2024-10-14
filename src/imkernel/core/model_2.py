from .utils import SnowflakeIDGenerator
from . import NodeBase
from . import TreeBase
import pandas as pd

id_generator = SnowflakeIDGenerator(datacenter_id=1, worker_id=1)


class SubType:
    def __init__(self, subtype_name):
        self.subtype_name = subtype_name


class ParameterProperty:
    # 参数特性
    def __init__(self, name):
        self.id = id_generator.generate_id()
        self.name = name


class Parameter:
    # 参数
    def __init__(self, name):
        self.id: int = id_generator.generate_id()
        self.name: str = name
        self.property_list: list[ParameterProperty] = []

    def __getattr__(self, name):
        """
        重写getattr
        :param name:
        :return:
        """
        for prop in self.property_list:
            if prop.name == name:
                return prop
        raise KeyError(f"参数：{self.name}中未找到名为{name}的特性")

    def add_property(self, name):
        """
        增加参数特性
        :param name:参数特性名
        """
        self.property_list.append(ParameterProperty(name=name))


class NewModel:
    def __init__(self, model_name, model_desc):
        self.model_name = model_name
        self.model_desc = model_desc
        self.model_subtype_list: list[SubType] = []
        self.parameter_list: list[Parameter] = []
        self.element_id_dict = {}

    def __getattr__(self, name):
        """
        重写getattr
        :param name:
        :return:
        """
        for para in self.parameter_list:
            if para.name == name:
                return para
        raise KeyError(f"未找到名为{name}的参数")

    def add_parameter(self, name):
        """
        增加参数
        :param name:参数名
        """
        self.parameter_list.append(Parameter(name=name))

    def add_subtype(self, subtype_name):
        subtype = SubType(subtype_name)
        self.model_subtype_list.append(subtype)

    def find_subtype(self, subtype_name):
        for subtype in self.model_subtype_list:
            if subtype.subtype_name == subtype_name:
                return subtype
        raise Exception(f"未找到{subtype_name}")


class ModelLib:
    # 模型库
    def __init__(self):
        # 固定名称
        self.ROOT_MODEL_NODE_NAME = "modeltype"
        self.ELEMENT_MODEL_NAME = '_element'
        self.METHOD_MODEL_NAME = '_method'
        self.PROCEDURE_MODEL_NAME = '_procedure'
        self.ELEMENT_MACHINE_NAME = '_machine'
        self.ELEMENT_PERSON_NAME = '_person'
        self.ELEMENT_PRODUCT_NAME = '_product'
        # 树结构
        self.tree = TreeBase()
        # 模型列表
        self.model_list = []
        # 创建根节点
        self.tree.create_node(NodeBase(identification=self.ROOT_MODEL_NODE_NAME, desc=self.ROOT_MODEL_NODE_NAME))

    def __str__(self):
        return self.tree.__str__()

    def __getattr__(self, name):
        """
        重写getattr
        :param name:
        :return:
        """
        for model in self.model_list:
            if model.model_name == name:
                return model
        raise KeyError(f"找不到{name}")

    def show_subtype(self):
        """
        显示subtype的df
        :return:
        """
        data = []
        for model in self.model_list:
            row_dict = {'model_name': model.model_name}
            model: NewModel
            for index, subtype in enumerate(model.model_subtype_list):
                row_dict[f'model_subtype_{index}'] = subtype.subtype_name
            data.append(row_dict)
        return pd.DataFrame(data)

    def _add_node_to_root(self):
        """
        为模型库添加新模型（三维四层初始结构）
        """

    def create_new_model(self, model_name):
        """
        为模型库添加新模型（三维四层初始结构）
        :param model_name:模型名称
        """
        # region 树结构处理
        node = self.tree.find_node_by_id(self.ROOT_MODEL_NODE_NAME)
        if node is None:
            raise Exception("根节点不存在，请重新初始化")
        is_model_name_duplicated = self.tree.find_node_by_id(model_name) is not None
        if is_model_name_duplicated:
            raise Exception(f"模型名称{model_name}重复，请检查")
        # 模型节点
        self.tree.create_node(NodeBase(identification=model_name, desc=model_name), self.ROOT_MODEL_NODE_NAME)
        # 单元、方法、流程节点
        # 单元、人、机、物
        self.tree.create_node(NodeBase(identification=f"{model_name}{self.ELEMENT_MODEL_NAME}", desc=f"{model_name}{self.ELEMENT_MODEL_NAME}"), model_name)
        self.tree.create_node(NodeBase(identification=f"{model_name}{self.ELEMENT_PERSON_NAME}", desc=f"{model_name}{self.ELEMENT_PERSON_NAME}"), f"{model_name}{self.ELEMENT_MODEL_NAME}")
        self.tree.create_node(NodeBase(identification=f"{model_name}{self.ELEMENT_MACHINE_NAME}", desc=f"{model_name}{self.ELEMENT_MACHINE_NAME}"), f"{model_name}{self.ELEMENT_MODEL_NAME}")
        self.tree.create_node(NodeBase(identification=f"{model_name}{self.ELEMENT_PRODUCT_NAME}", desc=f"{model_name}{self.ELEMENT_PRODUCT_NAME}"), f"{model_name}{self.ELEMENT_MODEL_NAME}")
        # 方法
        self.tree.create_node(NodeBase(identification=f"{model_name}{self.METHOD_MODEL_NAME}", desc=f"{model_name}{self.METHOD_MODEL_NAME}"), model_name)
        self.tree.create_node(NodeBase(identification=f"{model_name}{self.PROCEDURE_MODEL_NAME}", desc=f"{model_name}{self.PROCEDURE_MODEL_NAME}"), model_name)
        # endregion
        # region 模型处理
        model = NewModel(model_name=model_name, model_desc=model_name)
        self.model_list.append(model)
        # endregion


if __name__ == '__main__':
    a = ModelLib()
    a.create_new_model('insofaiam')
    a.create_new_model('insoftest')
    a.create_new_model('insofrobot')

    print(a.tree)
