from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QHeaderView

class QCommonTable(QTableWidget):
    def __init__(self, N_ROWS_TABLE, N_COLS_TABLE, header_labels=None):
        super().__init__(N_ROWS_TABLE, N_COLS_TABLE)
        self.setHorizontalHeaderLabels(header_labels)

        # Set compact horizontal spacing constrained by title text width for all columns except the last
        for col in range(self.columnCount() - 1):
            self.horizontalHeader().setSectionResizeMode(col, QHeaderView.ResizeToContents)
        # Set the last column ("Command") to take all remaining horizontal space
        self.horizontalHeader().setSectionResizeMode(self.columnCount() - 1, QHeaderView.Stretch)

        # Initialize empty cells for all rows
        for row in range(N_ROWS_TABLE):
            for col in range(N_COLS_TABLE):
                self.setItem(row, col, QTableWidgetItem(""))

    def proc_getfp(self, proc, key, unit, default='N/A'):
        value = proc.get(key, default)
        try:
            return f"{float(value):.2f}{unit}"
        except ValueError:
            return str(value)

class GPUStatsTable(QCommonTable):
    def __init__(self, N_ROWS_TABLE):
        super().__init__(N_ROWS_TABLE, 7, header_labels = [
            'Fan Speed', 'Temperature', 'Power Draw', 'Power Limit',
            'Memory Used', 'Memory Total', 'Utilization'
        ])

    def update_data(self, stats_dict, row=1):
        # Update the second row (index 1) with dynamic values
        # Set the third row (index 2) with fixed values on app startup
        for col, (key, value) in enumerate(stats_dict.items()):
            self.setItem(row, col, QTableWidgetItem(f"{value:.2f}"))

class ProcessTable(QCommonTable):
    def __init__(self, N_ROWS_TABLE):
        super().__init__(N_ROWS_TABLE, 12, header_labels = [
            'GPU idx', 'PID #', 'Type', 'SM %', 'Memory %', 'Encoder %', 'Decoder %', 'JPEG %', 'OFA %',
            'FB Mem (MB)', 'CCPM (MB)', 'Command'
        ])

    def update_data(self, processes):
        self.setRowCount(len(processes))
        for iRow, proc in enumerate(processes):
            if iRow == 0: # Skip the header row
                continue
            row = iRow - 1  # Adjust for header row
            self.setItem(row, 0, QTableWidgetItem(proc.get('gpu', '')))
            self.setItem(row, 1, QTableWidgetItem(proc.get('pid', '')))
            self.setItem(row, 2, QTableWidgetItem(proc.get('type', '')))
            self.setItem(row, 3, QTableWidgetItem(self.proc_getfp(proc, 'sm',  '%')))
            self.setItem(row, 4, QTableWidgetItem(self.proc_getfp(proc, 'mem', '%')))
            self.setItem(row, 5, QTableWidgetItem(self.proc_getfp(proc, 'enc', '%')))
            self.setItem(row, 6, QTableWidgetItem(self.proc_getfp(proc, 'dec', '%')))
            self.setItem(row, 7, QTableWidgetItem(self.proc_getfp(proc, 'jpg', '%')))
            self.setItem(row, 8, QTableWidgetItem(self.proc_getfp(proc, 'ofa', '%')))
            self.setItem(row, 9, QTableWidgetItem(self.proc_getfp(proc, 'fb', ' MB')))
            self.setItem(row, 10, QTableWidgetItem(self.proc_getfp(proc, 'ccpm', ' MB')))
            self.setItem(row, 11, QTableWidgetItem(str(proc.get('command', ''))))
