from pathlib import Path
import face_recognition
import numpy as np
from sklearn.cluster import DBSCAN
from PIL import Image


class FaceEngine:

    def __init__(self):

        self.faces = []

    def process_images(
        self,
        image_paths,
        preview_dir="face_previews"
    ):

        Path(preview_dir).mkdir(
            exist_ok=True
        )

        self.faces = []

        face_id = 0

        for image_path in image_paths:

            try:

                image = (
                    face_recognition
                    .load_image_file(
                        image_path
                    )
                )

                locations = (
                    face_recognition
                    .face_locations(image)
                )

                encodings = (
                    face_recognition
                    .face_encodings(
                        image,
                        locations
                    )
                )

                pil_image = (
                    Image.fromarray(image)
                )

                for encoding, location in zip(
                    encodings,
                    locations
                ):

                    top, right, bottom, left = (
                        location
                    )

                    face_crop = (
                        pil_image.crop(
                            (
                                left,
                                top,
                                right,
                                bottom
                            )
                        )
                    )

                    preview_path = (
                        Path(preview_dir)
                        / f"face_{face_id}.jpg"
                    )

                    face_crop.save(
                        preview_path
                    )

                    self.faces.append({

                        "encoding":
                            encoding,

                        "image_path":
                            image_path,

                        "preview_path":
                            preview_path.name
                    })

                    face_id += 1

            except Exception as e:

                print(e)

    def cluster_faces(self):

        if not self.faces:
            return {}

        X = np.array([
            f["encoding"]
            for f in self.faces
        ])

        clustering = DBSCAN(
            metric="euclidean",
            eps=0.5,
            min_samples=1
        )

        labels = (
            clustering.fit_predict(X)
        )

        grouped = {}

        for label, face in zip(
            labels,
            self.faces
        ):

            if label not in grouped:

                grouped[label] = []

            grouped[label].append(face)

        return grouped
