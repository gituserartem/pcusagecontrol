from PyQt5.QtWidgets import (QApplication)
from MainWindow import MainWindow

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())
