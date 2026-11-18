"""LB-5: Породжувальні патерни на прикладі сервісу замовлення піци.

Abstract Factory, Singleton, Factory Method, Builder, Prototype.
Усі інтерфейси починаються з літери K.
"""
import copy
from abc import ABC, ABCMeta, abstractmethod


# =====================================================================
# SINGLETON: метаклас, який дозволяє створити лише один екземпляр класу
# =====================================================================
class SingletonMeta(ABCMeta):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


# =====================================================================
# ABSTRACT FACTORY: родина продуктів "борт піци"
# =====================================================================
class KCrust(ABC):
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def price(self) -> float: ...


class ClassicCrust(KCrust):
    def name(self) -> str:
        return "звичайний борт"

    def price(self) -> float:
        return 0.0


class CheesyCrust(KCrust):
    def name(self) -> str:
        return "сирний борт"

    def price(self) -> float:
        return 40.0


class KPizzaFactory(ABC):
    @abstractmethod
    def create_crust(self) -> KCrust: ...

    @abstractmethod
    def title(self) -> str: ...


class ClassicPizzaFactory(KPizzaFactory, metaclass=SingletonMeta):
    def create_crust(self) -> KCrust:
        return ClassicCrust()

    def title(self) -> str:
        return "Фабрика звичайної піци"


class CheesyPizzaFactory(KPizzaFactory, metaclass=SingletonMeta):
    def create_crust(self) -> KCrust:
        return CheesyCrust()

    def title(self) -> str:
        return "Фабрика піци з сирним бортом"


def choose_factory(cheesy_crust: bool) -> KPizzaFactory:
    """Abstract Factory обирає стратегію: сирний борт чи ні."""
    return CheesyPizzaFactory() if cheesy_crust else ClassicPizzaFactory()


# =====================================================================
# PROTOTYPE: піца вміє клонувати себе
# =====================================================================
class KCloneable(ABC):
    @abstractmethod
    def clone(self): ...


class Pizza(KCloneable):
    BASE_PRICE = 150.0
    INGREDIENT_PRICE = 20.0

    def __init__(self, crust: KCrust):
        self.crust = crust
        self.ingredients = []

    def clone(self) -> "Pizza":
        return copy.deepcopy(self)

    def price(self) -> float:
        return (self.BASE_PRICE + self.crust.price()
                + self.INGREDIENT_PRICE * len(self.ingredients))

    def __str__(self) -> str:
        return (f"Піца: {self.crust.name()}, інгредієнти: "
                f"{', '.join(self.ingredients)} | ціна: {self.price()} грн")


# =====================================================================
# BUILDER: покрокове додавання інгредієнтів
# =====================================================================
class KPizzaBuilder(ABC):
    @abstractmethod
    def add_ingredient(self, ingredient: str) -> "KPizzaBuilder": ...

    @abstractmethod
    def build(self) -> Pizza: ...


class PizzaBuilder(KPizzaBuilder):
    def __init__(self, pizza: Pizza):
        self._pizza = pizza

    @classmethod
    def from_crust(cls, crust: KCrust) -> "PizzaBuilder":
        return cls(Pizza(crust))

    def add_ingredient(self, ingredient: str) -> "PizzaBuilder":
        self._pizza.ingredients.append(ingredient)
        print(f"  [Builder] додано: {ingredient}")
        return self

    def build(self) -> Pizza:
        return self._pizza


# =====================================================================
# FACTORY METHOD: створення доставки
# =====================================================================
class KDelivery(ABC):
    @abstractmethod
    def describe(self) -> str: ...

    @abstractmethod
    def cost(self) -> float: ...


class CourierDelivery(KDelivery):
    def __init__(self, address: str):
        self._address = address

    def describe(self) -> str:
        return f"кур'єр за адресою {self._address}"

    def cost(self) -> float:
        return 50.0


class PickupDelivery(KDelivery):
    def describe(self) -> str:
        return "самовивіз"

    def cost(self) -> float:
        return 0.0


class KDeliveryCreator(ABC):
    @abstractmethod
    def create_delivery(self) -> KDelivery:  # Factory Method
        ...


class CourierCreator(KDeliveryCreator):
    def __init__(self, address: str):
        self._address = address

    def create_delivery(self) -> KDelivery:
        return CourierDelivery(self._address)


class PickupCreator(KDeliveryCreator):
    def create_delivery(self) -> KDelivery:
        return PickupDelivery()


# =====================================================================
# Замовлення
# =====================================================================
class Order:
    def __init__(self, order_id: int, pizza: Pizza, delivery: KDelivery):
        self.order_id = order_id
        self.pizza = pizza
        self.delivery = delivery

    def total(self) -> float:
        return self.pizza.price() + self.delivery.cost()

    def print(self) -> None:
        print(f"\n===== ЗАМОВЛЕННЯ №{self.order_id} =====")
        print(f"  {self.pizza}")
        print(f"  Доставка: {self.delivery.describe()} ({self.delivery.cost()} грн)")
        print(f"  РАЗОМ: {self.total()} грн")
        print("=========================")


# =====================================================================
# MAIN
# =====================================================================
def main() -> None:
    # ---------- Замовлення 1: нове ----------
    print("КРОК 1. Нове замовлення")

    print("КРОК 1.1. Abstract Factory + Singleton: клієнт хоче сирний борт")
    factory = choose_factory(True)
    print(f"  Обрано: {factory.title()}")
    print(f"  Той самий екземпляр при повторному виклику? "
          f"{'так' if factory is choose_factory(True) else 'ні'}")

    print("КРОК 1.2. Builder: додаємо інгредієнти")
    builder = PizzaBuilder.from_crust(factory.create_crust())
    builder.add_ingredient("моцарела") \
           .add_ingredient("пепероні") \
           .add_ingredient("гриби")

    print("КРОК 1.3. Factory Method: доставка кур'єром")
    courier_creator = CourierCreator("Київ, вул. Хрещатик, 1")

    first = Order(1, builder.build(), courier_creator.create_delivery())
    first.print()

    # ---------- Замовлення 2: повтор попереднього ----------
    print("\nКРОК 2. Повтор попереднього замовлення")

    print("КРОК 2.1. Prototype: клонуємо попередню піцу")
    pizza_copy = first.pizza.clone()

    print("КРОК 2.2. Builder: додаємо ще один інгредієнт до копії")
    builder2 = PizzaBuilder(pizza_copy)
    builder2.add_ingredient("оливки")

    print("КРОК 2.3. Factory Method: цього разу самовивіз")
    pickup_creator = PickupCreator()

    second = Order(2, builder2.build(), pickup_creator.create_delivery())
    second.print()

    print("\nПерше замовлення не змінилося:")
    first.print()


if __name__ == "__main__":
    main()