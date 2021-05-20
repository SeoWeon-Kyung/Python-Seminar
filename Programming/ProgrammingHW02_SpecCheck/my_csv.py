# my_csv.py 
# csv 특징인 줄바꿈 공백과 열간 구분 , 삭제, parsing 함수
#===============================================================
import re

# csv 한 줄 맨 뒤 enter 없애고 , (comma) 로 나누어 리스트 반환 함수
def csv_parse(line):
    return line.strip().split(',')

# 문자 없는 수 (점 포함)를 (str-->)float 형으로 변환 함수
def only_float(line):
    p = re.compile(r'[a-zA-Z]')
    return [float(num) for num in line if not p.match(num)]

# 열 평균 구하는 함수 - zip 이용 열 2차원 배열 열 묶음
def column_ave(two_dm_data):
    aligned_data = list(zip(*two_dm_data))
    average = []
    for line in aligned_data:
        average.append(sum(line)/len(line))
    return average

# 최저, 최고값 이용하여 spec 충족 여부 확인, 벗어나는 값 list 로 반환
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