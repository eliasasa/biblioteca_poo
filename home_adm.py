import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
from controllers.biblioteca import Biblioteca as B

ui_file_home = 'views/home_adm.ui'
ui_file_cad = 'views/cad_livro.ui'

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(ui_file_home, self)
        self.cad_livro: QPushButton
        self.cad_livro.clicked.connect(self.tela_cad_livro)  

    def tela_cad_livro(self):
        # Carregar a tela de cadastro de livro
        uic.loadUi(ui_file_cad, self)
        self.butao.clicked.connect(self.click_cad) 
        self.cad_home.clicked.connect(self.voltar_home)  

    def voltar_home(self):
        uic.loadUi(ui_file_home, self)
        self.cad_livro.clicked.connect(self.tela_cad_livro)

    def click_cad(self):
        titulo = self.nTitle.text()
        autor = self.nAutor.text()
        genero = self.nGen.text()
        codigo = self.nCod.text()
        B.add_livro(titulo, autor, genero, 'Disponível', codigo)
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
