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

            # Записываем кадр в выходное видео
            out.write(frame_with_boxes)

        # Закрываем видео
        video.release()
        out.release()

        return output_path
