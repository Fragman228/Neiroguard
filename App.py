import os
import sys

import numpy as np
from PyQt6.QtCore import QLibraryInfo
from PyQt6.QtWidgets import QApplication
import torch
from ultralytics import YOLO

from CameraParser import CameraParser
from CameraStorage import CameraStorage
from Window import MainWindow


def main():
    # OpenCV wheels can set a Qt 5 plugin path that breaks the PyQt6 GUI.
    os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = QLibraryInfo.path(
        QLibraryInfo.LibraryPath.PluginsPath
    )
    storage = CameraStorage()
    for camera in CameraParser().load_raw_config():
        storage.put_camera(camera.camera_id, camera)
    device = os.environ.get("NEIROGUARD_DEVICE", "cuda:0")
    if device.startswith("cuda") and not torch.cuda.is_available():
        raise RuntimeError(
            "CUDA недоступна. Проверьте nvidia-smi и запустите .venv/bin/python test.py. "
            "Для проверки на CPU укажите NEIROGUARD_DEVICE=cpu."
        )
    model = YOLO(os.path.join(os.path.dirname(__file__), "best_old_50.pt"))
    model.to(device)
    # A real inference here catches an incompatible checkpoint or CUDA runtime
    # before camera worker threads and the window are started.
    model.predict(np.zeros((320, 320, 3), dtype=np.uint8), device=device, imgsz=320, verbose=False)
    app = QApplication(sys.argv)
    window = MainWindow(storage, model, device)
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
