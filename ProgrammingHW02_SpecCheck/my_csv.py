# csv 특징인 줄바꿈 공백과 열간 구분 , 삭제, parsing 함수
import re

def csv_parse(line):
    return line.strip().split(',')

def only_float(line):
    p = re.compile(r'[a-zA-Z]')
    return [float(num) for num in line if not p.match(num)]

def column_ave(two_di_data):
    aligned_data = list(zip(*two_di_data))
    average = []
    for line in aligned_data:
        average.append(sum(line)/len(line))
    return average

def check_spec(low_guide, high_guide, two_di_data):
    aligned_data = list(zip(*two_di_data))
    check_data = zip(low_guide, high_guide, aligned_data)
    spec_out = []
    for low, high, num_arr in check_data:
        for num in num_arr:
            if low <= num <= high:
                pass
            else: 
                spec_out.append(num)
    return spec_out