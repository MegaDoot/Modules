def dry_create(var_name, *funcs):
    def cls_decorator(cls):
        def cls_wrapper(*args, **kwargs):
            cls.bar = lambda self: type(self)
##            for func in funcs:
##                print(func)
##                setattr(cls, func, lambda self, other, func = func: ["Using " + func, getattr(getattr(self, var_name), func)(getattr(other, var_name))])
                #i.e. self.num.__add__(other.num)
            return cls
        return cls_wrapper
    return cls_decorator

def add_foo(value = "Hello"):
    def decorator(cls):
        def wrapper(*args, **kwargs):
            cls.foo = value
            return cls
        return wrapper
    return decorator

##@dry_create("num", "__mul__", "__add__")
@add_foo("G'day")
class Derivative(object):
    def __init__(self, num):
        self.num = num

if __name__ == "__main__":
  import inspect
##  Derivative = dry_create(Derivative, "num", "__mul__", "__add__")

  test1 = Derivative(2)
  test2 = Derivative(3)
  print(test1 + test2)
  print(test1 * test2)

##  print(inspect.getsource(test1.__sub__))
