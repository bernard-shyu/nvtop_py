from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QHeaderView

class GPUStatsTable(QTableWidget):
    def __init__(self):
        super().__init__(3, 7)  # 3 rows: title, dynamic values, fixed values
        self.setHorizontalHeaderLabels([
            'Fan Speed', 'Temperature', 'Power Draw', 'Power Limit',
            'Memory Used', 'Memory Total', 'Utilization'
        ])
        # Set flexible horizontal spacing constrained by title text width
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # Initialize empty cells for all rows
        for row in range(1, 3):
            for col in range(7):
                self.setItem(row, col, QTableWidgetItem(""))

    def update_data(self, stats_dict, row=1):
        # Update the second row (index 1) with dynamic values
        # Set the third row (index 2) with fixed values on app startup
        for col, (key, value) in enumerate(stats_dict.items()):
            self.setItem(row, col, QTableWidgetItem(f"{value:.2f}"))

class ProcessTable(QTableWidget):
    def __init__(self):
        super().__init__(6, 12)  # 1 title row + 5 data rows
        self.setHorizontalHeaderLabels([
            'GPU idx', 'PID #', 'Type', 'SM %', 'Memory %', 'Encoder %', 'Decoder %', 'JPEG %', 'OFA %', 'FB Mem (MB)', 'CCPM (MB)', 'Command'
        ])
        # Set compact horizontal spacing constrained by title text width for all columns except the last
        for col in range(self.columnCount() - 1):
            self.horizontalHeader().setSectionResizeMode(col, QHeaderView.ResizeToContents)
        # Set the last column ("Command") to take all remaining horizontal space
        self.horizontalHeader().setSectionResizeMode(self.columnCount() - 1, QHeaderView.Stretch)
        # Initialize empty cells for data rows (rows 1 to 5)
        for row in range(1, 6):
            for col in range(12):
                self.setItem(row, col, QTableWidgetItem(""))

    def proc_getfp(self, proc, key, default='N/A'):
        value = proc.get(key, default)
        try:
            return f"{float(value):.2f}%"
        except ValueError:
            return str(value)

    def update_data(self, processes):
        self.setRowCount(len(processes))
        for iRow, proc in enumerate(processes):
            if iRow == 0: # Skip the header row
                continue
            row = iRow - 1  # Adjust for header row
            self.setItem(row, 0, QTableWidgetItem(str(proc.get('#', ''))))
            self.setItem(row, 1, QTableWidgetItem(proc.get('gpu', '')))
            self.setItem(row, 2, QTableWidgetItem(proc.get('pid', '')))
            self.setItem(row, 3, QTableWidgetItem(proc.get('type', '')))
            self.setItem(row, 4, QTableWidgetItem(self.proc_getfp(proc, 'sm')))
            self.setItem(row, 5, QTableWidgetItem(self.proc_getfp(proc, 'mem')))
            self.setItem(row, 6, QTableWidgetItem(self.proc_getfp(proc, 'enc')))
            self.setItem(row, 7, QTableWidgetItem(self.proc_getfp(proc, 'dec')))
            self.setItem(row, 8, QTableWidgetItem(self.proc_getfp(proc, 'jpg')))
            self.setItem(row, 9, QTableWidgetItem(self.proc_getfp(proc, 'ofa')))
            self.setItem(row, 10, QTableWidgetItem(self.proc_getfp(proc, 'fb')))
            self.setItem(row, 11, QTableWidgetItem(str(proc.get('command', ''))))
