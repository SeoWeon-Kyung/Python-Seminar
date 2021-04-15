from random import randint
import re

class Account:

    count_account = 0
    depo_num = 0

    def __init__(self, owner, money_left):
        self.owner = owner
        self.money_left = money_left
        self.bank_name = "SC은행"
        
        acc_num = str(randint(0, 99999999999))
        acc_num.zfill(11)
        self.acc_num = acc_num[:3]+"-"+acc_num[3:5]+"-"+acc_num[-6:]
        self.depo_reco = []
        self.witd_reco = []

        Account.count_account += 1
    
    def __del__(self):
        Account.count_account -= 1
    
    @classmethod
    def get_account_count(cls):
        print(cls.count_account)
    
    def deposit(self, add_money):
        if add_money < 1: print("최소 입금 금액을 충족해야 합니다.")
        else: 
            self.money_left += add_money
            Account.depo_num += 1
            self.depo_reco.append(add_money)

            if Account.depo_num % 5 == 0:
                self.money_left *= 1.01
                self.money_left = int(self.money_left)
    
    def deposit_history(self):
        print("{:<^20}".format("입금내역"))
        for i in self.depo_reco:
            print(i)
        print("="*20, "\n")
                
    def withdraw(self, out_money):
        if out_money > self.money_left: print("잔고가 부족합니다.")
        else: 
            self.money_left -= out_money
            self.witd_reco.append(out_money)
    
    def withdraw_history(self):
        print("{:>^20}".format("출금내역"))
        for i in self.witd_reco:
            print(i)
        print("="*20, "\n")
    
    def display_info(self):
        info = """
        은행이름: {}
        예금주: {}
        계좌번호: {}
        잔고: {:,d}원
        """.format(self.bank_name, self.owner, self.acc_num, self.money_left)
        print(info)





acc1 = Account("경서원", 5500000)
for i in range(1000, 10000, 1000):
    acc1.deposit(i)
    acc1.withdraw(int(i/2))

acc1.deposit_history()
acc1.withdraw_history()
acc1.display_info()








    






    

    


