import os
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from globals.consts.const_strings import ConstStrings
from infrastructure.factories.infrastructure_factory import InfrastructureFactory
from infrastructure.factories.logger_factory import LoggerFactory
from model.managers.video_manager import VideoManager


class MainWindowViewModel(QObject):
    # Signals to view
    coordinates_changed_signal = pyqtSignal(int, int)
    frame_ready_signal = pyqtSignal(object)
    status_message_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._logger = LoggerFactory.get_logger_manager()
        self._event_bus = InfrastructureFactory.create_event_bus()
        self._current_x = 0
        self._current_y = 0
        self._current_click_point = None
        self._video_manager = None
        self._is_playing = False

    def load_default_video(self) -> bool:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        video_path = os.path.join(base_path, "videos", "video1.mp4")
        return self.load_video(video_path)

    def load_video(self, video_path: str) -> bool:
        self._logger.log(ConstStrings.LOG_NAME_DEBUG, f"Loading video from: {video_path}")
        self._logger.log(ConstStrings.LOG_NAME_DEBUG, f"Video exists: {os.path.exists(video_path)}")
        
        if os.path.exists(video_path):
            self._video_manager = VideoManager(video_path)
            if self._video_manager.load_video():
                self._is_playing = True
                self._logger.log(ConstStrings.LOG_NAME_DEBUG, f"Video loaded successfully! FPS: {self._video_manager.get_fps()}")
                return True
            else:
                self._logger.log(ConstStrings.LOG_NAME_DEBUG, "Failed to open video file")
                return False
        else:
            self._logger.log(ConstStrings.LOG_NAME_DEBUG, f"Video file not found at: {video_path}")
            return False

    def get_video_fps(self) -> float:
        if self._video_manager:
            return self._video_manager.get_fps()
        return 30.0

    def update_frame(self, label_width: int, label_height: int):
        if not self._video_manager:
            return
        
        if self._is_playing:
            self._video_manager.read_frame()
        
        frame_rgb = self._video_manager.get_display_frame(
            self._current_click_point, label_width, label_height
        )
        if frame_rgb is None:
            return
        
        self.frame_ready_signal.emit(frame_rgb)

    @pyqtSlot(int, int)
    def update_coordinates_slot(self, x: int, y: int) -> None:
        self._current_x = x
        self._current_y = y
        self._current_click_point = (x, y)
        self.coordinates_changed_signal.emit(x, y)
        self._event_bus.send_coordinates_signal.emit(x, y)

    def toggle_playback(self) -> bool:
        self._is_playing = not self._is_playing
        state_text = "playing" if self._is_playing else "paused"
        self._logger.log(ConstStrings.LOG_NAME_DEBUG, f"Video {state_text}")
        return self._is_playing       


    def clear_point(self):
        if self._current_click_point is None:
            self._logger.log(ConstStrings.LOG_NAME_DEBUG, "No point to clear")
            self.status_message_signal.emit("No point to clear")
        else:
            self._current_click_point = None
            self._logger.log(ConstStrings.LOG_NAME_DEBUG, "Point cleared")
            self.status_message_signal.emit("Point cleared")

    
 