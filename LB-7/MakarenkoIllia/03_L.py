#
#  Fix violation of  Liskov Substitution Principle (LSP)
# Objects of a superclass should be replaceable with objects of its subclasses without breaking program correctness.
#

class Bird:
    def eat(self):
        print(f"{self.__class__.__name__} is eating")


class FlyingBird(Bird):
    def fly(self):
        print(f"{self.__class__.__name__} is flying")


class Sparrow(FlyingBird):
    pass


class Penguin(Bird):
    def swim(self):
        print("Penguin is swimming")


def make_bird_fly(bird: FlyingBird):
    bird.fly()
