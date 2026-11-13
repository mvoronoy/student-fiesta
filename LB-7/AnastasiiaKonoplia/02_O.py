class Discount:
    def calculate(self, price):
        return price

class RegularDiscount(Discount):
    def calculate(self, price):
        return price * 0.95

class VIPDiscount(Discount):
    def calculate(self, price):
        return price * 0.80

class EmployeeDiscount(Discount):
    def calculate(self, price):
        return price * 0.50

class DiscountCalculator:
    def calculate(self, discount, price):
        return discount.calculate(price)

if __name__ == "__main__":
    calculator = DiscountCalculator()

    regular = RegularDiscount()
    vip = VIPDiscount()
    employee = EmployeeDiscount()

    price = 100

    print("Regular customer:", calculator.calculate(regular, price))
    print("VIP customer:", calculator.calculate(vip, price))
    print("Employee:", calculator.calculate(employee, price))

    class StudentDiscount(Discount):
        def calculate(self, price):
            return price * 0.90

    student = StudentDiscount()
    print("Student:", calculator.calculate(student, price))