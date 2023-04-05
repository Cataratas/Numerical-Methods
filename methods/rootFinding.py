from sympy import diff, symbols
import numpy


def functionRange(a, b, m):
    if function(m) * function(a) < 0:
        b = m
    else:
        a = m
    return a, b


def Bissecao(a, b, e, maxIter, i=0):
    if function(a) * function(b) >= 0:
        return "Error"
    while abs(function(m := (a + b) / 2)) > e and i < maxIter:
        a, b = functionRange(a, b, m)
        i += 1
    return m, i


def Secantes(a, b, e, maxIter, i=0):
    while abs(function(m := (a - function(a) * (b - a) / (function(b) - function(a))))) > e and i < maxIter:
        a, b = functionRange(a, b, m)
        i += 1
    return m, i


def Newton(a, b, e, maxIter, i=0):
    m = (a + b) / 2
    while abs(function(m)) > e and i < maxIter:
        m -= function(m) / derivative(m)
        i += 1
    return m, i


fString, dictionary = "", {"numpy": numpy}
function = lambda x: eval(fString, dictionary, dict(x=x))
derivative = lambda x: eval(str(diff(fString, symbols("x"))), dictionary, dict(x=x))


def calculate(functionStr: str, interval: tuple, epsilon: str, maxIter: int):
    global fString, dictionary
    fString = functionStr

    results = []
    for method in [Bissecao, Secantes, Newton]:
        result = {"name": method.__name__, "value": float, "error": False}
        while True:
            try:
                result["value"] = method(eval(interval[0], dictionary), eval(interval[1], dictionary), eval(epsilon), maxIter)
                if result["value"] == "Error":
                    result["error"] = True
                break
            except (ValueError, RuntimeError) as error:
                result["value"], result["error"] = str(error), True
                break
            except NameError as error:
                print(error)
                var = str(error).split()[1].strip("'")
                exec(f"dictionary.update({var} = numpy.{var})")
        results.append(result)

    return results
