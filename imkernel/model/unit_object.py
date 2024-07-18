from enum import Enum

import pandas as pd
from loguru import logger

from .unit_parameter import UnitParameter


class UnitCategory(Enum):
    H = "人"
    M = "机"
    P = "物料"


from typing import Dict, List, Any


class UnitObject:
    def __init__(self, name: str, category: 'UnitCategory'):
        self.name = name
        self.category = category
        self._parameters: Dict[str, 'UnitParameter'] = {}
        self.DataList: List[Any] = []

    def add_parameter(self, param):
        if isinstance(param, UnitParameter):
            self._parameters[param.name] = param
        elif isinstance(param, UnitObject):
            nested_param = UnitParameter(name=param.name, value_type="object", value=param, is_object=True)
            self._parameters[param.name] = nested_param
        else:
            raise ValueError("添加的参数必须是参数或者对象")
        self._update_data_list()

    def add_nested_object(self, name: str, nested_object: 'UnitObject'):
        param = UnitParameter(name, value_type="object", value=nested_object)
        self.add_parameter(param)
        self._update_data_list()

    def set_parameter_value(self, param_name: str, value):
        if param_name in self._parameters:
            self._parameters[param_name].value = value
            self._parameters[param_name].real_data = UnitParameter._deserialize(value)
            self._parameters[param_name].array_data = UnitParameter._deserialize(value)
        else:
            logger.error(f"参数 '{param_name}' 不存在")

        self._update_data_list()

    def set_all_parameters(self, **kwargs):
        for param_name, value in kwargs.items():
            self.set_parameter_value(param_name, value)

    def __setattr__(self, name, value):
        if name in ['name', 'category', '_parameters', 'DataList']:
            super().__setattr__(name, value)
        elif name in self._parameters:
            par = self._parameters.get(name)
            if isinstance(par.value, UnitObject):
                if isinstance(value, list) and all(isinstance(item, list) for item in value):
                    par.value.DataList = value
                    par.value._update_parameters()
                else:
                    logger.error("参数不匹配，应该使用嵌套列表赋值")
            else:
                par.value = value
                par.real_data = UnitParameter._deserialize(value)
                par.array_data = UnitParameter._deserialize(value)
        else:
            logger.error("参数不存在")

    def _update_parameters(self):
        if self.DataList:
            for i, param_name in enumerate(self._parameters):
                values = [group[i] for group in self.DataList if i < len(group)]
                self._parameters[param_name].value = values
                self._parameters[param_name].real_data = UnitParameter._deserialize(values)
                self._parameters[param_name].array_data = UnitParameter._deserialize(values)

    def __getattr__(self, name):
        if name in self._parameters:
            return self._parameters[name]
        raise AttributeError(f"'{self.__class__.__name__}' 没有参数： '{name}'")

    def _update_data_list(self):
        self.DataList = [par.value for par in self._parameters.values()]

    def to_dict(self):
        return {
            "name": self.name,
            "category": self.category.value,
            "parameters": {name: param.to_dict() for name, param in self._parameters.items()}
        }

    def _get_parameter(self, name: str):
        return self._parameters.get(name)

    def process(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        # 处理逻辑在这里实现
        # 可以根据 self.name 和 self.parameters 来决定具体的操作
        pass

    def __str__(self):
        params = ", ".join(f"{name}={param.value}" for name, param in self._parameters.items())
        return f"{self.name} ({self.category}): {params}"

    def to_imd(self) -> str:
        imd_content = []
        # 添加头部信息
        for data_entry in self.DataList:
            imd_content.append(f"U,{self.name}," + ",".join(map(str, data_entry)))
        if imd_content:
            r = "\n".join(imd_content)
        else:
            r = None
        return r


def unit_to_dict(unit):
    data = {}
    for name, param in unit._parameters.items():
        if isinstance(param, UnitObject):
            data[name] = unit_to_dict(param)
        else:
            data[name] = param.value
    return data


def unit_to_dataframe(unit):
    data = unit_to_dict(unit)
    return pd.DataFrame([data])
