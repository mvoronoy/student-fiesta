#
#   Fix violation of Open/Closed Principle (OCP)
#   Software entities should be open for extension but closed for modification.
#
from abc import ABC, abstractmethod

class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, price: float) -> float:
        ...


class NoDiscount(DiscountStrategy):
    def apply(self, price):
        return price


class RegularDiscount(DiscountStrategy):
    def apply(self, price):
        return price * 0.95


class VipDiscount(DiscountStrategy):
    def apply(self, price):
        return price * 0.80


class EmployeeDiscount(DiscountStrategy):
    def apply(self, price):
        return price * 0.50


class DiscountCalculator:
    def calculate(self, strategy: DiscountStrategy, price: float) -> float:
        return strategy.apply(price)

class StudentDiscount(DiscountStrategy):
    def apply(self, price):
        return price * 0.90