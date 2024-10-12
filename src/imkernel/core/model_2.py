from . import NodeBase
from . import TreeBase

ROOT_MODEL_NODE_NAME = "modeltype"


class NewModel:
    def __init__(self, model_name, model_desc):
        self.model_name = model_name
        self.model_desc = model_desc
        self.model_subtype_list = []


class ModelLib:
    # 模型库
    def __init__(self):
        self.ELEMENT_MODEL_NAME = '_element'
        self.METHOD_MODEL_NAME = '_method'
        self.PROCEDURE_MODEL_NAME = '_procedure'
        self.ELEMENT_MACHINE_NAME = '_machine'
        self.ELEMENT_PERSON_NAME = '_person'
        self.ELEMENT_PRODUCT_NAME = '_product'
        self.tree = TreeBase()
        self.model_list = []
        # 创建根节点
        self.tree.create_node(NodeBase(identification=ROOT_MODEL_NODE_NAME, desc=ROOT_MODEL_NODE_NAME))
        print(self.tree)

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
        node = self.tree.find_node_by_id(ROOT_MODEL_NODE_NAME)
        if node is None:
            raise Exception("根节点不存在，请重新初始化")
        is_model_name_duplicated = self.tree.find_node_by_id(model_name) is not None
        if is_model_name_duplicated:
            raise Exception(f"模型名称{model_name}重复，请检查")
        # 模型节点
        self.tree.create_node(NodeBase(identification=model_name, desc=model_name), ROOT_MODEL_NODE_NAME)
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


if __name__ == '__main__':
    a = ModelLib()
    a.create_new_model('insofaiam')
    a.create_new_model('insoftest')
    a.create_new_model('insofrobot')

    print(a.tree)
