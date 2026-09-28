import threading

import cv2
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QImage


class CameraThread(QThread):
    frame_ready = pyqtSignal(int, QImage)

    def __init__(self, camera, parent=None, frame_delay_ms: int = 1):
        super().__init__(parent)
        self.camera = camera
        self._running = True
        self._lock = threading.Lock()
        self.last_frame = None
        self.frame_delay_ms = frame_delay_ms

    def run(self):
        while self._running:
            frame = self.camera.read_data()

            if frame is None:
                self.msleep(10)
                continue

            with self._lock:
                self.last_frame = frame.copy()

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_frame.shape
            bytes_per_line = ch * w

            qimg = QImage(
                rgb_frame.data,
                w,
                h,
                bytes_per_line,
                QImage.Format.Format_RGB888
            ).copy()

            self.frame_ready.emit(self.camera.camera_id, qimg)
            self.msleep(self.frame_delay_ms)

    def get_last_frame_copy(self):
        with self._lock:
            if self.last_frame is None:
                return None
            return self.last_frame.copy()

    def stop(self):
        self._running = False
        self.quit()
        self.wait()
        self.camera.release()
