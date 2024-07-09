import json
import tomllib
import toml

def read_iml_file_return_data(file_path):
    """读取iml返回data

    Args:
        file_path (_type_): _description_

    Returns:
        _type_: _description_
    """
    with open(file_path, "rb") as f:
        data = tomllib.load(f)
    return data
def json_to_toml(json_file, toml_file):
    # 读取JSON文件
    with open(json_file, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    
    # 将JSON字符串转换为Python对象
    data = json.loads(json_data)

    # 为了满足TOML格式的需要，我们将每个内部列表转换为字典
    formatted_data = [{"x": item[0], "y": item[1], "z": item[2]} for item in data if isinstance(item, list) and len(item) == 3]

    # 将转换后的字典列表转换为TOML字符串
    toml_string = toml.dumps({"data": formatted_data})

# 输出TOML字符串
    print(toml_string)
if __name__ == "__main__":
        # 使用示例
    # 你提供的JSON数据字符串
    json_data = '''
    [
    [1, 0.5, 1], [1.2, 0.6, 2], [1.4, 1, 3], [1, 2, 1], [2, 3, 2],
    [3, 4, 3], [4, 5, 4], [5, 6, 5], [6, 7, 6], [7, 8, 7], [8, 9, 8],
    [9, 4, 9], [4, 2, 4], [2, 1, 2], [1, 4, 1], [4, "asdasdasd", 4],
    [1, "asdasdsa", 24], [1.2, 0.5, 2], [1.4, 0.6, 51], [1, 1, 51],
    [2, 2, 325], [3, 3, 1], [4, 4, 215], [5, 5, "asdasdasdsad"],
    [6, 6, {}], [7, 7, {}], [8, 8, {}], [9, 9, {}], [4, 4, {}],
    [2, 2, {}], [1, 1, {}], [4, 4, {}], [{}, "asdasdasd", {}],
    [{}, "asdasdsa", {}]
    ]
    '''

    # 将JSON字符串转换为Python对象
    data = json.loads(json_data)

    # 为了满足TOML格式的需要，我们将每个内部列表转换为字典
    formatted_data = [{"x": item[0], "y": item[1], "z": item[2]} for item in data if isinstance(item, list) and len(item) == 3]

    # 将转换后的字典列表转换为TOML字符串
    toml_string = toml.dumps({"data": formatted_data})

    # 输出TOML字符串
    print(toml_string)
# end main