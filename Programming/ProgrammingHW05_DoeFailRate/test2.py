import os
import re
from numpy.core.numeric import NaN
import pandas as pd
from pandas.core.indexes.base import Index
import seaborn as sns
import matplotlib.pyplot as plt

def read_log(fol_path, file_name, which):
    data = pd.read_csv(fol_path + '/' + file_name, dtype='unicode')

    if which == 'AA':
        data.drop_duplicates('SensorID', keep='last', inplace=True)
        temp = data[data['SensorID'] == 'SensorID'].index
    elif which == 'EOL':
        data.drop_duplicates('Tx_ASIC_ID', keep='last', inplace=True)
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

specout_sfr20_index = pd.DataFrame(specout_sfr20.index)
specout_sfr60_index = pd.DataFrame(specout_sfr60.index)

temp = pd.concat([specout_sfr20_index, specout_sfr60_index])
temp['TF'] = temp.duplicated(keep='first')
specout_sfr2060 = temp[temp['TF'] == True].reset_index()

fail_data = pd.DataFrame(index=data.index)
fail_data = data[['moduleConfig', 'site_AA', 'Offset_Z']].copy()
fail_data.columns = fail_data.columns.map(str.lower)
fail_data.rename(columns={'site_aa': 'site'}, inplace=True)
fail_data['sfr'] = ''
fail_data['sfr'][specout_sfr20.index] = 'cm20'
fail_data['sfr'][specout_sfr60.index] = 'cm60'
fail_data['sfr'][specout_sfr2060['Tx_ASIC_ID']] = 'cm2060'



"""
count를 만들어서 에러가 있으면 1을 넣는다. 
마찬가지로 sfr20 에는 거기만 에러가 난걸 넣는다.
sfr60에는 거기만. 
sfr 2060에는 둘다 난 애들만 넣는다. 

# fail data 수 세기 위한 결과물 sheet 만들기
fail_data = pd.DataFrame(index=data.index)
fail_data = data[['moduleConfig', 'site_AA', 'Offset_Z']].copy()
fail_data.columns = fail_data.columns.map(str.lower)
fail_data.rename({'size_AA': 'size'})
new_col = ['cm20', 'cm60', 'cm2060']
#fail_data['count'] = 1
#for col in new_col: fail_data[col] = 0

# fail data 를 sfr20, 60, 2060 exclusive 하게 만듬
fail_data[new_col[0]][specout_sfr20.index] = 1
fail_data[new_col[1]][specout_sfr60.index] = 1
fail_data[new_col[2]] = fail_data[new_col[0]] * fail_data[new_col[1]]
for col in new_col[0:2]: fail_data[col] -= fail_data[new_col[-1]]


# stack graph 뽑기 위해 column 만드는 부분
fail_data["sfr"] = None
fail_data["sfr"][fail_data['cm20'] == 1] = 'cm20'
fail_data["sfr"][fail_data['cm60'] == 1] = 'cm60'
fail_data["sfr"][fail_data['cm2060'] == 1] = 'cm2060'
"""

# Groupby
#fail_rate_result1 = fail_data.groupby(['moduleconfig', 'site', 'offset_z']).count()
#print(fail_data.groupby(['moduleconfig', 'site', 'offset_z']).count())
fail_ana = fail_data.groupby(['moduleconfig', 'site', 'offset_z', 'sfr']).agg('size')
print(fail_ana)
fail_ana_cou = fail_ana.groupby('size').sum()
print(fail_ana_cou)
#fail_ana = fail_ana.pivot()
#fail_rate_result2 = fail_rate_result1.groupby(level='moduleconfig').size()
#fail_rate_wide = fail_rate_result.pivot(index = ['moduleconfig', 'site', 'offset_z'], columns='sfr', values='count')
#fail_rate_result = fail_rate_result.agg(=, 'sum'])
#fail_rate_result = fail_rate_result.sum()

#print(fail_rate_result2)

#for col in new_col: fail_rate_result[col] = fail_rate_result[col] / fail_rate_result['count'] * 100

# result Failure analysis 출력
#fail_rate_result.to_csv(folderpath + '/hw5_result.csv')

"""
# stack graph 형태로 출력
graph1 = sns.histplot(data=fail_data[fail_data["moduleConfig"] == "C4004"], hue='sfr', x="Offset_Z", multiple="stack")
plt.show()
graph2 = sns.histplot(data=fail_data[fail_data["moduleConfig"] == "C4010"], hue='sfr', x="Offset_Z", multiple="stack")
plt.show()
graph3 = sns.histplot(data=fail_data[fail_data["moduleConfig"] == "C4011"], hue='sfr', x="Offset_Z", multiple="stack")
plt.show()
"""