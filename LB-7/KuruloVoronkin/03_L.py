from abc import ABC, abstractmethod


class Bird(ABC):
    @abstractmethod
    def move(self) -> None:
        pass


class FlyingBird(Bird):
    def fly(self) -> None:
        print("Flying...")

    def move(self) -> None:
        self.fly()


class Sparrow(FlyingBird):
    def fly(self) -> None:
        print("Sparrow is flying")


class Penguin(Bird):
    def swim(self) -> None:
        print("Penguin is swimming")

    def move(self) -> None:
        self.swim()


def make_bird_fly(bird: FlyingBird) -> None:
    bird.fly()


def make_bird_move(bird: Bird) -> None:
    bird.move()


if __name__ == "__main__":
    sparrow = Sparrow()
    penguin = Penguin()

    make_bird_fly(sparrow)

    birds: list[Bird] = [sparrow, penguin]
    for bird in birds:
        make_bird_move(bird)