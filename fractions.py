from math import sqrt, floor
from functools import reduce

def findFactors(num:int) -> list:
    num = num*-1 if num < 0 else num
    factors = []
    for i in range(1,floor(sqrt(num))+1):
        if num%i == 0:
            factors += [i,num//i]
    return factors

def sharedFactors(a:int,b:int) -> list:
    commonFactors=[]
    aFactors, bFactors = findFactors(a), findFactors(b)
    for aFactor in aFactors:
        if aFactor in bFactors:
            commonFactors.append(aFactor)
    return commonFactors

def hcf(a:int,b:int) -> int:
    commonFactors = sharedFactors(a,b)
    if commonFactors:
        return max(commonFactors)
    else: 
        return False

def primeFactors(num:int) -> list:
    num = num*-1 if num < 0 else num
    primesFactorsFound = []
    for i in range(2,floor(sqrt(num))+1):
        if num%i == 0:
            primesFactorsFound.append(i)
            primesFactorsFound += primeFactors(num//i)
            break
    if primesFactorsFound:
        return primesFactorsFound
    else:
        return [num]

def listProduct(ls:list) -> int:
    return reduce(lambda a,b: a*b, ls)

def lcm(a:int,b:int) -> int: 
    aPrimes, bPrimes = primeFactors(a), primeFactors(b)
    for aPrime in aPrimes:
        if aPrime in bPrimes:
            del bPrimes[bPrimes.index(aPrime)]
    return listProduct(aPrimes + bPrimes)

class Fraction:
    def __init__(self, numerator, denominator=1):
        if not (type(numerator) in (float,int) and type(numerator) in (float,int)):
            raise TypeError
        self.numerator = numerator
        self.denominator = denominator
        self = self.simplify()
        #Still need to handle input of float

    def __repr__(self):
        return str(self.numerator)+"/"+str(self.denominator)    
        
    def __str__(self):
        return str(self.numerator)+"/"+str(self.denominator)+" or "+str(self.getFloat())

    def __add__(self,other):
        self, other = self.equaliseDenominators(other)
        return Fraction(self.numerator+other.numerator,self.denominator)
    
    def __neg__(self):
        self.numerator = self.numerator * -1
        return self
    
    def __sub__(self,other):
        return other.__neg__().__add__(self)
    
    def __mul__(self,other):
        other = other if type(other) == Fraction else Fraction(other)
        return Fraction(self.numerator * other.numerator, self.denominator * other.denominator)
    
    def __truediv__(self,other):
        other = other if type(other) == Fraction else Fraction(other)
        return (self * other.flip()).simplify()
        
    def __pow__(self,power):
        if power < 0:
            power *= -1
            self = self.flip()
        elif power == 0:
            return 1
        self.numerator **= power
        self.denominator **= power
        return self

    def __mod__(self,divider):
        return (self/divider).fractPart()*divider
    
    def __floordiv__(self,divider):
        newFract = self.__truediv__(divider)
        return newFract.wholePart()

    def simplify(self):
        multiplier = hcf(self.numerator,self.denominator)
        if multiplier:
            self.numerator //= multiplier
            self.denominator //= multiplier
        return self

    def getFloat(self):
        return self.numerator/self.denominator

    def flip(self):
        return Fraction(self.denominator,self.numerator)

    def equaliseDenominators(self,other):
        other = other if type(other) == Fraction else Fraction(other)
        newDenominator = lcm(self.denominator,other.denominator)
        selfMultiplier, otherMultiplier = newDenominator//self.denominator, newDenominator//other.denominator
        self.numerator, other.numerator = self.numerator*selfMultiplier, other.numerator*otherMultiplier
        self.denominator, other.denominator = newDenominator, newDenominator
        return self, other

    def wholePart(self):
        return self.numerator // self.denominator

    def fractPart(self):
        self.numerator %= self.denominator
        return self

alexFraction = Fraction(5,6)
print("Alex's fraction is:",alexFraction)
alexBetterFraction = Fraction(7,32)
print("Alex's better fraction is:",alexBetterFraction)