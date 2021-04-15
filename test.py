from random import randint
import re

class Account:

    count_account = 0

    def __init__(self, owner, money_left):
        self.owner = owner
        self.money_left = money_left
        self.bank_name = "SC은행"
        
        acc_num = str(randint(0, 99999999999))
        acc_num.zfill(11)
        self.acc_num = acc_num[:3]+"-"+acc_num[3:5]+"-"+acc_num[-6:]

        Account.count_account += 1
    
    def __del__(self):
        Account.count_account -= 1
    
    @classmethod
    def get_account_count(cls):
        print(cls.count_account)
    
    def deposit(self, add_money):
        if add_money < 1: print("최소 입금 금액을 충족해야 합니다.")
        else: self.money_left += add_money

    def withdraw(self, out_money):
        if out_money > self.money_left: print("잔고가 부족합니다.")
        else: 
            self.money_left -= out_money
            return out_money
    
    def display_info(self):
        money ="".join(reversed(self.money_left))
        temp = re.sub(r'(.{3})', r':\1', money)[1:]
        money = "".join(reversed(new_money))

        info = """은행이름: {}
        예금주: {}
        계좌번호: {}
        잔고: {}원
        """.format(self.bank_name, self.owner, self.acc_num, new_money)
        print(info)




myacc = Account("Seoweon", 10000)
myacc.display_info()








    






    

    


