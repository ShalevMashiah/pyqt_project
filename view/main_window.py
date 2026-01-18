from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton)
from PyQt5.QtCore import Qt, pyqtSlot, QTimer
from PyQt5.QtGui import QImage, QPixmap

from globals.consts.const_styles import ConstStyles
from view_model.main_window_view_model import MainWindowViewModel
from view.widgets.clickable_video_label import ClickableVideoLabel


class MainWindow(QMainWindow):
    def __init__(self, view_model: MainWindowViewModel):
        super().__init__()
        self._view_model = view_model
        self._coordinates_label = QLabel("Click on video: X=-, Y=-")
        self._video_label = ClickableVideoLabel()
        self._timer = QTimer()
        self._init_ui()
        self._register_signals_from_vm()
        self._load_video()

    def _init_ui(self):
        # 1. Window Setup
        self.setWindowTitle('Video Display X Y Coordinates')
        self.setMinimumSize(800, 600)
        self.setStyleSheet(ConstStyles.MAIN_WINDOW_STYLE)

        # 2. Main Layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        #Video title Section
        video_title = QLabel("Click on Video to get X Y Coordinates")
        video_title.setObjectName("TitleLabel")
        video_title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(video_title)

        # Video display
        self._video_label.setMinimumSize(640, 360)
        self._video_label.setStyleSheet("background-color: black;")
        #self._video_label.clicked.connect(self._on_video_clicked)
        main_layout.addWidget(self._video_label)

        # 3. Title Section
        # title_label = QLabel("CURRENT COUNT")
        # title_label.setObjectName("TitleLabel")
        # title_label.setAlignment(Qt.AlignCenter)
        # main_layout.addWidget(title_label)

        # 4. Count Display Section
        # self._count_label.setObjectName("CountLabel")
        # self._count_label.setAlignment(Qt.AlignCenter)
        # main_layout.addWidget(self._count_label)

        # Spacer to push buttons to bottom slightly
        main_layout.addStretch()

        # 5. Controls Section (Horizontal Layout)
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def _register_signals_from_vm(self):
        self._view_model.frame_ready_signal.connect(self._display_frame)

    def _load_video(self):
        if self._view_model.load_default_video():
            fps = self._view_model.get_video_fps()
            self._timer.setInterval(int(1000 / fps))
            self._timer.timeout.connect(self._update_frame)
            self._timer.start()   

    def _update_frame(self):
        label_width = self._video_label.width()
        label_height = self._video_label.height()
        self._view_model.update_frame(label_width, label_height)

    @pyqtSlot(object)
    def _display_frame(self, frame_rgb):
        h, w, ch = frame_rgb.shape
        bytes_per_line = ch * w
        q_image = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self._video_label.setPixmap(QPixmap.fromImage(q_image))

        
    @pyqtSlot(int)
    def _update_view_slot(self, count: int) -> None:
        pass
        #self._count_label.setText(str(count))

        # Visual Logic: Set a dynamic property for color coding based on value
        # status = "zero"
        # if count > 0:
        #     status = "positive"
        # elif count < 0:
        #     status = "negative"
        # self._count_label.setProperty("valueStatus", status)

        # Re-polish the widget to apply the new style from the stylesheet
        # self._count_label.style().unpolish(self._count_label)
        # self._count_label.style().polish(self._count_label)
