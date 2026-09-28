import json
import os
from pathlib import Path
from urllib.parse import urlsplit

from IPCamera import IPCamera
from UsbCamera import UsbCamera


class CameraParser:
    DEFAULT_CONFIG_PATH = Path(__file__).with_name("camera_config.json")
    LOCAL_CONFIG_PATH = Path(__file__).with_name("camera_config.local.json")

    def __init__(self, config_path=None):
        if config_path is None:
            config_path = os.environ.get("NEIROGUARD_CAMERA_CONFIG")
        if config_path is None:
            config_path = self.LOCAL_CONFIG_PATH if self.LOCAL_CONFIG_PATH.exists() else self.DEFAULT_CONFIG_PATH
        self._config_path = Path(config_path)

    def load_raw_config(self):
        data = json.loads(self._config_path.read_text(encoding="utf-8"))
        entries = data.get("cams") if isinstance(data, dict) else None
        if not isinstance(entries, list) or not 1 <= len(entries) <= 3:
            raise ValueError("camera_config.json: ожидается список cams из 1–3 камер")

        cameras = []
        used_ids = set()
        for entry in entries:
            if not isinstance(entry, dict):
                raise ValueError("camera_config.json: каждая камера должна быть объектом")
            if entry.get("type") == "ip" and isinstance(entry.get("ip"), str) and not entry["ip"].strip():
                continue
            camera_id = entry.get("id")
            if type(camera_id) is not int or camera_id not in (1, 2, 3) or camera_id in used_ids:
                raise ValueError("camera_config.json: ID камер должны быть уникальными числами 1, 2 или 3")
            used_ids.add(camera_id)

            if entry.get("type") == "ip":
                address = entry.get("ip")
                if not isinstance(address, str):
                    raise ValueError(f"Камера {camera_id}: впишите ссылку RTSP/HTTP в поле ip")
                address = address.strip()
                parsed = urlsplit(address)
                if parsed.scheme.lower() not in {"rtsp", "rtsps", "http", "https"} or not parsed.hostname:
                    raise ValueError(f"Камера {camera_id}: неверный адрес; ожидается rtsp:// или http://")
                cameras.append(IPCamera(camera_id, address))
            elif entry.get("type") == "usb":
                index = entry.get("device_index", camera_id - 1)
                if type(index) is not int or index < 0:
                    raise ValueError(f"Камера {camera_id}: device_index должен быть целым числом >= 0")
                cameras.append(UsbCamera(camera_id, index))
            else:
                raise ValueError(f"Камера {camera_id}: type должен быть ip или usb")
        if not cameras:
            raise ValueError("camera_config.json: впишите хотя бы одну ссылку камеры в поле ip")
        return cameras
