import code
import json
from collections import defaultdict
from dataclasses import MISSING, dataclass, field, fields
from json import JSONDecodeError
from multiprocessing import Value
from tkinter import NO
from tracemalloc import stop
from typing import Any, List, Optional, TypeVar, Union

import toml
from loguru import logger
from pydantic import InstanceOf

from im.method_parameter import MethodParameter
from im.method_unit import MethodUnit

T = TypeVar("T")


@dataclass
class MethodModel:
    Name: str
    # Category: Optional[str] = None
    Unit: List[MethodUnit] = field(default_factory=list)

    # def __str__(self):
    #     return (f"方法模型:Name={self.Name}")

    def add_unit_layer(self, unit_layer: MethodUnit):
        self.Unit.append(unit_layer)

    def to_imd(self) -> str:
        imd_content = []
        # 添加头部信息
        imd_content.append(f"O,{self.Name}")
        # 添加单元信息
        for unit in self.Unit:
            r = unit.to_imd()
            if r:
                imd_content.append(r)

        return "\n".join(imd_content)

    def _获取指定单元(self, unit_name):
        for unit in self.Unit:
            if unit.Name == unit_name:
                return unit

    def _获取指定单元数据(self, unit_name):
        for unit in self.Unit:
            if unit.Name == unit_name:
                return unit.DataList

    # 写入数据模型

    def _write_method_data(self, file_path):
        logger.info("==============开始写入数据模型==============")

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(self.to_imd())

    # 读取数据模型

    def _read_method_data(self, file_path):

        logger.info("==============开始读取数据模型==============")
        current_model = None
        current_unit = None
        unit_list = self.Unit

        # 预处理：创建查找字典
        unit_dict = {u.Name: u for u in unit_list}
        param_dict = defaultdict(dict)
        for u in unit_list:
            for p in u.Parameter:
                param_dict[p.Name][u.Name] = p
        with open(file_path, "r", encoding="utf-8") as file:
            for i, line in enumerate(file):
                logger.info(f"第{i}行:{line}")
                parts = line.strip().split(",")
                if parts[0] == "M":
                    pass
                    current_model = MethodModel(Name=parts[1])
                elif parts[0] == "U":
                    unit_name = parts[1]
                    if unit_name in unit_dict:
                        u = unit_dict[unit_name]
                        param_values = parts[2:]
                        if len(param_values) == len(u.Parameter):
                            for p, value in zip(u.Parameter, param_values):
                                p.Value = value
                            u._generate_data_list()
                        else:
                            logger.error("参数数量与单元定义不匹配,跳过!")
                    else:
                        logger.error("参数名称单元定义不匹配,跳过!")
                elif parts[0] == "P":
                    pass
                print("-" * 200)

        logger.info("==============数据模型读取完毕==============")


def dict_to_dataclass(data: dict, cls: type[T]) -> T:
    """
    将字典转换为 dataclass 方法，使用默认值并忽略 dataclass 中不存在的字段
    """
    field_types = {f.name: f.type for f in fields(cls)}
    kwargs = {}
    for f in fields(cls):
        value = data.get(f.name, MISSING)
        if value is MISSING:
            # 使用默认值或忽略字段
            if f.default is not MISSING:
                value = f.default
            elif f.default_factory is not MISSING:  # type: ignore
                value = f.default_factory()  # type: ignore
            else:
                continue
        if isinstance(value, dict) and hasattr(f.type, "__dataclass_fields__"):
            value = dict_to_dataclass(value, f.type)
        elif isinstance(value, list):
            if len(value) > 0 and isinstance(value[0], dict):
                value = [dict_to_dataclass(item, f.type.__args__[0]) for item in value]
        kwargs[f.name] = value
    return cls(**kwargs)


def read_method_model(file_path: str) -> List[MethodModel]:
    """读入方法模型

    Args:
        file_path (str): 文件名

    Returns:
        List[MethodModel]: 方法模型
    """

    return_list = []
    data = toml.load(file_path)
    method_model_list = data.get(MethodModel.__name__)
    for objece_model_data in method_model_list:
        methodmodel_name = objece_model_data.get("Name")
        # methodmodel_category = objece_model_data.get('Category')
        unit_layers = objece_model_data.get("Unit", [])

        method_model = MethodModel(Name=methodmodel_name)
        logger.info(f"解析到: {method_model}")

        # 读取单元层
        for unit_data in unit_layers:
            unit_layer = MethodUnit(
                Name=unit_data["Name"],
                MethodBody=unit_data["MethodBody"],
                Category=unit_data["Category"],
            )
            logger.info(f"解析到: {unit_layer}")

            parameter_list = unit_data.get("Parameter", [])
            # 读取参数层
            for param_data in parameter_list:
                param_layer = MethodParameter(
                    Name=param_data["Name"],
                    ParName=param_data["ParName"],
                    Type=param_data["Type"],
                    Value="",
                )
                logger.info(f"解析到: {param_layer}")
                unit_layer.Parameter.append(param_layer)

            method_model.add_unit_layer(unit_layer)

        return_list.append(method_model)
    return return_list


def write_method_model(file_path: str, method_models: List[MethodModel]) -> None:
    """
    写入方法模型

    Args:
        file_path (str): 写入文件名
        method_models (List[MethodModel]): 待写入模型
    """
    if isinstance(method_models, MethodModel):
        method_models = [method_models]

    def serialize_parameter_layer(param_layer: MethodParameter) -> dict[str, any]:
        return {
            "Name": param_layer.Name,
            "ParName": param_layer.ParName,
            "Type": param_layer.Type,
            "Value": param_layer.Value,
        }

    def serialize_unit_layer(unit_layer: MethodUnit) -> dict[str, any]:
        return {
            "Name": unit_layer.Name,
            "MethodBody": unit_layer.MethodBody,
            "Category": unit_layer.Category,
            "Parameter": [serialize_parameter_layer(p) for p in unit_layer.Parameter],
        }

    def serialize_method_model(method_model: MethodModel) -> dict[str, any]:
        return {
            "Name": method_model.Name,
            # "Category": method_model.Category,
            "Unit": [serialize_unit_layer(u) for u in method_model.Unit],
        }

    data = {"MethodModel": [serialize_method_model(om) for om in method_models]}
    with open(file_path, "w", encoding="utf-8") as toml_file:
        toml.dump(data, toml_file)
