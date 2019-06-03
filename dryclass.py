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
    import dryclass as dc
    @dc.construct(args = ("genus", "species", "legs", "mass", "speed"), kwargs = [("eyes", 2)])
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
Here we see a use for 'generic'. It is the decorator equivalent of '*[]' (where
thereare no args but you need to type something to avoid a syntax error, i.e.
'"hello" if speak else *[]')
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
r"^__[A-Za-z_]+__$" (note that no dunders contain numbers).
HOW TO USE 'add_method':
Add a decorator before the function -
(Code Example 3)
-----------
    import dryclass as dc
    @dc.add_methods("__main__.Foo: obj.num", "__add__", "__sub__")
    class Foo:
        def __init__(self):
            self.num = 5
    print(repr(Foo() + Foo())) # Returns 10
-----------
This gets the class and adds each of the specified magic methods. An unlimited
amount is allowed. The lambda at the starts specifies which attribute of the
class to get.
-----------
Here is a usage of the function on the result (wrapper) and the function called
on each argument:
(Code Example 4)
-----------
    @dc.add_methods("__main__.Foo: int(obj.num)", "__add__", "__sub__","__mul__","__floordiv__", wrapper = "str")
    class Foo:
        def __init__(self):
            self.num = "5"
    print(repr(Foo() + Foo())) # Returns "10"
-----------
(Note that, intuitively, a lambda can be used for the wrapper or any valid
callable statement, i.e. lambda num: str(num))
Here, the value of num is always a string so it is converted to an integer, the
calculations are done and the result is converted back into a string, so
"5" + "6" would become "11" in this case despite being strings. The equivalent
of the code above/code example 4 done normally:
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
    print(repr(Foo() + Foo())) # Returns "10"
-----------
As you can see, this code is very WET, repetitive and time-consuming to edit.
-----------
Now for the mysterious syntax at the start of each decorator. This string
defines the statement that should be applied to each different data type. A
string is used over a dictionary for 3 reasons:
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
HOW TO USE 'Opers':
This contains several tuples of special methods so that if you want your object
to have specific uses, such as an iterable or a number, you can easily do
'*Opers.ITERS' or '*Opers.MATH'. They are dryclass._Special objects.
Methods (using Opers.MATH as an example):
Opers.MATH      ->   All methods          i.e. __add__, __iadd__ and __radd__
Opers.MATH.f    ->   Normal methods       i.e. __add__
Opers.MATH.fi   ->   Inplace methods      i.e. __iadd__
Opers.MATH.fr   ->   Right-side methods   i.e. __radd__
The currently available ones are 'MATH', 'EQ', 'ITER', 'TYPE' and 'COND'
"""
import operator
import inspect

__all__ = ("construct", "to_static", "to_cls", "generic", "dunders", "add_methods", "importer", "Opers")


def _has_init(cls):
    try:
        inspect.getsource(cls.__init__)  # Get the source code of the function
        return True  # If no error is raised, source code has been found
    except TypeError:  # Will raise this error if no Python code found (when initialised implicitly by Python and not the programmer)
        return False


def construct(args=[], kwargs=[], extra_a=None, extra_kw=None):
    def decorator(cls):  # Take class as input, edit class and then output
        star = []  # Unlimited args, such as *args
        starstar = {}  # Unlimited kwargs, such as **kwargs
        if _has_init(cls):  # hasattr(cls, "__init__") doesn't work as all classes have them automatically
            func = cls.__init__  # Set the function to run later. This will cause a recursion error if done later as it gets edited
        else:
            def func(self):
                return

        def init_wrapper(*a, **kw): # The actual arguments are processed later
            self = a[0]  # self' is still entered as a parameter
            a = a[1:]  # Save and remove 'self' argument
            if len(a) < len(args) or (extra_a is None and len(a) > len(args) + len(kwargs)):
                # If too few arguments or if extra arguments added without defining a place to store *args
                raise TypeError("Got {} args, expected {} to {}".format(len(a), len(args), len(args) + len(kwargs)))
            remove_kw = 0  # Ignore all that were entered as args
            for i in range(len(a)):  # arguments
                if i + 1 > len(args):  # If it exceeds the length of the args
                    if i + 1 > len(args) + len(kwargs):  # If it exceeds the length of args and kwargs
                        if extra_a is None:  # If not defined
                            raise Exception("This should've been caught already. Valve pls fix")
                        else:  # Add to *
                            star.append(a[i])
                    else:  # Must be a normal arg that represents a default argument
                        set_val = kwargs[1 + i - len(a)][0]  # Which variable is currently in use
                        remove_kw += 1  # i.e. f(a, b = 0, c = 1) would accept call f(4, 5). When processing kwargs, 'b' will be ignored.
                        # The '+=1' tells the process to ignore anything before that number when processing kwargs to avoid being counted twice
                        setattr(cls, set_val, a[i])  # Set the variable to the value entered
                else:
                    setattr(cls, args[i], a[i])  # Set the value in args tuple to this
            for k, v in kwargs[remove_kw:]:  # All kwargs entered in the keyword and argument format
                setattr(cls, k, v)  # i.e f=10 in kwargs would set the class' 'f' to '10'
            for k, v in kw.items():  # Iterate through each key in the dictionary
                if k in dict(kwargs).keys():  # If the k is in variables that have default values, it's not a **, so don't put it there
                    setattr(cls, k, v)
                else:
                    if extra_kw is None:  # If the output for ** has not yet been defined
                        raise TypeError("Unexpected keyword argument '{}'".format(k))
                    starstar[k] = v  # Add this key to the values if it has been defined
                    
            if extra_a is not None:  # If * pipe has been already defined
                setattr(cls, extra_a, tuple(star))
            if extra_kw is not None:  # If the ** pipe has already been defined
                setattr(cls, extra_kw, starstar)
            func(self)
        setattr(cls, "__init__", init_wrapper)  # Set the __init__ for the class to a new class that is identical but with extra variables and parameters
        return cls
    return decorator

def _edit(cls, function, exclude = tuple()):  # Change all instances of a function to a decorated one
    for func in filter(lambda name: not (name.startswith("__") and name.endswith("__")), dir(cls)): # All non-dunder methods
        if function not in exclude:  # If not specifically excluded
            setattr(cls, func, function(getattr(cls, func)))  # Add a 'function' (f) to pre-existing 'func' (g) so g(x) becomes fg(x)
    return cls  # Return newly edited class


def to_static(cls, **kwargs):  # Add the 'staticmethod' decorator to all non-dunder functions
    return _edit(cls, staticmethod, **kwargs)


def to_cls(cls, **kwargs):  # Add the 'classmethod' decorator to all non-dunder functions
    return _edit(cls, classmethod, **kwargs)


def generic(cls):  # Do nothing
    return


def dunders(obj):  # Lists all dunder methods of an object
    return tuple(filter(lambda func: func.startswith("__") and func.endswith("__"), dir(obj)))


@to_static  # Using my parts of the module to make other parts dryer. That's allowed, right?
class _Tkn:  # Deals with all tokenisation of a string
    def split_with(string, delimiter):  # Like .split() but has special behaviour for text in quotes
        not_quoted = _Tkn.out_quotes(string)  # Indexes not in quotation makes
        sep_positions = []

        for pos in not_quoted:
            if string[pos] == delimiter:  # Finds all positions places to split
                sep_positions.append(pos)

        split = [""]
        for i in range(len(string)):
            if i in sep_positions:  # If it reaches the delimiter start adding to new string
                split.append("")  # Always adds to end of last string so this means that a new part is defined
            else:  # Skips semicolons
                split[-1] += string[i]  # Add to end of last string of list
        return split

    def tokenise(string):
        not_quoted = _Tkn.out_quotes(string)  # Remove all text in quotation marks and apostrophes
        stripped = ""  # Spaces removed
        for i in range(len(string)):
            if string[i] == " ": # If a space
                if not i in not_quoted:  # If a whitespace, can be removed if it's not in a string
                    stripped += string[i]  # Add this character to stripped version of string
            else:
                stripped += string[i]
        string = stripped

        separated = _Tkn.split_with(string, ";")
        for i in range(len(separated)):
            separated[i] = _Tkn.split_with(separated[i], ":")
            separated[i][0] = list(_Tkn.split_with(separated[i][0], ","))
        return separated


    def out_quotes(string):  # All positions not in quotes (will not split anything in quotes)
        indexes = [i for i in range(len(string)) if string[i] == '"']
        inside = []
        iterate = tuple(range(0, len(indexes), 2))  # i.e. (0, 2, 4, 6)
        for i in iterate:
            inside += tuple(range(indexes[i], indexes[i + 1] + 1))  # range(5) goes 0 to 4, hence the '] + 1'
        outside = [i for i in range(len(string)) if not i in inside] # Negates inside
        return outside

    def unpack(tokens):  # Takes a list of tokens, i.e. '[[["float", "int"], "obj+1"],]' and makes a dictionary of string keys
        individual = {}
        for i in range(len(tokens)):  # Go through each set of tokens, such as '[["float", "int"], "obj+1"]'
            apply = tokens[i][1]  # i.e. '"obj+1"'
            for x in range(len(tokens[i][0])):  # Go through the list containing data types, i.e. '["float", "int"]'
                individual[tokens[i][0][x]] = apply  # Set each data type to its own key with the value as the apply function
        return individual  # i.e. {"float": "obj+1", "int": "obj+1"}

    def run(dict_, obj):
        for k, v in dict_.items():
            if eval(k) == type(obj):
                return eval(v)
        raise NameError("Behaviour of type '{}' is not defined".format(type(obj).__name__))

def _make_func(this, func, evaluator, wrapper, *args):
    evaluated = evaluator(this)
    if evaluated is this:  # If unchanged, it finds its own method, resulting in recursion :(
        raise RecursionError("Statement entered results in infinite recursion - statement type of class to be decorated must not equal 'obj'")
    # i.e. if class is called 'Foo', typing "Foo: obj" will result in it calling itself again as it hasn't yet defined it
    wrapper = eval(wrapper)
    mapped = tuple(map(evaluator, args))
    if func.startswith("__i") and func not in I_START:  # dir of int, str, etc. don't contain inplace operators
        op = getattr(operator, func[2:][:-2])  # i.e. func = __iadd__ -> operator.iadd
        called = op(evaluated, *mapped)
    else:
        to_call = getattr(evaluated, func)
        called = to_call(*mapped)
    wrapped = wrapper(called)
    return wrapped

def importer(name = "__main__"):
    globals()[name] = __import__("__main__")

class add_methods(object):  # The decorator
    def __init__(self, syntax, *funcs:str, wrapper = "lambda value: value"):
        self.func_dict = _Tkn.unpack(_Tkn.tokenise(syntax))
        self.funcs = funcs
        self.wrapper = wrapper

    def __call__(self, cls):
        def evaluator(obj):
            return _Tkn.run(self.func_dict, obj)
        for func in self.funcs: # func is a string
            def code(this, *args, func=func, wrapper=self.wrapper):
                return _make_func(this, func, evaluator, wrapper, *args)
            setattr(cls, func, code)
            # i.e. self.num.__add__(other.num)
            # Note that 'this' is used to distinguish from 'self' defined in the class
        return cls  # Turn the class into the decorated class


def _insert_letter(funcs, letter):
    return tuple(map(lambda func: "__" + letter + func[2:], funcs))


I_START = ("__index__", "__init__", "__instancecheck__", "__int__", "__invert__", "__iter__")


class _Special:
    def __init__(self, *normals):
        self.f = normals
        for char in "ir":
            setattr(self, "f" + char, _insert_letter(normals, char))

    def __repr__(self):
        return f"_Special({str(self.funcs)[1:-1]})"

    def __iter__(self):
        for el in self.funcs:
            yield el

    @property
    def funcs(self):  # Will update if any of the values are changed
        return self.f + self.fi + self.fr
    

class Opers:
    MATH = _Special("__add__", "__floordiv__", "__lshift__", "__mod__", "__mul__", "__pow__", "__rshift__", "__sub__", "__truediv__")

    EQ = _Special("__eq__", "__ge__", "__gt__", "__le__", "__lt__", "__ne__")

    ITER = _Special("__contains__", "__delitem__", "__delslice__", "__getitem__", "__getslice__", "__index__", "__len__", "__setitem__", "__setslice__")

    TYPE = _Special("__float__", "__int__", "__str__")

    COND = _Special("__and__", "__or__", "__xor__")


if __name__ == "__main__":
    import random

    # For construct
    @construct(args=("a", "b"), kwargs=(("c", 3), ("d", 4), ("e", 5)), extra_kw="keywords")
    class Foo:
        def __init__(self):
            print("Initialised")
            print(self.a, self.b, self.c, self.d, self.e)
            print(self.keywords, "\n")
    
    test = Foo(1, 2, 9, e=10, f=100)
    
    # For add_methods
    @add_methods("Derivative: obj.array; int: obj", *Opers.ITER)
    @add_methods("Derivative: int(obj.num); int, float: obj", *Opers.MATH, *Opers.COND, wrapper = "str")
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
