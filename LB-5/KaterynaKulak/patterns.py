import copy
import time
import random
from datetime import datetime

class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

#prototype
class Pizza:
    def __init__(self):
        self.size = ""
        self.border = ""
        self.ingredients = []
        self.base_price = 0
        self.border_price = 0
        self.ingredients_price = 0

    def clone(self):
        return copy.deepcopy(self)

    @property
    def total_price(self):
        return self.base_price + self.border_price + self.ingredients_price

    def __str__(self):
        ings = ", ".join(self.ingredients) if self.ingredients else "без додатків"
        return (f"Піца: {self.size}\n"
                f"Бортик: {self.border}\n"
                f"Інгредієнти: {ings}\n"
                f"-----------------------\n"
                f"Загальна вартість: {self.total_price} грн.")


class PizzaBuilder:
    def __init__(self, pizza=None):
        self.pizza = pizza if pizza else Pizza()

    def set_size(self, name, price):
        self.pizza.size = name
        self.pizza.base_price = price
        return self

    def set_border(self, name, price):
        self.pizza.border = name
        self.pizza.border_price = price
        return self

    def add_ingredient(self, name, price):
        self.pizza.ingredients.append(name)
        self.pizza.ingredients_price += price
        return self

    def get_result(self):
        return self.pizza

class PizzeriaFactory(metaclass=SingletonMeta):
    def __init__(self):
        self.sizes = {
            "1": ("Маленька", 150),
            "2": ("Середня", 200),
            "3": ("Велика", 250)
        }
        self.borders = {
            "1": ("Звичайний", 0),
            "2": ("Сирний", 50),
            "3": ("З чорним кунжутом", 40)
        }
        self.ingredients_menu = {
            "1": ("Пепероні", 30),
            "2": ("Гриби", 20),
            "3": ("Томати", 15),
            "4": ("Халапеньйо", 25),
            "5": ("Подвійний сир", 35)
        }
        self.favorite_pizza = None

    def create_builder(self, size_id, border_id):
        builder = PizzaBuilder()
        s_name, s_price = self.sizes.get(size_id, self.sizes["2"])
        b_name, b_price = self.borders.get(border_id, self.borders["1"])

        builder.set_size(s_name, s_price)
        builder.set_border(b_name, b_price)
        return builder

    def save_favorite(self, pizza):
        self.favorite_pizza = pizza

    def get_favorite_clone(self):
        return self.favorite_pizza.clone() if self.favorite_pizza else None


def save_to_history(pizza):
    filename = "order_history.txt"
    timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    with open(filename, "a", encoding="utf-8") as file:
        file.write(f"[{timestamp}]\n")
        file.write(str(pizza) + "\n")
        file.write("="*30 + "\n\n")

    print(f"Чек збережено у файл {filename}")

def clear_screen():
    print("\n" * 2)

def interactive_order():
    pizzeria = PizzeriaFactory()

    while True:
        clear_screen()
        print(" ВІТАЄМО В ПІЦЕРІЇ ")

        if pizzeria.favorite_pizza:
            print("\nУ вас є збережене 'Улюблене замовлення':")
            print(f"{pizzeria.favorite_pizza.size}, {pizzeria.favorite_pizza.border} бортик, {len(pizzeria.favorite_pizza.ingredients)} додатків.")
            choice = input("Бажаєте повторити його? (так/ні): ").strip().lower()
            if choice == "так":
                pizza = pizzeria.get_favorite_clone()
                print("\nЗамовлення успішно зклоновано!")
                finish_order(pizza)
                break

        print("\nОберіть розмір піци:")
        for key, (name, price) in pizzeria.sizes.items():
            print(f"{key}. {name} ({price} грн)")
        size_choice = input("Ваш вибір: ").strip()

        print("\nОберіть бортик:")
        for key, (name, price) in pizzeria.borders.items():
            print(f"{key}. {name} (+{price} грн)")
        border_choice = input("Ваш вибір: ").strip()

        builder = pizzeria.create_builder(size_choice, border_choice)

        print("\nДодайте інгредієнти (введіть номер, або 0 щоб завершити):")
        for key, (name, price) in pizzeria.ingredients_menu.items():
            print(f"{key}. {name} (+{price} грн)")

        while True:
            ing_choice = input("Ваш вибір: ").strip()
            if ing_choice == "0":
                break

            if ing_choice in pizzeria.ingredients_menu:
                ing_name, ing_price = pizzeria.ingredients_menu[ing_choice]
                builder.add_ingredient(ing_name, ing_price)
                print(f"+ : {ing_name}")
            else:
                print("unknown code try again.")

        pizza = builder.get_result()

        print("\nВАШЕ ЗАМОВЛЕННЯ")
        print(pizza)

        confirm = input("\nПідтвердити замовлення? (так/ні): ").strip().lower()
        if confirm == "так":
            save = input("Зберегти як улюблене для швидкого замовлення наступного разу? (так/ні): ").strip().lower()
            if save == "так":
                pizzeria.save_favorite(pizza)
                print("Збережено в улюблені!")

            finish_order(pizza)

            again = input("\nБажаєте зробити ще одне замовлення прямо зараз? (так/ні): ").strip().lower()
            if again != "так":
                break
        else:
            print("\nЗамовлення скасовано. Спробуємо ще раз!")

def finish_order(pizza):
    couriers = ["В'ячеслав", "Тетяна", "Настя", "Денджі", "Фрірен"]
    print("\nДякуємо! Відправляємо чек на кухню...")
    time.sleep(1)

    save_to_history(pizza)

    print("Ваша піца вже в печі.")
    time.sleep(1.5)
    print(f"Кур'єр {random.choice(couriers)} забрав замовлення і вже мчить до вас!")

if __name__ == "__main__":
    interactive_order()