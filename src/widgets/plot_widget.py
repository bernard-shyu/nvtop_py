import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class PlotWidget(FigureCanvas):
    def __init__(self, config):
        self.figure = Figure()
        self.ax = self.figure.add_subplot(111)
        super().__init__(self.figure)
        self.max_points = config.get('X_data_points', 1000)
        self.time_data = np.zeros(self.max_points)
        self.temperature_data = np.zeros(self.max_points)
        self.power_draw_data = np.zeros(self.max_points)
        self.memory_used_data = np.zeros(self.max_points)
        self.utilization_data = np.zeros(self.max_points)
        self.current_index = 0

    def update_plot(self, stats):
        # Update historical data
        self.time_data = np.roll(self.time_data, -1)
        self.temperature_data = np.roll(self.temperature_data, -1)
        self.power_draw_data = np.roll(self.power_draw_data, -1)
        self.memory_used_data = np.roll(self.memory_used_data, -1)
        self.utilization_data = np.roll(self.utilization_data, -1)

        self.time_data[-1] = self.current_index
        self.temperature_data[-1] = stats.get('temperature', 0)
        self.power_draw_data[-1] = stats.get('power_draw', 0)
        self.memory_used_data[-1] = stats.get('memory_used', 0)
        self.utilization_data[-1] = stats.get('utilization', 0)
        self.current_index += 1

        # Plot data
        self.ax.clear()
        self.ax.plot(self.time_data, self.temperature_data, label='Temperature', color='r')
        self.ax.plot(self.time_data, self.power_draw_data, label='Power Draw', color='g')
        self.ax.plot(self.time_data, self.memory_used_data, label='Memory Used', color='b')
        self.ax.plot(self.time_data, self.utilization_data, label='Utilization', color='y')
        self.ax.legend()
        self.ax.set_title('GPU Statistics Over Time')
        self.draw()
