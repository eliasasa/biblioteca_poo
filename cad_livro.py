import sys
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QRadioButton
from controllers.biblioteca import Biblioteca as B
 
# pip install PyQt6
# https://build-system.fman.io/qt-designer-download
 
ui_file = 'cad_livro.ui'
 
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.load_ui.loadUi(ui_file, self)
        self.butao.clicked.connect(self.click_cad)
 
    def click_cad(self):
        titulo = self.nTitle.text()
        autor = self.nAutor.text()
        genero = self.nGen.text()
        status = 'Disponível'
        codigo = self.nCod.text()
        B.add_livro(titulo, autor, genero, status, codigo)
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())