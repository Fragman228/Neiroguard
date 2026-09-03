import os
import shutil

# ===== НАСТРОЙКИ =====
SOURCE_DIR = "/home/egor/Загрузки/BEbra/obj_Validation_data"
TARGET_ROOT = "/media/egor/Data/ML"
DATASET_NAME = "BEbra_dataset"   # можешь назвать как угодно

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
LABEL_EXTENSION = ".txt"

# ===== ЦЕЛЕВЫЕ ПАПКИ =====
validation_dir = os.path.join(TARGET_ROOT, DATASET_NAME, "validation")
images_dir = os.path.join(validation_dir, "images")
labels_dir = os.path.join(validation_dir, "labels")

os.makedirs(images_dir, exist_ok=True)
os.makedirs(labels_dir, exist_ok=True)

# ===== ОБРАБОТКА =====
for filename in os.listdir(SOURCE_DIR):
    src_path = os.path.join(SOURCE_DIR, filename)
    name, ext = os.path.splitext(filename.lower())

    if ext in IMAGE_EXTENSIONS:
        shutil.copy2(src_path, os.path.join(images_dir, filename))

    elif ext == LABEL_EXTENSION:
        shutil.copy2(src_path, os.path.join(labels_dir, filename))

print("✅ Валидационный датасет успешно подготовлен")
print(f"📁 Путь: {validation_dir}")
