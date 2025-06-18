import sys
from PyQt5.QtWidgets import QApplication
from .main_window import MainWindow
from .config_handler import ConfigManager

def main():
    app = QApplication(sys.argv)
    config = ConfigManager()
    window = MainWindow(config)
    window.show()
    window.start_worker()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
