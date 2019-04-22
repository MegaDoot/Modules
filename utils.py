class DotDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__

def i_iter(iterable):
    return zip(iterable, range(len(iterable)))

def isiterable(obj):
    try:
        iter(obj)
        return True
    except TypeError:
        return False