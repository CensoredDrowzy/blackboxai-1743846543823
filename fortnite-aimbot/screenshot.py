import mss
import mss.tools
import numpy as np
import time
from typing import Tuple, Optional

class GameCapture:
    def __init__(self, monitor: int = 1):
        self.monitor = monitor
        self.sct = mss.mss()
        self.last_capture = time.time()
        self.fps = 0
        
    def get_monitors(self) -> list:
        """Return list of available monitors"""
        return self.sct.monitors
        
    def capture_region(self, region: Optional[Tuple[int, int, int, int]] = None) -> np.ndarray:
        """Capture screen region with performance monitoring"""
        start_time = time.time()
        
        if region:
            monitor = {
                "top": region[1],
                "left": region[0],
                "width": region[2] - region[0],
                "height": region[3] - region[1]
            }
        else:
            monitor = self.sct.monitors[self.monitor]
            
        img = np.array(self.sct.grab(monitor))
        
        # Calculate FPS
        now = time.time()
        self.fps = 1.0 / (now - self.last_capture)
        self.last_capture = now
        
        return img
        
    def show_fps(self) -> float:
        """Return current capture FPS"""
        return self.fps