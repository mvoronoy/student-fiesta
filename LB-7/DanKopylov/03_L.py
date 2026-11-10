class Bird:
    def move(self):
        print("Bird is moving")


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


def make_bird_fly(bird: FlyingBird):
    bird.fly()


if __name__ == "__main__":
    sparrow = Sparrow()
    penguin = Penguin()

    make_bird_fly(sparrow)

    sparrow.move()
    penguin.move()