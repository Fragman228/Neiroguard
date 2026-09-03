import os 
import sys
import cv2

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

from Camera import Camera

class IPCamera(Camera):
    def __init__(self, camera_id: int, address: str):
        super().__init__(camera_id)
        self._address = address
        self.cap = cv2.VideoCapture(self._address)

    @property
    def address(self):
        return self._address


    def read_data(self):
        # Проверка, открыто ли соединение, так как соединение может быть нестабильным.
        if not self.cap.isOpened():
            print(f"Ошибка: IP-камера {self.camera_id} ({self._address}) не открыта или потеряно соединение.")
            return None
        
        ret, frame = self.cap.read()
        if ret:
            # Если кадр успешно прочитан (ret is True), возвращаем его
            return frame
        else:
            print(f"Ошибка: Не удалось получить кадр с IP-камеры {self.camera_id} ({self._address}).")
            return None
        
    def release(self):
        """Закрыть соединение с камерой и освободить ресурсы."""
        if self.cap and self.cap.isOpened():
            self.cap.release()
            print(f"Соединение с IP-камерой {self.camera_id} закрыто.")