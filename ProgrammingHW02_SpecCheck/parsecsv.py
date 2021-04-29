# parsecsv.py
# project with no module except mine
# ===================================================================
import re
from my_csv import *

# use csv_parse function
with open('../PYTHON-SEMINAR/ProgrammingHW02_SpecCheck/log.csv', 'r') as f:
    low_limit = csv_parse(f.readline())      # csv 1st line - low limit
    high_limit = csv_parse(f.readline())     # csv 2nd line - high limit
    head = csv_parse(f.readline())           # csv 3rd line - Header

    # Limits : number
    low_limit = only_float(low_limit)        # Leave only num data, str --> float type
    high_limit = only_float(high_limit)

    # Get Dataset 
    data = f.readlines()
    num_data = [only_float(csv_parse(line)) for line in data]  # Leave only num data, str --> float type

    # Find column average
    average = column_ave(num_data)
    
    # Find spec out data 
    spec_out = check_spec(low_limit, high_limit, num_data)


""" 데이터 출력 순서
1. 헤더 --> head 의 앞칸 'barcode' 삭제 
2. 데이터 --> data (문자열상태) 이용하여 앞의 barcode 만 삭제 - 정규식 이용
3. 평균 --> average csv 형식 맞춘 문자열로 변환
4. spec out 데이터 --> spec_out 문자열로 ' ' 구분하여 변환
"""
# Data processing
head.remove('barcode')
head = ','.join(head) + '\n'

p = re.compile(r'\w+[,](.+$)')    # without barcode consists of characters
data_write = [p.sub('\g<1>', line) for line in data]

average_write = ','.join(map(str, average)) + '\n'
spec_out_write = ' '.join(map(str, spec_out)) + '\n'

# Data writing
with open('../PYTHON-SEMINAR/result_parsecsv.csv', 'w') as f:
    f.write(head)
    f.writelines(data_write)
    f.write(average_write)
    f.write(spec_out_write)