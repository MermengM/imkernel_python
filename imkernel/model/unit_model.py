from dataclasses import MISSING, fields
from typing import List, TypeVar

from .unit_object import UnitObject, UnitCategory
from .unit_parameter import UnitParameter

T = TypeVar("T")


class UnitModel:
    def __init__(self, name: str):
        self.name = name
        self.Objects = {category: [] for category in UnitCategory}

    def add_object(self, _object: UnitObject):
        self.Objects[_object.category].append(_object)

    def to_dict(self):
        return {
            "Name": self.name,
            "Objects": {cat.value: [obj.to_dict() for obj in objs] for cat, objs in self.Objects.items()}
        }

    def get_objects_by_unit_category(self, category: UnitCategory) -> List[UnitObject]:
        """
        根据分类获取单元中所有对象
        :param category:
        :return:
        """
        return self.Objects[category]

    def get_all_units(self) -> List[UnitObject]:
        return [unit for units in self.Objects.values() for unit in units]

    def __str__(self):
        unit_counts = {cat.value: len(units) for cat, units in self.Objects.items()}
        return f"单元模型: Name={self.name},  Units={unit_counts}"


def model_to_dict(obj):
    if isinstance(obj, list):
        return [model_to_dict(i) for i in obj]
    elif isinstance(obj, UnitModel):
        return obj.to_dict()
    elif isinstance(obj, UnitObject):
        return obj.to_dict()
    elif isinstance(obj, UnitParameter):
        return obj.to_dict()
    elif hasattr(obj, "__dataclass_fields__"):
        result = {}
        for key in obj.__dataclass_fields__:
            value = getattr(obj, key)
            result[key] = model_to_dict(value)
        return result
    else:
        return obj


def dict_to_dataclass(data: dict, cls: type[T]) -> T:
    field_types = {f.name: f.type for f in fields(cls)}
    kwargs = {}
    for f in fields(cls):
        value = data.get(f.name, MISSING)
        if value is MISSING:
            if f.default is not MISSING:
                value = f.default
            elif f.default_factory is not MISSING:
                value = f.default_factory()
            else:
                continue
        if isinstance(value, dict):
            if f.type == UnitObject:
                value = dict_to_unitobject(value)
            elif hasattr(f.type, "__dataclass_fields__"):
                value = dict_to_dataclass(value, f.type)
        elif isinstance(value, list):
            if len(value) > 0 and isinstance(value[0], dict):
                if f.type.__args__[0] == UnitObject:
                    value = [dict_to_unitobject(item) for item in value]
                else:
                    value = [dict_to_dataclass(item, f.type.__args__[0]) for item in value]
        kwargs[f.name] = value
    return cls(**kwargs)


def dict_to_unitobject(data: dict) -> UnitObject:
    obj = UnitObject(data['name'], UnitCategory(data['category']))
    for param_name, param_data in data['parameters'].items():
        if param_data['value_type'] == 'object':
            nested_obj = dict_to_unitobject(param_data['value'])
            obj.add_nested_object(param_name, nested_obj)
        else:
            param = UnitParameter(param_data['name'], param_data['par_name'], param_data['value_type'],
                                  param_data['value'])
            obj.add_parameter(param)
    return obj

# @dataclass
# class UnitModelold:
#     Name: str
#     # Category: Optional[str] = None
#     Unit: List[UnitObject] = field(default_factory=list)
#
#     # def __str__(self):
#     #     return (f"对象模型:Name={self.Name}")
#
#     def add_unit_layer(self, unit_layer: UnitObject):
#         self.Unit.append(unit_layer)
#
#     def _get_imd_string(self) -> str:
#         imd_content = []
#         # 添加头部信息
#         imd_content.append(f"O,{self.Name}")
#         # 添加单元信息
#         for unit in self.Unit:
#             r = unit.to_imd()
#             if r:
#                 imd_content.append(r)
#
#         return "\n".join(imd_content)
#
#     def get_unit(self, unit_name):
#         for unit in self.Unit:
#             if unit.name == unit_name:
#                 return unit
#
#     def get_unit_data(self, unit_name):
#         for unit in self.Unit:
#             if unit.name == unit_name:
#                 return unit.DataList
#
#     # 写入数据模型
#
#     def to_imd(self, file_path):
#         logger.info("==============开始写入数据模型==============")
#         with open(file_path, "w", encoding="utf-8") as file:
#             file.write(self._get_imd_string())
#         logger.info(f"成功写入数据模型到{file_path}")
#         logger.info("==============数据模型写入完成==============")
#
#     # 读取数据模型
#
#     def read_imd(self, file_path):
#         logger.info("==============开始读取数据模型==============")
#         current_model = None
#         current_unit = None
#         unit_list = self.Unit
#         # 预处理：创建查找字典
#         unit_dict = {u.name: u for u in unit_list}
#         param_dict = defaultdict(dict)
#         for u in unit_list:
#             for p in u._parameters:
#                 param_dict[p.name][u.name] = p
#         with open(file_path, "r", encoding="utf-8") as file:
#             for i, line in enumerate(file):
#                 logger.info(f"第{i}行:{line}")
#                 parts = line.strip().split(",")
#                 if parts[0] == "O":
#                     pass
#                     current_model = UnitModelold(Name=parts[1])
#                 elif parts[0] == "U":
#                     unit_name = parts[1]
#                     if unit_name in unit_dict:
#                         u = unit_dict[unit_name]
#                         param_values = parts[2:]
#                         if len(param_values) == len(u._parameters):
#                             for p, value in zip(u._parameters, param_values):
#                                 p.value = value
#                             logger.info("参数匹配,写入模型!")
#
#                             u._generate_data_list()
#                         else:
#                             logger.error("参数数量与单元定义不匹配,跳过!")
#                 elif parts[0] == "P":
#                     pass
#                 print("-" * 200)
#         logger.info("==============数据模型读取完毕==============")
#
#
# def dict_to_dataclass(data: dict, cls: type[T]) -> T:
#     """
#     将字典转换为 dataclass 对象，使用默认值并忽略 dataclass 中不存在的字段
#     """
#     field_types = {f.name: f.type for f in fields(cls)}
#     kwargs = {}
#     for f in fields(cls):
#         value = data.get(f.name, MISSING)
#         if value is MISSING:
#             # 使用默认值或忽略字段
#             if f.default is not MISSING:
#                 value = f.default
#             elif f.default_factory is not MISSING:  # type: ignore
#                 value = f.default_factory()  # type: ignore
#             else:
#                 continue
#         if isinstance(value, dict) and hasattr(f.type, "__dataclass_fields__"):
#             value = dict_to_dataclass(value, f.type)
#         elif isinstance(value, list):
#             if len(value) > 0 and isinstance(value[0], dict):
#                 value = [dict_to_dataclass(item, f.type.__args__[0]) for item in value]
#         kwargs[f.name] = value
#     return cls(**kwargs)
#
#
# def auto_read_object_model(file_path: str) -> List[UnitModelold]:
#     data = toml.load(file_path)
#     object_model_list = data.get("ObjectModel", [])
#     return [
#         dict_to_dataclass(model_data, UnitModelold) for model_data in object_model_list
#     ]
#
#
# def auto_write_object_model(file_path: str, object_models: List[UnitModelold]) -> None:
#     data = {"ObjectModel": [dataclass_to_dict(model) for model in object_models]}
#     with open(file_path, "w", encoding="utf-8") as toml_file:
#         toml.dump(data, toml_file)
#
#
# def dataclass_to_dict(instance: any) -> any:
#     """
#     将 dataclass 对象转换为字典
#     """
#     if hasattr(instance, "__dataclass_fields__"):
#         result = {}
#         for field_name, field_type in instance.__dataclass_fields__.items():
#             value = getattr(instance, field_name)
#             if isinstance(value, list):
#                 result[field_name] = [dataclass_to_dict(i) for i in value]
#             else:
#                 result[field_name] = dataclass_to_dict(value)
#         return result
#     else:
#         return instance
#
#
# def model_to_dict(obj):
#     """将 dataclass 对象转换为字典
#
#     Args:
#         obj (_type_): _description_
#
#     Returns:
#         _type_: _description_
#     """
#     if isinstance(obj, list):
#         return [model_to_dict(i) for i in obj]
#     elif hasattr(obj, "__dataclass_fields__"):
#         result = {}
#         for key in obj.__dataclass_fields__:
#             value = getattr(obj, key)
#             result[key] = model_to_dict(value)
#         return result
#     else:
#         return obj
#
#
# def auto_write_object_model(file_path: str, object_models: List[UnitModelold]) -> None:
#     """
#     将 ObjectModel 对象列表写入 TOML 文件
#     """
#     data = {"ObjectModel": model_to_dict(object_models)}
#
#     with open(file_path, "w", encoding="utf-8") as toml_file:
#         toml.dump(data, toml_file)
