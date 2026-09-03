from abc import ABC, abstractmethod

class Camera(ABC):
    def __init__(self, camera_id: int):
        self.camera_id = camera_id

    @property
    def cam_id(self):
        return self.camera_id

    @abstractmethod
    def read_data(self):
        raise NotImplementedError

    def release(self):
        raise NotImplementedError