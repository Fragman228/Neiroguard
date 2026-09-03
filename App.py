from CameraParser import CameraParser
from CameraStorage import CameraStorage
from CameraThread import CameraThread
from Camera import Camera 
import cv2
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QMainWindow
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from UsbCamera import UsbCamera
import sys
from Window import MainWindow
from PyQt6.uic import loadUi


if __name__ == "__main__":
    parser = CameraParser()
    storage = CameraStorage()
    cams = parser.load_raw_config()
    for cam in cams:
        storage.put_camera(cam.camera_id, cam)
    
    app = QApplication(sys.argv)
    window = MainWindow(storage)
    window.show()
    sys.exit(app.exec())

