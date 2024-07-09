import importlib
import json
import sys

from loguru import logger

from imkernel.im import MethodModel, ObjectModel
from imkernel.im.object_unit import ObjectUnit


def dynamic_method_call(fun_name, script_path, **kwargs):
    # 将脚本路径添加到sys.path
    script_dir = "\\".join(script_path.split("\\")[:-1])
    sys.path.append(script_dir)

    # 获取脚本文件名（不包含路径和.py扩展名）
    script_name = script_path.split("\\")[-1].replace(".py", "")

    try:
        # 动态导入模块
        module = importlib.import_module(script_name)

        # 获取指定的函数
        func = getattr(module, fun_name)

        # 调用函数并返回结果
        return func(**kwargs)
    except ImportError:
        print(f"无法导入模块: {script_name}")
    except AttributeError:
        print(f"函数 {fun_name} 在模块 {script_name} 中不存在")
    except Exception as e:
        print(f"调用函数时发生错误: {str(e)}")
