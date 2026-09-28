import os
import time

# OpenCV FFmpeg uses TCP for RTSP; set before importing cv2.
os.environ.setdefault("OPENCV_FFMPEG_CAPTURE_OPTIONS", "rtsp_transport;tcp")

import cv2

from Camera import Camera


class IPCamera(Camera):
    def __init__(self, camera_id: int, address: str):
        super().__init__(camera_id)
        self._address = address
        self.cap = None
        self._retry_after = 0.0
        self._retry_delay = 2.0
        self._reported_failure = False

    @property
    def address(self):
        return self._address

    def _connect(self):
        params = [cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, 5000,
                  cv2.CAP_PROP_READ_TIMEOUT_MSEC, 5000]
        cap = cv2.VideoCapture(self._address, cv2.CAP_FFMPEG, params)
        if cap.isOpened():
            self.cap = cap
            self._retry_delay = 2.0
            self._reported_failure = False
            return True
        cap.release()
        if not self._reported_failure:
            print(f"IP-камера {self.camera_id}: соединение недоступно, ожидаю переподключения", flush=True)
            self._reported_failure = True
        self._retry_after = time.monotonic() + self._retry_delay
        self._retry_delay = min(self._retry_delay * 2, 60.0)
        return False

    def read_data(self):
        if self.cap is None:
            if time.monotonic() < self._retry_after or not self._connect():
                return None
        ok, frame = self.cap.read()
        if ok:
            return frame
        print(f"IP-камера {self.camera_id}: поток прерван, переподключаюсь", flush=True)
        self.release()
        self._retry_after = time.monotonic() + self._retry_delay
        self._retry_delay = min(self._retry_delay * 2, 60.0)
        return None

    def release(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None
