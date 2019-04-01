"""
Alex Scorza 2019
"""

from inspect import signature as sig

__all__ = ("add_func",)

SPECIAL = {"__getitem__": (False,), "__setitem__": (False, False)}
#False: use value, True: use getattr(, var_name)

binary_operations = ("__add__", "__mul__", "____")

def _dunders(obj): #Lists all dunder methods of an object
    return tuple(filter(lambda func: func.startswith("__") and func.endswith("__"), dir(obj)))

def _mapper(this, func, var_name, *others):
    right_same = func[2]
    true_false = SPECIAL.get(func, (True,)) #Defaults to (True,) if not special
    arg_amount = _find_args(getattr(getattr(this, var_name), func)) #Number of arguments expected
    if len(true_false) < arg_amount: #If too few amount entered (ignores extra arguments)
        if func in SPECIAL.keys():
            raise DunderArgsError("Wrong number of values for {}, expected {}, got {} -> {}".format(func, arg_amount, len(true_false), others))
        else:
            raise NotImplementedError("Special magic method {} not recognised as special: {} (author's fault)".format(func, tuple(SPECIAL.keys())))
    args = []
    for i in range(len(others)):
        if true_false[i]: #== True
            args.append(getattr(others[i], var_name)) #i.e. CustomClass.num
        else:
            args.append(others[i]) #i.e. 5
    return tuple(args)
    

def _find_args(func):
    try:
        return len(sig(func).parameters)
    except ValueError:
        raise NoSignatureError("Function '{}' does not have a signature so the number of arguments required is not known".format(func))
  
def _make_func(this, func:str, var_name:str, *others) -> "function": #__add__, num
    function = getattr(getattr(this, var_name), func) #Retrive function to use dunder method: this.var_name.func
    args_num = _find_args(function) #Number of extra arguments taken (i.e. __add__ would be 1, __iter__ would be 0)
    mapped = _mapper(this, func, var_name, *others)
    return function(*mapped)

class DunderArgsError(TypeError): #Custom exception
    pass

class NoSignatureError(ValueError):
    pass

class add_methods(object):
    def __init__(self, var_name:str, *funcs:str, wrapper = lambda value: value):
        self.var_name = var_name
        self.funcs = funcs
        self.wrapper = wrapper
    
    def __call__(self, cls):
        class Decorated(cls):
            for func in self.funcs:
                setattr(cls, func, lambda this, *others, func = func: _make_func(this, func, self.var_name, *others))
                #i.e. self.num.__add__(other.num)
                #Note that 'this' is used to distinguish from 'self' defined in the class
        Decorated.__name__ = cls.__name__
        return Decorated

if __name__ == "__main__":
    @add_methods("num", "__add__", "__mul__") #"__add__" -> def __add__(self, other): return self.num + other.num
    @add_methods("array", "__setitem__", "__iter__", "__len__", "__setitem__") #"__iter__": def __iter__(self): for i in self.array: yield i
    @add_methods("string", "__getitem__")
    class Derivative(object):
        def __init__(self, num, array, string):
            self.num = num
            self.array = array
            self.string = string

    test1 = Derivative(2, [1, 2, 3], "hello")
    test2 = Derivative(3, [1, 3, 3, 7], "hi")
    print(test1 + test2)
    print(test1 * test2)
    print(len(test2))
    print(test2[-1])
    print("Before:", list(test1))
    test1.__setitem__(0, 100)
    print("After:", list(test1))
