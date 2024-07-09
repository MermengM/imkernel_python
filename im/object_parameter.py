
from loguru import logger

from dataclasses import dataclass
from json import JSONDecodeError
import json
from typing import Any


@dataclass
class ObjectParameter():
    """对象模型参数层"""
    Name: str
    ParName: str
    Type: str
    Value: Any = None

    def __post_init__(self):
        self.real_data = self.deserialize_data(self.Value, self.Type)
        self.array_data = self.deserialize_array(self.Value)

    def __str__(self):
        return (f"对象模型-参数:Name={self.Name}, ParName={self.ParName}, Type={self.Type}, value={self.Value}")

    # def _to_imd(self) -> str:
    #     imd_content = []
    #     # 添加头部信息
    #     imd_content.append(f"P,{self.Name}")
    #     # 添加单元信息
    #     for par in self.Parameter:
    #         imd_content.append(par.to_imd())
    #     # 读取数据模型

    @staticmethod
    def deserialize_data(value, dtype):
        if isinstance(value, (list, dict)):
            return value
        try:
            if value and isinstance(value, str):
                r = json.loads(value)
                if r:
                    logger.info("deserialize_data")
                    return r
        except JSONDecodeError:
            print("Failed to deserialize data")
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
