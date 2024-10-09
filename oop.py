class Vehicle:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model

    def move(self):
        print("Move!")


class Car(Vehicle):
    pass


class Boat(Vehicle):
    def move(self):
        print("Sail!")


class Plane(Vehicle):
    def move(self):
        print("Fly!")

    def fly(self):
        print("only plane can fly")


car1 = Car("Ford", "Mustang")  # Create a Car object
boat1 = Boat("Ibiza", "Touring 20")  # Create a Boat object
plane1 = Plane("Boeing", "747")  # Create a Plane object

for x in (car1, boat1, plane1):
    x.__class__ = Vehicle
    print(x.__class__)
    print(x.brand)
    print(x.move())
    x.move()


def fact(n):
    if n <= 1:
        return 1
    else:
        return n * fact(n - 1)


print(fact(5))
print(fact(0))
