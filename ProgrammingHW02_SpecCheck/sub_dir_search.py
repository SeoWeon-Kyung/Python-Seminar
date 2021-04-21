import os

# 아래 코드를 수정하여 파일 리스트를 반환하는 기능을 구현하세요. 
# --> 구현 완료
def search(dirname):
    try:
        filenames = os.listdir(dirname)
        result = []
        for filename in filenames:
            full_filename = os.path.join(dirname, filename)
            if os.path.isdir(full_filename):
                result += search(full_filename)     # 재귀 형태로 계속 타고 들어감
            else:
                ext = os.path.splitext(full_filename)[-1]
                if ext == '.py':
 #                   print(full_filename)  -->  수정
                    result.append(full_filename)
    except PermissionError:               # 접근 제한된 디렉토리 패스
        pass
    return result

result_list = search("C:/Users/user/Desktop/Python-Seminar")

for name in result_list: print(name)