import csv
import chardet
f_in = open("copy_a.csv", 'rb')  # csv 파일 객체에 열기    , encoding='utf-8'
result = chardet.detect(f_in.readline())
print(result['encoding'])