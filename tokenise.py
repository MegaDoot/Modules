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
    not_quoted = out_quotes(string) #Remove all text in quotation marks and apostrophes
    print(not_quoted)
    stripped = "" #Spaces removed
    for i in range(len(string)):
        if string[i] == " ":
            if not i in not_quoted:
                stripped += string[i]
        else:
            stripped += string[i]
    string = stripped
    not_quoted = out_quotes(string) #Needs to re-calculate

    sep_positions = []
    for pos in not_quoted:
        if string[pos] == ";":
            sep_positions.append(pos)
    print(sep_positions)
    split = [""]
    for i in range(len(string)):
        if i in sep_positions:
            split.append("")
        else: #Skips semicolons
            split[-1] += string[i]

    print(split)

    

def out_quotes(string):
    print("max =", len(string))
    indexes = [i for i in range(len(string)) if string[i] == '"']
    inside = []
    iterate = tuple(range(0, len(indexes), 2))
    for i in iterate:
        inside += tuple(range(indexes[i], indexes[i + 1] + 1))
    outside = [i for i in range(len(string)) if not i in inside]
    return outside

if __name__ == "__main__":
    tokenise('obj - type(obj): obj.num; int, float: obj; str: "hello there,"  + obj')
