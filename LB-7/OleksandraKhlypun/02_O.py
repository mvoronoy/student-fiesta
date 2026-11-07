from abc import ABC, abstractmethod


class Discount(ABC):
    """Абстракція знижки."""

    @abstractmethod
    def apply(self, price):
        pass


class RegularDiscount(Discount):
    def apply(self, price):
        return price * 0.95


class VipDiscount(Discount):
    def apply(self, price):
        return price * 0.80


class EmployeeDiscount(Discount):
    def apply(self, price):
        return price * 0.50


class NoDiscount(Discount):
    def apply(self, price):
        return price


class DiscountCalculator:
    """Не знає про конкретні типи клієнтів - працює з абстракцією Discount."""

    def calculate(self, discount, price):
        return discount.apply(price)


class StudentDiscount(Discount):
    def apply(self, price):
        return price * 0.70


if __name__ == "__main__":
    calculator = DiscountCalculator()

    print(calculator.calculate(RegularDiscount(), 100))
    print(calculator.calculate(VipDiscount(), 100))
    print(calculator.calculate(EmployeeDiscount(), 100))
    print(calculator.calculate(NoDiscount(), 100))
    print(calculator.calculate(StudentDiscount(), 100))