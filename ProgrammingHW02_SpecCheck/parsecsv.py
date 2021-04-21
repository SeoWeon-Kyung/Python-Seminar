import re
from my_csv import csv_parse, only_float

with open('../PYTHON-SEMINAR/ProgrammingHW02_SpecCheck/log.csv', 'r') as f:
    low_limit = csv_parse(f.readline())      # csv 1st line
    high_limit = csv_parse(f.readline())     # csv 2nd line
    head = csv_parse(f.readline())           # csv 3rd line

    low_limit = only_float(low_limit)        # num data 만 남김
    high_limit = only_float(high_limit)

    data = f.readlines()
    num_data = [only_float(csv_parse(line)) for line in data]
    data_length = len(data)

     # 각 열 평균 구하기
    align_data = list(zip(*num_data))
    average = []
    for line in align_data:
        average.append(sum(line)/data_length)
    
    # spec out 찾기
    spec_out = []
    check_data = list(zip(low_limit, high_limit, align_data))
    for guide_low, guide_high, data_line in check_data:    
        for num in data_line:
            if guide_low <= num <= guide_high:
                pass
            else: spec_out.append(num)

""" 데이터 출력 순서
1. 헤더 --> head 의 앞칸 'barcode' 삭제 
2. 데이터 --> data (문자열상태) 이용하여 앞의 barcode 만 삭제 - 정규식 이용
3. 평균 --> average csv 형식 맞춘 문자열로 변환
4. spec out 데이터 --> spec_out 문자열로 ' ' 구분하여 변환
"""

# 데이터 출력
head.remove('barcode')
head = ','.join(head) + '\n'

p = re.compile(r'\w+[,](.+$)')
data_write = [p.sub('\g<1>', line) for line in data]

average_write = ','.join(map(str, average)) + '\n'
spec_out_write = ' '.join(map(str, spec_out)) + '\n'

with open('../PYTHON-SEMINAR/result.csv', 'w') as f:
    f.write(head)
    f.writelines(data_write)
    f.write(average_write)
    f.write(spec_out_write)