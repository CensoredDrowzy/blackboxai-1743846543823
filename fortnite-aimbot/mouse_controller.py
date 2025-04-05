from pynput.mouse import Controller
import random
import time
import math
from typing import Tuple

class SilentMouse:
    def __init__(self, smoothness: float = 0.8, jitter: float = 0.1):
        self.controller = Controller()
        self.smoothness = max(0.1, min(1.0, smoothness))
        self.jitter = max(0.0, min(0.5, jitter))
        self.last_position = self.controller.position
        
    def _bezier_curve(self, start: Tuple[int, int], end: Tuple[int, int], t: float) -> Tuple[int, int]:
        """Generate smooth bezier curve coordinates"""
        x = (1-t)**2 * start[0] + 2*(1-t)*t * (start[0] + end[0])/2 + t**2 * end[0]
        y = (1-t)**2 * start[1] + 2*(1-t)*t * (start[1] + end[1])/2 + t**2 * end[1]
        return (int(x), int(y))
        
    def move_to(self, x: int, y: int, duration: float = 0.2):
        """Move mouse to target coordinates with human-like motion"""
        start = self.controller.position
        end = (x, y)
        
        steps = max(5, int(duration * 100))
        for i in range(steps):
            t = i / steps
            # Apply smooth bezier curve
            target = self._bezier_curve(start, end, t)
            
            # Add random jitter
            jitter_x = random.uniform(-self.jitter, self.jitter) * (end[0] - start[0])
            jitter_y = random.uniform(-self.jitter, self.jitter) * (end[1] - start[1])
            target = (target[0] + int(jitter_x), target[1] + int(jitter_y))
            
            self.controller.position = target
            time.sleep(duration/steps)
            
        # Ensure final position is exact
        self.controller.position = end
        self.last_position = end

    def click(self, button: str = 'left', count: int = 1):
        """Simulate mouse click with random delays"""
        for _ in range(count):
            delay = random.uniform(0.05, 0.15)
            time.sleep(delay)
            if button == 'left':
                self.controller.click(Controller.Button.left)
            else:
                self.controller.click(Controller.Button.right)
            time.sleep(delay * 2)