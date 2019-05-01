"""
Alex Scorza 2019
Avoids doing something like this:

    def __init__(genus, species, legs, eyes, speed):
        self.genus = genus
        self.species = species
        self.legs = legs
        self.eyes = eyes
        self.speed = speed

BECAUSE THAT WOULD BE  W E T
"""

__all__ = ("construct",)

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
                setattr(cls, k, v)
            func(self)
        setattr(cls, "__init__", init_wrapper)
        return cls
    return decorator

if __name__ == "__main__":
    @construct(args = ("a", "b"), kwargs = (("c", 3), ("d", 4)))
    class Foo:
        def __init__(self):
            print(self.a, self.b, self.c, self.d)
    
    test = Foo(1, 2, 8)
