from PyQt5.QtCore import QThread, pyqtSignal
from .data_collector import DataCollector
import time

class CollectorWorker(QThread):
    data_ready = pyqtSignal(dict)

    def __init__(self, config):
        super().__init__()
        self.running = False
        self.config = config
        self.refresh_interval = self.config.get('refresh_interval')

    def run(self):
        collector = DataCollector()
        self.running = True
        while self.running:
            static_stats = collector.get_gpu_stats()
            process_stats = collector.get_process_stats()
            data = {
                'static': static_stats,
                'processes': process_stats
            }
            self.data_ready.emit(data)
            time.sleep(float(self.config.get('refresh_interval', 1.0)))

    def stop(self):
        self.running = False
