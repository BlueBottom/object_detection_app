from ultralytics import YOLO
import cv2
import random
import numpy as np

class ObjectDetector:
    def __init__(self, model_name='yolov8n'):
        self.model = YOLO(model_name)
        self.colors = {}

    def detect(self, image):
        results = self.model(image)
        return results

    def draw_boxes(self, image, results):
        for result in results:
            for bbox, cls_id in zip(result.boxes.xyxy.tolist(), result.boxes.cls.tolist()):
                x1, y1, x2, y2 = map(int, bbox)
                class_name = self.model.names[int(cls_id)]
                color = self.get_color(class_name)
                label_str = f'{class_name}'
                cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
                cv2.putText(image, label_str, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
        return image

    def get_color(self, label):
        if label == "vehicle":
            return (0, 165, 255)  # Оранжевый цвет в BGR
        if label not in self.colors:
            self.colors[label] = self.random_bright_color()
        return self.colors[label]

    def random_bright_color(self):
        # Генерация случайного яркого цвета
        hsv_color = [random.randint(0, 179), 255, 255]
        rgb_color = cv2.cvtColor(np.uint8([[hsv_color]]), cv2.COLOR_HSV2BGR)[0][0]
        return tuple(int(c) for c in rgb_color)