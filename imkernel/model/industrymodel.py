import json

import pandas as pd


class IndustryModel:
    def __init__(self, data=None):
        self.data = data or {}
        self.current_path = []

    def __repr__(self):
        """返回对象的字符串表示"""
        return f"IndustryModel({self.data})"

    def _repr_html_(self):
        """返回 DataFrame 的 HTML 表示，用于 Jupyter Notebook 显示"""
        return self.to_dataframe().to_html()

    def __str__(self):
        """返回 DataFrame 的字符串表示"""
        return self.to_dataframe().to_string()

    def set_value(self, path, value):
        keys = path.split('.')
        current = self.data
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]

        # 直接设置值，不进行特殊处理
        current[keys[-1]] = value

    def get_value(self, path, default=None):
        keys = path.split('.')
        current = self.data
        for key in keys:
            if not isinstance(current, dict) or key not in current:
                return default
            current = current[key]
        return current

    def delete_value(self, path):
        keys = path.split('.')
        current = self.data
        for key in keys[:-1]:
            if not isinstance(current, dict) or key not in current:
                return
            current = current[key]
        if keys[-1] in current:
            del current[keys[-1]]

    def to_json(self):
        return json.dumps(self.data, indent=4)

    def save_json(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.data, f, indent=4)

    @classmethod
    def load_json(cls, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
        return cls(data)

    def to_dataframe(self):
        data = []

        def traverse(d, current_path=[]):
            for key, value in d.items():
                new_path = current_path + [key]
                if isinstance(value, dict):
                    if value:  # 如果字典不为空
                        traverse(value, new_path)
                    else:  # 如果字典为空，我们认为这是一个叶节点
                        data.append(new_path + [''])
                elif isinstance(value, list):  # 处理列表类型的值
                    for i, item in enumerate(value):
                        data.append(new_path + [f'{i}', str(item)])
                else:
                    data.append(new_path + [str(value)])

        traverse(self.data)

        # 找出最长的路径长度
        max_depth = max(len(path) for path in data)

        # 用空字符串填充较短的路径
        padded_data = [path + [''] * (max_depth - len(path)) for path in data]

        # 创建列名
        columns = [f'{i}' for i in range(max_depth)]

        # 创建DataFrame
        df = pd.DataFrame(padded_data, columns=columns)

        # 设置多重索引
        df = df.set_index(columns)

        return df

    def add(self, text):
        key, values = text.split('=')
        key = key.strip()
        values = values.strip()[1:-1].split(',')
        values = [v.strip() for v in values]

        if not self.current_path or key == self.current_path[0]:
            self.current_path = [key]
        else:
            while self.current_path and key not in self.get_value('.'.join(self.current_path), {}):
                self.current_path.pop()
            self.current_path.append(key)

        self.set_value('.'.join(self.current_path), {v: {} for v in values})

        return self

    def set_leaf_value(self, path, value):
        keys = path.split('.')
        current = self.data
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        current[keys[-1]] = value

    def update_from_dataframe(self, df):
        for index, row in df.iterrows():
            path = '.'.join(filter(None, index))
            value = row['值']
            if value != '':  # 只更新非空值
                self.set_leaf_value(path, value)


def parse_model_structure(text):
    lines = text.strip().split('\n')
    model = IndustryModel()
    current_path = []

    for line in lines:
        key, values = line.split('=')
        key = key.strip()
        values = values.strip()[1:-1].split(',')
        values = [v.strip() for v in values]

        if not current_path or key == current_path[0]:
            current_path = [key]
        else:
            while current_path and key not in model.get_value('.'.join(current_path), {}):
                current_path.pop()
            current_path.append(key)

        if len(values) == 1 and values[0].startswith('[') and values[0].endswith(']'):

            try:
                numeric_values = json.loads(values[0])
                model.set_value('.'.join(current_path), numeric_values)
            except json.JSONDecodeError:
                model.set_value('.'.join(current_path), {v: {} for v in values})
        else:
            model.set_value('.'.join(current_path), {v: {} for v in values})

    return model
