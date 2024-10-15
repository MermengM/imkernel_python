import imkernel
from imkernel.core import ModelLib
from imkernel.core.model_2 import NewModel

modeltype = ModelLib()
modeltype.create_new_model('insofaiam')
modeltype.create_new_model('insoftest')
modeltype.create_new_model('insofrobot')
print(modeltype)
print(modeltype.insoftest)
insoftest: NewModel = modeltype.insoftest
insoftest.add_subtype('DTIS-511')
insoftest.add_subtype('NDT-SNPTC')
show_type_df = modeltype.show_subtype()
insoftest.add_parameter('人员')
insoftest.add_parameter('机构')
insoftest.add_parameter('职位')
insoftest.add_parameter('个人')
insoftest.add_parameter('角色')
insoftest.add_parameter('账号')
insoftest.人员.add_property('机构编号')
insoftest.人员.add_property('级别')
insoftest.人员.add_property('机构编码')
insoftest.人员.add_property('排序')
insoftest.人员.add_property('状态')
DTIS_511 = insoftest.find_subtype('DTIS-511')
print(insoftest.人员.机构编号.name)
print(1)
