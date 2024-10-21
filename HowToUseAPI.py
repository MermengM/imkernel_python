from treelib import Tree
from imkernel.core.api_utils import APIUtils
from imkernel.core.node import Node
from imkernel import get_paths_dict

tree = Tree()
tree.create_node("modeltype", "modeltype")  # 根节点
tree.create_node("insofaiam", "insofaiam", parent="modeltype")
tree.create_node("insofmining", "insofmining", parent="insofaiam")
tree.create_node("insofrobot", "insofrobot", parent="modeltype")
tree.create_node("insofbend", "insofbend", parent="insofrobot")
tree.create_node("insoflaser", "insoflaser", parent="insofrobot")
tree.create_node("insoftube", "insoftube", parent="insofrobot")
tree.create_node("insoftest", "insoftest", parent="modeltype")
tree.create_node("DTIS-511", "DTIS-511", parent="insoftest")
tree.create_node("NDT-SNPTC", "NDT-SNPTC", parent="insoftest")
tree.create_node("个人", "personal", parent="DTIS-511")
tree.create_node("机构", "organization", parent="DTIS-511")
tree.create_node("职位", "position", parent="DTIS-511")
tree.create_node("角色", "role", parent="DTIS-511")
tree.create_node("账号", "account", parent="DTIS-511")
tree.create_node("你好", "nihao", parent="insoftube")
a = get_paths_dict(tree)
print(a)
api_utils = APIUtils("http://139.196.154.85:54742")
try:
    # api_utils.create_node("ExampleNode", "example_type")  # 创建节点.
    print(api_utils.get_all_model())  # 获取所有model
    # print(api_utils.get_all_supermodel())  # 获取所有supermodel
    # print(api_utils.tree_init())  # 初始化树
    # node = api_utils.trees()
    # node[0].print_tree()
    # api_utils.create_model('DTIS-511', 'insoftest')
    # node = api_utils.get_node_by_id('1847150891292037120')
    # node[0].print_tree()
    # api_utils.create_node("ExampleNode", "example_type")  # 创建节点
    # api_utils.create_node("ExampleNode", "example_type")  # 创建节点
    print(1)
except Exception as e:
    print(e)
