# Neuroguard

Приложение по распознованию оружия  с нескольких камер (USB и IP).  
Архитектура построена на конфигурационном файле, классовой и потоковой системе.

---

## Структура проекта

- **`App.py`** – основной входной файл. Загружает конфигурацию камер, создаёт хранилище и запускает PyQt6-приложение.  
- **`camera_config.json`** – конфигурационный файл со списком камер.  
- **`CameraParser.py`** – парсинг конфигурации и создание объектов камер (`UsbCamera`, `IPCamera`).  
- **`CameraStorage.py`** – хранилище объектов камер (добавление, получение, список всех).  
- **`Camera.py`** – абстрактный класс камеры.  
- **`UsbCamera.py` / `IPCamera.py`** – реализации конкретных типов камер.  
- **`CameraThread.py`** – поток захвата видеопотока и передачи кадров в GUI.  
- **`detection_window_new.ui`** – описание интерфейса (Qt Designer).  
- **`requirements.txt`** – список зависимостей Python.  

---

## ⚙️ Первый запуск

1. **Клонировать проект**
   ```bash
   git clone <repo_url>
   cd <repo_name>
   ```

2. **Создать и активировать виртуальное окружение**

   ```bash
   python3 -m venv venv
   source venv/bin/activate      # Linux/macOS
   venv\Scripts\activate         # Windows
   ```

3. **Установить зависимости**

   ```bash
   pip install -r requirements.txt
   ```

4. **Настроить конфигурацию камер**
   В файле `camera_config.json`:

   ```json
   {
     	"cams": [
        {
            "id": 1,	
            "type": "usb"	
        },	
        {   "id": 2,	
            "type": "usb"	
        },	
        {   "id": 3,	
            "type": "usb"
        }
        ]     
   }
   ```

5. **Запустить приложение**

   ```bash
   python3.11 App.py
   ```

