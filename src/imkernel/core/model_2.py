from . import NodeBase
from . import TreeBase

ROOT_MODEL_NODE_NAME = "modeltype"


class ModelLib:
    # 模型库
    def __init__(self):
        self.ELEMENT_MODEL_NAME = '_element'
        self.METHOD_MODEL_NAME = '_method'
        self.PROCEDURE_MODEL_NAME = '_procedure'
        self.MACHINE_PERSON_NAME = '_person'
        self.ELEMENT_PERSON_NAME = '_person'
        self.PROCEDURE_MODEL_NAME = '_procedure'
        self.PROCEDURE_MODEL_NAME = '_procedure'
        self.tree = TreeBase()
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
        node = self.tree.find_node_by_id(ROOT_MODEL_NODE_NAME)
        if node is None:
            raise Exception("根节点不存在，请重新初始化")
        is_model_name_duplicated = self.tree.find_node_by_id(model_name) is not None
        if is_model_name_duplicated:
            raise Exception(f"模型名称{model_name}重复，请检查")
        # 模型节点
        self.tree.create_node(NodeBase(identification=model_name, desc=model_name), ROOT_MODEL_NODE_NAME)
        # 单元、方法、流程节点
        self.tree.create_node(NodeBase(identification=f"{model_name}{self.ELEMENT_MODEL_NAME}", desc=f"{model_name}{self.ELEMENT_MODEL_NAME}"), model_name)
        self.tree.create_node(NodeBase(identification=f"{model_name}{self.METHOD_MODEL_NAME}", desc=f"{model_name}{self.METHOD_MODEL_NAME}"), model_name)
        self.tree.create_node(NodeBase(identification=f"{model_name}{self.PROCEDURE_MODEL_NAME}", desc=f"{model_name}{self.PROCEDURE_MODEL_NAME}"), model_name)


if __name__ == '__main__':
    a = TreeBase()
    print(a)
