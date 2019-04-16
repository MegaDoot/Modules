import dunderdec


##########################################################################################
@dunderdec.add_methods("__main__.Foo: obj.num", "__add__", "__sub__")
class Foo:
    def __init__(self):
        self.num = 5
print(repr(Foo() + Foo()))


##########################################################################################
@dunderdec.add_methods("__main__.Foo: int(obj.num)", "__add__", "__sub__", wrapper = str)
class Foo:
    def __init__(self):
        self.num = "5"
print(repr(Foo() + Foo()))


##########################################################################################
class Foo:
    def __init__(self):
        self.num = "5"
        
    def __add__(self, other):
        return str(int(self.num) + int(other.num))
        
    def __mul__(self, other):
        return str(int(self.num) * int(other.num))
        
    def __sub__(self, other):
        return str(int(self.num) - int(other.num))
        
    def __floordiv__(self, other):
        return str(int(self.num) // int(other.num))
print(repr(Foo() + Foo()))
##########################################################################################
@dunderdec.add_methods("__main__.Foo: float(obj.num); float, int: obj", "__add__", "__radd__")
class Foo:
    def __init__(self):
        self.num = 5
print(repr(Foo() + 1), repr(Foo() + Foo()), repr(3 + Foo()))
