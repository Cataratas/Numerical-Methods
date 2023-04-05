import numpy


def compTrapezoidal(a, b, n):
    h = (b - a) / n
    x = numpy.linspace(a, b, num=n + 1)
    y = h * (function(x[0]) + function(x[n])) / 2
    i = 1
    while i != n:
        y = y + h * function(x[i])
        i += 1
    return y


def oneThirdSimp(a, b, n):
    h = (b - a) / n
    x = numpy.linspace(a, b, num=n + 1)
    y = function(x[0])

    for i in range(int(n / 2)):
        j = 2 * i + 1
        y = y + 4 * (function(x[j]))

    for i in range(1, int(n / 2)):
        j = 2 * i
        y = y + 2 * (function(x[j]))

    y = y + function(x[n])
    y = h * y / 3

    return y


def threeOctaveSimp(a, b, n):
    h = (b - a) / n
    x = numpy.linspace(a, b, num=n + 1)
    y = function(x[0])

    for i in range(1, n):
        y = y + 2 * (function(x[i])) if (i % 3 == 0) else y + 3 * (function(x[i]))
    y = y + (function(x[n]))
    y = h * y * 3 / 8
    return y


fString, dictionary = "", {"numpy": numpy}
function = lambda x: eval(fString, dictionary, dict(x=x))


def calculate(functionStr: str, interval: tuple, points: str) -> list:
    global fString, dictionary
    fString = functionStr

    results = []
    methodNames = ["Trapezoidal", "1/3 Simpson", "3/8 Simpson"]
    for i, method in enumerate([compTrapezoidal, oneThirdSimp, threeOctaveSimp]):
        result = {"name": methodNames[i], "value": float, "error": False}
        while True:
            try:
                result["value"] = method(eval(interval[0], dictionary), eval(interval[1], dictionary), int(points))
                break
            except (ValueError, RuntimeError) as error:
                result["value"], result["error"] = str(error), True
            except NameError as error:
                var = str(error).split()[1].strip("'")
                exec(f"dictionary.update({var} = numpy.{var})")
        results.append(result)

    return results
