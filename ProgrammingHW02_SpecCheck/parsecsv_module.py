import csv  
from my_csv import csv_parse, only_float, column_ave, check_spec

with open("../Python-Seminar/ProgrammingHW02_SpecCheck/log.csv", 'r') as f:
    data = list(csv.reader(f))  
    low_limit = only_float(data.pop(0))
    high_limit = only_float(data.pop(0))
    head = data.pop(0)
    num_data = [only_float(line) for line in data]
    
     # 각 열 평균 구하기
    average = column_ave(num_data)
    
    # spec out 찾기
    spec_out = check_spec(low_limit, high_limit, num_data)



""" 데이터 출력 순서
1. 헤더 --> head 의 맨앞 요소 'barcode' 삭제 
2. 데이터 --> num_data 활용하여 각 float --> str로만 변환
3. 평균 --> float --> str만 변환 후 data_write에 붙이기
4. spec out 데이터 --> spec_out 문자열로 ' ' 구분하여 제작
"""
# 데이터 출력
head.remove('barcode')
data_write = [[str(num) for num in line] for line in num_data]
average_write = [str(num) for num in average]
spec_out_write = [' '.join(map(str, spec_out))]

with open("../Python-Seminar/result_2.csv", 'w', newline='') as f:
    writedata = csv.writer(f)           
    writedata.writerow(head)
    writedata.writerows(data_write)
    writedata.writerow(average_write)
    writedata.writerow(spec_out_write)




    
