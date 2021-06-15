import os
import re
from numpy.core.numeric import NaN
import pandas as pd
from pandas.core.indexes.base import Index
import seaborn as sns
import matplotlib.pyplot as plt

folderpath = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
print(folderpath)
file_list = os.listdir(folderpath)

# folder 내 file 중 log file만 골라내기 
p_log = re.compile(r'LOT_TIME')
log_files = []
for file in file_list:
    m_log = p_log.search(file)
    if m_log: log_files.append(file)

datas = []
for name in log_files:
    data = pd.read_csv(folderpath + '/' + name)
    datas.append(data)


mer_data = pd.DataFrame(datas[0])
mer_data = pd.concat([mer_data, datas[1], datas[2], datas[3], datas[4]])
mer_data.drop_duplicates('Barcode', keep='last', inplace=True)


print(len(mer_data))

error_num = mer_data.groupby('ERROR').size()

writer = pd.ExcelWriter(folderpath + '/UPDOWN_analysis.xlsx', engine='xlsxwriter')

mer_data.to_excel(writer, sheet_name = 'UPDOWN_log')
error_num.to_excel(writer, sheet_name = 'FAILURE num')

writer.save()

graph1 = sns.histplot(data=mer_data[mer_data['ERROR'] != 'PASS'], x="ERROR")
plt.show()
