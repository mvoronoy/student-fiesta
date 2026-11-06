# Створено базовий клас для розрахунку знижки
# кожен тип клієнта реалізовано як окремий підклас

from abc import ABC, abstractmethod

class DiscountStrategy(ABC):
    @abstractmethod
    def calculate(self, price: float) -> float:
        pass

class RegularDiscount(DiscountStrategy):
    def calculate(self, price: float) -> float:
        return price * 0.95

class VIPDiscount(DiscountStrategy):
    def calculate(self, price: float) -> float:
        return price * 0.80

class EmployeeDiscount(DiscountStrategy):
    def calculate(self, price: float) -> float:
        return price * 0.50

class DiscountCalculator:
    def calculate(self, strategy: DiscountStrategy, price: float) -> float:
        return strategy.calculate(price)