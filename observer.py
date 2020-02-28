class Subject:
    """
    important to note that objects that inherit from this class
    will have state, that will then be passed to the 'notify_observers'
    method in the event that this state mutates.
    """
    def __init__(self):
        self.observers = set()

    def register_observer(self, observer):
        self.observers.add(observer)

    def remove_observer(self, observer):
        try:
            self.observers.remove(observer)
        except KeyError:
            print("observer not present")  # TODO change this

    def notify_observers(self, **values):
        """
        :param values: series of keyword arguments so that it is clear what values are being represented
        :return: none
        """
        for observer in self.observers:
            observer.update(values)


class Observer:
    def __init__(self, subject):
        self.subject = subject
        self.subject.register_observer(self)

    def update(self, values):
        """
        children of this class need to override this method.
        'values' parameter will be a dictionary.
        """
        pass

########################################################################################################################
# BELOW IS A CALCULATOR EXAMPLE USING THESE CONCEPTS
########################################################################################################################


class Calculator(Subject):
    def __init__(self):
        super().__init__()
        self.state = 0

    def add(self, *values):
        self.state = self.state + sum(values)
        self.notify_observers(state=self.state)

    def subtract(self, *values):
        for val in values:
            self.state -= val
        self.notify_observers(state=self.state)

    def clear(self):
        self.state = 0
        self.notify_observers(state=self.state)


class Foo(Observer):
    """
    for illustrative purposes, this is some class that
    needs to be aware of changes in Calc's state
    """
    def __init__(self, subject):
        """
        remember we pass a reference to the subject so that
        we can register this observer to that subject when this
        observer is instantiated.
        """
        super().__init__(subject)
        self.state = 0

    def update(self, values):
        self.state = values["state"]


class CommandLineInterfaceLoop:
    def __init__(self):
        self.contents = Calculator()
        self.observer1 = Foo(self.contents)
        self.observer2 = Foo(self.contents)
        self.buffer = ""

    def parse_buffer(self):
        nums = []
        for word in self.buffer.split(" "):
            try:
                nums.append(int(word))
            except:
                pass
        if "exit" in self.buffer.split(" "):
            return 0
        elif "add" in self.buffer.split(" "):
            self.contents.add(*nums)
            return 1
        elif "subtract" in self.buffer.split(" "):
            self.contents.subtract(*nums)
            return 1
        elif "clear" in self.buffer.split(" "):
            self.contents.clear()
            return 1
        else:
            return 2

    def main_loop(self):
        self.buffer = input("type something in lowercase to add/subtract")
        result = self.parse_buffer()
        if result == 0:
            print("exiting calc app")
            exit()
        elif result == 1:
            print(f"calc state is now {self.contents.state}")
            print(f"obs1 state is now {self.observer1.state}")
            print(f"obs2 state is now {self.observer2.state}")
            self.main_loop()
        elif result == 2:
            print(f"error in parsing. buffer is \n{self.buffer}")
            self.main_loop()

if __name__ == "__main__":
    myloop = CommandLineInterfaceLoop()
    myloop.main_loop()