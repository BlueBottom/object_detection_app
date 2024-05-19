import cv2
import os

class VideoProcessor:
    def __init__(self, detector):
        self.detector = detector

    def process_video(self, video_path):
        # Открываем видео
        video = cv2.VideoCapture(video_path)

        # Получаем параметры видео
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = video.get(cv2.CAP_PROP_FPS)

        # Создаем видеописатель
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        output_path = os.path.join("processed_videos", os.path.basename(video_path))
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        while video.isOpened():
            ret, frame = video.read()
            if not ret:
                break

            # Обрабатываем кадр
            results = self.detector.detect(frame)
            frame_with_boxes = self.detector.draw_boxes(frame, results)

            # Подсчет объектов каждого класса
            class_counts = self.count_classes(results)
            object_count_text = ', '.join(f"{class_name}: {count}" for class_name, count in class_counts.items())

            # Добавление текста с подсчетом объектов на кадр
            cv2.putText(frame_with_boxes, object_count_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            # Записываем кадр в выходное видео
            out.write(frame_with_boxes)

        # Закрываем видео
        video.release()
        out.release()

        return output_path

    def count_classes(self, results):
        class_counts = {}
        for result in results:
            for cls_id in result.boxes.cls.tolist():
                class_name = self.detector.model.names[int(cls_id)]
                if class_name not in class_counts:
                    class_counts[class_name] = 0
                class_counts[class_name] += 1
        return class_counts
