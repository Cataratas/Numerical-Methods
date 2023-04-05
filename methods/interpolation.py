from scipy.interpolate import interp1d
import numpy


def calculate(functionStr: str, X: list, interpolate: list):
    result = []

    for i, r in enumerate(numpy.interp(interpolate, X, [(eval(functionStr, {'x': i})) for i in X])):
        result.append({'x': interpolate[i], 'y': r})

    return result
