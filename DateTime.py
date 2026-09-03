from PyQt6.QtCore import QThread, pyqtSignal
from datetime import datetime
import time

class DateTimeThread(QThread):
    date_signal = pyqtSignal(str)
    time_signal = pyqtSignal(str)

    def run(self):
        while True:
            now = datetime.now()
            self.date_signal.emit(now.strftime("%d.%m.%Y"))  # формат: 20.09.2025
            self.time_signal.emit(now.strftime("%H:%M:%S"))  # формат: 14:33:10
            time.sleep(1)
