class NormalFactory:
    def create_crust(self):
        return "Звичайний бортик", 0

class CheeseFactory:
    def create_crust(self):
        return "Сирний бортик", 40

class Factory:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    def get_factory(self, cheese):
        if cheese:
            return CheeseFactory()
        return NormalFactory()

class PreviousOrder:
    def __init__(self, ingredients):
        self.ingredients = ingredients

    def clone(self):
        return self.ingredients.copy()

class PizzaBuilder:
    def __init__(self, name, crust, price):
        self.name = name
        self.crust = crust
        self.price = price
        self.ingredients = []

    def add_ingredient(self, ingredient, price):
        self.ingredients.append(ingredient)
        self.price += price

    def build(self):
        return {
            "name": self.name,
            "crust": self.crust,
            "ingredients": self.ingredients,
            "price": self.price
        }

class PizzaCreator:
    def create_pizza(self, crust, price):
        name = input("Оберіть піцу (1 - Маргарита, 2 - Пепероні): ")

        if name == "1":
            return PizzaBuilder("Маргарита", crust, price)
        return PizzaBuilder("Пепероні", crust, price)


cheese = input("Сирний бортик? (так/ні): ").lower() == "так"

factory = Factory()
crust_factory = factory.get_factory(cheese)
crust, crust_price = crust_factory.create_crust()

print("Обрано:", crust)

creator = PizzaCreator()
builder = creator.create_pizza(crust, crust_price)

previous = PreviousOrder(["Томатний соус", "Моцарела"])
use_previous = input("Повторити попереднє замовлення? (так/ні): ")

if use_previous.lower() == "так":
    builder.ingredients = previous.clone()
    print("Інгредієнти попереднього замовлення скопійовано")
    builder.price += 15 + 30

print("Додайте інгредієнти: 1 - Пепероні, 2 - Гриби, 3 - Оливки, 0 - завершити")
prices = {"1": ("Пепероні", 35), "2": ("Гриби", 20), "3": ("Оливки", 15)}

while True:
    choice = input("Ваш вибір: ")
    if choice == "0":
        break
    if choice in prices:
        ingredient, price = prices[choice]
        builder.add_ingredient(ingredient, price)
        print("Додано:", ingredient)
    else:
        print("Невірний вибір")

order = builder.build()

print("\nВаще замовлення:")
print("Піца:", order["name"])
print("Бортик:", order["crust"])
print("Інгредієнти:", ", ".join(order["ingredients"]))
print("Вартість:", order["price"], "грн")

paid = input("Оплатити замовлення? (так/ні): ")
if paid.lower() == "так":
    print("Оплата успішна!")
    print("Статус доставки: Замовлення готується")
    print("Кур'єр отримав замовлення")
    print("Статус доставки: Замовлення передано кур'єру")
else:
    print("Замовлення не оплачено")
