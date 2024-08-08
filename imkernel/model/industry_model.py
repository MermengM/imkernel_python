import pandas as pd


class IdGenerator:
    def __init__(self):
        self.current_id = 0

    def get_next_id(self):
        self.current_id += 1
        return self.current_id


# 全局 ID 生成器
global_id_generator = IdGenerator()


class TreeNode:
    def __init__(self, name):
        self.id = global_id_generator.get_next_id()
        self.name = name
        self.children = []
        self.parent = None

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def remove_child(self, child):
        if child in self.children:
            child.parent = None
            self.children.remove(child)


class IMElement:
    UnitObject = "[E]"
    UnitParameter = "[C]"
    MethodObject = "[F]"
    MethodParameterInput = "[X]"
    MethodParameterOutput = "[Y]"
    ProcessObject = "[P]"
    ProcessParameterTime = "[T]"
    ProcessParameterSpace = "[S]"
    ProcessParameterUnit = "[PE]"
    ProcessParameterMethod = "[PF]"


class Element:
    def __init__(self, name, element_type):
        self.id = global_id_generator.get_next_id()
        self.name = name
        self.type = element_type
        self.children = []
        self.parent = None
        self.parameters = []  # 用于存储关联的参数

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def find_or_create_child(self, name):
        for child in self.children:
            if child.name == name:
                return child
        new_child = Element(name, self.type)
        self.add_child(new_child)
        return new_child

    def add_parameter(self, parameter):
        self.parameters.append(parameter)


class UnitObject:
    def __init__(self):
        self.root = Element("Root", IMElement.UnitObject)

    def create_unit_structure(self, df):
        for _, row in df.iterrows():
            current = self.root
            for item in row:
                current = current.find_or_create_child(item)

    def print_tree(self, element=None, level=0):
        if element is None:
            element = self.root
        print("  " * level + f"id:{str(element.id)} " + f"{element.name} ({element.type})")
        if element.parameters:
            print("  " * (level + 1) + "Parameters:")
            for param in element.parameters:
                print("  " * (level + 2) + f"{param.name} ({param.type})")
        for child in element.children:
            self.print_tree(child, level + 1)

    def to_dataframe(self):
        rows = []
        self._collect_paths(self.root, [], rows)
        return pd.DataFrame(rows)

    def _collect_paths(self, element, current_path, rows):
        if element.name != "Root":
            current_path.append(element.name)
        if not element.children:
            rows.append(current_path.copy())
        for child in element.children:
            self._collect_paths(child, current_path, rows)
        if element.name != "Root":
            current_path.pop()

    def find_element(self, path):
        current = self.root
        for item in path:
            found = False
            for child in current.children:
                if child.name == item:
                    current = child
                    found = True
                    break
            if not found:
                return None
        return current


class UnitParameter:
    def __init__(self):
        self.root = Element("Root", IMElement.UnitParameter)

    def create_parameter_structure(self, df):
        for _, row in df.iterrows():
            current = self.root
            for item in row:
                current = current.find_or_create_child(item)

    def print_tree(self, element=None, level=0):
        if element is None:
            element = self.root
        print("  " * level + f"id:{str(element.id)} " + f"{element.name} ({element.type})")
        for child in element.children:
            self.print_tree(child, level + 1)

    def to_dataframe(self):
        rows = []
        self._collect_paths(self.root, [], rows)
        return pd.DataFrame(rows)

    def _collect_paths(self, element, current_path, rows):
        if element.name != "Root":
            current_path.append(element.name)
        if not element.children:
            rows.append(current_path.copy())
        for child in element.children:
            self._collect_paths(child, current_path, rows)
        if element.name != "Root":
            current_path.pop()

    def find_parameter(self, path):
        current = self.root
        for item in path:
            found = False
            for child in current.children:
                if child.name == item:
                    current = child
                    found = True
                    break
            if not found:
                return None
        return current


class UnitModel:
    def __init__(self, unit_object, unit_parameter):
        self.unit_object = unit_object
        self.unit_parameter = unit_parameter

    def link_parameters_to_objects(self, link_df):
        for _, row in link_df.iterrows():
            object_path = row[:-1]
            parameter_name = row[-1]

            object_element = self.unit_object.find_element(object_path)
            parameter_element = self.unit_parameter.find_parameter([parameter_name])

            if object_element and parameter_element:
                object_element.add_parameter(parameter_element)

    def print_model(self):
        print("Unit Model Structure:")
        self.unit_object.print_tree()

    def to_dataframes(self):
        return {
            'objects': self.unit_object.to_dataframe(),
            'parameters': self.unit_parameter.to_dataframe()
        }


unit_object = pd.DataFrame(data=[
    ('Blade', 'BladeCross', 'BladePolyLine', 'ElevenParameters'),
    ('Blade', 'BladeCross', 'BladePolyLine', 'SectionPoints'),
    ('Blade', 'BladeCross', 'BladePolyLine', 'CurvePonits'),
    ('Blade', 'BladeCross', 'BladePolyLine', 'cpts'),
    ('Blade', 'FinishingPoint'),
    ('Blade', 'ClosedBladeCross'),
    ('machine', 'BasicParameters'),
    ('machine', 'MachiningParameter'),
    ('cutter', 'BasicParameters'),
    ('cutter', 'P_Parameter')
])
unit_object

# 使用示例

unit_parameter = pd.DataFrame(data=[
    ('DesginParameters', 'ElevenParameters', 'Chord_Length'),
    ('DesginParameters', 'ElevenParameters', 'Upper_Max_Width'),
    ('DesginParameters', 'ElevenParameters', 'Upper_Max_Width_Loc'),
    ('DesginParameters', 'ElevenParameters', 'Upper_Angle'),
    ('DesginParameters', 'ElevenParameters', 'Upper_tip_coeff'),
    ('DesginParameters', 'ElevenParameters', 'Upper_aft_part_shape'),
    ('DesginParameters', 'ElevenParameters', 'Lower_max_width'),
    ('DesginParameters', 'ElevenParameters', 'Lower_max_width_loc'),
    ('DesginParameters', 'ElevenParameters', 'Lower_Angle'),
    ('DesginParameters', 'ElevenParameters', 'Lower_tip_coeff'),
    ('DesginParameters', 'ElevenParameters', 'Lower_aft_part_shape'),
    ('DesginParameters', 'ElevenParameters', 'Tangent_Leading_Edge'),
    ('SectionPoints', 'x'),
    ('SectionPoints', 'y'),
    ('SectionPoints', 'z'),
    ('CurvePonits', 'x'),
    ('CurvePonits', 'y'),
    ('CurvePonits', 'z'),
    ('FinishingPoint', 'x'),
    ('FinishingPoint', 'y'),
    ('FinishingPoint', 'z'),
    ('FinishingPoint', 'i'),
    ('FinishingPoint', 'j'),
    ('FinishingPoint', 'k'),
    ('BasicParameters', 'A'),
    ('BasicParameters', 'B'),
    ('BasicParameters', 'C'),
])
parameter_links_df = pd.DataFrame(data=[
    ('BladePolyLine', 'Chord_Length'),
    ('ElevenParameters', 'Upper_Max_Width'),
])
# 创建单元对象
unit_object = UnitObject()
unit_object.create_unit_structure(unit_object)

print("Unit Object Structure:")
unit_object.print_tree()

# 创建单元参数
unit_parameter = UnitParameter()
unit_parameter.create_parameter_structure(unit_parameter)

print("\nUnit Parameter Structure:")
unit_parameter.print_tree()

# 创建单元模型并关联参数
unit_model = UnitModel(unit_object, unit_parameter)
unit_model.link_parameters_to_objects(parameter_links_df)

print("\nUnit Model Structure (after linking parameters):")
unit_model.print_model()

print("\nConverting Unit Model back to DataFrames:")
df_output = unit_model.to_dataframes()
print("Objects DataFrame:")
print(df_output['objects'])
print("\nParameters DataFrame:")
print(df_output['parameters'])
