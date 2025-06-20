import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class PlotWidget(FigureCanvas):
    def __init__(self, config):
        self.figure = Figure()
        self.ax = self.figure.add_subplot(111)
        super().__init__(self.figure)
        
        # Ensure we have at least 100 data points
        self.max_points = config.get('X_data_points', 1000)
        self.max_points = max(100, int(self.max_points))  # Ensure minimum of 100 points

        # Initialize circular buffer arrays
        self.buffer_index = 0
        self.time_data = np.zeros(self.max_points)
        self.temperature_data = np.zeros(self.max_points)
        self.power_draw_data = np.zeros(self.max_points)
        self.memory_used_data = np.zeros(self.max_points)
        self.utilization_data = np.zeros(self.max_points)
        self.data_count = 0

        # Initialize plot lines
        self.lines = {
            'temp': self.ax.plot([], [], label='Temperature', color='r')[0],
            'power': self.ax.plot([], [], label='Power Draw', color='g')[0],
            'memory': self.ax.plot([], [], label='Memory Used', color='b')[0],
            'util': self.ax.plot([], [], label='Utilization', color='y')[0]
        }
        
        # Configure plot
        self.ax.legend(loc='upper left')
        self.ax.set_title('GPU Statistics Over Time')
        self.ax.set_xlabel('Time Steps')
        self.ax.set_ylabel('Values')
        self.ax.grid(True)

    def update_plot(self, stats):
        # Update circular buffer
        current_time = self.data_count
        index = self.buffer_index
        
        self.time_data[index] = current_time
        self.temperature_data[index] = stats.get('temperature', 0)
        self.power_draw_data[index] = stats.get('power_draw', 0)
        self.memory_used_data[index] = stats.get('memory_used', 0)
        self.utilization_data[index] = stats.get('utilization', 0)
        
        # Update buffer index
        self.buffer_index = (index + 1) % self.max_points
        self.data_count += 1
        
        # Determine data range to plot
        valid_count = min(self.data_count, self.max_points)
        start_index = (self.buffer_index - valid_count) % self.max_points
        
        # Extract data in chronological order
        if start_index < 0:  # No wrap-around
            time_segment = self.time_data[:valid_count]
            temp_segment = self.temperature_data[:valid_count]
            power_segment = self.power_draw_data[:valid_count]
            memory_segment = self.memory_used_data[:valid_count]
            util_segment = self.utilization_data[:valid_count]
        else:  # Handle wrap-around
            time_segment = np.concatenate((
                self.time_data[start_index:self.max_points],
                self.time_data[:self.buffer_index]
            ))
            temp_segment = np.concatenate((
                self.temperature_data[start_index:self.max_points],
                self.temperature_data[:self.buffer_index]
            ))
            power_segment = np.concatenate((
                self.power_draw_data[start_index:self.max_points],
                self.power_draw_data[:self.buffer_index]
            ))
            memory_segment = np.concatenate((
                self.memory_used_data[start_index:self.max_points],
                self.memory_used_data[:self.buffer_index]
            ))
            util_segment = np.concatenate((
                self.utilization_data[start_index:self.max_points],
                self.utilization_data[:self.buffer_index]
            ))
        
        # Update plot data
        self.lines['temp'].set_data(time_segment, temp_segment)
        self.lines['power'].set_data(time_segment, power_segment)
        self.lines['memory'].set_data(time_segment, memory_segment)
        self.lines['util'].set_data(time_segment, util_segment)
        
        # Auto-scale axes
        self.ax.relim()
        self.ax.autoscale_view(True, True, True)
        
        # Redraw canvas
        self.draw()
