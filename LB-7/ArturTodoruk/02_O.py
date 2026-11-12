# В оригінальному варіанті метод calculate у класі DiscountCalculator використовує ланцюжок умовних операторів для перевірки типу клієнта.
# Потрібно, щоб програмні сутності були відкритими для розширення, але закритими для модифікації.
# Для цього був виділений абстрактний базовий клас DiscountStrategy та створені окремі класи для кожного типу знижки.

from abc import ABC, abstractmethod

class DiscountStrategy(ABC):
    @abstractmethod
    def apply_discount(self, price: float) -> float:
        pass

class NoDiscount(DiscountStrategy):
    def apply_discount(self, price: float) -> float:
        return price

class RegularDiscount(DiscountStrategy):
    def apply_discount(self, price: float) -> float:
        return price * 0.95

class VipDiscount(DiscountStrategy):
    def apply_discount(self, price: float) -> float:
        return price * 0.80

class EmployeeDiscount(DiscountStrategy):
    def apply_discount(self, price: float) -> float:
        return price * 0.50

class DiscountCalculator:
    def calculate(self, strategy: DiscountStrategy, price: float) -> float:
        return strategy.apply_discount(price)
