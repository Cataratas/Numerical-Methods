import pandas
import numpy
from scipy import optimize
import statsmodels.api as sm


def rSquared(x, y, degree):
    xpoly = numpy.column_stack([x**i for i in range(degree+1)])
    return sm.OLS(y, xpoly).fit().rsquared


def fixString(function: str) -> str:
    function = function[function.find("\n"):].replace("x", "* x")

    numberOfX = function.count("x")
    newF = ""
    for x in function.split():
        if x == "x" and numberOfX > 1:
            newF += f"{x}"
            newF += f"**{numberOfX} "
            numberOfX -= 1
        else:
            newF += f"{x} "
    return newF


def calculate(x: list, y: list, order: str, functionType: str):
    result = {"function": "", "r2": "", "error": False, "evFunction": None}
    try:
        data = pandas.DataFrame({"x": x, "y": y})
        if functionType == "Polynomial":
            result["evFunction"] = numpy.poly1d(numpy.polyfit(data.x, data.y, int(order)))
            result["function"] = fixString(str(result["evFunction"]))
            result["r2"] = rSquared(data.x, data.y, int(order))

        elif functionType == "y = A*e^(B*x)":
            params, cv = optimize.curve_fit(lambda x, m, t: m * numpy.exp(t * x), data.x, data.y)
            m, t = params

            result["function"] = f"{m} * e^({t} * x)"
            result["evFunction"] = lambda x: eval(f"{m}*numpy.exp({t}*x)", {"numpy": numpy}, dict(x=x))
            result["r2"] = rSquared(data.x, data.y, 1)

        elif functionType == "y = A+B*log(x)":
            params, cv = optimize.curve_fit(lambda t, a, b: a + b * numpy.log(t), data.x, data.y)
            m, t = params

            result["function"] = f"{m} + {t} * log(x)"
            result["evFunction"] = lambda x: eval(f"{m}+{t}*numpy.log(x)", {"numpy": numpy}, dict(x=x))
            result["r2"] = rSquared(data.x, data.y, 1)

    except (TypeError, ValueError) as e:
        result["function"], result["error"] = str(e), True

    return result
