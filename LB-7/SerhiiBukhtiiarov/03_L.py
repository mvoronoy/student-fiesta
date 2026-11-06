#Розділив птахів на тих, що літають, і тих, що не літають,
# щоб уникнути виклику невластивих методів.

class Bird:
    pass

class FlyingBird(Bird):
    def fly(self):
        print("Flying...")

class Sparrow(FlyingBird):
    def fly(self):
        print("Sparrow is flying")

class Penguin(Bird):
    def swim(self):
        print("Penguin is swimming")

def make_bird_fly(bird: FlyingBird):
    bird.fly()

birds = [Sparrow()] # Пінгвіна сюди не додаємо, бо він не FlyingBird

for bird in birds:
    make_bird_fly(bird)
