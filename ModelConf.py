from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal

class ConfidenceController(QWidget):
    confidence_changed = pyqtSignal(float)  # наружу — значение от 0.0 до 1.0

    def __init__(self, ui, default_conf=0.6):
        super().__init__()
        self.ui = ui
        self.default_conf = default_conf
        self.current_conf = default_conf

        # Настраиваем диал (0–100%)
        self.ui.dial.setMinimum(0)
        self.ui.dial.setMaximum(100)
        self.ui.dial.setValue(int(default_conf * 100))

        # Подключаем сигналы
        self.ui.dial.valueChanged.connect(self.update_confidence_display)
        self.ui.pushButton_4.clicked.connect(self.apply_confidence)   
        self.ui.pushButton_3.clicked.connect(self.reset_confidence)

        # Отобразим дефолт в поле
        self.ui.lineEdit_dial.setText(str(int(default_conf * 100)))

    def update_confidence_display(self, value):
        """При вращении диала обновляем QLineEdit"""
        self.ui.lineEdit_dial.setText(str(value))
        self.current_conf = value / 100.0  # переводим в 0.0–1.0

    def apply_confidence(self):
        """Отправляем наружу выбранную уверенность"""
        self.confidence_changed.emit(self.current_conf)

    def reset_confidence(self):
        """Сброс в дефолт"""
        self.ui.dial.setValue(int(self.default_conf * 100))
        self.ui.lineEdit_dial.setText(str(int(self.default_conf * 100)))
        self.current_conf = self.default_conf
        self.confidence_changed.emit(self.current_conf)