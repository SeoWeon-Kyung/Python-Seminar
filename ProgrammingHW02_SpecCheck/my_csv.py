# csv 특징인 줄바꿈 공백과 열간 구분 , 삭제, parsing 함수
import re

def csv_parse(line):
    return line.strip().split(',')

def only_float(line):
    p = re.compile(r'[a-zA-Z]')
    return [float(num) for num in line if not p.match(num)]