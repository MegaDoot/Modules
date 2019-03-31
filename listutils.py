from typing import Optional, Callable

def no_repeats(array:list, comp:Callable[[list, list], bool] = lambda a, b: a == b) -> list:
    return _repeat_sweep(_repeat_sweep(array, comp)[::-1], comp)

def _repeat_sweep(array:list, comp:Callable[[list, list], bool]) -> list:
    new_array = []
    for item, i in zip(array, range(len(array))):
        if not any(comp(item, comp_to) for comp_to in array[i+1:]):
            new_array.append(item)
    return new_array

def matches(a:list, b:list, overlap:Callable[[list, list], Optional[list]] = lambda a, b: a if a == b else None) -> list:
    new_array = []
    for item_a in a:
        for item_b in b:
            result = overlap(item_a, item_b)
            if result:
                new_array.append(result)
    return new_array

def contained_in(sub_set:list, super_set:list) -> bool:
    return all(item in super_set for item in sub_set)

def common_elements(a:list, b:list) -> Optional[list]:
    if contained_in(a, b):
        return a
    elif contained_in(b, a):
        return b

__all__ = ("no_repeats", "matches", "contained_in", "common_elements")
