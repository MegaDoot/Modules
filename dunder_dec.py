class Derivative(object):
    def __init__(self, num):
        self.num = num

def dry_create(cls, var_name, *funcs):
    for func in funcs:
        setattr(cls, func, lambda self, other: [print(f"Function {func} on self.{var_name}, other.{var_name}")])
    return cls

Derivative = dry_create(Derivative, "num", "foo")

test = Derivative(5)
