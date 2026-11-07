
from abc import ABC, abstractmethod

class DiscountStrategy(ABC):
    @abstractmethod
    def calculate(self, price):
        pass

class RegularDiscount(DiscountStrategy):
    def calculate(self, price):
        return price * 0.95

class VIPDiscount(DiscountStrategy):
    def calculate(self, price):
        return price * 0.80

class EmployeeDiscount(DiscountStrategy):
    def calculate(self, price):
        return price * 0.50

class NoDiscount(DiscountStrategy):
    def calculate(self, price):
        return price

class DiscountCalculator:
    def __init__(self, strategy: DiscountStrategy):
        self.strategy = strategy

    def calculate(self, price):
        return self.strategy.calculate(price)
