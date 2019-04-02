"""
Alex Scorza 2019

Documentation:

Add a decorator before the function -

(Code Example 1)
-----------
    @dunderdec.add_func(lambda obj: obj.num, "__add__", "__sub__", wrapper = float)
    class Foo:
        def __init__(self):
            self.num = 5
-----------

This gets the class and adds each of the specified magic methods. An unlimited amount is allowed
The lambda at the starts specifies which attribute of the class to get. However, in this case,
' lambda obj: obj.num ' can be changed to ' "num" ' and will be converted to a function automatically:

(Code Example 2)
-----------
    @dunderdec.add_func("num", "__add__", "__sub__", wrapper = float)
    class Foo:
        def __init__(self):
            self.num = 5
-----------

The wrapper is the function that is done on the return value of a function.

(Code Example 3)
-----------
    @dunderdec.add_func(lambda obj: int(obj.num), "__add__", "__mul__", "__sub__", wrapper = str)
    class Foo:
        def __init__(self):
            self.num = "5"
-----------

Here, the value of num is always a string so it is converted to an integer, the calculations are done
and the result is converted back into a string, so "5" + "6" would become "11" in this case, despite
being strings. A lambda must be used in this case as a function, ' int ', is done on the values. 

The equivalent of the code above/code example 3 done normally:
-----------
    class Foo:
        def __init__(self):
            self.num = "5"

        def __add__(self, other):
            return str(int(self.num) + int(self.other))

        def __mul__(self, other):
            return str(int(self.num) * int(self.other))

        def __sub__(self, other):
            return str(int(self.num) - int(self.other))
-----------

The more dunder methods used, the more concise and 'dry' the code becomes.
"""

from inspect import signature as sig

__all__ = ("add_func", "BIN_OPERS", "IBIN_OPERS")

SPECIAL = {"__getitem__": (False,), "__setitem__": (False, False)}
#False: use value, True: use getattr(, variable name)

BIN_OPERS = ("__add__", "__mul__", "__div__", "__truediv__", "__sub__")
IBIN_OPERS = tuple(map(lambda func: "__i" + func[2:], BIN_OPERS))

def _dunders(obj): #Lists all dunder methods of an object
    return tuple(filter(lambda func: func.startswith("__") and func.endswith("__"), dir(obj)))

def _mapper(this, func, var_func, *others):
    true_false = SPECIAL.get(func, (True,)) #Defaults to (True,) if not special
    function = getattr(var_func(this), func)
    arg_amount = _find_args(function) #Number of arguments expected
    if len(true_false) < arg_amount: #If too few amount entered (ignores extra arguments)
        if func in SPECIAL.keys():
            raise DunderArgsError("Wrong number of values for {}, expected {}, got {} -> {}".format(func, arg_amount, len(true_false), others))
        else:
            raise NotImplementedError("Special magic method {} not recognised as special: {} (author's fault)".format(func, tuple(SPECIAL.keys())))
    args = []
    for i in range(len(others)):
        if true_false[i]: #== True
            args.append(var_func(others[i])) #i.e. CustomClass.num
        else:
            args.append(others[i]) #i.e. 5
    return tuple(args)
    

def _find_args(func):
    try:
        return len(sig(func).parameters)
    except ValueError:
        raise NoSignatureError("Function '{}' does not have a signature so the number of arguments required is not known".format(func))
  
def _make_func(this, func:str, var_func, wrapper, *others): #__add__, num
    function = getattr(var_func(this), func)
    args_num = _find_args(function) #Number of extra arguments taken (i.e. __add__ would be 1, __iter__ would be 0)
    mapped = _mapper(this, func, var_func, *others)
    return wrapper(function(*mapped))

class DunderArgsError(TypeError): #Custom exception
    pass

class NoSignatureError(ValueError):
    pass

class add_methods(object):
    def __init__(self, var_func, *funcs:str, wrapper = lambda value: value):
        if type(var_func) == str: #i.e. "num" to obj.num
            var_func = lambda obj: getattr(obj, var_func)
        self.var_func = var_func #Can be string or function
        self.funcs = funcs
        self.wrapper = wrapper
    
    def __call__(self, cls):
        class Decorated(cls):
            for func in self.funcs:
                setattr(cls, func, lambda this, *others, func = func: _make_func(this, func, self.var_func, self.wrapper, *others))
                #i.e. self.num.__add__(other.num)
                #Note that 'this' is used to distinguish from 'self' defined in the class
        Decorated.__name__ = cls.__name__
        return Decorated

if __name__ == "__main__":
    @add_methods(lambda obj: int(obj.num), "__add__", "__mul__", wrapper = str) #"__add__" -> def __add__(self, other): return self.num + other.num
    @add_methods(lambda obj: obj.array, "__setitem__", "__iter__", "__len__", "__setitem__") #"__iter__": def __iter__(self): for i in self.array: yield i
    @add_methods(lambda obj: obj.string, "__getitem__")
    class Derivative(object):
        def __init__(self, num, array, string):
            self.num = num
            self.array = array
            self.string = string

    test1 = Derivative("2", [1, 2, 3], "hello")
    test2 = Derivative("3", [1, 3, 3, 7], "hi")
    print(test1 + test2)
    print(test1 * test2)
    print(len(test2))
    print(test2[-1])
    print("Before:", list(test1))
    test1.__setitem__(0, 100)
    print("After:", list(test1))
