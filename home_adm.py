import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
from controllers.biblioteca import Biblioteca as B

ui_file_home = 'views/homeAdm.ui'
ui_file_cadLivro = 'views/cadLivro.ui'
ui_file_cadUser = 'views/cadUser.ui'
ui_file_login = 'views/logUser.ui'

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(ui_file_login, self)
        self.logBut.clicked.connect(self.logar)
        self.cadBut.clicked.connect(self.tela_cad_user)
        self.login = False

    def logar(self):
        usuario = self.logUser.text()
        senha = self.logSen.text()

        # Fazer tratamento, criar table de adm e emprestimo

        print(usuario, senha)

        self.login = True
        self.voltar_home()
    
    def tela_cad_user (self):
        # Carrrega tela de cadastro de usuário
        uic.loadUi(ui_file_cadUser, self)
        self.cadUserBut.clicked.connect(self.click_cad_user)
        self.cadUser_home.clicked.connect(self.voltar_home)

    def tela_cad_livro(self):
        # Carregar a tela de cadastro de livro
        uic.loadUi(ui_file_cadLivro, self)
        self.butao.clicked.connect(self.click_cad_livro) 
        self.cad_home.clicked.connect(self.voltar_home)  

    # Voltar
    def voltar_home(self):
        if self.login:
            uic.loadUi(ui_file_home, self)
            self.cad_livro.clicked.connect(self.tela_cad_livro)
            self.cad_user.clicked.connect(self.tela_cad_user)
        else:
            uic.loadUi(ui_file_login, self)
            self.logBut.clicked.connect(self.logar)
            self.cadBut.clicked.connect(self.tela_cad_user)

    # Funções (services)
    def click_cad_livro(self):
        titulo = self.nTitle.text()
        autor = self.nAutor.text()
        genero = self.nGen.text()
        codigo = self.nCod.text()
        B.add_livro(titulo, autor, genero, 'Disponível', codigo)
    
    def click_cad_user(self):
        nome = self.nomeCad.text()
        cpf = self.cpfCad.text()
        telefone = self.telCad.text()
        senha = self.senCad.text()
        email = self.emailCad.text()

        print(nome, cpf, telefone, senha, email)
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
