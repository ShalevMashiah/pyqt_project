from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton)
from PyQt5.QtCore import Qt, pyqtSlot

from globals.consts.const_styles import ConstStyles
from view_model.main_window_view_model import MainWindowViewModel


class MainWindow(QMainWindow):
    def __init__(self, view_model: MainWindowViewModel):
        super().__init__()
        self._view_model = view_model
        self._count_label = QLabel("0")
        self._init_ui()
        self._register_signals_from_vm()

    def _init_ui(self):
        # 1. Window Setup
        self.setWindowTitle('Modern Counter')
        self.setMinimumSize(400, 300)
        self.setStyleSheet(ConstStyles.MAIN_WINDOW_STYLE)

        # 2. Main Layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(40, 40, 40, 40)

        # 3. Title Section
        title_label = QLabel("CURRENT COUNT")
        title_label.setObjectName("TitleLabel")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # 4. Count Display Section
        self._count_label.setObjectName("CountLabel")
        self._count_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self._count_label)

        # Spacer to push buttons to bottom slightly
        main_layout.addStretch()

        # 5. Controls Section (Horizontal Layout)
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)

        # Decrement Button
        btn_dec = QPushButton("-")
        btn_dec.setObjectName("DecButton")
        btn_dec.setCursor(Qt.PointingHandCursor)
        btn_dec.clicked.connect(self._view_model.decrement_slot)
        button_layout.addWidget(btn_dec)

        # Reset Button
        btn_reset = QPushButton("Reset")
        btn_reset.setCursor(Qt.PointingHandCursor)
        btn_reset.clicked.connect(self._view_model.reset_slot)
        button_layout.addWidget(btn_reset)

        # Increment Button
        btn_inc = QPushButton("+")
        btn_inc.setObjectName("IncButton")
        btn_inc.setCursor(Qt.PointingHandCursor)
        btn_inc.clicked.connect(self._view_model.increment_slot)
        button_layout.addWidget(btn_inc)

        # Add control layout to main layout
        main_layout.addLayout(button_layout)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def _register_signals_from_vm(self):
        self._view_model.count_changed_signal.connect(self._update_view_slot)

    @pyqtSlot(int)
    def _update_view_slot(self, count: int) -> None:
        self._count_label.setText(str(count))

        # Visual Logic: Set a dynamic property for color coding based on value
        status = "zero"
        if count > 0:
            status = "positive"
        elif count < 0:
            status = "negative"
        self._count_label.setProperty("valueStatus", status)

        # Re-polish the widget to apply the new style from the stylesheet
        self._count_label.style().unpolish(self._count_label)
        self._count_label.style().polish(self._count_label)
