import tkinter as tk
from tkinter import ttk, filedialog
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

        # Цветовая палитра
        dark_blue = "#1E1E3F"
        mid_blue = "#2B2B6E"
        light_blue = "#3C3C88"
        accent_blue = "#00AFFF"
        text_color = "#FFFFFF"

        # Configure root window style
        self.root.configure(bg=dark_blue)

        # Define styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TButton", padding=6, relief="flat",
                             background=accent_blue, foreground=text_color, font=('Helvetica', 12),
                             borderwidth=0, focusthickness=0)
        self.style.map("TButton",
                       background=[('active', light_blue)],
                       foreground=[('active', text_color)])

        # Split the window into two parts
        self.left_frame = tk.Frame(root, bg=mid_blue)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.right_frame = tk.Frame(root, bg=dark_blue)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.object_count_label = tk.Label(self.right_frame, bg=dark_blue, fg=text_color, font=('Helvetica', 14))
        self.object_count_label.pack(pady=10)

        # List of loaded images and videos
        self.label = tk.Label(self.left_frame, text=" Загруженные медиафайлы ", bg=mid_blue, fg=text_color, font=('Helvetica', 12))
        self.label.pack(pady=10)

        self.listbox = tk.Listbox(self.left_frame, bg=light_blue, fg=text_color, font=('Helvetica', 12), bd=0, highlightthickness=0, selectbackground=accent_blue)
        self.listbox.pack(fill=tk.BOTH, expand=True)

        self.load_image_button = ttk.Button(self.left_frame, text="Загрузить изображение", command=self.load_image)
        self.load_image_button.pack(fill=tk.X, pady=5)

        self.load_video_button = ttk.Button(self.left_frame, text="Загрузить видео", command=self.load_video)
        self.load_video_button.pack(fill=tk.X, pady=5)

        # Canvas for displaying images
        self.canvas = tk.Canvas(self.right_frame, width=800, height=600, bg=dark_blue, highlightthickness=0)
        self.canvas.pack(expand=True)

        self.media = []  # List for storing processed images and videos

        # Load and process the initial image
        self.load_initial_image()

    def load_initial_image(self):
        initial_image_path = 'data/uploaded_image.png'
        if os.path.exists(initial_image_path):
            image = cv2.imread(initial_image_path)
            results = self.detector.detect(image)
            image_with_boxes = self.detector.draw_boxes(image, results)

            # Save image with boxes
            output_path = os.path.join("processed_images", os.path.basename(initial_image_path))
            cv2.imwrite(output_path, image_with_boxes)

            # Add image to list
            self.media.append((output_path, image_with_boxes))
            self.listbox.insert(tk.END, os.path.basename(initial_image_path))
            self.listbox.bind('<<ListboxSelect>>', self.show_selected_media)

            # Display current image
            self.display_image(image_with_boxes)

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            image = cv2.imread(file_path)
            results = self.detector.detect(image)
            image_with_boxes = self.detector.draw_boxes(image, results)

            # Save image with boxes
            output_path = os.path.join("processed_images", os.path.basename(file_path))
            cv2.imwrite(output_path, image_with_boxes)

            # Add image to list
            self.media.append((output_path, image_with_boxes))
            self.listbox.insert(tk.END, os.path.basename(file_path))
            self.listbox.bind('<<ListboxSelect>>', self.show_selected_media)

            # Display current image
            self.display_image(image_with_boxes, results)

    def load_video(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            output_path = self.video_processor.process_video(file_path)

            # Add video to list
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

    def count_classes(self, results):
        class_counts = {}
        for result in results:
            for cls_id in result.boxes.cls.tolist():
                class_name = self.detector.model.names[int(cls_id)]
                if class_name not in class_counts:
                    class_counts[class_name] = 0
                class_counts[class_name] += 1
        return class_counts

    def display_image(self, image, results=None):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image_rgb)

        if results is not None:
            class_counts = self.count_classes(results)
            object_count_text = ', '.join(f"{class_name}: {count}" for class_name, count in class_counts.items())
            self.object_count_label.config(text=object_count_text)

        # Resize image to fit canvas while maintaining aspect ratio
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        image_pil = self.resize_image(image_pil, canvas_width, canvas_height)

        image_tk = ImageTk.PhotoImage(image_pil)
        self.canvas.create_image(canvas_width // 2, canvas_height // 2, anchor=tk.CENTER, image=image_tk)
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