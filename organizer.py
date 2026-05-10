from pathlib import Path
import shutil


class Organizer:

    @staticmethod
    def organize(grouped_faces, output_folder):

        output_folder = Path(output_folder)

        output_folder.mkdir(parents=True, exist_ok=True)

        for label, images in grouped_faces.items():

            person_dir = output_folder / f"person_{label}"

            person_dir.mkdir(exist_ok=True)

            for image_path in images:

                destination = person_dir / image_path.name

                try:
                    shutil.copy(image_path, destination)

                except Exception as e:
                    print(f"Copy failed: {e}")
