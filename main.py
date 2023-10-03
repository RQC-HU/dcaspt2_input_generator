import os
import sys

from qtpy.QtGui import QScreen
from qtpy.QtWidgets import QApplication

from components.main_window import MainWindow

# import qt_material


def main():
    app = QApplication(sys.argv)
    # qt_material.apply_stylesheet(app, theme='dark_teal.xml') # 'dark_teal.xml
    # stylesheet = app.styleSheet()
    # app.setStyleSheet(stylesheet + "QTableView {background-color: #514;}")
    window = MainWindow()
    width, height = int(QScreen.availableGeometry(QApplication.primaryScreen()).width() * (2 / 3)), int(
        QScreen.availableGeometry(QApplication.primaryScreen()).height() * (2 / 3)
    )
    window.setWindowTitle("DIRAC-CASPT2 Input Generator")
    window.resize(width, height)
    window.show()
    try:
        sys.exit(app.exec())
    except SystemExit:
        # Remove the sum_dirac_dfcoef.out file
        filename = "sum_dirac_dfcoef.out"
        if os.path.exists(filename):
            os.remove(filename)


if __name__ == "__main__":
    main()
