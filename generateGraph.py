import tkinter
import numpy
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.pyplot import xlim
from mpmath import linspace
from sv_ttk import root
from methods import curve, interpolation


def graphWindow(function: str, interval: tuple, xx: list = None, yy: list = None, order: str = "", functionType: str = "", line: bool = False, points=.1, interp: bool = False):
    window = tkinter.Toplevel(root)
    window.geometry("435x300")
    window.title(f"Graph | ({interval[0]}, {interval[1]})")

    fig = Figure(figsize=(5, 5), dpi=100)
    graph = fig.add_subplot(111)

    numberOfPoints = float(interval[1] + 1) / int(points) if points != .1 else .1
    x, y, dictionary = list(numpy.arange(float(interval[0]), float(interval[1]) + 1, numberOfPoints)), [], {"numpy": numpy}

    if function != "":
        f = lambda x: eval(function, dictionary, dict(x=x))
        while True:
            try:
                y = [f(i) for i in numpy.arange(float(interval[0]), float(interval[1]) + 1, numberOfPoints)]
                break
            except NameError as error:
                var = str(error).split()[1].strip("'")
                exec(f"dictionary.update({var} = numpy.{var})")
    if not function:
        results = curve.calculate(xx, yy, order, functionType)
        resultF = lambda x: eval(results["function"], dictionary, dict(x=x))
        resultsX = numpy.arange(int(min(xx)) - 1, int(max(xx)) + 1, .1)
        resultsY = [results["evFunction"](i) for i in resultsX]

        graph.plot(xx, yy, ".", color="red")
        graph.plot(resultsX, resultsY)
        y, x = yy, xx
    if interp:
        results = interpolation.calculate(function, xx, yy)
        for r in results:
            graph.plot(r['x'], r['y'], ".", color="red")

    xlim(float(interval[0]), float(interval[1]))
    if function:
        graph.plot(x, y)

    if line:
        graph.axhline(0, linewidth=.5, color="gray")

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()
