from abc import ABC, abstractmethod


class Discount(ABC):
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


class StudentDiscount(Discount):
    def apply(self, price):
        return price * 0.70


class DiscountCalculator:
    def calculate(self, discount, price):
        return discount.apply(price)


if __name__ == "__main__":
    calculator = DiscountCalculator()

    print("Regular:", calculator.calculate(RegularDiscount(), 100))
    print("VIP:", calculator.calculate(VipDiscount(), 100))
    print("Employee:", calculator.calculate(EmployeeDiscount(), 100))
    print("Student:", calculator.calculate(StudentDiscount(), 100))