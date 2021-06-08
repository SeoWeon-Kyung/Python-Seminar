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
    checked_arr['error sum'] = checked_arr.sum(1)
    specout = checked_arr[checked_arr['error sum'] != 0]

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
    log[k] = pd.merge(AA_data, EOL_data, how='inner', left_on='SensorID', right_on='Tx_ASIC_ID', on='site')
    log[k].set_index('Tx_ASIC_ID', drop=False, inplace=True)


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

# spec limit과 Data 비교해서 spec out 인것만 True로 쓰기 
C4004specout_sfr20 = spec_check(spec_sfr20, log['C4004'])
C4004specout_sfr60 = spec_check(spec_sfr60, log['C4004'])
#C4004_sfr20_specout = C4004spec_sfr20.sum(1)[C4004spec_sfr20.sum(1) != 0]
#C4004_sfr60_specout = C4004spec_sfr60.sum(1)[C4004spec_sfr60.sum(1) != 0]

#print(len(C4004specout_sfr20.index))
"""
count를 만들어서 에러가 있으면 1을 넣는다. 
마찬가지로 sfr20 에는 거기만 에러가 난걸 넣는다.
sfr60에는 거기만. 
sfr 2060에는 둘다 난 애들만 넣는다. 
"""
"""
C4004specout_both = pd.merge(C4004specout_sfr20, C4004specout_sfr60, how='inner', \
    left_index=True, right_index=True, suffixes=('_sfr20', '_sfr60'))
print(C4004specout_both)
C4004specout_exc20 = C4004specout_sfr20.loc[C4004specout_both.index]

print(C4004specout_exc20)
"""
fail_data = pd.DataFrame(index=log['C4004'].index)
#print(log['C4004'].columns)
fail_data = log['C4004']['site'].copy()
print(fail_data.head())





#test_sfr20 = spec_data['SUMMARY_LOG'][lambda indx: p_sfr20.search(indx)]
#print(test_sfr20)
#spec_data.loc(,)
