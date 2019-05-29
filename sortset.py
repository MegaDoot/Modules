class sortset(set):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._sorted = tuple(sorted(self))
    
    def __getitem__(self, key):
        return self._sorted.__getitem__(key)
    
    def union(self, *others):
        return sortset(super().union(*others))

    def __or__(self, other):
        return sortset(super().__or__(other))

    def intersection(self, *others):
        return sortset(super().intersection(*others))

    def __and__(self, other):
        return sortset(super().__and__(other))

    def difference(self, *others):
        return sortset(super().difference(*others))
        
    def __sub__(self, other):
        return sortset(super().__sub__(other))
    
    def symmetric_difference(self, other):
        return sortset(super().symmetric_difference(other))

    def __xor__(self, other):
        return sortset(super().__xor__(other))
    
    def copy(self):
        return sortset(super().copy())
    
    def __str__(self):
        return str(self._sorted)

if __name__ == "__main__":
    from random import randrange as rand
    def randlist(max_len, max_item_size):
        return [rand(max_item_size) for i in rand(max_len)]

    a = sortset((2, 4, 8, 3, 2))
    print("A:", a)
    b = {5, 6, 3, 2}
    print("B:", b)
    print("A & B:", a & b)
    print("A | B:", a | b)