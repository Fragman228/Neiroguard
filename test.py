"""Проверка установки и инференса без подключённых камер."""

import os
from pathlib import Path

import cv2
import numpy as np
import torch
from ultralytics import YOLO, __version__ as ultralytics_version


def main():
    device = os.environ.get("NEIROGUARD_DEVICE", "cuda:0")
    print(f"PyTorch: {torch.__version__}; CUDA runtime: {torch.version.cuda}")
    print(f"Ultralytics: {ultralytics_version}; OpenCV: {cv2.__version__}")
    print(f"CUDA доступна: {torch.cuda.is_available()}")
    if device.startswith("cuda"):
        if not torch.cuda.is_available():
            raise SystemExit("GPU NVIDIA недоступен для PyTorch: проверьте драйвер и доступ к GPU")
        print(f"GPU: {torch.cuda.get_device_name(0)}")
    elif device != "cpu":
        raise SystemExit(f"Неизвестное устройство: {device}")

    model = YOLO(Path(__file__).with_name("best_old_50.pt"))
    model.to(device)
    result = model.predict(
        np.zeros((320, 320, 3), dtype=np.uint8),
        device=device,
        imgsz=320,
        verbose=False,
    )[0]
    actual_device = next(model.model.parameters()).device
    if actual_device.type != device.split(":")[0]:
        raise SystemExit(f"Модель оказалась на {actual_device}, ожидалось {device}")
    print(f"Модель загружена; классы: {result.names}; вычисления: {actual_device}")


if __name__ == "__main__":
    main()
