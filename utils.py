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
    
def unpack_nested(seq, unpack_check = None):
    if len(seq) == 1:
        return seq[0]
    results = []
    for item in seq:
        if (not unpack_check) or unpack_check(item):
            try:
                results += unpack_nested(item, unpack_check)
                continue
            except TypeError:
                pass
        results.append(item)
    return results

if __name__ == "__main__":
    print("Unpack Nested:")
    dataset = [
        {
            "name": "Any iterable",
            "data": (["ab", [], [["b", "ded"], "c"]],),
        }, {
            "name": "Lists only",
            "data": (["ab", [], [["b", "ded"], "c"]], lambda obj: isinstance(obj, list)),
        }
        
    ]
    for test in dataset:
        print(str(test["name"])+":")
        print(" Initial data:", ", ".join(str(item) for item in test["data"]))
        print(" Result:", unpack_nested(*test["data"]))