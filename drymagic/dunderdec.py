"""
Alex Scorza 2019
Plz don't steal
Documentation:
Add a decorator before the function -
(Code Example 1)
-----------
    @dunderdec.add_func(lambda obj: {[ type(obj) ]: obj.num}, "__add__", "__sub__", wrapper = float)
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
    @dunderdec.add_func(lambda obj: {[ type(obj) ]: int(obj.num)}, "__add__", "__mul__", "__sub__", "__floordiv__", wrapper = str)
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
        return str(int(self.num) + int(other.num))
        
    def __mul__(self, other):
        return str(int(self.num) * int(other.num))
        
    def __sub__(self, other):
        return str(int(self.num) - int(other.num))
        
    def __floordiv__(self, other):
        return str(int(self.num) // int(other.num))
-----------
The more dunder methods used, the more concise and 'dry' the code becomes.
"""

from inspect import signature as sig
import tokenise as tkn

__all__ = ("add_methods", "BIN_OPERS", "IBIN_OPERS")

SPECIAL = {"__getitem__": (False,), "__setitem__": (False, False)}
#False: use value, True: use getattr(, variable name)

BIN_OPERS = ("__add__", "__mul__", "__div__", "__truediv__", "__sub__")
IBIN_OPERS = tuple(map(lambda func: "__i" + func[2:], BIN_OPERS))

def _mkdict(dict_, key):
    for keys_tuple in dict_.keys():
        if key in keys_tuple:
            return dict_[keys_tuple]
    raise KeyError("Key '{}' not found".format(key))

def _dunders(obj): #Lists all dunder methods of an object
    return tuple(filter(lambda func: func.startswith("__") and func.endswith("__"), dir(obj)))

def _mapper(this, func:str, magic_method, var_func, *others):
    true_false = SPECIAL.get(func, (True,)) #Defaults to (True,) if not special
    #For each boolean in the list, True: Use the specified attribute of the class, False: Use the value outright
    arg_amount = _find_args(magic_method) #Number of arguments expected
    if len(true_false) < arg_amount: #If too few amount entered (ignores extra arguments)
        if func in SPECIAL.keys(): #If it's a special snowflake with arguments other than: [The Same Type], the case for most arithmetic methods
            raise DunderArgsError("Wrong number of values for {}, expected {}, got {} -> {}".format(func, arg_amount, len(true_false), others))
        else:
            raise NotImplementedError("Special magic method {} not recognised as special: {} (author's fault)".format(func, tuple(SPECIAL.keys())))
    args = [] #Mutable so items can be appended
    for i in range(len(others)):
        print(others[i])
        var_dict = var_func(others[i])
        print(var_dict)
        funcified = _mkdict(var_dict, type(others[i])) #Get the specific value set by dict lambda var_func
        args.append(funcified) #i.e. CustomClass.num
    return tuple(args) #No longer needs to be changed, therefore tuple
    

def _find_args(func): #Number of arguments required. Note that extra arguments are ignored, like JavaScript
    try:
        return len(sig(func).parameters) #sig: inspect.signature
    except ValueError: #Could not find a signtature - invalid
        raise NoSignatureError("Function '{}' does not have a signature so the number of arguments required is not known".format(func))
  
def _make_func(this, func:str, var_func, wrapper, *others): #var_func = original function
    magic_method = getattr(_mkdict(var_func(this), type(this)), func) #Function for data type of original class/self
    mapped = _mapper(this, func, magic_method, var_func, *others)
    #Gets values, either an attribute of 'this', i.e. 'this.num' or a value, i.e. "Hello World"
    return wrapper(magic_method(*mapped)) #function: do the calculation, wrapper: apply a function to the value returned

def make_func(this, func, evaluator, wrapper, *args):
    def foo(this, other):
        print(this.num + evaluator(other))
    return foo

class DunderArgsError(TypeError): #Custom exception
    pass

class NoSignatureError(ValueError): #Custom exception
    pass

class add_methods(object): #The decorator
    def __init__(self, syntax, *funcs:str, wrapper = lambda value: value):
        self.func_dict = tkn.unpack(tkn.tokenise(syntax))
        print(self.func_dict)
        self.funcs = funcs
        self.wrapper = wrapper
    
    def __call__(self, cls):
        evaluator = lambda obj: tkn.run(self.func_dict, obj)
        class Decorated(cls): #Temporary decorated class that contains all of the
            for func in self.funcs: #func is a string
                setattr(cls, func, lambda this, *args, func = func: make_func(this, func, evaluator, self.wrapper, *args))
##                setattr(cls, func, lambda this, *others, func = func: _make_func(this, func, self.var_func, self.wrapper, *others))
                #i.e. self.num.__add__(other.num)
                #Note that 'this' is used to distinguish from 'self' defined in the class
        Decorated.__name__ = cls.__name__ #Otherwise, lots of obfuscated and probably useless information
        return Decorated #Turn the class into the decorated class

if __name__ == "__main__":
    #Example below, see documentation at top for information
    @add_methods("int, float: obj", "__add__", wrapper = str)
##    @add_methods(lambda obj: {(type(obj),): obj.array}, "__setitem__", "__iter__", "__len__")
##    @add_methods(lambda obj: {(type(obj),): obj.string}, "__getitem__")
    class Derivative(object):
        def __init__(self, num, array, string):
            self.num = num
            self.array = array
            self.string = string

    test1 = Derivative("3", [1, 2, 3], "hello")
    test2 = Derivative("4", [1, 3, 3, 7], "hi")
    print(repr(test1 + 5))
    print(repr(test1 + test2))
##    print(repr(test1 * test2))
##    print(len(test2))
##    print(repr(test2[-1]))
##    print("Before:", list(test1))
##    test1[0] = 100
##    print("After:", list(test1))
