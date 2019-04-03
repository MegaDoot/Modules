import re

__all__ = ("tokenise",)

opening = "[{("
closing = "]})"

regexps = (r"^\s*", r"^\w+", r"^\s*-\s*")
args_re = (r"^\b+", r"^\s*:\s*")

def tokenise(string):
    parts = []
    for regex in regexps:
        found = re.findall(regex, string)
        parts.append(found[0] if len(found) == 1 else "")
        string = string[len(parts[-1]):]
    print(parts)
    print(string)
    brackets = 0
    for char in string:
        if char in opening:
            brackets += 1
        elif chars in closing:
            brackets -= 1

def out_quotes(string):
    positions = []
    for i in range(len(string)):
        if string[i] == '"':
            positions.append(i)
    print(positions)

out_quotes('[char + "hi" for char in "hello"]')

#tokenise("obj - type(obj): obj.num; int, float: obj")
