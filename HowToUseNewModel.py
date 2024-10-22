import imkernel as imk

tree_1 = imk.system(supname='insofsys', name='insoftest', subname='DTIS_511')
tree_2 = imk.system(supname='insofsys', name='insoftest', subname=['DTIS_511', 'NDT_SNPTC'])
tree_3 = imk.system(supname='insofsys', name=['insoftest', 'insofrobot'], subname=[['DTIS_511', 'NDT_SNPTC'], ['insoftube', 'insofbend', 'insoflaser']])
tree_4 = imk.system(supname='insofsys', name=['insoftest', 'insofrobot'], subname=['DTIS_511', ['insoftube', 'insofbend', 'insoflaser']])
tree_5 = imk.system(supname='insofsys', name=['insoftest', 'insofrobot'], subname=[['DTIS_511', 'NDT_SNPTC'], 'insoftube'])
tree_6 = imk.system(supname='insofsys', name=['insofaiam', 'insoftest', 'insofrobot'], subname=[None, ['DTIS_511', 'NDT_SNPTC'], ['insoftube', 'insofbend', 'insoflaser']])
df_6 = imk.tree_to_df(tree_6)
print('end')
