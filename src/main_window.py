from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel
from .worker import CollectorWorker
from .widgets.table_widget import GPUStatsTable, ProcessTable

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NVTop Monitor")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout()
        self.central_widget.setLayout(layout)

        self.plot_label = QLabel("Plot Area")
        self.gpu_table = GPUStatsTable()
        self.process_table = ProcessTable()
        layout.addWidget(self.plot_label)
        layout.addWidget(self.gpu_table)
        layout.addWidget(self.process_table)

    def start_worker(self, config):
        self.worker = CollectorWorker()
        self.worker.data_ready.connect(self.update_ui)
        self.worker.start()

    def update_ui(self, data):
        self.gpu_table.update_data(data['static'])
        self.process_table.update_data(data['processes'])
