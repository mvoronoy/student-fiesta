# В оригінальному варіанті базовий клас Bird визначає метод fly().
# Клас Penguin успадковує Bird, але оскільки пінгвіни не літають, метод fly() викидає виняток NotImplementedError("Penguins cannot fly").
# Тобто функція make_bird_fly(bird), яка очікує будь-який об'єкт типу Bird, аварійно завершує роботу при передачі екземпляра Penguin.
# Нам потрібно, щоб об'єкти базового класу без проблем могли замінюватися об'єктами його підкласів без порушення коректності роботи програми.
# Для цього ієрархія птахів була розділена так, щоб базовий клас Bird містив лише спільну для всіх птахів поведінку, а здатність літати була винесена в окремий підклас FlyingBird.

from abc import ABC, abstractmethod

class Bird(ABC):
    @abstractmethod
    def move(self):
        pass

class FlyingBird(Bird):
    def fly(self):
        print("Flying...")

    def move(self):
        self.fly()

class Sparrow(FlyingBird):
    def fly(self):
        print("Sparrow is flying")

class Penguin(Bird):
    def swim(self):
        print("Penguin is swimming")

    def move(self):
        self.swim()

def make_bird_move(bird: Bird):
    bird.move()

def make_flying_bird_fly(bird: FlyingBird):
    bird.fly()
