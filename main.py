from models.detection import ObjectDetector
from gui.main_window import MainWindow
import tkinter as tk
import os

def main():
    # Создание директории для сохранения обработанных изображений
    if not os.path.exists("processed_images"):
        os.makedirs("processed_images")

    # Инициализация детектора объектов
    object_detector = ObjectDetector('best.pt')  # Используем предобученную модель YOLOv8n

    # Графический интерфейс
    root = tk.Tk()
    app = MainWindow(root, object_detector)
    root.mainloop()

if __name__ == "__main__":
    main()
