class Bird:
    def eat(self):
        print("Bird is eating")

class FlyingBird(Bird):
    def fly(self):
        print("Flying...")

class NonFlyingBird(Bird):
    def walk(self):
        print("Walking...")

class Sparrow(FlyingBird):
    def fly(self):
        print("Sparrow is flying")

class Penguin(NonFlyingBird):
    def walk(self):
        print("Penguin is walking")

def make_bird_fly(bird):
    bird.fly()

if __name__ == "__main__":
    birds = [Sparrow(), Penguin()]

    for bird in birds:
        bird.eat()

        if isinstance(bird, FlyingBird):
            make_bird_fly(bird)
        else:
            bird.walk()