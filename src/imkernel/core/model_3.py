from treelib import Tree

# data 人员特性
SUPER_MODEL_NAME = "super_"
SYSTEM_MODEL_NAME = "system_"
SUB_MODEL_NAME = "sub_"

from imkernel.utils import idgen
from imkernel.utils.tree_utils import tree_to_df


def system(supname, name, subname) -> Tree:
    tree = Tree()
    sup_node = tree.create_node(supname, idgen.next_id(), None, data=SUPER_MODEL_NAME)

    if isinstance(name, str):
        if not (isinstance(subname, str) or isinstance(subname, list)):
            raise ValueError("name为字符串时，subname必须是字符串或列表.")
        sys_node = tree.create_node(name, idgen.next_id(), sup_node.identifier, data=SYSTEM_MODEL_NAME)
        if isinstance(subname, str):
            tree.create_node(subname, idgen.next_id(), sys_node.identifier, data=SUB_MODEL_NAME)
        elif isinstance(subname, list):
            for sub in subname:
                if sub is not None:
                    tree.create_node(sub, idgen.next_id(), sys_node.identifier, data=SUB_MODEL_NAME)
    elif isinstance(name, list):
        if not isinstance(subname, list):
            raise ValueError("name为列表时，subname必须是对应长度的列表.")
        if len(name) != len(subname):
            raise ValueError(f"name与subname长度不匹配: name长度：{len(name)}, subname长度：{len(subname)}.")
        for i, sys in enumerate(name):
            sys_node = tree.create_node(sys, idgen.next_id(), sup_node.identifier, data=SYSTEM_MODEL_NAME)
            sub_list = subname[i]
            if sub_list is None:
                continue
            if isinstance(sub_list, str):
                tree.create_node(sub_list, idgen.next_id(), sys_node.identifier, data=SUB_MODEL_NAME)
            elif isinstance(sub_list, list):
                for sub in sub_list:
                    tree.create_node(sub, idgen.next_id(), sys_node.identifier, data=SUB_MODEL_NAME)
            else:
                raise ValueError(f"subname的元素必须是None或列表，第{i + 1}个数组类型为{type(sub_list).__name__}")
    else:
        raise ValueError(f"name类型错误，仅允许字符串或列表，实际为{type(name).__name__}")

    print(tree)
    return tree
