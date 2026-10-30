from abc import ABC, abstractmethod
import itertools
import copy

class CatOwner(ABC):
    def __init__(self, name, contact_number):
        self.name = name
        self.number = contact_number

class Cat(ABC):
    def __init__(self, name, gender):
         self.name = name
         self.gender = gender

class Dates(ABC):
    def __init__(self, arrival_date, due_date):
        self.arrival_date = arrival_date
        self.due_date = due_date

class Room(ABC):
    def __init__(self, room_number, room_type, availability_status):
        self.number = room_number
        self.type = room_type
        self.status = availability_status

class StandardRoom(Room):
     def __init__(self, room_number, availability_status='free'):
            super().__init__(room_number, 'standard', availability_status)

     def get_Room(self):
        return "Standard Room"

class QuietRoom(Room):
     def __init__(self, room_number, availability_status='free'):
            super().__init__(room_number, 'quiet', availability_status)

     def get_Room(self):
        return "Quiet Room"

class MealPlan:
    def __init__(self, meal_plan="Standard meal plan"):
        self.meal = meal_plan

class CheckUpPlan(ABC):
    def __init__(self, check_up):
        self.check = check_up

class StandardCheckUp(CheckUpPlan):
    def __init__(self):
        super().__init__("Standard checkups for male cats")

class ExtendedCheckUp(CheckUpPlan):
    def __init__(self):
        super().__init__("Extended checkups for female cats")

class AdditionalService:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class VetService(AdditionalService):
    pass


class GroomingService(AdditionalService):
    pass


class CatFactoryMethod(ABC):
    @abstractmethod
    def create_room(self, room_number, availability_status='free'):
        pass

    @abstractmethod
    def create_CheckUp(self):
        pass

    @abstractmethod
    def create_meal_plan(self):
        pass

class MaleCatFactory(CatFactoryMethod):
    def create_room(self,room_number, availability_status='free'): return StandardRoom(room_number, availability_status)
    def create_CheckUp(self): return StandardCheckUp()
    def create_meal_plan(self):
        return MealPlan()

    def create_check_up(self):
        return StandardCheckUp()

class FemaleCatFactory(CatFactoryMethod):
    def create_room(self, room_number, availability_status='free'): return QuietRoom(room_number, availability_status)
    def create_CheckUp(self): return ExtendedCheckUp()
    def create_meal_plan(self):
        return MealPlan()

    def create_check_up(self):
        return ExtendedCheckUp()

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class FactoryProvider(metaclass=SingletonMeta):
    def __init__(self):
        self._factories = {"male": MaleCatFactory(), "female": FemaleCatFactory()}

    def get_factory(self, gender):
        return self._factories[gender]

order_id = itertools.count(1)
class Order:
    def __init__(self):
        self.id = next(order_id)
        self.cat: Cat | None = None
        self.owner: CatOwner | None = None
        self.dates: Dates | None = None
        self.room: Room | None = None
        self.meal_plan: MealPlan | None = None
        self.checklist: CheckUpPlan | None = None
        self.services: list[AdditionalService] = []
        self.status = "new"

    def clone(self):
       new = copy.deepcopy(self)
       new.id = next(order_id)
       new.dates = None
       new.status = "new"
       return new


    def __str__(self):
        services = ", ".join(s.name for s in self.services) or "none"
        return (
            f"\nOrder #{self.id} for {self.cat.name}\n"
            f"\nCat Owner Info: Name #{self.owner.name} and phone number {self.owner.number}\n"
            f"\nDates: {self.dates.arrival_date} - {self.dates.due_date}\n"
            f"\n{self.room.get_Room()}; {self.meal_plan.meal}; \n"
            f"\n{self.checklist.check}\n"
            f"\nServices: {services}\n")

class OrderBuilder(ABC):
    @abstractmethod
    def check_availability(self):
        pass

    @abstractmethod
    def get_result(self):
        pass

    @abstractmethod
    def create_meal_plan(self, meal_plan):
        pass

class ServicesBuilder(OrderBuilder):
    def __init__(self, order):
        self._order = order

    def check_availability(self):
        return self._order.room.status == "free"

    def create_meal_plan(self, meal_plan):
        self._order.meal_plan = meal_plan
        return self

    def add_vet_service(self, service):
        self._order.services.append(service)
        return self

    def add_grooming_service(self, service):
        self._order.services.append(service)
        return self

    def get_result(self):
        return self._order


def ask_gender():
    while True:
        value = input("Cat gender (1 - male, 2 - female): ").strip()
        if value == "1":
            return "male"
        if value == "2":
            return "female"
        print("Choose 1 or 2.")


def add_services(builder):
    while True:
        print("\nAdd a service:")
        print("  1. Dental Care (230)")
        print("  2. Grooming (350)")
        print("  3. Close services menu")
        choice = input("Your choice: ").strip()
        if choice == "1":
            builder.add_vet_service(VetService("Dental Care", 400))
        elif choice == "2":
            builder.add_grooming_service(GroomingService("Grooming", 350))
        elif choice == "3":
            return
        else:
            print("Unknown option.")
            continue
        print("Service added.")


def create_new_order(provider, history):
    print("\nNew order")
    owner = CatOwner(input("Owner name: "), input("Owner phone: "))
    cat = Cat(input("Cat name: "), ask_gender())
    dates = Dates(input("Arrival date (Format: DD.MM.YYYY): "), input("Departure date (Format: DD.MM.YYYY): "))
    print(f"Step 1: cat info is collected: {cat.name} ({cat.gender})")

    factory = provider.get_factory(cat.gender)
    print(f"Step 2: factory is chosen by gender: {type(factory).__name__}")

    order = Order()
    order.owner = owner
    order.cat = cat
    order.dates = dates
    order.room = factory.create_room(int(input("Room number: ")))

    builder = ServicesBuilder(order)
    print("Step 3: room is available:", builder.check_availability())
    order.meal_plan = factory.create_meal_plan()
    order.checklist = factory.create_check_up()
    print("Step 4: room, meal plan and check-up are created by the factory")

    add_services(builder)
    order = builder.get_result()

    history.append(order)
    print("\nStep 5: order is created:\n" + str(order))


def repeat_order(history):
    print("\nRepeat previous order: ")
    name = input("Cat name: ").strip().lower()
    found = [o for o in history if o.cat.name.lower() == name]
    print("The previous order is found in the base: ")
    if not found:
        print("No previous order for this cat.")
        return

    new = found[-1].clone()
    new.dates = Dates(input("Arrival date: "), input("Departure date: "))
    print(f"Step 1: order #{found[-1].id} is cloned. New order #{new.id}")
    print("\nStep 2: new order is created:\n" + str(new))


def show_orders(history):
    print("\nAll orders:")
    if not history:
        print("No orders yet")
    for o in history:
        print(o)

def main():
    s1 = FactoryProvider()
    s2 = FactoryProvider()
    if id(s1) == id(s2):
        print("Singleton works, both variables contain the same instance.")
    else:
        print("Singleton failed, variables contain different instances.")

    history = []
    while True:
        print("\nCatel")
        print("1. Create new order")
        print("2. Repeat previous order (Prototype)")
        print("3. Show all orders")


        choice = input("Your choice: ").strip()
        if choice == "1":
            create_new_order(s1, history)
        elif choice == "2":
            repeat_order(history)
        elif choice == "3":
            show_orders(history)

if __name__ == "__main__":
    main()