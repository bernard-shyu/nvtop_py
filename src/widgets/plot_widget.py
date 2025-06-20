import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class PlotWidget(FigureCanvas):
    def __init__(self, config):
        self.figure = Figure()
        self.ax_temp = self.figure.add_subplot(111)
        self.ax_power = self.ax_temp.twinx()
        self.ax_memory = self.ax_temp.twinx()
        self.ax_util = self.ax_temp.twinx()
        super().__init__(self.figure)
        
        # Ensure we have at least 100 data points
        self.max_points = config.get('X_data_points', 1000)
        self.max_points = max(100, int(self.max_points))  # Ensure minimum of 100 points

        # Initialize circular buffer arrays
        self.buffer_index = 0
        self.time_data = np.zeros(self.max_points)
        self.temperature_data = np.zeros(self.max_points)
        self.power_draw_data = np.zeros(self.max_points)
        self.mem_utilization_data = np.zeros(self.max_points)
        self.gpu_utilization_data = np.zeros(self.max_points)
        self.data_count = 0

        # Initialize plot lines on respective axes with styles from config
        self.lines = {
            'temp': self.ax_temp.plot([], [], label='Temperature (°C)', 
                                      color=config.get('temp_color', '#FF0000'), 
                                      linewidth=config.get('temp_width', 1.5))[0],
            'power': self.ax_power.plot([], [], label='Power Draw (%)', 
                                      color=config.get('power_color', '#00FF00'), 
                                      linewidth=config.get('power_width', 1.5))[0],
            'memory': self.ax_memory.plot([], [], label='Memory Used (%)', 
                                      color=config.get('memory_color', '#0000FF'), 
                                      linewidth=config.get('memory_width', 1.5))[0],
            'util': self.ax_util.plot([], [], label='GPU Utilization (%)', 
                                      color=config.get('util_color', '#FFFF00'), 
                                      linewidth=config.get('util_width', 1.5))[0]
        }
        
        # Configure axes with specific Y-axis display range to accommodate data value 0 visually
        self.ax_temp.set_ylim(-5,   100)  # Temperature range in Celsius, max 100 degree
        self.ax_power.set_ylim(-5,  100)  # Power usage in percent, max 100%
        self.ax_memory.set_ylim(-5, 100)  # Memory usage in percent, max 100%
        self.ax_util.set_ylim(-5,   100)  # Utilization in percent, max 100%
        
        # Offset the right spines for visibility
        self.ax_memory.spines["right"].set_position(("axes", 1.1))
        self.ax_util.spines["right"].set_position(("axes", 1.2))
        
        # Set colors for axis labels to match lines
        self.ax_temp.yaxis.label.set_color('r')
        self.ax_power.yaxis.label.set_color('g')
        self.ax_memory.yaxis.label.set_color('b')
        self.ax_util.yaxis.label.set_color('y')
        
        # Get font size from config for plot elements
        font_size = config.get('plot_style', {}).get('font_size', 10)
        
        # Configure plot with custom font sizes
        self.ax_temp.legend(handles=[self.lines['temp'], self.lines['power'], self.lines['memory'], self.lines['util']], loc='upper left', fontsize=font_size)
        self.ax_temp.set_title('GPU Statistics Over Time', fontsize=font_size + 2)
        self.ax_temp.set_xlabel('Time Steps', fontsize=font_size)
        self.ax_temp.set_ylabel('Temperature (°C)', fontsize=font_size)
        self.ax_power.set_ylabel('Power Draw (%)', fontsize=font_size)
        self.ax_memory.set_ylabel('Memory Used (%)', fontsize=font_size)
        self.ax_util.set_ylabel('Utilization (%)', fontsize=font_size)
        self.ax_temp.grid(True)
        # Set tick label sizes
        self.ax_temp.tick_params(axis='both', labelsize=font_size)
        self.ax_power.tick_params(axis='y', labelsize=font_size)
        self.ax_memory.tick_params(axis='y', labelsize=font_size)
        self.ax_util.tick_params(axis='y', labelsize=font_size)

    def update_plot(self, stats):
        # Update circular buffer
        index = self.buffer_index
        
        # Update data arrays
        self.time_data[index] = self.data_count

        power_used  = stats.get('power_draw', 0)
        power_limit = stats.get('power_limit', 100) or 100                # Avoid division by zero, default to 100W
        self.power_draw_data[index] =  (power_used / power_limit * 100)

        memory_used  = stats.get('memory_used', 0)
        memory_total = stats.get('memory_total', 16384) or 16384          # Avoid division by zero, default to 16GB
        self.mem_utilization_data[index] = (memory_used / memory_total * 100)

        self.temperature_data[index]     = stats.get('temperature', 0)
        self.gpu_utilization_data[index] = stats.get('utilization', 0)
        
        # Update buffer index
        self.buffer_index = (index + 1) % self.max_points
        self.data_count += 1
        
        # Always plot the last self.max_points data points (sliding window effect)
        if self.data_count <= self.max_points:
            start_index = 0
            end_index = self.data_count
        else:
            start_index = self.buffer_index
            end_index = (self.buffer_index + self.max_points) % self.max_points
        
        # Extract data in chronological order with wrap-around handling
        if start_index < end_index:
            time_segment = self.time_data[start_index:end_index]
            temp_segment = self.temperature_data[start_index:end_index]
            power_segment = self.power_draw_data[start_index:end_index]
            memory_segment = self.mem_utilization_data[start_index:end_index]
            util_segment = self.gpu_utilization_data[start_index:end_index]
        else:
            time_segment = np.concatenate((self.time_data[start_index:self.max_points], self.time_data[0:end_index]))
            temp_segment = np.concatenate((self.temperature_data[start_index:self.max_points], self.temperature_data[0:end_index]))
            power_segment = np.concatenate((self.power_draw_data[start_index:self.max_points], self.power_draw_data[0:end_index]))
            memory_segment = np.concatenate((self.mem_utilization_data[start_index:self.max_points], self.mem_utilization_data[0:end_index]))
            util_segment = np.concatenate((self.gpu_utilization_data[start_index:self.max_points], self.gpu_utilization_data[0:end_index]))
        
        # Adjust time data to show sliding effect (normalize to 0 to max_points for display)
        if len(time_segment) > 0:
            time_segment = np.arange(len(time_segment))
        
        # Update plot data
        self.lines['temp'].set_data(time_segment, temp_segment)
        self.lines['power'].set_data(time_segment, power_segment)
        self.lines['memory'].set_data(time_segment, memory_segment)
        self.lines['util'].set_data(time_segment, util_segment)
        
        # Set X-axis limits to show sliding window from right to left
        self.ax_temp.set_xlim(0, self.max_points)
        
        # Y-axis is fixed, no need to autoscale
        self.ax_temp.relim()
        self.ax_temp.autoscale_view(False, False, False)
        
        # Redraw canvas
        self.draw()
