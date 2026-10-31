import copy

class PizzaPrototype:
    def clone(self):
        return copy.deepcopy(self)


class Pizza(PizzaPrototype):
    def __init__(self):
        self.crust = "Звичайний"
        self.ingredients = []

    def __str__(self):
        return f"Піца ({self.crust} бортик), інгредієнти: {', '.join(self.ingredients) if self.ingredients else 'без нічого'}"

class PizzaBuilder:
    def __init__(self):
        self.pizza = Pizza()

    def set_crust(self, crust_type):
        self.pizza.crust = crust_type
        return self

    def add_ingredient(self, ingredient):
        self.pizza.ingredients.append(ingredient)
        return self

    def build(self):
        return self.pizza

class PizzaFactorySingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PizzaFactorySingleton, cls).__new__(cls)
        return cls._instance

    def create_order(self, with_cheese_crust=False):
        builder = PizzaBuilder()
        if with_cheese_crust:
            builder.set_crust("Сирний")
        else:
            builder.set_crust("Звичайний")
        return builder

if __name__ == "__main__":
    print("--- Створення нового замовлення ---")
    factory = PizzaFactorySingleton()

    builder1 = factory.create_order(with_cheese_crust=True)

    pizza1 = builder1.add_ingredient("Пепероні").add_ingredient("Гриби").add_ingredient("Оливки").build()
    print("Перше замовлення:", pizza1)

    print("\n--- Копіювання попереднього замовлення (Prototype) ---")
    pizza2 = pizza1.clone()
    pizza2.ingredients.append("Подвійний сир")
    print("Друге замовлення (копія першого + сир):", pizza2)

    print("\n--- Перевірка Singleton ---")
    factory2 = PizzaFactorySingleton()
    print("Чи фабрики ідентичні (Singleton)?", factory is factory2)