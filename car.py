class Car:
    def __init__(self, wheel, price):
        self.wheel = wheel
        self.price = price
    
    def info(self):
        print("바퀴수", self.wheel)
        print("가격", self.price)

class RealCar(Car):
    def __init__(self, wheel, price):
        super().__init__(wheel, price)
    

class Bicycle(RealCar):
    def __init__(self, wheel, price, oper):
        super().__init__(wheel, price)
        self.oper = oper
    
    def info(self):
        super().info()
        print("구동계", self.oper)

car = Car(2, 1000)
bi = Bicycle(2, 100, "시마노")
realcar = RealCar(4, 1000)
bi.info()