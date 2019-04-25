def run(cmd:str, **kwargs):
    cmds = cmd.split("&")
    returns = []
    for cmd in cmds:
        tokens = shlex.split(cmd)
        for i in range(len(tokens)):
            if tokens[i] == "cd..":
                del tokens[i]
                tokens.insert(i, "cd")
                tokens.insert(i + 1, "..")
                
        if tokens[0] == "cd" and len(tokens) == 2:
            print(tokens[1])
            os.chdir(tokens[1])
        else:
            obj = sp.Popen(tokens, stdout = sp.PIPE, stderr = sp.PIPE, creationflags = 0x08000000, shell = True, **kwargs)
##            print("Output:", obj.communicate(), end = "\n")
            returns.append(obj.communicate()[0].decode("UTF-8").rstrip("\r\n"))
    return "\n".join(returns)
