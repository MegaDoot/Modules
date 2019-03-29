import functools

class add_func(object):
    def __init__(self, var_name, *funcs):
        self.var_name = var_name
        self.funcs = funcs
    
    def __call__(self, cls):
        class Decorated(cls):
            for func in self.funcs:
                print(func)
                setattr(cls, func, lambda this, other, func = func: getattr(getattr(this, self.var_name), func)(getattr(other, self.var_name)))
                #i.e. self.num.__add__(other.num)
                #Note that 'this' is used to distinguish from 'self' defined in the class
        Decorated.__name__ = cls.__name__
        return Decorated
    

@add_func("num", "__add__", "__mul__")
class Derivative(object):
    def __init__(self, num):
        self.num = num

if __name__ == "__main__":
    test1 = Derivative(2)
    test2 = Derivative(3)
    print(test1 + test2)
    print(test1 * test2)
