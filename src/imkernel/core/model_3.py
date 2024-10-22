from treelib import Tree

# data 人员特性
SUPER_MODEL_NAME = "super_"
SYSTEM_MODEL_NAME = "system_"
SUB_MODEL_NAME = "sub_"


def system(supname, name, subname) -> Tree:
    tree = Tree()
    sup_node = tree.create_node(supname, SUPER_MODEL_NAME + supname, None)
    if isinstance(name, str):
        sys_node = tree.create_node(name, SYSTEM_MODEL_NAME + name, sup_node)
    elif isinstance(name, str):
        pass

    if isinstance(subname, str):
        sub_node = tree.create_node(subname, SUB_MODEL_NAME + subname, sys_node)
    elif isinstance(subname, list):
        sub_model_list = []
        for sub in subname:
            sub_node = tree.create_node(sub, SUB_MODEL_NAME + sub, sys_node)
            sub_model_list.append(sub_node)
    print(tree)
    return tree


if __name__ == '__main__':
    tree_1 = system(supname='insofsys', name='insoftest', subname='DTIS_511')
    tree_2 = system(supname='insofsys', name='insoftest', subname=['DTIS_511', 'NDT_SNPTC'])
    print('end')
