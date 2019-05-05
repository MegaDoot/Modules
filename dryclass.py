"""
Alex Scorza 2019
Copyright statement:
1.
    1. Pls dont steal

HOW TO USE 'construct'
Avoids doing something like this:
(Code Example 1)
-----------
    def __init__(genus, species, legs, mass, speed, eyes = 2):
        self.genus = genus
        self.species = species
        self.legs = legs
        self.mass = mass
        self.speed = speed
        self.eyes = eyes
        print("Initialised")
-----------        
BECAUSE THAT WOULD BE  W E T
Instead, you can do:
-----------
    @construct(args = ("genus", "species", "legs", "mass", "speed"), kwargs = [("eyes", 2)])
    class Foo:
        def __init__(self):
            print("Initialised")
-----------
W O W
ISN'T
THAT
D          R          Y
You can also add a list for extra arguments (*args) to go with 'extra_a = "name_of_variable"'
A dictionary can be saved for keyword arguments (**kwargs): 'extra_kw = "name_of_variable"'
Both are None by default

HOW TO USE 'to_static', 'to_cls' and 'generic':
Recommended: look at the code in __name__ == "__main__" section
'to_static': converts all methods in a class into staticmethods
'to_cls': converts all methods in a class into classmethods
'generic': does not affect function/method/class
Here we see a use for 'generic'. It is the decorator equivalent of '*[]' (where there are no args
but you need to type something to avoid a syntax error, i.e. '"hello" is speak else *[]')
(Code Example 2)
-----------
    import random
    decorators = [generic, to_cls, to_static]
    selected = decorators[random.randrange(0, 3)]
    @selected
    class Foo:
        def bar():
            pass
-----------

HOW TO USE 'dunders':
'dunders(obj)' returns all magic methods from a class/instance - all that are in the format
\^__[A-Za-z_]+__$\ (note that no dunders contain numbers).

HOW TO USE 'add_method':
Add a decorator before the function -
(Code Example 3)
-----------
    import dryclass as dc
    @dc.add_methods("__main__.Foo: obj.num", "__add__", "__sub__")
    class Foo:
        def __init__(self):
            self.num = 5
    print(repr(Foo() + Foo())) #Returns 10
-----------
This gets the class and adds each of the specified magic methods. An unlimited amount is allowed.
The lambda at the starts specifies which attribute of the class to get.
-----------
Here is a usage of the function on the result (wrapper) and the function called on each argument:
(Code Example 4)
-----------
    @dc.add_methods("__main__.Foo: int(obj.num)", "__add__", "__sub__", "__mul__", "__floordiv__", wrapper = "str")
    class Foo:
        def __init__(self):
            self.num = "5"
    print(repr(Foo() + Foo())) #Returns "10"
-----------
(Note that, intuitively, a lambda can be used for the wrapper or any valid callable statement, i.e. lambda num: str(num))
Here, the value of num is always a string so it is converted to an integer, the calculations are
done and the result is converted back into a string, so "5" + "6" would become "11" in this case,
despite being strings. The equivalent of the code above/code example 4 done normally:
(Code Example 5)
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
    print(repr(Foo() + Foo())) #Returns "10"
-----------
As you can see, this code is very WET, repetitive and time-consuming to edit.
-----------
Now for the mysterious syntax at the start of each decorator. This string defines the statement that
should be applied to each different data type. A string is used over a dictionary for 3 reasons:
-Making different data types have the same statement is easier
-More freedom
-Improved readability and writability
In the example below, both 'float' and 'int' have the same behaviour so we do
'float, int: obj' instead of 'float: obj; int: obj' because that would be  W E T
It's important to note that anything defined within the program would not be
available to the module, hence the need to write '__main__' beforehand. Also,
each section (made up of data types separated by commas, a colon and a statement)
is separated by a SEMICOLON and not a comma.
(Code Example 6)
-----------
    @dc.add_methods("__main__.Foo: float(obj.num); float, int: obj", "__add__", "__radd__")
    class Foo:
        def __init__(self):
            self.num = 5
    print(repr(Foo() + 1), repr(Foo() + Foo()), repr(3 + Foo()))
-----------

HOW TO USE 'importer':
What if you don't want to add '__main__' before all functions you define?
The 'importer' function allows you to write your own statement, i.e.
'importer("m")', so you can now write it as m.Foo not __main__.Foo
'importer("m")' is equivalent to 'import __main__ as m'
"""
import operator

__all__ = ("construct", "to_static", "to_cls", "generic", "dunders", "IMATH_OPERS", "MATH_OPERS", "EQ_OPERS", "ITER_OPERS", "TYPE_OPERS", "COND_OPERS", "ICOND_OPERS", "add_methods", "importer")

def construct(args = [], kwargs = [], extra_a = None, extra_kw = None):
    def decorator(cls):
        star = []
        starstar = {}
        if hasattr(cls, "__init__"):
            func = cls.__init__
        else:
            func = lambda self: None
        def init_wrapper(*a, **kw):
            self = a[0]
            a = a[1:] #Save and remove 'self' argument
            if len(a) < len(args) or (extra_a is None and len(a) > len(args) + len(kwargs)):
                raise TypeError("Got {} args, expected {} to {}".format(len(a), len(args), len(args) + len(kwargs)))
            remove_kw = 0 #Ignore all that were entered as args
            for i in range(len(a)): #arguments
                if i + 1 > len(args): #If it exceeds the length of the args
                    if i + 1 > len(args) + len(kwargs): #If it exceeds the length of args and kwargs
                        if extra_a is None: #If not defined
                            raise Exception("This should've been caught already. Valve pls fix")
                        else: #Add to *
                            star.append(a[i])
                    else: #Must be a normal arg that represents a default argument
                        set_val = kwargs[1 + i - len(a)][0]
                        remove_kw += 1
                        setattr(cls, set_val, a[i])
                else:
                    setattr(cls, args[i], a[i])
            for k, v in kwargs[remove_kw:]: #All kwargs entered in the keyword and argument format
                setattr(cls, k, v)
            for k, v in kw.items():
                if k in dict(kwargs).keys():
                    setattr(cls, k, v)
                else:
                    if extra_kw is None:
                        raise TypeError("Unexpected keyword argument '{}'".format(k))
                    starstar[k] = v
                    
            if extra_a is not None:
                setattr(cls, extra_a, star)
            if extra_kw is not None:
                setattr(cls, extra_kw, starstar)
            func(self)
        setattr(cls, "__init__", init_wrapper)
        return cls
    return decorator

def edit(cls, function, exclude = tuple()):
    for func in filter(lambda name: not (name.startswith("__") and name.endswith("__")), dir(cls)):
##        print(func, type(func))
        if function not in exclude:
            setattr(cls, func, function(getattr(cls, func)))
##        print(func)
    return cls

def to_static(cls, **kwargs):
    return edit(cls, staticmethod, **kwargs)

def to_cls(cls, **kwargs):
    return edit(cls, classmethod, **kwargs)

generic = lambda obj: obj

def dunders(obj): #Lists all dunder methods of an object
    return tuple(filter(lambda func: func.startswith("__") and func.endswith("__"), dir(obj)))

@to_static
class Tkn:
    def split_with(string, delimiter):
        not_quoted = Tkn.out_quotes(string)
        sep_positions = []

        for pos in not_quoted:
            if string[pos] == delimiter:
                sep_positions.append(pos)

        split = [""]
        for i in range(len(string)):
            if i in sep_positions:
                split.append("")
            else: #Skips semicolons
                split[-1] += string[i]
        return split

    def tokenise(string):
        not_quoted = Tkn.out_quotes(string) #Remove all text in quotation marks and apostrophes
        stripped = "" #Spaces removed
        for i in range(len(string)):
            if string[i] == " ":
                if not i in not_quoted:
                    stripped += string[i]
            else:
                stripped += string[i]
        string = stripped

        separated = Tkn.split_with(string, ";")
        for i in range(len(separated)):
            separated[i] = Tkn.split_with(separated[i], ":")
            separated[i][0] = list(Tkn.split_with(separated[i][0], ","))
        return separated

    def method(multi_key_dict, obj, key):
        type_ = type(obj)
        for k_tuple in multi_key_dict.keys():
            evaluated = tuple(map(eval, k_tuple))
            if type_ in evaluated:
                return multi_key_dict[k_tuple]
        raise KeyError("Key '{}' not found".format(key))

    def out_quotes(string):
        indexes = [i for i in range(len(string)) if string[i] == '"']
        inside = []
        iterate = tuple(range(0, len(indexes), 2))
        for i in iterate:
            inside += tuple(range(indexes[i], indexes[i + 1] + 1))
        outside = [i for i in range(len(string)) if not i in inside]
        return outside

    def unpack(tokens):
            individual = {}
            for i in range(len(tokens)):
                for x in range(len(tokens[i][0])):
                    individual[tokens[i][0][x]] = tokens[i][1]
            return individual

    def run(dict_, obj):
        for k, v in dict_.items():
            if eval(k) == type(obj):
                return eval(v)
        raise NameError("Behaviour of type '{}' is not defined".format(type(obj).__name__))

def from_i(funcs):
    return tuple(map(lambda func: "__" + func[3:], funcs))

I_START = ("__index__", "__init__", "__instancecheck__", "__int__", "__invert__", "__iter__")

IMATH_OPERS = ("__iadd__", "__ifloordiv__", "__ilshift__", "__imod__", "__imul__", "__ipow__", "__irshift__", "__isub__", "__itruediv__")
MATH_OPERS = from_i(IBIN_OPERS)
EQ_OPERS = ("__eq__", "__ge__", "__le__", "__gt__", "__lt__", "__ne__")
ITER_OPERS = ("__contains__", "__delitem__", "__delslice__", "__getslice__", "__index__", "__len__", "__setitem__", "__setslice__")
TYPE_OPERS = ("__float__", "__int__")
COND_OPERS = ("__iand__", "__ior__", "__ixor__")
ICOND_OPERS = from_i(COND_OPERS)

def make_func(this, func, evaluator, wrapper, *args):
##    print("\nCalled")
    evaluated = evaluator(this)
    print(this, evaluated)
    if evaluated is this: #If unchanged, it finds its own method, resulting in recursion :(
        raise RecursionError("Statement entered results in infinite recursion - statement type of class to be decorated must not equal 'obj'")
    wrapper = eval(wrapper)
    mapped = tuple(map(evaluator, args))
    if func.startswith("__i") and func not in I_START: #dir of int, str, etc. don't contain inplace operators
        op = getattr(operator, func[2:][:-2]) #i.e. func = __iadd__ -> operator.iadd
        called = op(evaluated, *mapped)
    else:
        to_call = getattr(evaluated, func)
        called = to_call(*mapped)
##    print("called =", called)
    wrapped = wrapper(called)
    return wrapped

class DunderArgsError(TypeError): #Custom exception
    pass

class NoSignatureError(ValueError): #Custom exception
    pass

def importer(name = "__main__"):
    globals()[name] = __import__("__main__")

class add_methods(object): #The decorator
    def __init__(self, syntax, *funcs:str, wrapper = "lambda value: value"):
        self.func_dict = Tkn.unpack(Tkn.tokenise(syntax))
##        print(self.func_dict)
        self.funcs = funcs
        self.wrapper = wrapper
    
    def __call__(self, cls):
        evaluator = lambda obj: Tkn.run(self.func_dict, obj)
##        class Decorated(cls): #Temporary decorated class that contains all of the
        for func in self.funcs: #func is a string
##            print("Iterated with", func)
            
            code = lambda this, *args, func = func, wrapper = self.wrapper: make_func(this, func, evaluator, wrapper, *args)
            setattr(cls, func, code)
                #i.e. self.num.__add__(other.num)
                #Note that 'this' is used to distinguish from 'self' defined in the class
        return cls #Turn the class into the decorated class

if __name__ == "__main__":
    import random

    #For construct
    @construct(args = ("a", "b"), kwargs = (("c", 3), ("d", 4), ("e", 5)), extra_kw = "keywords")
    class Foo:
        def __init__(self):
            print("Initialised")
            print(self.a, self.b, self.c, self.d, self.e)
            print(self.keywords, "\n")
    
    test = Foo(1, 2, 9, e = 10, f = 100)
    
    #For add_methods
    @add_methods("Derivative: obj.array; int: obj", "__len__", "__iter__", "__getitem__", "__setitem__")
    @add_methods("Derivative: int(obj.num); int, float: obj", "__add__", "__mul__", wrapper = "str")
    class Derivative(object):
        def __init__(self, num, array, string):
            self.num = num
            self.array = array
            self.string = string

    test1 = Derivative("3", [1, 2, 3], "hello")
    test2 = Derivative("10", [1, 3, 3, 7], "hi")
    print(len(test2))
    print(repr(test1 + 5))
    print(repr(test1 + test2))
    print(repr(test1 * test2))
    print(repr(test2[-1]))
    print("Before:", list(test1))
    test1[0] = 100
    print("After:", list(test1), "\n")

    decorators = [generic, to_cls, to_static]
    selected = decorators[random.randrange(0, 3)]
    @selected
    class Foo:
        def bar():
            pass
    test3 = Foo()
    print(type(test3.bar))
    try:
        Foo.bar()
        print({"function": "staticmethod", "method": "instancemethod"}[type(test3.bar).__name__])
    except TypeError:
        print("classmethod")
    
    @generic
    def hello():
        print("Hello!")
else:
    importer()
