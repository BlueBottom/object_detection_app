import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import os
from ultralytics import YOLO
import random
import numpy as np


import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import os

class MainWindow:
    def __init__(self, root, detector, video_processor):
        self.current_video = None
        self.root = root
        self.root.title("Object Detection Application")
        self.detector = detector
        self.video_processor = video_processor

        # Разделение окна на две части
        self.left_frame = tk.Frame(root)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.right_frame = tk.Frame(root)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Список загруженных изображений и видео
        self.label = tk.Label(self.left_frame, text="Загруженные медиафайлы")
        self.label.pack()

        self.listbox = tk.Listbox(self.left_frame)
        self.listbox.pack(fill=tk.BOTH, expand=True)

        self.load_button = tk.Button(self.left_frame, text="Загрузить изображение", command=self.load_image)
        self.load_button.pack()

        self.load_video_button = tk.Button(self.left_frame, text="Загрузить видео", command=self.load_video)
        self.load_video_button.pack()

        # Холст для отображения изображений
        self.canvas = tk.Canvas(self.right_frame, width=800, height=600)
        self.canvas.pack()

        self.media = []  # Список для хранения обработанных изображений и видео

        # Load and process the initial image
        self.load_initial_image()

    def load_initial_image(self):
        initial_image_path = 'data/uploaded_image.png'
        if os.path.exists(initial_image_path):
            image = cv2.imread(initial_image_path)
            results = self.detector.detect(image)
            image_with_boxes = self.detector.draw_boxes(image, results)

            # Сохранение изображения с боксами
            output_path = os.path.join("processed_images", os.path.basename(initial_image_path))
            cv2.imwrite(output_path, image_with_boxes)

            # Добавление изображения в список
            self.media.append((output_path, image_with_boxes))
            self.listbox.insert(tk.END, os.path.basename(initial_image_path))
            self.listbox.bind('<<ListboxSelect>>', self.show_selected_media)

            # Отображение текущего изображения
            self.display_image(image_with_boxes)

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            image = cv2.imread(file_path)
            results = self.detector.detect(image)
            image_with_boxes = self.detector.draw_boxes(image, results)

            # Сохранение изображения с боксами
            output_path = os.path.join("processed_images", os.path.basename(file_path))
            cv2.imwrite(output_path, image_with_boxes)

            # Добавление изображения в список
            self.media.append((output_path, image_with_boxes))
            self.listbox.insert(tk.END, os.path.basename(file_path))
            self.listbox.bind('<<ListboxSelect>>', self.show_selected_media)

            # Отображение текущего изображения
            self.display_image(image_with_boxes)

    def load_video(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            output_path = self.video_processor.process_video(file_path)

            # Добавление видео в список
            self.media.append((output_path, file_path))
            self.listbox.insert(tk.END, os.path.basename(file_path))
            self.listbox.bind('<<ListboxSelect>>', self.show_selected_media)

    def show_selected_media(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            media_path, _ = self.media[index]
            if media_path.endswith('.jpg') or media_path.endswith('.png'):
                image_with_boxes = cv2.imread(media_path)
                self.display_image(image_with_boxes)
            else:
                self.display_video(media_path)

    def display_image(self, image):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image_rgb)

        # Resize image to fit canvas while maintaining aspect ratio
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        image_pil = self.resize_image(image_pil, canvas_width, canvas_height)

        image_tk = ImageTk.PhotoImage(image_pil)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=image_tk)
        self.canvas.image = image_tk

    def display_video(self, video_path):
        cap = cv2.VideoCapture(video_path)

        while (cap.isOpened()):
            ret, frame = cap.read()
            if ret:
                cv2.imshow('Video', frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break

        cap.release()
        cv2.destroyAllWindows()

    def resize_image(self, image, max_width, max_height):
        # Get current and new size of the image
        width, height = image.size
        ratio = min(max_width / width, max_height / height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)



