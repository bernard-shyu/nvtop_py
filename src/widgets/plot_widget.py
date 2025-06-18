import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class PlotWidget(FigureCanvas):
    def __init__(self):
        self.figure = Figure()
        self.ax = self.figure.add_subplot(111)
        super().__init__(self.figure)

    def update_plot(self, stats):
        self.ax.clear()
        metrics = ['temperature', 'power_draw', 'memory_used', 'utilization']
        values = [stats.get(m, 0) for m in metrics]
        self.ax.bar(metrics, values)
        self.ax.set_title('GPU Statistics')
        self.draw()
