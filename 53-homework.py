def print_data():
    print("1. 입력")
    print("2. 출력")
    print("3. 검색")
    print("4. 종료")
    menu = int(input("메뉴를 선택하세요.:"))
    temp = []


    if menu==1:
       print(write_data())
       question = str(input("계속 입력하시겠습니까? n/y"))
       if question == "y":
           write_data()
       if question == "n":
           print(print_data())
       else:
           print("end")
    if menu==2:
       print(mylist)
    if menu==3:
       search_out()
    if menu==4:
       print("end")

def write_data(list_):

    name = input("제품명:")
    qty = input("수량: ")
    date = input("생산일: ")
    mylist = name + qty + date
    return mylist

print_data()





