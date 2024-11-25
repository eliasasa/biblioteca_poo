import sys
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton

ui_file = 'views/home_adm.ui'

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.load_ui.loadUi(ui_file, self)
        self.cad_livro:QPushButton
        self.cad_livro.clicked.connect(self.tela_cad_livro)

    def tela_cad_livro(self):
        ui_file = 'cad_livro.ui'
        uic.load_ui.loadUi(ui_file, self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())