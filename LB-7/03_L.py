#
#  Fix violation of  Liskov Substitution Principle (LSP)
# Objects of a superclass should be replaceable with objects of its subclasses without breaking program correctness.
#

class Bird:
    def fly(self):
        print("Flying...")

class Sparrow(Bird):
    def fly(self):
        print("Sparrow is flying")

class Penguin(Bird):
    def fly(self):
        raise NotImplementedError("Penguins cannot fly")


def make_bird_fly(bird):
    bird.fly()


birds = [Sparrow(), Penguin()]

for bird in birds:
    make_bird_fly(bird)
