from abc import abstractclassmethod, ABC
class FlyingBirds(ABC):
    @abstractclassmethod
    def fly(self):
        pass

class Sparrow(FlyingBirds):
    def fly(self):
        print("Sparrow is flying")

class Pengiun:
    pass

def make_bird_fly(bird : FlyingBirds):
    bird.fly()

birds = [Sparrow()]
for bird in birds:
    make_bird_fly(bird)