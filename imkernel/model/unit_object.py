from enum import Enum

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

    def add_parameter(self, param: 'UnitParameter'):
        self._parameters[param.name] = param

    def add_nested_object(self, name: str, nested_object: 'UnitObject'):
        param = UnitParameter(name, value_type="object", value=nested_object)
        self.add_parameter(param)

    def __setattr__(self, name, value):
        if name in ['name', 'category', '_parameters', 'DataList']:
            super().__setattr__(name, value)
        elif name in self._parameters:
            if isinstance(value, UnitObject):
                self._parameters[name].value = value
                self._parameters[name].is_object = True
            else:
                self._parameters[name].value = value
                self._parameters[name].real_data = UnitParameter._deserialize(value)
                self._parameters[name].array_data = UnitParameter._deserialize(value)
        else:
            logger.error("参数不存在")

    def __getattr__(self, name):
        if name in self._parameters:
            return self._parameters[name].value
        raise AttributeError(f"'{self.__class__.__name__}' 没有参数： '{name}'")

    def to_dict(self):
        return {
            "name": self.name,
            "category": self.category.value,
            "parameters": {name: param.to_dict() for name, param in self._parameters.items()}
        }

    def get_parameter(self, name: str) -> 'UnitParameter':
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
