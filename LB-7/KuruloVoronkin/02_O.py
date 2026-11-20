from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, price: float) -> float:
        pass


class NoDiscount(DiscountStrategy):
    def apply(self, price: float) -> float:
        return price


class RegularDiscount(DiscountStrategy):
    def apply(self, price: float) -> float:
        return price * 0.95


class VipDiscount(DiscountStrategy):
    def apply(self, price: float) -> float:
        return price * 0.80


class EmployeeDiscount(DiscountStrategy):
    def apply(self, price: float) -> float:
        return price * 0.50


class DiscountCalculator:
    def calculate(self, strategy: DiscountStrategy, price: float) -> float:
        return strategy.apply(price)


if __name__ == "__main__":
    calculator = DiscountCalculator()
    print(f"Regular: {calculator.calculate(RegularDiscount(), 1000)}")
    print(f"VIP: {calculator.calculate(VipDiscount(), 1000)}")
    print(f"Employee: {calculator.calculate(EmployeeDiscount(), 1000)}")