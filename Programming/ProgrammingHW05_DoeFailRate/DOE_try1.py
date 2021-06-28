import os
import re
from numpy.core.numeric import NaN
import pandas as pd
from pandas.io.parsers import read_csv
import seaborn as sns
import matplotlib.pyplot as plt
from compare_df import *
"""======================================================================================
                                         함수 목록 
======================================================================================"""
# read_log :  이름 알아낸 로그 파일 읽어오기 
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

# spec_check :  spec out 찾아 True써서 test column들과 spec out 여부 2차원 배열 반환하는 함수
def spec_check(specarr, dataarr):
    test_names = list(specarr.index)
    dataarr = dataarr[test_names].astype('float')
    checked_arr = (specarr.loc[test_names, 'LOWER_LIMIT'] > dataarr[test_names]) \
        | (specarr.loc[test_names, 'UPPER_LIMIT'] < dataarr[test_names])
    checked_arr['error_sum'] = checked_arr.sum(1)
    specout = checked_arr[checked_arr['error_sum'] != 0]  # 검사한 column중 error가 하나라도 있는 index return

    return specout

# stacked_bar_fig :  config 별 sfr error stacked bar graph 그리는 함수
def stacked_bar_fig(config, datasheet):
    graph = sns.displot(data=datasheet[datasheet["moduleconfig"] == config],  
                x="offset_z", 
                hue='sfr',
                multiple="stack", 
                hue_order=['cm2060', 'cm20', 'cm60'],
                col="site",
                col_wrap=2,
                height=4,
                aspect=1)
    graph.set_titles(col_template=config + ' {col_name}')
    graph.set_xticklabels(rotation=90)
    graph.tight_layout()

    return graph



"""==============================================================================
                                  프로그램 시작
==============================================================================""" 

# 원하는 공정 로그 파일 찾기
folderpath = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
file_list = os.listdir(folderpath)

# 골라낸 file을 AA, EOL file로 분류하고 config로 key 설정, file name을 dict에 저장
p_AA = re.compile(r'BA.*A{2}')
p_EOL = re.compile(r'BA.*LAS')
p_config = re.compile(r'C\d{4}')
AA_files = {}
EOL_files = {}
for log_file in file_list:
    m_AA = p_AA.match(log_file)
    m_EOL = p_EOL.match(log_file)
    if m_AA: 
        m_config = p_config.search(log_file)
        AA_files[m_config.group()] = log_file
    elif m_EOL: 
        m_config = p_config.search(log_file)
        EOL_files[m_config.group()] = log_file

# file name으로 data 불러와 AA data concat, EOL data concat 후 AA-EOL merge
# AA file concat
AA_data = pd.DataFrame()
file = read_csv(folderpath + '/' + AA_files['C4004'], dtype='unicode')
file = file.iloc[:, 18:].astype('float')
print(file.iloc[:, 19].dtypes)



"""
for k in AA_files.keys():         #config 별로 file 읽어와 concat
    data = read_log(folderpath, AA_files[k], 'AA')
    AA_data = pd.concat([AA_data, data], join='outer')

# EOL file concat
EOL_data = pd.DataFrame()
for k in EOL_files.keys():
    data = read_log(folderpath, EOL_files[k], 'EOL')
    data['moduleConfig'] = k
    EOL_data = pd.concat([EOL_data, data], join='outer')

# AA data 와 EOL data merge
data = pd.merge(AA_data, EOL_data, how='inner', left_on='SensorID', right_on='Tx_ASIC_ID', suffixes=('_AA', '_EOL'))
data.set_index('Tx_ASIC_ID', drop=False, inplace=True)

# merge 한 data의 불량률 계산 
# spec data 받아오기 
spec = pd.read_csv(folderpath + '/' + 'SUMMARY_LOG_FORMAT.csv', \
    index_col='SUMMARY_LOG', na_values='None', keep_default_na=True)
# LIMIT 가 하나도 주어지지 않은 test 없는 항목 제외
spec = spec.loc[spec[['LOWER_LIMIT', 'UPPER_LIMIT']].notnull().sum(1) != 0] 

# spec data중 sfr 관련만 뽑아내기 - 정규표현식 이용
p_sfr20 = re.compile(r'sfr_20cm')
p_sfr60 = re.compile(r'sfr_60cm')

spec_sfr20 = spec.loc[[col for col in spec.index if p_sfr20.search(col)]]
spec_sfr60 = spec.loc[[col for col in spec.index if p_sfr60.search(col)]]

# spec limit와 Data 비교해서 spec out Data가 있는 index만 골라내기
specout_sfr20 = spec_check(spec_sfr20, data)
specout_sfr60 = spec_check(spec_sfr60, data)

"""
"""
count를 만들어서 1을 넣는다. (groupby sum에서 갯수 계산 용)
sfr20 에는 sfr 20 test 결과 중 에러가 있을 경우 1을 넣는다.
sfr60 마찬가지 
sfr 2060에는 둘다 에러가 발생한 경우 1을 넣는다.
후에 sfr20, sfr60에서 둘 다 에러 발생한 경우들을 제외한다. 
"""
"""
# fail data 수 세기 위한 결과물 sheet 만들기
fail_data = pd.DataFrame(index=data.index)
fail_data = data[['moduleConfig', 'site_AA', 'Offset_Z']].copy()
fail_data.columns = [x.lower() for x in fail_data.columns]       # 예시 결과에 맞게 column 명 변경
fail_data.rename(columns={'site_aa': 'site'}, inplace=True)
new_col = ['cm20', 'cm60', 'cm2060']
fail_data['count'] = 1                                           # 갯수 세기 위한 count column 추가
for col in new_col: fail_data[col] = 0                           # fail data 표시하기 위한 column 종류별 3개 생성, default = 0

# fail data 를 sfr20, 60, 2060 exclusive 하게 만듬
fail_data[new_col[0]][specout_sfr20.index] = 1
fail_data[new_col[1]][specout_sfr60.index] = 1
fail_data[new_col[2]] = fail_data[new_col[0]] * fail_data[new_col[1]]    # 20과 60모두 1인경우만 1이됨 -> 교집합
for col in new_col[0:2]: fail_data[col] -= fail_data[new_col[2]]         # 20과 60 결과에서 교집합 제외

# Groupby
fail_rate_result = fail_data.groupby(['moduleconfig', 'site', 'offset_z']).sum()

# 갯수 --> 퍼센트로 변환 연산
fail_rate_result.loc[:, ['cm20', 'cm60', 'cm2060']] = \
     fail_rate_result.loc[:, ['cm20', 'cm60', 'cm2060']].div(fail_rate_result['count'], axis=0) * 100

# result Failure analysis 출력 - 현재 실행파일 존재하는 폴더 안에 생성
fail_rate_result.to_csv(folderpath + '/hw5_result.csv')




# Bonus - Graph 출력
# stack graph 뽑기 위해 hue 가 될 'sfr' column 만듬
fail_data["sfr"] = NaN       # PASS 인 Data
fail_data["sfr"][fail_data['cm20'] == 1] = 'cm20'
fail_data["sfr"][fail_data['cm60'] == 1] = 'cm60'
fail_data["sfr"][fail_data['cm2060'] == 1] = 'cm2060'

# 그래프 출력 위한 figure 설정
sns.set()
sns.set_style(style="darkgrid")


# stack graph 형태로 출력
# figure : config 별
# axe : site 별
# hue : sfr 불량 종류 별 (20, 60, 2060둘다)
for config in AA_files.keys():
    graphname = 'g_' + config     # 변수 이름에 config 이름을 넣으려 함
    locals()[graphname] = stacked_bar_fig(config, fail_data)

plt.show()

plt.close()
"""