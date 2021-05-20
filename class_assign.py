def beginning(memory):
    menu_num = choose_menu()
    
    if menu_num == 1:
        memory = inputData(memory)
    elif menu_num == 2:
        outputData(memory)
    elif menu_num == 3:
        searchData(memory)
    elif menu_num == 4:
        close_protocol(memory)
    else: 
        print("존재하지 않는 명령입니다.")
        beginning(memory)
    return

def choose_menu():
    print("1. 입력")
    print("2. 출력")
    print("3. 검색")
    print("4. 종료")
    menu = int(input("메뉴를 선택하세요.:"))
    return menu

def inputData(list_):
    
    name = input("제품명:")
    qty = input("수량: ")
    date = input("생산일: ")
    dataline = [name, qty, date]
    
    list_.append(dataline)
    
    while(True):
        question = str(input("계속 입력하시겠습니까? n/y   : "))
        if question == "y":
            inputData(list_)
            break
        elif question == "n":
            beginning(list_)
            break
        else: continue


def outputData(list_):
    print("-"*70)
    print(f'{"제품명":^20}{"수량":^18}{"생산일":^18}')
    print("-"*70)
    for line in list_:
        for word in line:
            print(f'{word:^20}', end='')
        print('\n')

def searchData(list_):
    name = input("검색할 제품명을 입력하세요 : ")
    get_data = []

    for line in list_:
        if line[0] == name:
            get_data.append(line)
    
    if get_data != []:
        print("-"*70)
        print(f'{"제품명":^20}{"수량":^18}{"생산일":^18}')
        print("-"*70)
        for line in get_data:
            for word in line:
                print(f'{word:^20}', end='')
            print('\n')
    else: beginning(list_)

def close_protocol(list_):
    close = str(input("프로그램을 종료하시겠습니까? (y/n) : "))
    if close == 'n':
        beginning(list_)
    elif close == 'y':
        return

            

my_memory = []    
beginning(my_memory)

