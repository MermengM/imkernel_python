import json
from json import JSONDecodeError

from loguru import logger


class ElementParameter:
    """
    单元参数类。

    :Attributes:
        name (str): 参数名称
        par_name (str): 父参数名称
        value_type (str): 值类型
        value: 参数值
        real_data: 反序列化后的实际数据
        array_data: 反序列化后的数组数据
        is_object (bool): 是否为嵌套对象
    """

    def __init__(self, name, par_name=None, value_type=None, value=None, is_object=False):
        self.name = name
        self.par_name = par_name
        self.value_type = value_type
        self._value = None
        self.real_data = None
        self.array_data = None
        self.is_object = is_object
        self.value = value  # 这里会触发setter方法

    @property
    def value(self):
        if not self.is_object:
            return self._value
        else:
            return self.array_data

    @value.setter
    def value(self, new_value):
        self._value = new_value
        # self.real_data = self._deserialize(new_value)
        # self.array_data = self._deserialize(new_value)

    @staticmethod
    def _check_if_object(value):
        from .unit_object import Element
        return isinstance(value, Element)

    def __str__(self):
        return f"对象模型参数: Name={self.name}, ParName={self.par_name}, Type={self.value_type}, Value={self.value}"

    def to_dict(self):
        if self.is_object:
            return {
                "name": self.name,
                "par_name": self.par_name,
                "value_type": self.value_type,
                "value": (self.value.to_dict() if hasattr(self.value, 'to_dict') else
                          vars(self.value) if hasattr(self.value, '__dict__') else
                          str(self.value)) if self.value is not None else None
            }
        else:
            return {
                "name": self.name,
                "par_name": self.par_name,
                "value_type": self.value_type,
                "value": self.value
            }

    @staticmethod
    def _deserialize(value):
        if isinstance(value, (list, dict)):
            return value
        if isinstance(value, str):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                pass
        return value

    @staticmethod
    def deserialize_array(value):
        if isinstance(value, list):
            return value
        try:
            if value and isinstance(value, str):
                r = json.loads(value)
                if r:
                    logger.info("deserialize_arraySUCCESS")
                    return r
        except JSONDecodeError:
            print("Failed to deserialize JSON array")
        return value
