from pathlib import Path
import face_recognition
import numpy as np
from sklearn.cluster import DBSCAN


class FaceEngine:

    def __init__(self):
        self.image_paths = []
        self.encodings = []
        self.encoding_to_image = []

    def load_images(self, folder):
        folder = Path(folder)

        supported = [".jpg", ".jpeg", ".png"]

        self.image_paths = [
            p for p in folder.iterdir()
            if p.suffix.lower() in supported
        ]

    def process_images(self, progress_callback=None):

        total = len(self.image_paths)

        for idx, image_path in enumerate(self.image_paths):

            try:
                image = face_recognition.load_image_file(image_path)

                locations = face_recognition.face_locations(image)

                encodings = face_recognition.face_encodings(
                    image,
                    locations
                )

                for encoding in encodings:
                    self.encodings.append(encoding)
                    self.encoding_to_image.append(image_path)

            except Exception as e:
                print(f"Error processing {image_path}: {e}")

            if progress_callback:
                progress_callback(idx + 1, total)

    def cluster_faces(self):

        if not self.encodings:
            return {}

        X = np.array(self.encodings)

        clustering = DBSCAN(
            metric="euclidean",
            eps=0.5,
            min_samples=1
        )

        labels = clustering.fit_predict(X)

        grouped = {}

        for label, image_path in zip(labels, self.encoding_to_image):

            if label not in grouped:
                grouped[label] = set()

            grouped[label].add(image_path)

        return grouped
