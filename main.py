import tkinter
import numpy as np
from tkinter import ttk
import sv_ttk
from generateGraph import graphWindow
from results import rootWindow, integrationWindow, curveWindow, interpolationWindow


def addButtons(tab, text1: str, text2: str, command1, command2):
    frame = tkinter.Frame(tab)
    graph, calculate = ttk.Button(frame, text=text1, command=command1), ttk.Button(frame, text=text2, command=command2)
    frame.grid(row=3, column=1, sticky="e")
    graph.grid(row=0, column=1, padx=6, pady=0, sticky="e")
    calculate.grid(row=0, column=2, padx=6, pady=0, sticky="e")


class App(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)

        for index in (0, 1, 2):
            self.columnconfigure(index=index, weight=1)
            self.rowconfigure(index=index, weight=1)

        self.setup_widgets()

    def setup_widgets(self):
        def rootButton():
            rootWindow(function.get(), (startInterval.get(), endInterval.get()), epsilon.get(), iterations.get())

        def integrationButton():
            integrationWindow(function3.get(), (startInterval3.get(), endInterval3.get()), numberPoints.get())

        def curveButton():
            curveWindow([float(x) for x in X.get().split(",")], [float(x) for x in Y.get().split(",")], order.get(), functionType.get())

        def graphButtonRoot():
            graphWindow(function.get(), (startInterval.get(), endInterval.get()), line=True)

        def graphButtonIntegration():
            graphWindow(function3.get(), (eval(startInterval3.get(), dictionary), eval(endInterval3.get(), dictionary)), points=numberPoints.get())

        def graphButtonCurve():
            assert X.get() != "" and Y.get() != ""
            x, y = [float(x) for x in X.get().split(",")], [float(x) for x in Y.get().split(",")]

            graphWindow("", (min(x), max(x)), x, y, order.get(), functionType.get())

        def graphButtonInterpolate():
            f = function2.get()
            x = [float(x) for x in X2.get().split(",")]
            interp = [float(x) for x in interpolate.get().split(",")]

            graphWindow(f, (int(min(min(x), min(interp))), int(max(max(x), max(interp)))), x, interp, interp=True)

        def interpolateButton():
            interpolationWindow(function2.get(), [float(x) for x in X2.get().split(",")], [float(x) for x in interpolate.get().split(",")])

        def calculateSystem():
            pass

        paned = ttk.PanedWindow(self)
        paned.grid(row=0, column=0, pady=(0, 0), sticky="nsew", rowspan=5)
        pane_2 = ttk.Frame(self, padding=0)
        paned.add(pane_2, weight=1)
        notebook = ttk.Notebook(pane_2, width=675)
        notebook.pack(fill="both", expand=True)

        tab1 = ttk.Frame(notebook)
        notebook.add(tab1, text="Root Finding")

        tab2 = ttk.Frame(notebook)
        notebook.add(tab2, text="Interpolation")

        tab3 = ttk.Frame(notebook)
        notebook.add(tab3, text="Integration")

        tab4 = ttk.Frame(notebook)
        notebook.add(tab4, text="Curve Fitting")

        function = ttk.Entry(tab1)
        ttk.Label(tab1, text="Function:").grid(row=0, column=0)
        function.grid(row=0, column=1, padx=15, pady=12, ipadx=135)

        rangeFrame = tkinter.Frame(tab1)
        ttk.Label(tab1, text="Interval:").grid(row=1, column=0, padx=35)
        startInterval, endInterval = ttk.Entry(rangeFrame, width=5), ttk.Entry(rangeFrame, width=5)
        rangeFrame.grid(row=1, column=1, sticky="nsew")
        startInterval.grid(row=1, column=1, ipadx=5, padx=15)
        ttk.Label(rangeFrame, text="-").grid(row=1, column=2, ipadx=7)
        endInterval.grid(row=1, column=3, ipadx=5)

        ttk.Label(tab1, text="Epsilon:").grid(row=2, column=0, padx=35, pady=20)
        epsilon = ttk.Combobox(tab1, state="readonly", values=[f"10**{-i}" for i in range(1, 17)], width=9)
        epsilon.current(15)
        epsilon.grid(row=2, column=1, padx=15, pady=0, sticky="w")

        ttk.Label(tab1, text="Iterations:").grid(row=3, column=0)
        iterations = ttk.Entry(tab1, width=12)
        iterations.insert(0, "500")
        iterations.grid(row=3, column=1, padx=15, sticky="w")

        addButtons(tab1, "Graph", "Calculate", graphButtonRoot, rootButton)

        function2 = ttk.Entry(tab2)
        ttk.Label(tab2, text="Function:").grid(row=0, column=0, padx=32)
        function2.grid(row=0, column=1, padx=15, pady=12, ipadx=135)
        X2 = ttk.Entry(tab2)
        ttk.Label(tab2, text="X:").grid(row=1, column=0)
        X2.grid(row=1, column=1, padx=15, ipadx=135)
        interpolate = ttk.Entry(tab2)
        ttk.Label(tab2, text="Interpolate:").grid(row=2, column=0, pady=12)
        interpolate.grid(row=2, column=1, padx=15, ipadx=135, pady=12)

        addButtons(tab2, "Graph", "Calculate", graphButtonInterpolate, interpolateButton)

        function3 = ttk.Entry(tab3)
        ttk.Label(tab3, text="Function:").grid(row=0, column=0)
        function3.grid(row=0, column=1, padx=15, pady=12, ipadx=135)

        rangeFrame3 = tkinter.Frame(tab3)
        ttk.Label(tab3, text="Interval:").grid(row=1, column=0, padx=35)
        startInterval3, endInterval3 = ttk.Entry(rangeFrame3, width=5), ttk.Entry(rangeFrame3, width=5)
        rangeFrame3.grid(row=1, column=1, sticky="nsew")
        startInterval3.grid(row=1, column=1, ipadx=5, padx=15)
        ttk.Label(rangeFrame3, text="-").grid(row=1, column=2, ipadx=7)
        endInterval3.grid(row=1, column=3, ipadx=5)

        numberPoints = ttk.Entry(tab3, width=12)
        ttk.Label(tab3, text="Points:").grid(row=2, column=0)
        numberPoints.grid(row=2, column=1, padx=15, pady=12, sticky="w")

        addButtons(tab3, "Graph", "Calculate", graphButtonIntegration, integrationButton)

        X = ttk.Entry(tab4)
        ttk.Label(tab4, text="X:").grid(row=0, column=0, pady=20)
        X.grid(row=0, column=1, padx=15, ipadx=135)
        Y = ttk.Entry(tab4)
        ttk.Label(tab4, text="Y:").grid(row=1, column=0)
        Y.grid(row=1, column=1, padx=15, ipadx=135)

        ttk.Label(tab4, text="Type:").grid(row=2, column=0, pady=20, padx=42)
        functionType = ttk.Combobox(tab4, state="readonly", values=["Polynomial", "y = A*e^(B*x)", "y = A+B*log(x)"])
        functionType.grid(row=2, column=1, padx=15, pady=0, sticky="w")
        functionType.current(0)

        ttk.Label(tab4, text="Order:", state='normal' if functionType.get() == "Polynomial" else 'disabled').grid(row=3, column=0)
        order = ttk.Combobox(tab4, state="readonly", values=[str(i) for i in range(2, 7)], width=4)
        order.grid(row=3, column=1, padx=15, pady=0, sticky="w")
        order.current(0)

        addButtons(tab4, "Graph", "Calculate", graphButtonCurve, curveButton)


def main():
    screen = tkinter.Tk()
    screen.title("Numerical Methods")
    sv_ttk.use_light_theme()

    app = App(screen)
    app.pack(fill="both", expand=True)

    screen.resizable(False, False)
    windowWidth, windowHeight = 575, 235
    xCoordinate = int((screen.winfo_screenwidth() / 2) - (windowWidth / 2))
    yCoordinate = int((screen.winfo_screenheight() / 2) - (windowHeight / 2))
    screen.geometry(f"{windowWidth}x{windowHeight}+{xCoordinate}+{yCoordinate}")

    screen.mainloop()


if __name__ == "__main__":
    dictionary = {"pi": np.pi, "cos": np.cos, "sin": np.sin, "sen": np.sin, "tan": np.tan, "e": np.e, "log": np.log, "sqrt": np.sqrt,
                  "cbrt": np.cbrt}
    main()
