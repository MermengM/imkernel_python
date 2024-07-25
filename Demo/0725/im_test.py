from imkernel.model import IndustryModel
from imkernel.model.industrymodel import parse_model_structure

with open('im.txt', 'r', encoding='utf-8') as file:
    content = file.read()

model = parse_model_structure(content)

print(model.to_json())

model.save_json("model.json")

loaded_model = IndustryModel.load_json("model.json")

df = model.to_dataframe()

print(df)

df.to_csv('output.csv')

# 操作
print(model.get_value("Model.Element.Blade.BladeCross.BladePolyLine.SectionPoints.x"))
model.set_value("Model.Element.Blade.BladeCross.BladePolyLine.SectionPoints.x", [1, 2, 3, 4, 5])
model.set_value("Model.Element.Blade.BladeCross.BladePolyLine.SectionPoints.y", [2, 3, 4, 5, 6])
model.set_value("Model.Element.Blade.BladeCross.BladePolyLine.SectionPoints.z", [3, 4, 5, 6, 7])
print(model.get_value("Model.Element.Blade.BladeCross.BladePolyLine.SectionPoints.x"))
model.delete_value("Model.Element.Blade.BladeCross.BladePolyLine.SectionPoints.z")
print(model.get_value("Model.Element.Blade.BladeCross.BladePolyLine.SectionPoints"))

df_new = model.to_dataframe()

print(df_new)

df_new.to_csv('output_new.csv')
