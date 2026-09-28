import sys

import cv2

from Camera import Camera


class UsbCamera(Camera):
    def __init__(self, camera_id: int, device_index: int):
        super().__init__(camera_id)
        self.device_index = device_index
        backend = cv2.CAP_DSHOW if sys.platform == "win32" else cv2.CAP_ANY
        self.cap = cv2.VideoCapture(device_index, backend)
        if not self.cap.isOpened():
            self.cap.release()
            raise RuntimeError(f"Не удалось открыть USB-камеру {device_index}")

    def read_data(self):
        if self.cap is None or not self.cap.isOpened():
            return None
        ok, frame = self.cap.read()
        return frame if ok else None

    def release(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None
