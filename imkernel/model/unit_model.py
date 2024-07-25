from dataclasses import MISSING, fields
from typing import List, TypeVar

from .unit_object import Element, UnitCategory
from .unit_parameter import ElementParameter

T = TypeVar("T")


class UnitModel:
    def __init__(self, name: str):
        self.name = name
        self.Objects = {category: [] for category in UnitCategory}

    def add_object(self, _object: Element):
        self.Objects[_object.category].append(_object)

    def to_dict(self):
        return {
            "Name": self.name,
            "Objects": {cat.value: [obj.to_dict() for obj in objs] for cat, objs in self.Objects.items()}
        }

    def get_objects_by_unit_category(self, category: UnitCategory) -> List[Element]:
        """
        根据分类获取单元中所有对象
        :param category:
        :return:
        """
        return self.Objects[category]

    def get_all_units(self) -> List[Element]:
        return [unit for units in self.Objects.values() for unit in units]

    def __str__(self):
        unit_counts = {cat.value: len(units) for cat, units in self.Objects.items()}
        return f"单元模型: Name={self.name},  Units={unit_counts}"


def model_to_dict(obj):
    if isinstance(obj, list):
        return [model_to_dict(i) for i in obj]
    elif isinstance(obj, UnitModel):
        return obj.to_dict()
    elif isinstance(obj, Element):
        return obj.to_dict()
    elif isinstance(obj, ElementParameter):
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
            if f.type == Element:
                value = dict_to_unitobject(value)
            elif hasattr(f.type, "__dataclass_fields__"):
                value = dict_to_dataclass(value, f.type)
        elif isinstance(value, list):
            if len(value) > 0 and isinstance(value[0], dict):
                if f.type.__args__[0] == Element:
                    value = [dict_to_unitobject(item) for item in value]
                else:
                    value = [dict_to_dataclass(item, f.type.__args__[0]) for item in value]
        kwargs[f.name] = value
    return cls(**kwargs)


def dict_to_unitobject(data: dict) -> Element:
    obj = Element(data['name'], UnitCategory(data['category']))
    for param_name, param_data in data['parameters'].items():
        if param_data['value_type'] == 'object':
            nested_obj = dict_to_unitobject(param_data['value'])
            obj.add_nested_object(param_name, nested_obj)
        else:
            param = ElementParameter(param_data['name'], param_data['par_name'], param_data['value_type'],
                                     param_data['value'])
            obj.add_parameter(param)
    return obj


import pandas as pd


def unitmodel_to_dataframe(unit_model):
    data_list = []
    for category, units in unit_model.Objects.items():
        for unit in units:
            unit_dict = unit.to_dict()
            unit_dict['category'] = category
            data_list.append(unit_dict)
    df = pd.DataFrame(data_list)
    return df
