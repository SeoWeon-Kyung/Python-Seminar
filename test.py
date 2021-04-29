class ScopeTest:
    spam = "test spam"

    def do_local(self):
        self.spam = "local spam"

    @classmethod
    def do_global(cls):
        cls.spam = "global spam"
    
first = ScopeTest()
second = ScopeTest()
print(f"초기 글로벌 변수 spam : {first.spam}")

first.spam = "change spam"   # 글로벌 변수 spam이 아니라 새롭게 만들어지는 인스턴스 변수 spam임
print(f'인스턴스에서 글로벌 변수 변경 : {first.spam},  다른 인스턴스 : {second.spam}')
print(dir(first))

"""
first.do_local()   # self 떼면 글로벌 변수 변경 가능 
print(f'인스턴스 메서드로 접근해서 변경 : {first.spam}, 다른 인스턴스 : {second.spam}')

ScopeTest().do_global()
print(f'클래스 메서드로 접근해서 변경 : {first.spam}, 다른 인스턴스 : {second.spam}')
"""
