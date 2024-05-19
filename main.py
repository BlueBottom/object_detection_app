from models.detection import ObjectDetector
from gui.main_window import MainWindow
import tkinter as tk
import os

from models.videodetection import VideoProcessor


def main():
    # Создание директории для сохранения обработанных изображений и видео
    if not os.path.exists("processed_images"):
        os.makedirs("processed_images")
    if not os.path.exists("processed_videos"):
        os.makedirs("processed_videos")

    # Инициализация детектора объектов и процессора видео
    object_detector = ObjectDetector('best.pt')  # Используем предобученную модель YOLOv8n
    video_processor = VideoProcessor(object_detector)

    # Графический интерфейс
    root = tk.Tk()
    app = MainWindow(root, object_detector, video_processor)
    root.mainloop()

if __name__ == "__main__":
    main()

