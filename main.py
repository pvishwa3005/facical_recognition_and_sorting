import sys
from PyQt6.QtWidgets import QApplication

from gui import FaceSorterGUI


def main():

    app = QApplication(sys.argv)

    window = FaceSorterGUI()

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
