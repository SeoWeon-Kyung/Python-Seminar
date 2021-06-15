import numpy as np
import pandas as pd
import os

folderpath = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')

my_result = pd.read_csv(folderpath + '/hw5_result.csv', dtype='unicode')
my_result.rename(columns={'moduleConfig': 'moduleconfig', 'site_AA': 'site', 'Offset_Z': 'offset_z'}, inplace=True)
answer_result = pd.read_csv(folderpath + '/report_kim.csv', dtype='unicode')

df = pd.concat([my_result, answer_result])
df = df.reset_index(drop=True)

df_grp = df.groupby(df.columns.tolist())
df_di = df_grp.groups

idx = [x[0] for x in df_di.values() if len(x) == 1]
print(idx)
not_match = df.loc[idx, :]
print(not_match)
