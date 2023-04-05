import tkinter
from tkinter import ttk
from sv_ttk import root
from methods import curve, integration, rootFinding, interpolation


def createWindow(size: str, title: str) -> tkinter.Toplevel:
    window = tkinter.Toplevel(root)
    window.geometry(size)
    window.title(title)
    return window


def addLabel(window: tkinter.Toplevel, text: str, variable: str, *, row: int, column: int, **kwargs):
    ttk.Label(window, text=text).grid(row=row, column=column, padx=10, pady=5)
    ttk.Label(window, text=variable, foreground="gray").grid(row=row, column=column + 1, padx=0, pady=5, **kwargs)


def rootWindow(function: str, interval: tuple, epsilon: str, maxIter: str):
    window = createWindow("500x160", "Root Finding Results")

    addLabel(window, "Function:", function, row=0, column=0, sticky="w")
    addLabel(window, "Interval:", f"{interval[0]} - {interval[1]}", row=1, column=0)
    addLabel(window, "Epsilon:", epsilon, row=1, column=2)
    addLabel(window, "Iterations:", maxIter, row=1, column=5)
    ttk.Separator(window).place(x=0, y=56, relwidth=1)

    results = rootFinding.calculate(function, interval, epsilon, int(maxIter))
    for i, r in enumerate(results):
        ttk.Label(window, text=f"{r['name']}: {r['value']}", foreground="red" if r["error"] else "black").place(x=10, y=60 + i * 25)


def interpolationWindow(function: str, x: list, interpolate: list):
    window = createWindow("500x160", "Interpolation Results")

    addLabel(window, "Function:", function, row=0, column=0, sticky="w")
    addLabel(window, "X:", str(x), row=1, column=0, sticky="w")
    addLabel(window, "Interp:", str(interpolate), row=1, column=2, sticky="w")
    ttk.Separator(window).place(x=0, y=56, relwidth=1)

    results = interpolation.calculate(function, x, interpolate)
    for i, r in enumerate(results):
        ttk.Label(window, text=f"X: {r['x']} : {r['y']}").place(x=10, y=60 + i * 25)


def integrationWindow(function: str, interval: tuple, points: str):
    window = createWindow("500x160", "Integration Results")

    addLabel(window, "Function:", function, row=0, column=0, sticky="w")
    addLabel(window, "Interval:", f"{interval[0]} - {interval[1]}", row=1, column=0)
    addLabel(window, "Points:", points, row=1, column=2)
    ttk.Separator(window).place(x=0, y=56, relwidth=1)

    results = integration.calculate(function, interval, points)
    for i, r in enumerate(results):
        ttk.Label(window, text=f"{r['name']}: {r['value']}", foreground="red" if r["error"] else "black").place(x=10, y=60 + i * 25)


def curveWindow(x: list, y: list, order: str, type: str):
    window = createWindow("500x160", "Curve Results")

    addLabel(window, "Function:", f"{type}{f' - {order} ' if type == 'Polynomial' else ''}", row=0, column=0, sticky="w")
    addLabel(window, "X:", str(x), row=1, column=0, sticky="w")
    addLabel(window, "Y:", str(y), row=2, column=0, sticky="w")

    ttk.Separator(window).place(x=0, y=84, relwidth=1)

    r = curve.calculate(x, y, order, type)
    if r["error"]:
        ttk.Label(window, text=r["function"], foreground="red").place(x=10, y=90)
    else:
        ttk.Label(window, text=r["function"]).place(x=10, y=90)
        ttk.Label(window, text=f"r²: {r['r2']}").place(x=10, y=115)
