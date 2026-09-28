from pathlib import Path

from ultralytics import YOLO


model = YOLO(Path(__file__).with_name("best_old_50.pt"))
print("Версия сохранения модели:", model.ckpt.get("version", "не указана"))
print("Классы:", model.names)
