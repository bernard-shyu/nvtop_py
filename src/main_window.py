from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel
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
        self.plot_widget = PlotWidget(self.config)
        self.stats_table = GPUStatsTable()
        self.process_table = ProcessTable()
        layout.addWidget(self.plot_widget)
        layout.addWidget(self.stats_table)
        layout.addWidget(self.process_table)

    def start_worker(self):
        self.worker = CollectorWorker(self.config)
        self.worker.data_ready.connect(self.update_ui)
        self.worker.start()

    def update_ui(self, data):
        self.stats_table.update_data(data['static'])
        self.process_table.update_data(data['processes'])
        self.plot_widget.update_plot(data['static'])
