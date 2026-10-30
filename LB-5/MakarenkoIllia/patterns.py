class Pizza:
    def __init__(self, crust):
        self.crust = crust
        self.ingredients = []
    def clone(self):
        new_pizza = Pizza(self.crust)
        new_pizza.ingredients = self.ingredients.copy()
        return new_pizza
    def __str__(self):
        return "Піца [" + self.crust + "]: " + ", ".join(self.ingredients)

class Singleton:
    instances = {}
    def __new__(cls):
        if cls not in Singleton.instances:
            Singleton.instances[cls] = super().__new__(cls)
        return Singleton.instances[cls]

class PizzaFactory(Singleton):
    def create_pizza(self):
        pass

class SimpleFactory(PizzaFactory):
    def create_pizza(self):
        return Pizza("Звичайний бортик")

class CheeseFactory(PizzaFactory):
    def create_pizza(self):
        return Pizza("Сирний бортик")

class PizzaBuilder:
    def __init__(self, pizza):
        self.pizza = pizza
    def add(self, ingredient):
        self.pizza.ingredients.append(ingredient)
        return self
    def build(self):
        return self.pizza

last_order = None

def make_order():
    global last_order

    if last_order is not None:
        print("Є попереднє замовлення, копіюю його")
        pizza = last_order.clone()
    else:
        answer = input("Сирний бортик? (y/n): ")
        if answer == "y":
            factory = CheeseFactory()
        else:
            factory = SimpleFactory()
        pizza = factory.create_pizza()

    builder = PizzaBuilder(pizza)
    print("Додайте інгредієнти (порожній рядок - кінець):")
    while True:
        item = input("> ")
        if item == "":
            break
        builder.add(item)

    last_order = builder.build()
    return last_order

while True:
    print("\n--- Нове замовлення ---")
    print(make_order())
    again = input("\nЗамовити ще? (y/n): ")
    if again != "y":
        break