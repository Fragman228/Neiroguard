import os
import sys
import json
from pathlib import Path
import platform

import cv2

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

from Camera import Camera
from UsbCamera import UsbCamera
from IPCamera import IPCamera


class CameraParser:
    DEFAULT_CONFIG_PATH: str = "camera_config.json"

    def __init__(self, config_path: str = DEFAULT_CONFIG_PATH):
        self._config_path = Path(config_path)
        self._usb_devices = self._get_usb_devices()

    def _get_usb_devices(self):
        """
        Windows-версия:
        ищем доступные USB/веб-камеры по индексам 0..9.
        """
        system = platform.system()
        if system != "Windows":
            raise NotImplementedError("Этот вариант написан только под Windows")

        devices = []

        for idx in range(10):
            cap = cv2.VideoCapture(idx, cv2.CAP_DSHOW)

            if cap.isOpened():
                ret, _ = cap.read()
                if ret:
                    devices.append(idx)

            cap.release()

        print(f"Detected USB devices (Windows indexes): {devices}")
        return devices

    def load_raw_config(self) -> list:
        if not self._config_path.exists():
            raise FileNotFoundError(f"File does not exist: {self._config_path}")

        data = json.loads(self._config_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("Bad format.")

        self._print_raw_config(data)
        return self._build_cameras_from_raw(data)

    def _print_raw_config(self, data: dict) -> None:
        if not data:
            raise ValueError("Data must be non null")
        print(json.dumps(data, ensure_ascii=False, indent=2), flush=True)

    def _build_cameras_from_raw(self, data) -> list:
        cams = []
        camera_list = list(data.values())[0]
        usb_camera_index = 0

        print(f"list : {camera_list}")

        for i in range(len(camera_list)):
            if not isinstance(camera_list[i], dict):
                raise ValueError("Item bad format")

            camera: Camera = None

            if camera_list[i].get("type") == "usb":
                if usb_camera_index >= len(self._usb_devices):
                    raise IndexError("USB camera index out of range")

                device_index = self._usb_devices[usb_camera_index]
                camera = UsbCamera(camera_list[i].get("id"), device_index)
                usb_camera_index += 1
            else:
                camera = IPCamera(camera_list[i].get("id"), camera_list[i].get("ip"))

            print(f"{camera}")
            cams.append(camera)

        return cams


if __name__ == "__main__":
    parser = CameraParser("camera_config.json")
    cameras = parser.load_raw_config()
    print(f"Loaded cameras: {cameras}")