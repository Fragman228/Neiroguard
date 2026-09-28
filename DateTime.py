from datetime import datetime

from PyQt6.QtCore import QThread, pyqtSignal


class DateTimeThread(QThread):
    date_signal = pyqtSignal(str)
    time_signal = pyqtSignal(str)

    def run(self):
        while not self.isInterruptionRequested():
            now = datetime.now()
            self.date_signal.emit(now.strftime("%d.%m.%Y"))
            self.time_signal.emit(now.strftime("%H:%M:%S"))
            self.msleep(1000)

    def stop(self):
        self.requestInterruption()
        self.wait(1500)
