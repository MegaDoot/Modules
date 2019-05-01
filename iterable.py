import inspect
def is_iter(val):
  if hasattr(val, "__iter__") and not inspect.isclass(val):
    return True
  return False
if __name__ == "__main__":
  while 1:
   print(is_iter(eval(input("\n> "))))
