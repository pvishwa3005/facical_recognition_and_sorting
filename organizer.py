from pathlib import Path
import shutil


class Organizer:

    @staticmethod
    def organize(groups, output_dir):

        output_dir = Path(output_dir)

        output_dir.mkdir(
            exist_ok=True
        )

        for label, faces in groups.items():

            person_dir = (
                output_dir
                / f"person_{label}"
            )

            person_dir.mkdir(
                exist_ok=True
            )

            copied = set()

            for face in faces:

                image_path = (
                    Path(face["image_path"])
                )

                if image_path in copied:
                    continue

                copied.add(image_path)

                destination = (
                    person_dir
                    / image_path.name
                )

                shutil.copy(
                    image_path,
                    destination
                )
