import sys
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QRadioButton
# pip install PyQt6
# https://build-system.fman.io/qt-designer-download

ui_file = 'C:/Users/EliasNeto/Documents/GitHub/biblioteca_poo/teste.ui'

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.load_ui.loadUi(ui_file, self)
        self.butao.setText('0')
        self.butao.clicked.connect(self.clicked)
        self.a = 2

    def clicked(self):
        while self.a < 9999999999999:
            self.a += self.a
            self.butao.setText(str(self.a))

        print(self.a)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())