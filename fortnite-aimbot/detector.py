import cv2
import numpy as np
import time
from typing import List, Tuple
from tensorflow.keras.models import load_model

class AimbotDetector:
    def __init__(self, model_path: str = 'models/yolov5s320Half.onnx'):
        self.model = cv2.dnn.readNetFromONNX(model_path)
        self.classes = ['player', 'head', 'body']  # Example classes
        self.conf_threshold = 0.6
        self.nms_threshold = 0.4
        self.input_size = (320, 320)
        self.last_detection = time.time()
        self.fps = 0
        
    def preprocess(self, frame: np.ndarray) -> np.ndarray:
        """Prepare frame for model input"""
        blob = cv2.dnn.blobFromImage(
            frame, 
            1/255.0, 
            self.input_size, 
            swapRB=True, 
            crop=False
        )
        return blob
        
    def postprocess(self, outputs: np.ndarray, frame_shape: Tuple[int, int]) -> List[Tuple]:
        """Process model outputs into detections"""
        height, width = frame_shape[:2]
        
        # Filter by confidence threshold
        boxes = []
        confidences = []
        class_ids = []
        
        for detection in outputs[0, 0, :, :]:
            confidence = detection[4]
            if confidence > self.conf_threshold:
                class_id = int(detection[1])
                x = int(detection[0] * width)
                y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
                
        # Apply non-max suppression
        indices = cv2.dnn.NMSBoxes(
            boxes, 
            confidences, 
            self.conf_threshold, 
            self.nms_threshold
        )
        
        results = []
        for i in indices:
            box = boxes[i]
            results.append((
                box[0], box[1], box[0]+box[2], box[1]+box[3],  # x1,y1,x2,y2
                confidences[i],
                class_ids[i]
            ))
            
        return results
        
    def process_frame(self, frame: np.ndarray) -> List[Tuple]:
        """Run full detection pipeline on a frame"""
        start_time = time.time()
        
        # Preprocess
        blob = self.preprocess(frame)
        
        # Inference
        self.model.setInput(blob)
        outputs = self.model.forward()
        
        # Postprocess
        detections = self.postprocess(outputs, frame.shape)
        
        # Calculate FPS
        now = time.time()
        self.fps = 1.0 / (now - self.last_detection)
        self.last_detection = now
        
        return detections
        
    def show_fps(self) -> float:
        """Return current detection FPS"""
        return self.fps