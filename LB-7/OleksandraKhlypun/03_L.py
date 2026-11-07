class Bird:
    """Базовий птах: містить лише те, що вміють усі птахи."""

    def move(self):
        print("Bird is moving")


class FlyingBird(Bird):
    """Птах, який вміє літати."""

    def fly(self):
        print("Flying...")

    def move(self):
        self.fly()


class Sparrow(FlyingBird):
    def fly(self):
        print("Sparrow is flying")


class Penguin(Bird):
    """Пінгвін не літає, тому не успадковує fly()."""

    def swim(self):
        print("Penguin is swimming")

    def move(self):
        self.swim()


def make_bird_fly(bird: FlyingBird):
    bird.fly()


if __name__ == "__main__":
    flying_birds = [Sparrow(), FlyingBird()]
    for bird in flying_birds:
        make_bird_fly(bird)

    for bird in [Sparrow(), Penguin()]:
        bird.move()