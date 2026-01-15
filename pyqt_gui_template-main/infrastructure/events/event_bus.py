from PyQt5.QtCore import QObject, pyqtSignal


class EventBus(QObject):
    send_counter_signal = pyqtSignal(int)

    def __init__(self):
        super().__init__()
