from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from infrastructure.factories.infrastructure_factory import InfrastructureFactory
from model.data_classes.counter import Counter


class MainWindowViewModel(QObject):
    # Signals to view
    count_changed_signal = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self._counter_data = Counter()
        self._event_bus = InfrastructureFactory.create_event_bus()
        self._register_event_bus_signals()

    @pyqtSlot()
    def increment_slot(self) -> None:
        self._counter_data.increment()
        self._emit_signals(self._counter_data.count)

    @pyqtSlot()
    def decrement_slot(self) -> None:
        self._counter_data.decrement()
        self._emit_signals(self._counter_data.count)

    @pyqtSlot()
    def reset_slot(self) -> None:
        self._counter_data.reset()
        self._emit_signals(self._counter_data.count)

    def _emit_signals(self, count: int) -> None:
        self._event_bus.send_counter_signal.emit(count)
        self.count_changed_signal.emit(count)

    def _register_event_bus_signals(self) -> None:
        pass
