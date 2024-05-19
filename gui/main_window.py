import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import os
from ultralytics import YOLO
import random
import numpy as np


class MainWindow:
    def __init__(self, root, detector):
        self.root = root
        self.root.title("Object Detection Application")
        self.detector = detector

        # Разделение окна на две части
        self.left_frame = tk.Frame(root)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.right_frame = tk.Frame(root)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Список загруженных изображений
        self.label = tk.Label(self.left_frame, text="Загруженные изображения")
        self.label.pack()

        self.listbox = tk.Listbox(self.left_frame)
        self.listbox.pack(fill=tk.BOTH, expand=True)

        self.load_button = tk.Button(self.left_frame, text="Загрузить изображение", command=self.load_image)
        self.load_button.pack()

        # Холст для отображения изображений
        self.canvas = tk.Canvas(self.right_frame, width=800, height=600)
        self.canvas.pack()

        self.images = []  # Список для хранения обработанных изображений

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
            self.images.append((output_path, image_with_boxes))
            self.listbox.insert(tk.END, os.path.basename(initial_image_path))
            self.listbox.bind('<<ListboxSelect>>', self.show_selected_image)

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
            self.images.append((output_path, image_with_boxes))
            self.listbox.insert(tk.END, os.path.basename(file_path))
            self.listbox.bind('<<ListboxSelect>>', self.show_selected_image)

            # Отображение текущего изображения
            self.display_image(image_with_boxes)

    def show_selected_image(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            _, image_with_boxes = self.images[index]
            self.display_image(image_with_boxes)

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

    def resize_image(self, image, max_width, max_height):
        # Get current and new size of the image
        width, height = image.size
        ratio = min(max_width / width, max_height / height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)
