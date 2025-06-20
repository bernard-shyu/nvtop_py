from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel, QSizePolicy
from .worker import CollectorWorker
from .widgets.table_widget import GPUStatsTable, ProcessTable
from .widgets.plot_widget import PlotWidget

class MainWindow(QMainWindow):
    N_ROWS_STATS_TABLE = 2
    N_ROWS_PROC_TABLE  = 5

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
        table_cell_height = int(table_font_size) + 4     # Table cell height, need extra padding space

        self.plot_widget   = PlotWidget(self.config)
        self.stats_table   = GPUStatsTable(self.N_ROWS_STATS_TABLE)
        self.process_table = ProcessTable(self.N_ROWS_PROC_TABLE)

        self.plot_widget.setStyleSheet(f"font-size: {plot_font_size}px;")
        self.stats_table.setStyleSheet(f"font-size: {table_font_size}px;")
        self.process_table.setStyleSheet(f"font-size: {table_font_size}px;")
        
        self.stats_table_row = 0  # Start with the third row for static values
        layout.addWidget(self.plot_widget, stretch = 1)  # Stretch factor 1 to expand
        layout.addWidget(self.stats_table, stretch = 0)  # No stretch, fixed height
        layout.addWidget(self.process_table, stretch = 0)  # No stretch, fixed height

    def start_worker(self):
        self.worker = CollectorWorker(self.config)
        self.worker.data_ready.connect(self.update_ui)
        self.worker.start()

    def update_ui(self, data):
        self.process_table.update_data(data['processes'])
        self.stats_table.update_data(data['static'], row=self.stats_table_row)
        self.plot_widget.update_plot(data['static'])
        self.stats_table_row = 1 # Reset to the first row for dynamic updates
