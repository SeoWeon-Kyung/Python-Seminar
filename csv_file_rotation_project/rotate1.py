import csv     # 각 라인 컬럼들이 콤마로 분리된 텍스트 파일 포맷 처리 위한 모듈

#### 파일 오픈 후 리스트 형태로 변경 ####
f_in = open("copy_a.csv", 'r', encoding='utf-8')  # csv 파일 객체에 열기    , encoding='utf-8'
data = csv.reader(f_in)                           # csv reader형태 객체 

arr = []
for i in data:   
    i.reverse()                                 # csv reader형태 객체 안 리스트들을 역순으로 바꿔 좌우대칭
    arr.append(i)                               # 좌우대칭한 리스트들을 엮어 2차원 리스트 만듬

#### 앞서 리스트화 한 데이터를 회전 ####
new_arr = list(map(list, zip(*arr)))   # map과 zip 함수 이용하여 2차원 리스트 행, 열 바꿈 --> 왼쪽 90도 회전 구현

f_in.close()


#### 회전한 리스트 형태의 데이터를 CSV 파일로 저장 ####
f_out = open("output_a.csv", 'w', encoding='utf-8', newline='')  # write할 파일 미리 해당위치에 만들어놓아야 함. 
                                                   # newline을 공백으로 지정해야 라인 입력 후 한 라인을 비우고 다음이 입력되는 현상 방지.
writedata = csv.writer(f_out)           # 받아온 CSV 파일객체에서 _csv.writer type iterator 객체를 return하여 지정
writedata.writerows(new_arr)            # 지정한 iterator type 객체에 list 파일 입력. --> list 형식 데이터를 CSV 데이터로 입력

f_out.close()

