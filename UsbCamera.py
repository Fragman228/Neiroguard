import cv2


class UsbCamera:
    def __init__(self, camera_id, device_index):
        self.camera_id = camera_id
        self.id = camera_id          # запасной алиас для совместимости
        self.device_index = device_index
        self.cap = cv2.VideoCapture(self.device_index, cv2.CAP_DSHOW)

        if not self.cap.isOpened():
            raise RuntimeError(f"Не удалось открыть USB-камеру с индексом {self.device_index}")

    def read_data(self):
        if self.cap is None or not self.cap.isOpened():
            raise RuntimeError(f"Камера {self.camera_id} не открыта")

        ret, frame = self.cap.read()
        if not ret:
            return None
        return frame

    def release(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None

    def __str__(self):
        return f"UsbCamera(id={self.camera_id}, device_index={self.device_index})"