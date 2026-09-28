# Neiroguard

Просмотр до трёх IP/USB-камер и обнаружение оружия моделью `best_old_50.pt`. Захват и отрисовка кадров выполняются OpenCV/PyQt6, инференс модели — на NVIDIA GPU через PyTorch CUDA.

## Установка (Python 3.12, Linux/Windows)

Для RTX 5060 используется сборка PyTorch с CUDA 13.0. В WSL нужен драйвер NVIDIA на стороне Windows версии не ниже 580.88; проверенный драйвер 592.07 подходит. Версия установленного в Ubuntu `nvcc` не определяет версию CUDA, которую использует PyTorch: runtime поставляется с wheel-пакетами. Драйвер NVIDIA для Linux в WSL устанавливать не нужно.

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install --prefer-binary --timeout 120 --retries 5 -r requirements.txt
.venv/bin/python test.py
```

В Windows используйте `py -3.12 -m venv .venv`, затем `.venv\Scripts\python.exe` вместо `.venv/bin/python`. Установка идёт одним вызовом pip и кэширует загруженные пакеты. Если в существующем `.venv` команда `test.py` уже сообщает `вычисления: cuda:0`, переустановка для запуска камер не требуется. `torchaudio`, PyQt5 и пакеты для обучения не нужны приложению.

## Камеры и запуск

Адреса камер и пароли храните в `camera_config.local.json` (файл игнорируется Git). Приложение читает его автоматически, если он существует; [camera_config.json](camera_config.json) служит шаблоном. Например:

```json
{
  "cams": [
    {"id": 1, "type": "ip", "ip": "rtsp://user:password@host:554/path"},
    {"id": 2, "type": "ip", "ip": "http://host/video"}
  ]
}
```

Пустые поля `ip` пропускаются, поэтому достаточно вписать ссылки только для имеющихся камер. Поддерживается от одной до трёх камер с ID 1, 2, 3. Для USB-камеры используйте `{"id": 1, "type": "usb", "device_index": 0}`. Для Hikvision основной поток первого канала имеет путь `/Streaming/Channels/101`, дополнительный — `/Streaming/Channels/102`.

В обычном терминале Ubuntu WSL проверьте сеть и инференс до запуска окна:

```bash
.venv/bin/python check_cameras.py
.venv/bin/python test.py
```

Первая команда проверяет TCP-порт камеры и получение кадра через OpenCV, не печатая пароль; вторая проверяет модель на CUDA. Если камера видна в Windows, но TCP-порт недоступен из WSL, проверьте сеть WSL командой `ip route get <IP-камеры>`.

Если FFmpeg сообщает `401 Unauthorized`, проверьте логин и пароль именно этой камеры через её веб-интерфейс, затем исправьте ссылку в `camera_config.local.json`. После нескольких неверных входов Hikvision может временно заблокировать учётную запись. Если порт 554 недоступен, откройте настройки камеры **Configuration → Network → Basic Settings → Port** и проверьте **RTSP Port**. Колонка **Port** в SADP обычно показывает серверный порт SDK (8000/8080), а не RTSP.

```bash
.venv/bin/python App.py
```

Приложение по умолчанию требует CUDA и выдаёт понятную ошибку, если GPU недоступен. Для проверки без видеокарты можно запустить `NEIROGUARD_DEVICE=cpu .venv/bin/python test.py` и затем `NEIROGUARD_DEVICE=cpu .venv/bin/python App.py`. IP-потоки используют FFmpeg/TCP, открываются в рабочих потоках и переподключаются после разрыва. Переключение камеры сохраняет уже загруженную модель в памяти.
