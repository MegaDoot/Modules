__all__ = ("to_static", "to_cls")

def edit(cls, function):
    print(function)
    for func in filter(lambda name: not (name.startswith("__") and name.endswith("__")), dir(cls)):
        print(func, type(func))
        setattr(cls, func, function(getattr(cls, func)))
        print(func)
    return cls

def to_static(cls):
    return edit(cls, staticmethod)

def to_cls(cls):
    return edit(cls, classmethod)

if __name__ == "__main__":
    @to_static
    class Foo:
        def bar():
            print("Howdy")
