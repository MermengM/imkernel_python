# 创建方法对象dataframe
import pandas as pd

method_df = pd.DataFrame(data=[
    ('叶片设计方法', '型线生成方法(Python型线程序)', '十一参数法'),
    ('叶片设计方法', '型线生成方法(Python型线程序)', '采样点法'),
    ('叶片设计方法', '曲面生成法(PeriodicTsplineSkinningLib.dll)'),
    ('叶片设计方法', '端面封闭生成法(Fill_empty_obj2stl.py)'),
    ('轨迹规划方法', '精加工算法'),
    ('加工规划方法', 'NC代码生成方法(FiveAxisSolver.dll)'),
    ('检测方法', '采样算法'),
    ('检测方法', '配准算法'),
    ('人工智能优化方法', '复杂型面加工特征参数优化迭代算法'),
    ('人工智能优化方法', '面向复杂型面的铣削参数优化方法')
])

print(method_df)
