from datetime import datetime

from PyQt6.QtWidgets import QMainWindow, QPlainTextEdit, QVBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PyQt6.uic import loadUi

from CameraStorage import CameraStorage
from CameraThread import CameraThread
from DetectionThread import DetectionThread
from CameraSelector import CameraSelector
from ModelConf import ConfidenceController
from DateTime import DateTimeThread


class MainWindow(QMainWindow):
    def __init__(self, storage: CameraStorage):
        super().__init__()
        loadUi("detection_window_new.ui", self)

        self.storage = storage
        self.camera_selector = CameraSelector(self.comboBox)

        self.camera_threads = {}
        self.current_detection_thread = None

        self.preview_labels = {
            1: self.label_miniframe_cam1,
            2: self.label_7,
            3: self.label
        }

        self.conf_controller = ConfidenceController(self, default_conf=0.6)
        self.conf_controller.confidence_changed.connect(self.update_confidence)

        self._setup_log_widget()
        self.setup_camera_previews()

        self.camera_selector.camera_selected.connect(self.switch_detection_camera)

        self.date_time_thread = DateTimeThread()
        self.date_time_thread.date_signal.connect(self.lineEdit_date.setText)
        self.date_time_thread.time_signal.connect(self.lineEdit_time.setText)
        self.date_time_thread.start()

        first_cam_id = self.camera_selector.get_selected_camera_id()
        if first_cam_id is not None:
            self.switch_detection_camera(first_cam_id)

    def _setup_log_widget(self):
        if hasattr(self, "plainTextEdit_log"):
            self.log_output = self.plainTextEdit_log
        else:
            self.log_output = QPlainTextEdit(self.scrollAreaWidgetContents)
            self.log_output.setObjectName("plainTextEdit_log")
            self.log_output.setReadOnly(True)

            layout = self.scrollAreaWidgetContents.layout()
            if layout is None:
                layout = QVBoxLayout(self.scrollAreaWidgetContents)
                layout.setContentsMargins(0, 0, 0, 0)

            layout.addWidget(self.log_output)

        self.log_output.setReadOnly(True)
        self.log_output.document().setMaximumBlockCount(500)

    def setup_camera_previews(self):
        all_cameras = self.storage.get_all_cameras()
        self.camera_selector.populate(all_cameras)

        for cam in all_cameras:
            label_for_preview = self.preview_labels.get(cam.camera_id)
            if label_for_preview is None:
                print(
                    f"Предупреждение: для камеры с ID={cam.camera_id} "
                    f"не найден QLabel в словаре self.preview_labels."
                )
                continue

            thread = CameraThread(cam)
            thread.frame_ready.connect(self.update_preview_frame)
            self.camera_threads[cam.camera_id] = thread
            thread.start()

    def update_preview_frame(self, camera_id: int, qimg):
        label = self.preview_labels.get(camera_id)
        if label is None:
            return

        pixmap = QPixmap.fromImage(qimg)
        label.setPixmap(
            pixmap.scaled(
                label.width(),
                label.height(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        )

    def update_detection_frame(self, qimg):
        pixmap = QPixmap.fromImage(qimg)
        self.label_detection.setPixmap(
            pixmap.scaled(
                self.label_detection.width(),
                self.label_detection.height(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        )

    def append_log(self, text: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_output.appendPlainText(f"[{timestamp}] {text}")

        sb = self.log_output.verticalScrollBar()
        sb.setValue(sb.maximum())

    def switch_detection_camera(self, camera_id: int):
        print(f"Получена команда на переключение детекции на камеру с ID: {camera_id}")

        if self.current_detection_thread and self.current_detection_thread.isRunning():
            self.current_detection_thread.stop()

        source_camera_thread = self.camera_threads.get(camera_id)
        if not source_camera_thread:
            print(f"Критическая ошибка: не удалось найти поток для камеры с ID {camera_id}!")
            return

        self.current_detection_thread = DetectionThread(
            source_camera_thread,
            device="cuda:0",
            default_conf=self.conf_controller.default_conf
        )

        self.current_detection_thread.detection_ready.connect(self.update_detection_frame)
        self.current_detection_thread.log_signal.connect(self.append_log)

        self.current_detection_thread.start()
        print(f"Поток детекции для камеры ID:{camera_id} успешно запущен.")

    def update_confidence(self, new_conf: float):
        if self.current_detection_thread:
            self.current_detection_thread.set_confidence(new_conf)
            print(f"Установлена новая уверенность: {new_conf}")

    def closeEvent(self, event):
        print("Получен сигнал на закрытие окна. Остановка всех потоков...")

        if self.current_detection_thread and self.current_detection_thread.isRunning():
            self.current_detection_thread.stop()

        if hasattr(self, "date_time_thread") and self.date_time_thread.isRunning():
            stop_method = getattr(self.date_time_thread, "stop", None)
            if callable(stop_method):
                stop_method()
            else:
                self.date_time_thread.terminate()
                self.date_time_thread.wait(1000)

        for thread in self.camera_threads.values():
            thread.stop()

        print("Все потоки успешно остановлены.")
        event.accept()