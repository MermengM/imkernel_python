from imkernel.utils.tree_utils import tree_to_df
from treelib import Tree

# 示例树
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

index_levels = ['model', 'model_type', 'submodel type', 'person']
columns = ['penson0', 'person1']
# index_levels=None
# columns=None
df = tree_to_df(tree=tree, index_num=4, columns_num=1, index_levels=index_levels, columns=columns)
print(df)
df
