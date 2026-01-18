from PyQt5.QtCore import QObject, pyqtSignal


class EventBus(QObject):
    send_coordinates_signal = pyqtSignal(int, int)

    def __init__(self):
        super().__init__()
