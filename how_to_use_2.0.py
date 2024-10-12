import imkernel
from imkernel.core import ModelLib

a = ModelLib()
a.create_new_model('insofaiam')
a.create_new_model('insoftest')
a.create_new_model('insofrobot')

print(a)
print(a.insofaiam)
insofaiam = a.insofaiam
insofaiam.add_subtype('DTIS-511')
insofaiam.add_subtype('NDT-SNPTC')
show_type_df = a.show_subtype()
print(1)
