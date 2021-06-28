import numpy as np
import pandas as pd
import os

def compare_df(df1, df2):
    df = pd.concat([df1, df2])
    df = df.reset_index(drop=True)

    df_grp = df.groupby(df.columns.tolist())
    df_dict = df_grp.groups

    no_match_idx = [x[0] for x in df_dict.values() if len(x) == 1]
    no_match = df.loc[no_match_idx, :]
    
    #match_idx = [x[0] for x in df_dict.values() if len(x) == 2]
    #match = df.loc[match_idx, :]

    return no_match #, match

folderpath = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')

my_result = pd.read_csv(folderpath + '/hw5_result.csv', dtype='unicode')
my_result.rename(columns={'moduleConfig': 'moduleconfig', 'site_AA': 'site', 'Offset_Z': 'offset_z'}, inplace=True)
answer_result = pd.read_csv(folderpath + '/report_kim.csv', dtype='unicode')

not_match = compare_df(my_result, answer_result)
