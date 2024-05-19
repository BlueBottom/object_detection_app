import os
import cv2
import numpy as np

class DataLoader:
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path

    def load_images(self):
        images = []
        for img_file in os.listdir(self.dataset_path):
            if img_file.endswith('.jpg') or img_file.endswith('.png'):
                img = cv2.imread(os.path.join(self.dataset_path, img_file))
                images.append(img)
        return images

    def preprocess(self, image):
        # Предобработка изображений (например, изменение размера, нормализация и т.д.)
        preprocessed_image = cv2.resize(image, (704, 704))
        preprocessed_image = preprocessed_image / 255.0
        return preprocessed_image