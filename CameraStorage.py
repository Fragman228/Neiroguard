import os, sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

from Camera import Camera

class CameraStorage:
    def __init__(self):
        self._cameras = {}

    def put_camera(self, cam_name: str, cam: Camera) -> None:
        self._cameras[cam_name] = cam

    def get_camera(self, cam_name: str) -> Camera:
        return self._cameras[cam_name]

    def get_all_cameras(self) -> list:
        return list(self._cameras.values())

    def get_all_camera_names(self) -> list:
        return list(self._cameras.keys())
    