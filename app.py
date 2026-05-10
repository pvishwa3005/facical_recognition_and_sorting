from flask import (
    Flask,
    render_template,
    request,
    send_from_directory
)

from pathlib import Path
import os

from face_engine import FaceEngine
from organizer import Organizer


app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
PREVIEW_FOLDER = "face_previews"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PREVIEW_FOLDER, exist_ok=True)


@app.route("/")
def index():

    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    files = request.files.getlist("photos")

    output_dir = request.form["output_dir"]

    uploaded_paths = []

    for file in files:

        if file.filename == "":
            continue

        save_path = (
            Path(UPLOAD_FOLDER)
            / file.filename
        )

        file.save(save_path)

        uploaded_paths.append(
            str(save_path)
        )

    engine = FaceEngine()

    engine.process_images(
        uploaded_paths,
        PREVIEW_FOLDER
    )

    groups = engine.cluster_faces()

    Organizer.organize(
        groups,
        output_dir
    )

    display_groups = {}

    for label, faces in groups.items():

        display_groups[label] = []

        for face in faces:

            display_groups[label].append({

                "preview":
                    face["preview_path"]
                    .replace("\\", "/"),

                "image":
                    face["image_path"]
            })

    return render_template(
        "index.html",
        groups=display_groups
    )


@app.route(
    '/face_previews/<path:filename>'
)
def face_previews(filename):

    return send_from_directory(
        PREVIEW_FOLDER,
        filename
    )


if __name__ == "__main__":

    app.run(debug=True)
