from abc import ABC, abstractclassmethod
class DiscountCalculator:
    def __init__(self, price):
        self.price = price

    @abstractclassmethod
    def calculate(self, price):
        pass

class Regular_Discount(DiscountCalculator):
    def calculate(self, price):
        return price * 0.95

class Vip_Discount(DiscountCalculator):
    def calculate(self, price):
        return price * 0.80

class Employee_Discount(DiscountCalculator):
    def calculate(self, price):
        return price * 0.50

class Discount:
    def __init__(self, price, discount: DiscountCalculator):
        self.price = price
        self.discount = discount

    def total_discount(self):
        return self.discount.calculate(self.price)