from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

class GPUStatsTable(QTableWidget):
    def __init__(self):
        super().__init__(1, 7)
        self.setHorizontalHeaderLabels([
            'Fan Speed', 'Temperature', 'Power Draw', 'Power Limit',
            'Memory Used', 'Memory Total', 'Utilization'
        ])

    def update_data(self, stats_dict):
        for col, (key, value) in enumerate(stats_dict.items()):
            self.setItem(0, col, QTableWidgetItem(f"{value:.2f}"))

class ProcessTable(QTableWidget):
    def __init__(self):
        super().__init__(0, 12)
        self.setHorizontalHeaderLabels([
            'GPU idx', 'PID #', 'Type', 'SM %', 'Memory %', 'Encoder %', 'Decoder %', 'JPEG %', 'OFA %', 'FB Mem (MB)', 'CCPM (MB)', 'Command'
        ])

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
            self.setItem(row, 11, QTableWidgetItem(self.proc_getfp(proc, 'ccpm', 'N/A')))
            self.setItem(row, 12, QTableWidgetItem(str(proc.get('command', ''))))
