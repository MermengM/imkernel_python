import json
from typing import Dict, Optional, List

import requests
from .node import Node


def build_tree(data) -> List[Node]:
    root_nodes: List[Node] = []

    def create_node(node_data: Dict, parent: Optional[Node] = None) -> Node:
        node = Node(
            id=node_data['id'],
            name=node_data['name'],
            node_type=node_data['node_type'],
            parent=parent
        )

        # Set parent relationship
        if parent:
            parent.children.append(node)
            node.parent = parent
            node.parent_id = parent.id

        # Recursively create child nodes
        for child_data in node_data.get('children', []):
            create_node(child_data, node)

        return node

    # Create nodes starting from root nodes
    for root_node_data in data:
        root_node = create_node(root_node_data)
        root_nodes.append(root_node)

    return root_nodes


class APIUtils:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_all_model(self):
        """获取所有model"""
        response = requests.get(f'{self.base_url}/get_all_model')
        if response.status_code == 200:
            d = response.json()['data']
            return response.json()['data']
        else:
            raise Exception(f"获取模型失败: {response.text}")

    def get_node_by_id(self, node_id):
        """
        根据id获取节点名称
        :return:
        """
        response = requests.get(f'{self.base_url}/get_node_by_id', params={'id': node_id})
        if response.status_code == 200:
            return response.json()['data']
        else:
            raise Exception(f"Failed to fetch models: {response.text}")

    def get_all_supermodel(self):
        """获取所有supermodel"""
        response = requests.get(f'{self.base_url}/get_all_supermodel')
        if response.status_code == 200:
            return response.json()['data']
        else:
            raise Exception(f"Failed to fetch supermodels: {response.text}")

    def get_all_type(self):
        """获取所有类型"""
        response = requests.get(f'{self.base_url}/get_all_type')
        if response.status_code == 200:
            return response.json()['data']
        else:
            raise Exception(f"Failed to fetch types: {response.text}")

    def tree_init(self):
        """初始化树"""
        response = requests.get(f'{self.base_url}/tree_init')
        if response.status_code == 200:
            return response.json()['message']
        else:
            raise Exception(f"Failed to initialize tree: {response.text}")

    def trees(self):
        response = requests.get(f'{self.base_url}/trees')
        if response.status_code == 200:
            data = response.json()['data']
            node_list = build_tree(data)
            return node_list
        else:
            raise Exception(f"Failed to create node: {response.text}")

    def create_node(self, name, node_type, parent_id=None):
        """创建节点"""
        payload = {
            'name': name,
            'node_type': node_type,
            'parent_id': parent_id
        }
        response = requests.post(f'{self.base_url}/create_node', json=payload)
        if response.status_code == 200:
            return response.json()['message']
        else:
            raise Exception(f"Failed to create node: {response.text}")

    def create_model(self, name, node_type):
        """创建节点"""
        payload = {
            'name': name,
            'supermodel_type': node_type
        }
        response = requests.post(f'{self.base_url}/create_model', json=payload)
        if response.status_code == 200:
            return response.json()['message']
        else:
            raise Exception(f"创建失败： {response.text}")

    def update(self, name, node_type, parent_id=None):
        """创建节点"""
        payload = {
            'name': name,
            'node_type': node_type,
            'parent_id': parent_id
        }
        response = requests.post(f'{self.base_url}/create_node', json=payload)
        if response.status_code == 200:
            return response.json()['message']
        else:
            raise Exception(f"Failed to create node: {response.text}")
