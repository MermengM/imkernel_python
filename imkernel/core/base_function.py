import json
from typing import List

import toml
from loguru import logger

from imkernel.model import UnitModelold, ElementParameter, Element


def read_object_model(file_path: str) -> List[UnitModelold]:
    """读入对象模型

    Args:
        file_path (str): 文件名

    Returns:
        List[UnitModelold]: 对象模型
    """

    return_list = []
    data = toml.load(file_path)
    object_model_list = data.get(UnitModelold.__name__)
    for objece_model_data in object_model_list:
        objectmodel_name = objece_model_data.get("Name")
        # objectmodel_category = objece_model_data.get('Category')
        unit_layers = objece_model_data.get("Unit", [])

        object_model = UnitModelold(Name=objectmodel_name)
        logger.info(f"解析到: {object_model}")

        # 读取单元层
        for unit_data in unit_layers:
            unit_layer = Element(
                name=unit_data["Name"], category=unit_data["Category"]
            )
            logger.info(f"解析到: {unit_layer}")

            parameter_list = unit_data.get("Parameter", [])
            # 读取参数层
            for param_data in parameter_list:
                param_layer = ElementParameter(
                    name=param_data["Name"],
                    par_name=param_data["ParName"],
                    value_type=param_data["Type"],
                    value="",
                )
                logger.info(f"解析到: {param_layer}")
                unit_layer._parameters.append(param_layer)

            object_model.add_unit_layer(unit_layer)

        return_list.append(object_model)
    return return_list


def write_object_model(file_path: str, object_models: List[UnitModelold]) -> None:
    """
    写入对象模型

    Args:
        file_path (str): 写入文件名
        object_models (List[UnitModelold]): 待写入模型
    """
    if isinstance(object_models, UnitModelold):
        object_models = [object_models]

    def serialize_parameter_layer(param_layer: ElementParameter) -> dict[str, any]:
        return {
            "Name": param_layer.name,
            "ParName": param_layer.par_name,
            "Type": param_layer.value_type,
            "Value": param_layer.value,
        }

    def serialize_unit_layer(unit_layer: Element) -> dict[str, any]:
        return {
            "Name": unit_layer.name,
            "Category": unit_layer.category,
            "Parameter": [serialize_parameter_layer(p) for p in unit_layer._parameters],
        }

    def serialize_object_model(object_model: UnitModelold) -> dict[str, any]:
        return {
            "Name": object_model.Name,
            # "Category": object_model.Category,
            "Unit": [serialize_unit_layer(u) for u in object_model.Unit],
        }

    data = {"ObjectModel": [serialize_object_model(om) for om in object_models]}
    with open(file_path, "w", encoding="utf-8") as toml_file:
        toml.dump(data, toml_file)


def update_object_model(json_data: str, object_unit: Element):
    """使用数据更新对象模型

    Args:
        json_data (str): _description_
        object_unit (Element): _description_
    """
    # 解析JSON数据
    data_list = json.loads(json_data)

    # 获取参数名列表
    param_names = [param.par_name for param in object_unit._parameters]

    # 初始化DataList
    object_unit.DataList = []

    # 遍历JSON数据
    for item in data_list:
        # 创建一个新的数据项
        data_item = []
        for param_name in param_names:
            if param_name in item:
                data_item.append(item[param_name])
            else:
                # 如果JSON中没有对应的键，添加None或者其他默认值
                data_item.append(None)

        # 将数据项添加到DataList
        object_unit.DataList.append(data_item)
    print(object_unit)


def merge_object_data(iml_path: str, imd_path: str):
    """合并对象模型与对象数据模型

    Args:
        iml_path (str): _description_
        imd_path (str): _description_

    Returns:
        _type_: _description_
    """
    object_model = read_object_model(iml_path)
    object_model = object_model[0]
    object_model.read_imd(imd_path)
    return object_model
