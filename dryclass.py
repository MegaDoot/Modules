"""
Alex Scorza 2019

HOW TO USE 'construct'
Avoids doing something like this:

    def __init__(genus, species, legs, speed, eyes = 2):
        self.genus = genus
        self.species = species
        self.legs = legs
        self.speed = speed
        self.eyes = eyes
        print("Initialised")
        
BECAUSE THAT WOULD BE  W E T
Instead, you can do:

    @construct(args = ("genus", "species", "legs", "speed"), kwargs = [("eyes", 2)])
    class Foo:
        def __init__(self):
            print("Initialised")

W  O W
ISN'T
THAT


D          R          Y


HOW TO USE 'add_method':
Add a decorator before the function -
(Code Example 1)
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
(Code Example 2)
-----------
    @dc.add_methods("__main__.Foo: int(obj.num)", "__add__", "__sub__", "__mul__", "__floordiv__", wrapper = str)
    class Foo:
        def __init__(self):
            self.num = "5"
    print(repr(Foo() + Foo())) #Returns "10"
-----------
Here, the value of num is always a string so it is converted to an integer, the calculations are
done and the result is converted back into a string, so "5" + "6" would become "11" in this case,
despite being strings. The equivalent of the code above/code example 2 done normally:
(Code Example 3)
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
'float, int: obj' instead of 'float: obj, int: obj' because that would be  W E T
It's important to note that anything defined within the program would not be
available to the module, hence the need to write '__main__' beforehand. Also,
each section (made up of data types separated by commas, a colon and a statement)
is separated by a SEMICOLON and not a comma.
(Code Example 4)
-----------
    @dc.add_methods("__main__.Foo: float(obj.num); float, int: obj", "__add__", "__radd__")
    class Foo:
        def __init__(self):
            self.num = 5
    print(repr(Foo() + 1), repr(Foo() + Foo()), repr(3 + Foo()))
-----------
"""

__all__ = ("construct", "add_methods", "BIN_OPERS", "IBIN_OPERS")

def construct(args = [], kwargs = []):
    def decorator(cls):
        if hasattr(cls, "__init__"):
            func = cls.__init__
        else:
            func = lambda self: None
        def init_wrapper(*a, **kw):
            print(a)
            self = a[0]
            a = a[1:] #Save and remove 'self' argument
            if len(a) < len(args) or len(a) > len(args) + len(kwargs):
                raise TypeError("Got {} args, expected {} to {}".format(len(a), len(args), len(args) + len(kwargs)))
            remove_kw = 0 #Ignore all that were entered as args
            for i in range(len(a)): #arguments
                if i + 1 > len(args):
                    set_val = kwargs[1 + i - len(a)][0]
                    remove_kw += 1
                    setattr(cls, set_val, a[i])
                else:
                    setattr(cls, args[i], a[i])
            for k, v in kwargs[remove_kw:]: #All kwargs entered in the keyword and argument format
                if k in kw:
                    setattr(cls, k, kw[k])
                else:
                    setattr(cls, k, v)
            func(self)
        setattr(cls, "__init__", init_wrapper)
        return cls
    return decorator

BIN_OPERS = ("__add__", "__mul__", "__div__", "__truediv__", "__sub__")
IBIN_OPERS = tuple(map(lambda func: "__i" + func[2:], BIN_OPERS))

class tkn:
    opening = "[{("
    closing = "]})"

    @staticmethod
    def split_with(string, delimiter):
        not_quoted = tkn.out_quotes(string)
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

    @staticmethod
    def tokenise(string):
        not_quoted = tkn.out_quotes(string) #Remove all text in quotation marks and apostrophes
        stripped = "" #Spaces removed
        for i in range(len(string)):
            if string[i] == " ":
                if not i in not_quoted:
                    stripped += string[i]
            else:
                stripped += string[i]
        string = stripped

        separated = tkn.split_with(string, ";")
        for i in range(len(separated)):
            separated[i] = tkn.split_with(separated[i], ":")
            separated[i][0] = list(tkn.split_with(separated[i][0], ","))
        return separated

    @staticmethod
    def method(multi_key_dict, obj, key):
        type_ = type(obj)
        for k_tuple in multi_key_dict.keys():
            evaluated = tuple(map(eval, k_tuple))
            if type_ in evaluated:
                return multi_key_dict[k_tuple]
        raise KeyError("Key '{}' not found".format(key))

    @staticmethod
    def out_quotes(string):
        indexes = [i for i in range(len(string)) if string[i] == '"']
        inside = []
        iterate = tuple(range(0, len(indexes), 2))
        for i in iterate:
            inside += tuple(range(indexes[i], indexes[i + 1] + 1))
        outside = [i for i in range(len(string)) if not i in inside]
        return outside

    @staticmethod
    def unpack(tokens):
            individual = {}
            for i in range(len(tokens)):
                for x in range(len(tokens[i][0])):
                    individual[tokens[i][0][x]] = tokens[i][1]
            return individual

    @staticmethod
    def run(dict_, obj):
        for k, v in dict_.items():
            if eval(k) == type(obj):
                return eval(v)
        raise NameError("Behaviour of type '{}' is not defined".format(type(obj).__name__))

def dunders(obj): #Lists all dunder methods of an object
    return tuple(filter(lambda func: func.startswith("__") and func.endswith("__"), dir(obj)))

def find_args(func): #Number of arguments required. Note that extra arguments are ignored, like JavaScript
##    print("func:", func)
    try:
        return len(signature(func).parameters) #signature: inspect.signature
    except ValueError: #Could not find a signtature - invalid
        raise NoSignatureError("Function '{}' does not have a signature so the number of arguments required is not known".format(func))
  
def make_func(this, func, evaluator, wrapper, *args):
##    print("\nCalled")
    evaluated = evaluator(this)
    if evaluated == this: #If unchanged, it finds its own method, resulting in recursion :(
        raise RecursionError("Statement entered results in recursion - statement type of class to be decorated must not equal 'obj'")
    method = getattr(evaluator(this), func)
##    print("Amount:", extra_args)
    
    to_call = getattr(evaluated, func)
##    print("Type:", type(to_call))
##    print("Will call:", to_call)
    return wrapper(to_call(*map(evaluator, args)))

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
##        class Decorated(cls): #Temporary decorated class that contains all of the
        for func in self.funcs: #func is a string
##            print("Iterated with", func)
            code = lambda this, *args, func = func: make_func(this, func, evaluator, self.wrapper, *args)
            setattr(cls, func, code)
                #i.e. self.num.__add__(other.num)
                #Note that 'this' is used to distinguish from 'self' defined in the class
        return cls #Turn the class into the decorated class


if __name__ == "__main__":
    @construct(args = ("a", "b"), kwargs = (("c", 3), ("d", 4), ("e", 5)))
    class Foo:
        def __init__(self):
            print("Initialised")
            print(self.a, self.b, self.c, self.d, self.e)
    
    test = Foo(1, 2, 9, e = 10)
