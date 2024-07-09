import toml


def read_iml(file_path):
    # 读取并解析 TOML 文件
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = toml.load(file)
            return data
    except FileNotFoundError:
        return Exception("文件未找到，请检查路径是否正确。")
    except Exception as e:
        return Exception(f"读取文件时发生错误: {e}")
        