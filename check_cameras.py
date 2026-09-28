"""Проверка RTSP-камер из локальной конфигурации без вывода паролей."""

import socket
import sys
from urllib.parse import urlsplit

from CameraParser import CameraParser
from IPCamera import IPCamera


def probe_ports(host, configured_port):
    for candidate in (80, 10554, 8000, 8080):
        if candidate == configured_port:
            continue
        try:
            with socket.create_connection((host, candidate), timeout=1):
                print(f"  Дополнительная проверка: TCP {candidate} доступен", flush=True)
        except OSError:
            pass


def main():
    cameras = CameraParser().load_raw_config()
    failures = 0
    for camera in cameras:
        if isinstance(camera, IPCamera):
            url = urlsplit(camera.address)
            host = url.hostname
            port = url.port or 554
            if not host:
                print(f"Камера {camera.camera_id}: неверный адрес")
                failures += 1
                continue
            print(f"Камера {camera.camera_id}: проверка {host}:{port}", flush=True)
            try:
                with socket.create_connection((host, port), timeout=3):
                    pass
            except PermissionError:
                print("  Сеть заблокирована для этого процесса; запустите проверку в обычном терминале WSL", flush=True)
                failures += 1
                continue
            except OSError as exc:
                print(f"  TCP-порт недоступен: {exc}", flush=True)
                probe_ports(host, port)
                failures += 1
                continue
            print("  TCP-порт доступен; читаю RTSP-кадр", flush=True)
        else:
            print(f"USB-камера {camera.camera_id}: читаю кадр", flush=True)

        frame = None
        try:
            frame = camera.read_data()
        finally:
            camera.release()

        if frame is None:
            print("  Кадр не получен: проверьте путь RTSP, порт, учётные данные и кодек", flush=True)
            failures += 1
        else:
            height, width = frame.shape[:2]
            print(f"  Кадр получен: {width}×{height}", flush=True)

    return 1 if failures else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("Проверка прервана", flush=True)
        sys.exit(130)
