from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel, QSizePolicy, QSplitter
from PyQt5.QtCore import Qt
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
        
        # Use QSplitter for adjustable heights
        self.splitter = QSplitter(Qt.Vertical)
        main_layout = QVBoxLayout() # Create a layout instance
        main_layout.addWidget(self.splitter) # Add the splitter to this layout
        self.central_widget.setLayout(main_layout) # Set this layout for the central widget

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
        
        # Add widgets to the splitter
        self.splitter.addWidget(self.plot_widget)
        self.splitter.addWidget(self.stats_table)
        self.splitter.addWidget(self.process_table)

        # Set initial sizes for the splitter (optional, but good for default layout)
        # These values are just examples, you might need to adjust them based on desired initial appearance
        self.splitter.setSizes([int(height * 0.6), int(height * 0.2), int(height * 0.2)])

    def start_worker(self):
        self.worker = CollectorWorker(self.config)
        self.worker.data_ready.connect(self.update_ui)
        self.worker.start()

    def update_ui(self, data):
        self.process_table.update_data(data['processes'])
        self.stats_table.update_data(data['static'], row=self.stats_table_row)
        self.plot_widget.update_plot(data['static'])
        self.stats_table_row = 1 # Reset to the first row for dynamic updates
