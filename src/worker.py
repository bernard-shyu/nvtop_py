from PyQt5.QtCore import QThread, pyqtSignal
from .data_collector import DataCollector
from .config_handler import ConfigManager

class CollectorWorker(QThread):
    data_ready = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = ConfigManager()
        self.refresh_interval = self.config.get('refresh_interval')

    def run(self):
        while True:
            collector = DataCollector()
            static_stats = collector.get_gpu_stats()
            process_stats = collector.get_process_stats()
            data = {
                'static': static_stats,
                'processes': process_stats
            }
            self.data_ready.emit(data)
            QThread.sleep(int(self.refresh_interval))  # type: ignore
