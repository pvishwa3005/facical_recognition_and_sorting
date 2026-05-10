from PyQt6.QtWidgets import (
    QWidget,
    QPushButton,
    QLabel,
    QFileDialog,
    QVBoxLayout,
    QProgressBar,
    QMessageBox,
    QApplication
)

from face_engine import FaceEngine
from organizer import Organizer


class FaceSorterGUI(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Face Photo Sorter")
        self.setGeometry(200, 200, 400, 250)

        self.input_folder = None
        self.output_folder = None

        self.face_engine = FaceEngine()

        self.init_ui()

    def init_ui(self):

        layout = QVBoxLayout()

        self.input_label = QLabel("No input folder selected")
        self.output_label = QLabel("No output folder selected")

        self.select_input_btn = QPushButton("Select Photos Folder")
        self.select_output_btn = QPushButton("Select Output Folder")

        self.start_btn = QPushButton("Start Sorting")

        self.progress = QProgressBar()

        layout.addWidget(self.input_label)
        layout.addWidget(self.select_input_btn)

        layout.addWidget(self.output_label)
        layout.addWidget(self.select_output_btn)

        layout.addWidget(self.progress)
        layout.addWidget(self.start_btn)

        self.setLayout(layout)

        self.select_input_btn.clicked.connect(
            self.select_input_folder
        )

        self.select_output_btn.clicked.connect(
            self.select_output_folder
        )

        self.start_btn.clicked.connect(
            self.start_sorting
        )

    def select_input_folder(self):

        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Photos Folder"
        )

        if folder:
            self.input_folder = folder
            self.input_label.setText(folder)

    def select_output_folder(self):

        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Output Folder"
        )

        if folder:
            self.output_folder = folder
            self.output_label.setText(folder)

    def update_progress(self, current, total):

        percent = int((current / total) * 100)

        self.progress.setValue(percent)

        QApplication.processEvents()

    def start_sorting(self):

        if not self.input_folder or not self.output_folder:

            QMessageBox.warning(
                self,
                "Error",
                "Please select both folders."
            )

            return

        self.face_engine.load_images(self.input_folder)

        self.face_engine.process_images(
            progress_callback=self.update_progress
        )

        grouped = self.face_engine.cluster_faces()

        Organizer.organize(
            grouped,
            self.output_folder
        )

        QMessageBox.information(
            self,
            "Done",
            f"Finished sorting into {len(grouped)} groups."
        )
