class Derivative(object):
    def __init__(self, num):
        self.num = num
    
    def mul(self, other):
        return self.num * other.num

def dry_create(cls, var_name, *funcs):
    for func in funcs:
        print(func)
        setattr(cls, func, lambda self, other: getattr(getattr(self, var_name), func)(getattr(other, var_name)))
        #i.e. self.num.__add__(other.num)
    return cls

Derivative = dry_create(Derivative, "num", "__sub__", "__mul__")

test1 = Derivative(2)
test2 = Derivative(3)
print(test1 - test2)
