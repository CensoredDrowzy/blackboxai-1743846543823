import cv2
import time
import argparse
from detector import AimbotDetector
from mouse_controller import SilentMouse
from screenshot import GameCapture
from safety_checks import SafetySystem

class FortniteAimbot:
    def __init__(self, config: dict):
        self.config = config
        self.detector = AimbotDetector(config['model_path'])
        self.mouse = SilentMouse(
            smoothness=config['smoothness'],
            jitter=config['jitter']
        )
        self.capture = GameCapture(config['monitor'])
        self.safety = SafetySystem()
        self.running = False
        self.debug = config['debug']
        
    def start(self):
        """Main execution loop"""
        self.running = True
        print("[+] Fortnite Aimbot started (Educational Use Only)")
        
        try:
            while self.running:
                # Run safety checks
                if not self.safety.run_checks():
                    break
                
                # Capture frame
                frame = self.capture.capture_region()
                
                # Process detection
                detections = self.detector.process_frame(frame)
                
                if detections:
                    # Get best target (highest confidence head detection)
                    head_detections = [d for d in detections if d[5] == 1]  # class 1 = head
                    if head_detections:
                        best_target = max(head_detections, key=lambda x: x[4])
                        x_center = (best_target[0] + best_target[2]) // 2
                        y_center = (best_target[1] + best_target[3]) // 2
                        
                        # Move mouse to target
                        self.mouse.move_to(x_center, y_center)
                        
                        if self.config['auto_fire']:
                            self.mouse.click(count=1)
                
                # Debug info
                if self.debug:
                    print(f"Capture FPS: {self.capture.show_fps():.1f} | "
                          f"Detection FPS: {self.detector.show_fps():.1f} | "
                          f"Targets: {len(detections)}")
                
                # Control loop speed
                time.sleep(1/self.config['max_fps'])
                
        except KeyboardInterrupt:
            print("\n[!] Stopped by user")
        finally:
            self.stop()
            
    def stop(self):
        """Clean shutdown"""
        self.running = False
        print("[+] Aimbot stopped")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", help="Enable debug output")
    parser.add_argument("--auto-fire", action="store_true", help="Enable automatic firing")
    args = parser.parse_args()
    
    config = {
        'model_path': 'models/yolov5s320Half.onnx',
        'monitor': 1,
        'smoothness': 0.7,
        'jitter': 0.15,
        'max_fps': 60,
        'auto_fire': args.auto_fire,
        'debug': args.debug
    }
    
    aimbot = FortniteAimbot(config)
    aimbot.start()