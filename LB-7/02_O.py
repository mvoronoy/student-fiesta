#
#   Fix violation of Open/Closed Principle (OCP)
#   Software entities should be open for extension but closed for modification.
#

class DiscountCalculator:
    def calculate(self, customer_type, price):
        if customer_type == "regular":
            return price * 0.95

        elif customer_type == "vip":
            return price * 0.80

        elif customer_type == "employee":
            return price * 0.50

        return price
