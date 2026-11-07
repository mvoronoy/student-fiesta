
class Bird:
    def move(self):
        print("Moving...")

class FlyingBird(Bird):
    def fly(self):
        print("Flying...")

class Sparrow(FlyingBird):
    def fly(self):
        print("Sparrow is flying")

class Penguin(Bird):
    def move(self):
        print("Penguin is swimming or walking")

def make_bird_fly(bird: FlyingBird):
    bird.fly()

birds = [Sparrow()]

for bird in birds:
    make_bird_fly(bird)