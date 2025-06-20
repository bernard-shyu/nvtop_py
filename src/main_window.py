from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel, QSizePolicy
from .worker import CollectorWorker
from .widgets.table_widget import GPUStatsTable, ProcessTable
from .widgets.plot_widget import PlotWidget

class MainWindow(QMainWindow):
    def __init__(self, config):
        super().__init__()
        self.setWindowTitle("NVTop Monitor")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout()
        self.central_widget.setLayout(layout)

        self.config = config
        # Set initial resolution if provided in config
        resolution = self.config.get('RESOLUTION', '1920x1080')
        width, height = map(int, resolution.split('x'))
        self.resize(width, height)

        # Apply QT styles from configuration
        plot_font_size = self.config.get('plot_style', {}).get('font_size', 20)
        table_font_size = self.config.get('table_style', {}).get('font_size', 20)
        table_cell_height = self.config.get('table_style', {}).get('table_cell_height', 40)  # Default to 40px  per row to ensure visibility

        self.plot_widget = PlotWidget(self.config)
        self.stats_table = GPUStatsTable()
        self.process_table = ProcessTable()

        self.plot_widget.setStyleSheet(f"font-size: {plot_font_size}px;")
        self.stats_table.setStyleSheet(f"font-size: {table_font_size}px;")
        self.process_table.setStyleSheet(f"font-size: {table_font_size}px;")
        
        # Set size policies for layout constraints
        self.process_table.setMaximumHeight(7 * table_cell_height)  # Fixed to 6 rows (5 data + 1 title), +1 for extra row
        self.process_table.setSizePolicy(self.process_table.sizePolicy().horizontalPolicy(), 
                                         QSizePolicy.Fixed)
        self.stats_table.setMaximumHeight(4 * table_cell_height)  # Fixed to 3 rows (2 data + 1 title), +1 for extra row
        self.stats_table.setSizePolicy(self.stats_table.sizePolicy().horizontalPolicy(), 
                                       QSizePolicy.Fixed)
        self.plot_widget.setSizePolicy(QSizePolicy.Expanding, 
                                       QSizePolicy.Expanding)
        
        self.stats_table_row = 0  # Start with the third row for static values
        layout.addWidget(self.plot_widget, 1)  # Stretch factor 1 to expand
        layout.addWidget(self.stats_table, 0)  # No stretch, fixed height
        layout.addWidget(self.process_table, 0)  # No stretch, fixed height

    def start_worker(self):
        self.worker = CollectorWorker(self.config)
        self.worker.data_ready.connect(self.update_ui)
        self.worker.start()

    def update_ui(self, data):
        self.process_table.update_data(data['processes'])
        self.stats_table.update_data(data['static'], row=self.stats_table_row)
        self.plot_widget.update_plot(data['static'])
        self.stats_table_row = 1 # Reset to the first row for dynamic updates
