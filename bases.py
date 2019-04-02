""
Note the following:
Decimal places are not allowed because I am lazy.
Not all operators are used
Consider yourselves honoured that I took the time to add augmented assigment - 'ctrl+c', 'ctrl+v' and 'i' take a lot of effort
"""
class Base:
    def __init__(self,num,base = 10): #ACCEPTS 1 OR 2 ARGUMENTS, base defaults to 10
        self.num = str(num)
        self.base = base
        check(self.num,self.base)

    def in_base(self,to): #Displays in base, for user/not referenced
        return from_ten(to_ten(self.num,self.base),to)

    def to_base(self,to): #Uses self.num and self.base, changes to base
        self.num = self.in_base(to)
        self.base = to
        check(self.num,self.base) #Ensure that it only contains the correct characters
    
    #Note that any magic/dunder methods will return base 10 number/decimal
    def __add__(self,other):
        return eval(calc("+"))
    
    def __sub__(self,other):
        return eval(calc("-"))
    
    def __mul__(self,other):
        return eval(calc("*"))
    
    def __pow__(self,other):
        return eval(calc("**"))
    
    def __floordiv__(self,other):
        return eval(calc("//"))
    
    def __truediv__(self,other): #__div__ is not for Python 3.x
        return eval(calc("//")) #I can't be bothered to do decimals places
    
    def __mod__(self,other):
        return eval(calc("%"))

    def __eq__(self,other):
        return eval(calc("=="))

    def __iadd__(self,other):
        return eval(calc_base("+"))
    
    def __isub__(self,other):
        return eval(calc_base("-"))
    
    def __imul__(self,other):
        return eval(calc_base("*"))
    
    def __ipow__(self,other):
        return eval(calc_base("**"))
    
    def __ifloordiv__(self,other):
        return eval(calc_base("//"))
    
    def __itruediv__(self,other):
        return self.__ifloordiv__(other)
    
    def __imod__(self,other):
        return eval(calc_base("%"))
chars = "0123456789abcdefghijklmnopqrstuvwxyz" #Up to base 36

#Magic methods return new 'Base' object
def calc(oper): #More concise to add new magic methods
    return "to_ten(self.num,self.base)"+oper+"to_ten(other.num,other.base)"

def calc_base(oper):
    return "Base(to_ten(self.num,self.base)"+oper+"to_ten(other.num,other.base))"

def check(num,base):
    num = str(num)  
    if num[0] == "-": #Remove leading '-'
        num = num[1:]
    if not base in range(2,len(chars)+1):
        raise ValueError("Base of {} is invalid - must be between (and inclusive of 2 and {})".format(base,len(chars)))
    for x in str(num):
            if x not in chars or chars.index(x) > base:
                raise ValueError("Invalid character used: '{}' for base {}".format(str(x),base))

def to_ten(num,base):#Could be done in one line
    neg = 0
    if num[0] == "-":
        num = num[1:]
        neg = 1
    result = 0
    for n in reversed(range((len(str(num))))):
        result += chars.index((str(num)[len(str(num))-n-1]).lower())*(base**n)
        #'chars.index' to account for letters - numbers > 9 are letters
    if neg == 0:
        return result
    else:
        return -result

def from_ten(num,base): #Returns string as there may be letters
    num = int(num)
    values = []
    if num < 0:
        values += "-"
    n = 0
    while base**(n+1) < num: #Stops 1 before so it doesn't become too large
        n += 1
    
    for x in reversed(range(n+1)):#Must include last number
        values += [num//(base**x)] #Integer division and carry the remainder
        num %= base**x #Becomes remainder
    return "".join(chars[x] for x in values) #'chars[x]' not 'int(x)' in case of letter
a = Base("-f3",16) #-243
b = Base("-10101",2) #-21
c = Base(a-b) #Defauts to base 10
print(c.num)
c /= Base("2")
print(c.num)
print(Base("f",16) == Base("15",10))
