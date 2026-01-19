import cv2
import numpy as np
from typing import Optional, Tuple, Union
from model.data_classes.point import Point


class VideoManager:
    
    def __init__(self, video_path: str):
        self._video_path = video_path
        self._video_capture = None
        self._current_frame = None
        
    def load_video(self) -> bool:
        self._video_capture = cv2.VideoCapture(self._video_path)
        return self._video_capture.isOpened()
    
    def get_fps(self) -> float:
        if self._video_capture:
            fps = self._video_capture.get(cv2.CAP_PROP_FPS)
            return fps if fps > 0 else 30.0
        return 30.0
    
    def read_frame(self) -> bool:
        if self._video_capture:
            ret, frame = self._video_capture.read()
            if ret:
                self._current_frame = frame.copy()
                return True
            else:
                # Loop video
                self._video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
                return False
        return False
    
    def get_current_frame(self) -> Optional[np.ndarray]:
        return self._current_frame.copy() if self._current_frame is not None else None
    
    def get_current_frame_rgb(self) -> Optional[np.ndarray]:
        if self._current_frame is not None:
            return cv2.cvtColor(self._current_frame, cv2.COLOR_BGR2RGB)
        return None
    
    def get_display_frame(self, click_point: Optional[Union[Point, Tuple[int, int]]], 
                          label_width: int, label_height: int) -> Optional[np.ndarray]:
        if self._current_frame is None:
            return None
        
        frame = self._current_frame.copy()
        
        if click_point:
            # Handle both Point dataclass and tuple
            if isinstance(click_point, Point):
                x, y = click_point.x, click_point.y
            else:
                x, y = click_point
            
            frame_h, frame_w = frame.shape[:2]
            scaled_x = int(x * frame_w / label_width)
            scaled_y = int(y * frame_h / label_height)
            
            cv2.circle(frame, (scaled_x, scaled_y), 8, (255, 0, 0), -1)
            cv2.circle(frame, (scaled_x, scaled_y), 10, (255, 255, 255), 2)
        
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    
    def draw_point(self, frame: np.ndarray, x: int, y: int, 
                   frame_width: int, frame_height: int,
                   label_width: int, label_height: int) -> np.ndarray:
        scaled_x = int(x * frame_width / label_width)
        scaled_y = int(y * frame_height / label_height)
        
        cv2.circle(frame, (scaled_x, scaled_y), 8, (255, 0, 0), -1)
        cv2.circle(frame, (scaled_x, scaled_y), 10, (255, 255, 255), 2)
        
        return frame
    
    def release(self):
        if self._video_capture:
            self._video_capture.release()
