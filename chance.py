from random import randrange

def places(decimal):
    if int(decimal) == decimal:
        return 0
    return len(str(float(decimal)).split(".")[1])

def chance(decimal):
    mul = 10 ** places(decimal)
    return randrange(0, mul) < mul * decimal

if __name__ == "__main__":
    vals = []
    iters = 100000
    probability = 0.5
    for i in range(iters):
        vals.append(chance(probability))

    predicted = int(iters * probability)
    actual = vals.count(True)
    print("Predicted {}, got {}, off by {}%".format(predicted, actual, round(100 * abs((actual / predicted) - 1), 4)))
