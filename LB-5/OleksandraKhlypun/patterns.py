from __future__ import annotations

import copy
import os
import pickle
from abc import ABC, ABCMeta, abstractmethod


class SingletonMeta(ABCMeta):
    _instances: dict = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Crust(ABC):
    name: str
    price: int


class ClassicCrust(Crust):
    name, price = "класичні бортики", 0


class CheeseCrust(Crust):
    name, price = "сирні бортики", 30


class Sauce(ABC):
    name: str
    price: int


class TomatoSauce(Sauce):
    name, price = "томатний соус", 10


class CreamySauce(Sauce):
    name, price = "вершковий соус", 15

class Pizza:
    BASE_PRICE = 100

    def __init__(self, name: str, crust: Crust, sauce: Sauce):
        self.name = name
        self.crust = crust
        self.sauce = sauce
        self.ingredients: list[tuple[str, int]] = []

    def clone(self) -> "Pizza":
        """Prototype: глибока копія піци разом з інгредієнтами."""
        return copy.deepcopy(self)

    @property
    def price(self) -> int:
        return (self.BASE_PRICE + self.crust.price + self.sauce.price
                + sum(p for _, p in self.ingredients))

    def __str__(self) -> str:
        ingr = ", ".join(n for n, _ in self.ingredients) or "—"
        return (f"Піца «{self.name}»\n"
                f"  Бортики:    {self.crust.name}\n"
                f"  Соус:       {self.sauce.name}\n"
                f"  Інгредієнти: {ingr}\n"
                f"  Ціна:       {self.price} грн")


class PizzaFactory(ABC, metaclass=SingletonMeta):
    @abstractmethod
    def create_crust(self) -> Crust: ...

    @abstractmethod
    def create_sauce(self) -> Sauce: ...


class ClassicPizzaFactory(PizzaFactory):
    def create_crust(self) -> Crust:
        return ClassicCrust()

    def create_sauce(self) -> Sauce:
        return TomatoSauce()


class CheeseCrustPizzaFactory(PizzaFactory):
    def create_crust(self) -> Crust:
        return CheeseCrust()

    def create_sauce(self) -> Sauce:
        return CreamySauce()


def choose_factory(with_cheese_crust: bool) -> PizzaFactory:
    """Abstract Factory обирає стратегію (кожна фабрика — Singleton)."""
    return CheeseCrustPizzaFactory() if with_cheese_crust else ClassicPizzaFactory()


EXTRA_INGREDIENTS = {
    "1": ("гриби", 15),
    "2": ("оливки", 12),
    "3": ("бекон", 25),
    "4": ("ананас", 18),
    "5": ("халапеньо", 10),
    "6": ("кукурудза", 10),
}


class PizzaBuilder:
    def __init__(self, factory: PizzaFactory):
        self._factory = factory
        self.reset()

    def reset(self) -> "PizzaBuilder":
        self._pizza = Pizza("Власна", self._factory.create_crust(),
                            self._factory.create_sauce())
        return self

    def set_name(self, name: str) -> "PizzaBuilder":
        self._pizza.name = name
        return self

    def add_ingredient(self, name: str, price: int) -> "PizzaBuilder":
        self._pizza.ingredients.append((name, price))
        return self

    def from_prototype(self, prototype: Pizza) -> "PizzaBuilder":
        """Старт будування з клону попередньої піци (Prototype).
        Бортики й соус беремо з поточної фабрики."""
        self._pizza = prototype.clone()
        self._pizza.crust = self._factory.create_crust()
        self._pizza.sauce = self._factory.create_sauce()
        return self

    def preview(self) -> Pizza:
        """Поточна (ще не завершена) піца — для виводу в консоль."""
        return self._pizza

    def build(self) -> Pizza:
        pizza = self._pizza
        self.reset()
        return pizza


class PizzaCreator(ABC):
    @abstractmethod
    def create_pizza(self, builder: PizzaBuilder) -> Pizza:
        """Factory Method"""


class MargheritaCreator(PizzaCreator):
    def create_pizza(self, builder: PizzaBuilder) -> Pizza:
        return (builder.set_name("Маргарита")
                .add_ingredient("моцарела", 20)
                .add_ingredient("базилік", 5)
                .build())


class PepperoniCreator(PizzaCreator):
    def create_pizza(self, builder: PizzaBuilder) -> Pizza:
        return (builder.set_name("Пепероні")
                .add_ingredient("моцарела", 20)
                .add_ingredient("пепероні", 30)
                .build())


class HawaiianCreator(PizzaCreator):
    def create_pizza(self, builder: PizzaBuilder) -> Pizza:
        return (builder.set_name("Гавайська")
                .add_ingredient("моцарела", 20)
                .add_ingredient("шинка", 25)
                .add_ingredient("ананас", 18)
                .build())


MENU = {
    "1": ("Маргарита", MargheritaCreator),
    "2": ("Пепероні", PepperoniCreator),
    "3": ("Гавайська", HawaiianCreator),
}


HISTORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "order_history.pkl")


def load_history() -> dict[str, Pizza]:
    try:
        with open(HISTORY_FILE, "rb") as f:
            return pickle.load(f)
    except Exception:
        return {}


def save_history() -> None:
    with open(HISTORY_FILE, "wb") as f:
        pickle.dump(order_history, f)


order_history: dict[str, Pizza] = load_history()


def ask_yes_no(question: str) -> bool:
    while True:
        ans = input(f"{question} (т/н): ").strip().lower()
        if ans in ("т", "так", "y", "yes"):
            return True
        if ans in ("н", "ні", "n", "no"):
            return False
        print("  Введіть «т» або «н».")


def ask_choice(options: dict, title: str) -> str:
    print(title)
    for key, val in options.items():
        label = val[0] if isinstance(val, tuple) else val
        print(f"  {key}. {label}")
    while True:
        choice = input("Ваш вибір: ").strip()
        if choice in options:
            return choice
        print("  Невірний вибір, спробуйте ще раз.")


def make_order() -> None:
    print("\n=== Нове замовлення ===")
    user = input("Крок 1. Ваше ім'я: ").strip() or "Гість"

    print("\nКрок 2. Вибір стратегії фабрики")
    cheese = ask_yes_no("Робимо піцу з сирними бортиками?")
    factory = choose_factory(cheese)
    print(f"  → Обрана фабрика: {type(factory).__name__}")
    print(f"  → Singleton працює: "
          f"{factory is choose_factory(cheese)} (той самий екземпляр)")

    builder = PizzaBuilder(factory)

    user_key = user.lower()
    previous = order_history.get(user_key)
    if previous:
        print(f"\nКрок 3. Знайдено ваше попереднє замовлення:\n{previous}")
    else:
        print("\nКрок 3. Попередніх замовлень для цього імені немає "
              "(історія зберігається за іменем).")
    if previous and ask_yes_no("Скопіювати його інгредієнти?"):
        builder.from_prototype(previous)
        builder.set_name(f"{previous.name} (повтор)")
        clone = builder.preview()
        print("\n  --- Prototype: клонування ---")
        print(f"  Оригінал: id={id(previous)}, "
              f"інгредієнти={[n for n, _ in previous.ingredients]}")
        print(f"  Копія:    id={id(clone)}, "
              f"інгредієнти={[n for n, _ in clone.ingredients]}")
        print(f"  Це різні об'єкти: {clone is not previous}")
        print(f"  Списки інгредієнтів незалежні: "
              f"{clone.ingredients is not previous.ingredients}")
        print(f"  Бортики/соус оновлено з нової фабрики: "
              f"{clone.crust.name}, {clone.sauce.name}")
        print("  -----------------------------")
    else:
        key = ask_choice(MENU, "\nКрок 3. Оберіть піцу з меню:")
        creator = MENU[key][1]()
        pizza = creator.create_pizza(builder)
        builder.from_prototype(pizza)
        print(f"  → Створено базову піцу «{pizza.name}» (Factory Method)")

    print("\nКрок 4. Додавання інгредієнтів (Builder)")
    while ask_yes_no("Додати ще інгредієнт?"):
        key = ask_choice(
            {k: f"{n} (+{p} грн)" for k, (n, p) in EXTRA_INGREDIENTS.items()},
            "Доступні інгредієнти:")
        name, price = EXTRA_INGREDIENTS[key]
        builder.add_ingredient(name, price)
        print(f"  → Додано: {name}")

    final_pizza = builder.build()
    order_history[user_key] = final_pizza
    save_history()

    print("\n=== Підсумок замовлення ===")
    print(f"Клієнт: {user}")
    print(final_pizza)
    print("===========================\n")


def main() -> None:
    print("Ласкаво просимо до піцерії!")
    while True:
        make_order()
        if not ask_yes_no("Зробити ще одне замовлення?"):
            print("Дякуємо! Смачного!")
            break


if __name__ == "__main__":
    main()