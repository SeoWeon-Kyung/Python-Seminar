import os
import re
from numpy.core.numeric import NaN
import pandas as pd
from pandas.core.indexes.base import Index

def read_log(fol_path, file_name, which):
    data = pd.read_csv(fol_path + '/' + file_name, dtype='unicode')
    data.drop_duplicates(keep='last', inplace=True)

    if which == 'AA':
        temp = data[data['SensorID'] == 'SensorID'].index
    elif which == 'EOL':
        temp = data[data['Tx_ASIC_ID'] == 'Tx_ASIC_ID'].index
    data = data.drop(temp)

    return data

# spec out 찾아 True써서 test column들과 spec out 여부 2차원 배열 반환하는 함수
def spec_check(specarr, dataarr):
    test_names = list(specarr.index)
    dataarr = dataarr[test_names].astype('float')
    checked_arr = (specarr.loc[test_names, 'LOWER_LIMIT'] > dataarr[test_names]) \
        | (specarr.loc[test_names, 'UPPER_LIMIT'] < dataarr[test_names])
    checked_arr['error_sum'] = checked_arr.sum(1)
    specout = checked_arr[checked_arr['error_sum'] != 0]

    return specout


# 원하는 공정 로그 파일 찾기
folderpath = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
file_list = os.listdir(folderpath)

# folder 내 file 중 log file만 골라내기 
p_log = re.compile(r'BA')
log_files = []
for file in file_list:
    m_log = p_log.match(file)
    if m_log: log_files.append(file)

# 골라낸 file을 AA, EOL file로 분류하고 config로 key 
p_AA = re.compile(r'BA.*A{2}')
p_EOL = re.compile(r'BA.*LAS')
p_config = re.compile(r'C\d{4}')
AA_files = {}
EOL_files = {}
for log_file in log_files:
    m_config = p_config.search(log_file)
    m_AA = p_AA.match(log_file)
    m_EOL = p_EOL.match(log_file)
    if m_AA: 
        AA_files[m_config.group()] = log_file
    elif m_EOL: 
        EOL_files[m_config.group()] = log_file

# file name으로 data 불러와 AA-EOL merge 
log = {}
for k in AA_files.keys():
    AA_data = read_log(folderpath, AA_files[k], 'AA')
    EOL_data = read_log(folderpath, EOL_files[k], 'EOL')
    EOL_data['moduleConfig'] = k
    log[k] = pd.merge(AA_data, EOL_data, how='inner', left_on='SensorID', right_on='Tx_ASIC_ID', suffixes=('_AA', '_EOL'))
    log[k].set_index('Tx_ASIC_ID', drop=False, inplace=True)

# config 별 데이터를 위아래로 하나로 합치기 - 위의 for 문에 넣어도 됨
data = pd.DataFrame()
for k in log.keys():
    data = pd.concat([data, log[k]])

# merge 한 data의 불량률 계산 
# spec data 받아오기 
spec = pd.read_csv(folderpath + '/' + 'SUMMARY_LOG_FORMAT.csv', \
    index_col='SUMMARY_LOG', na_values='None', keep_default_na=True)
# LIMIT 값 둘 다 없는 항목 제외
spec = spec.loc[spec[['LOWER_LIMIT', 'UPPER_LIMIT']].notnull().sum(1) != 0]

# spec data중 sfr 관련만 뽑아내기
p_sfr20 = re.compile(r'sfr_20cm')
p_sfr60 = re.compile(r'sfr_60cm')

spec_sfr20 = spec.loc[[col for col in spec.index if p_sfr20.search(col)]]
spec_sfr60 = spec.loc[[col for col in spec.index if p_sfr60.search(col)]]

# spec limit과 Data 비교해서 spec out Data가 있는 index만 골라내기
specout_sfr20 = spec_check(spec_sfr20, data)
specout_sfr60 = spec_check(spec_sfr60, data)

"""
count를 만들어서 에러가 있으면 1을 넣는다. 
마찬가지로 sfr20 에는 거기만 에러가 난걸 넣는다.
sfr60에는 거기만. 
sfr 2060에는 둘다 난 애들만 넣는다. 
"""
# fail data 수 세기 위한 결과물 sheet 만들기
fail_data = pd.DataFrame(index=data.index)
fail_data = data[['moduleConfig', 'site_AA', 'Offset_Z']].copy()
new_col = ['count', 'cm20', 'cm60', 'cm2060']
for col in new_col: fail_data[col] = 0

# fail data 를 sfr20, 60, 2060 exclusive 하게 만듬
fail_data[new_col[1]][specout_sfr20.index] = 1
fail_data[new_col[2]][specout_sfr60.index] = 1
fail_data[new_col[3]] = fail_data[new_col[1]] * fail_data[new_col[2]]
for col in new_col[1:3]: fail_data[col] -= fail_data[new_col[-1]]
for col in new_col[1:]: fail_data[new_col[0]] += fail_data[col]

# Groupby
fail_rate_result = fail_data.groupby(['moduleConfig', 'site_AA', 'Offset_Z']).sum()
for col in new_col[1:]: fail_rate_result[col] = fail_rate_result[col] / fail_rate_result[new_col[0]] * 100

# result 출력
fail_rate_result.to_csv(folderpath+ '/hw5_result.csv')

