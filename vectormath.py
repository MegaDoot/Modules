from math import sqrt, sin as sinr, cos as cosr, atan as atanr, radians, degrees
sin = lambda x: sinr(radians(x))
cos = lambda x: cosr(radians(x))
atan = lambda x: degrees(atanr(x))

def from_polar(size, angle):
    return [sin(angle) * size, cos(angle) * size]

def to_polar(a):
    return {"size": size(a), "angle": angle(a)}

def size(a):
    return sqrt(sum(val**2 for val in a))

def angle(a):
    return 90 if a[1] == 0 else atan(a[0]/a[1])

def _vectorise_binary(func):
    def new_func(a, b):
        try:
            return [func(val_a, val_b) for val_a, val_b in zip(a, b)]
        except TypeError:
            return [func(val, b) for val in a]
        
    return new_func

def _iterate(func):
    def new_func(a, b):
        a = func(a, b)
    return new_func

funcs = {
    "add": lambda a, b: a + b,
    "sub": lambda a, b: a - b,
    "mul": lambda a, b: a * b,
    "div": lambda a, b: a / b,
    "power": lambda a, b: a ** b
}

for name, func in funcs.items():
    vectored = _vectorise_binary(func)
    globals()[name] = vectored

if __name__ == "__main__":
    for testA, testB in (([1, 5, 7], [1, 5, 7]), ([2, 5, 4], 8)):
        print("A:", testA, "B:", testB)
        for funcName in funcs.keys():
            print(funcName.title()+":", globals()[funcName](testA, testB))
        print()

    testA = [2, 3]
    print("Cart:",testA)
    resultA = to_polar(testA)
    print("to_polar:",resultA)
    print("from_polar:", from_polar(**resultA))
