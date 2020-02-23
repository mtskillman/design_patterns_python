class Vehicle:
    '''
    the essence of what is going here, is that, implementation of the 'move' method is not yet decided, but
    an interface for it is provided.
    '''
    def __init__(self, behavior):
        self.behavior = behavior

    def move(self):
        self.behavior()


class Car(Vehicle):
    def honk(self):
        print('honk')


class Plane(Vehicle):
    pass


if __name__ == "__main__":
    for Foo in [Car(lambda: print("drive")), Plane(lambda: print("fly"))]:
        Foo.move()
        if isinstance(Foo, Car):
            Foo.honk()
