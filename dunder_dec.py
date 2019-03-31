"""
Alex Scorza 2019
"""

from inspect import signature as sig

SPECIAL = {"__getitem__": (False,), "__setitem__": (False, False)}
#False: use value, True: use getattr(, var_name)

def _dunders(obj):
    return tuple(filter(lambda func: func.startswith("__") and func.endswith("__"), dir(obj)))

def _mapper(this, func, var_name, *others):
    true_false = SPECIAL.get(func, (True,))
    print(true_false, len(true_false))
    arg_amount = _find_args(getattr(getattr(this, var_name), func))
    if len(true_false) != arg_amount:
        if func in SPECIAL.keys():
            raise DunderArgsError("Wrong number of values for {}, expected {}, got {} -> {}".format(func, arg_amount, len(true_false), others))
        else:
            raise NotImplementedError("Special magic method {} not recognised as special: {} (author's fault)".format(func, tuple(SPECIAL.keys())))
    args = []
    for i in range(len(others)):
        print(true_false[i])
        if true_false[i]: #== True
            args.append(getattr(others[i], var_name)) #i.e. CustomClass.num
        else:
            args.append(others[i]) #i.e. 5
    return tuple(args)
    

def _find_args(func):
    return len(sig(func).parameters)

def _make_func(this, other, func:str, var_name:str) -> "function": #__add__, num
##    print("func, var_name:", func, var_name)
    function = getattr(getattr(this, var_name), func) #Retrive function to use dunder method: this.var_name.func
    args_num = _find_args(function) #Number of extra arguments taken (i.e. __add__ would be 1, __iter__ would be 0)
    if func in SPECIAL.keys(): #If args are not all the same type
        mapped = _mapper(this, func, var_name, other)
        return function(*mapped)
    else:
        if args_num == 1: #If binary
            return function(getattr(other, var_name))
        elif args_num == 0: #If unary, i.e. len or iter
            return function() #No arguments needed
        else:
            raise DunderArgsError("Accepting only 1 or 2 arguments") #As far as know they all accept 1 or 2

class DunderArgsError(TypeError): #Custom exception
    pass

class add_methods(object):
    def __init__(self, var_name:str, *funcs:str):
        self.var_name = var_name
        self.funcs = funcs
    
    def __call__(self, cls):
        class Decorated(cls):
            for func in self.funcs:
                setattr(cls, func, lambda this, other = None, func = func: _make_func(this, other, func, self.var_name))
                #i.e. self.num.__add__(other.num)
                #Note that 'this' is used to distinguish from 'self' defined in the class
        Decorated.__name__ = cls.__name__
        return Decorated

__all__ = ("add_func",)

if __name__ == "__main__":
    @add_methods("num", "__add__", "__mul__") #"__add__" -> def __add__(self, other): return self.num + other.num
    @add_methods("array", "__iter__", "__len__") #"__iter__": def __iter__(self): for i in self.array: yield i
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
    print(list(test1))
    print(test1.__getitem__(0))
##    print(_mapper(test1, "__setitem__", "array", 0, 100))
