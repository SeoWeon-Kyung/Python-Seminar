""" ############################################################### 
   모듈 사용 없이, 1줄씩 읽어 주어진 csv 데이터 왼쪽으로 90도 회전하기
#################################################################"""

f = open("C:/Users/LGITLocalAdmin/Desktop/Git_Python_Seminar/csv_file_rotation_project/copy_a.csv", 'r')
data_write = ''     #회전하여 write할 데이터 저장할 변수

# 첫 인덱스 행으로 데이터 가로 크기 확인, 저장할 리스트 형성
indx = f.readline().replace('\n', '').split(',')     # 줄바꿈 없앰, comma로 구분하여 데이터 리스트에 각 문자열로 저장
indx.reverse()                     # 회전 위해 역순 

# 한줄씩 읽어와 돌려 넣어 돌린 결과 2차원 리스트 완성
while True:
    data = f.readline()                  # 데이터 한줄씩 읽어옴
    if not data: break                   # 읽어올 데이터가 없으면 루프 종료

    rot = data.replace('\n', '').split(',')      # 리스트 형태로 변환
    rot.reverse()                                # 회전 위한 역순
 
    indx = list(x + ',' + y for x, y in zip(indx, rot))      # 읽어온 한 줄의 데이터를 문자열로 세로로 붙여 문자열 리스트 만듬 --> 각 줄이 엑셀 가로 입력 1줄

data_write = "\n".join(indx)     # 만든 전체 데이터를 csv 파일로 저장하기 위해 형식 맞춤 (줄바꿈에 \n 기호 삽입)
            
f.close()                        # 읽어온 파일 종료
 
f = open('output_a_3.csv', 'w')      # 회전한 데이터 출력할 파일 생성
f.write(data_write)                  # 데이터 출력

f.close()                            # 출력용 데이터 종료





