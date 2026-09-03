from PyQt6.QtWidgets import QComboBox
from PyQt6.QtCore import QObject, pyqtSignal
from typing import List
from Camera import Camera

class CameraSelector(QObject):
    camera_selected = pyqtSignal(int)

    def __init__(self, comboBox: QComboBox, parent=None):
        super().__init__(parent)
        
        self.comboBox = comboBox 
        self.comboBox.currentIndexChanged.connect(self.on_camera_change)

    def populate(self, cameras: List[Camera]):
        self.comboBox.clear()
        for cam in cameras:
            self.comboBox.addItem(str(cam.camera_id), userData=cam.camera_id)

    def on_camera_change(self, index: int):
        if index == -1:
            return
            
        selected_cam_id = self.comboBox.itemData(index)
        print(f"Выбран пункт '{self.comboBox.itemText(index)}', ID камеры: {selected_cam_id}")
        
        self.camera_selected.emit(selected_cam_id)

    def get_selected_camera_id(self) -> int: 
        if self.comboBox.currentIndex() == -1:
            return None
        return self.comboBox.itemData(self.comboBox.currentIndex())