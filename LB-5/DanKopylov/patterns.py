from abc import ABC, abstractmethod
from copy import deepcopy


# =========================
# Product + Prototype
# =========================

class Shawarma:
    def __init__(self, size, lavash, base_price):
        self.size = size
        self.lavash = lavash
        self.ingredients = []
        self.price = base_price
        self.delivery_address = ""
        self.status = "Створено"

    def clone(self):
        return deepcopy(self)

    def show(self):
        print("\n=== Ваше замовлення ===")
        print(f"Розмір: {self.size}")
        print(f"Лаваш: {self.lavash}")
        print("Інгредієнти:", ", ".join(self.ingredients))
        print(f"Адреса доставки: {self.delivery_address}")
        print(f"Вартість: {self.price} грн")
        print(f"Статус: {self.status}")


# =========================
# Builder
# =========================

class ShawarmaBuilder:
    def __init__(self, shawarma):
        self.shawarma = shawarma

    def add_ingredient(self, name, price):
        self.shawarma.ingredients.append(name)
        self.shawarma.price += price
        return self

    def set_delivery_address(self, address):
        self.shawarma.delivery_address = address
        return self

    def build(self):
        return self.shawarma


# =========================
# Abstract Factory
# =========================

class ShawarmaFactory(ABC):

    @abstractmethod
    def create_shawarma(self):
        pass


class RegularShawarmaFactory(ShawarmaFactory):

    def create_shawarma(self):
        return Shawarma(
            size="Звичайна",
            lavash="Класичний",
            base_price=120
        )


class LargeShawarmaFactory(ShawarmaFactory):

    def create_shawarma(self):
        return Shawarma(
            size="Велика",
            lavash="Великий",
            base_price=160
        )


# =========================
# Singleton
# =========================

class FactoryManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_factory(self, choice):
        if choice == "2":
            return LargeShawarmaFactory()

        return RegularShawarmaFactory()


# =========================
# Factory Method
# =========================

class OrderCreator:

    def create_order(self, factory):
        return factory.create_shawarma()


# =========================
# Main program
# =========================

ingredients_menu = {
    "1": ("Курка", 35),
    "2": ("Помідор", 15),
    "3": ("Огірок", 15),
    "4": ("Сир", 25),
    "5": ("Часниковий соус", 20),
}


print("=== FOOD DELIVERY ===")

print("\nОберіть розмір шаурми:")
print("1 - Звичайна (120 грн)")
print("2 - Велика (160 грн)")

size_choice = input("Ваш вибір: ")

# Singleton
manager = FactoryManager()

# Abstract Factory
factory = manager.get_factory(size_choice)

# Factory Method
creator = OrderCreator()
shawarma = creator.create_order(factory)

# Builder
builder = ShawarmaBuilder(shawarma)

print("\nДодайте інгредієнти:")
for key, value in ingredients_menu.items():
    print(f"{key} - {value[0]} (+{value[1]} грн)")
print("0 - Завершити")

while True:
    choice = input("Ваш вибір: ")

    if choice == "0":
        break

    if choice in ingredients_menu:
        name, price = ingredients_menu[choice]
        builder.add_ingredient(name, price)
        print("Додано:", name)
    else:
        print("Невірний вибір")


address = input("\nВведіть адресу доставки: ")
builder.set_delivery_address(address)

order = builder.build()

order.show()


# =========================
# Prototype
# =========================

repeat = input("\nПовторити це замовлення? (так/ні): ").lower()

if repeat == "так":
    copied_order = order.clone()

    print("\nЗамовлення скопійовано через Prototype")

    new_address = input("Введіть нову адресу доставки: ")
    copied_order.delivery_address = new_address

    copied_order.show()


# =========================
# Payment
# =========================

pay = input("\nОплатити замовлення? (так/ні): ").lower()

if pay == "так":
    order.status = "Оплачено"
    print("\nОплата успішна")
    print("Статус: Замовлення готується")
else:
    order.status = "Не оплачено"
    print("\nЗамовлення не оплачено")