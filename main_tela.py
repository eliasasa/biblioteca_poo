import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit
from controllers.biblioteca import Biblioteca as B

ui_file_home = 'views/homeAdm.ui'
ui_file_cadLivro = 'views/cadLivro.ui'
ui_file_cadUser = 'views/cadUser.ui'
ui_file_login = 'views/logUser.ui'
ui_file_deletarLivro = 'views/deletarLivro.ui'
ui_file_emp = 'views/empLivro.ui'

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

        if not usuario or not senha:
            QMessageBox.warning(self, "Erro", "Por favor, preencha nome de usuário e senha.")
            return

        login_sucesso, is_admin = B.logar(usuario, senha)

        if login_sucesso:
            if is_admin:
                QMessageBox.information(self, "Login bem-sucedido", "Usuário logado com sucesso! Você é um administrador.")
                self.login = True
                self.voltar_home()

            else:
                QMessageBox.information(self, "Login bem-sucedido", "Usuário logado com sucesso!")
                self.login = True
                # self.abrir_tela_usuario()
        else:
            QMessageBox.critical(self, "Erro", "Falha no login. Usuário ou senha incorretos.")

    def tela_emp (self):
        uic.loadUi(ui_file_emp, self)
        self.emp_home.clicked.connect(self.voltar_home)
        self.emp_but.clicked.connect(self.click_emp)

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

    def tela_del_livro(self):
        uic.loadUi(ui_file_deletarLivro, self)  
        self.del_but.clicked.connect(self.click_del_livro)
        self.delLivro_home.clicked.connect(self.voltar_home)

    # Voltar
    def voltar_home(self):
        if self.login:
            uic.loadUi(ui_file_home, self)
            self.cad_livro.clicked.connect(self.tela_cad_livro)
            self.cad_user.clicked.connect(self.tela_cad_user)
            self.del_livro.clicked.connect(self.tela_del_livro)
            self.emp_livro.clicked.connect(self.tela_emp)

        else:
            uic.loadUi(ui_file_login, self)
            self.logBut.clicked.connect(self.logar)
            self.cadBut.clicked.connect(self.tela_cad_user)

    # Funções (services)

    def limpar_inputs(self):
        for campo in self.findChildren(QLineEdit):
            campo.clear()


    def confirmar(self, mensagem):

        resposta = QMessageBox.question(
            self,
            "Confirmação",
            mensagem,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        return resposta == QMessageBox.StandardButton.Yes

    def click_emp(self):
        id_user = self.id_user.text().strip()
        cod_livro = self.cod_livro.text().strip()

        if not id_user.isdigit() or not cod_livro.isdigit():
            QMessageBox.warning(self, "Erro", "Por favor, insira um código numérico válido.")
            return

        sucesso, mensagem = B.realizar_emprestimo(id_user, cod_livro)

        if sucesso:
            QMessageBox.information(self, "Sucesso", mensagem)
        else:
            QMessageBox.warning(self, "Erro", mensagem)

        self.limpar_inputs()

    def click_cad_livro(self):
        titulo = self.nTitle.text()
        autor = self.nAutor.text()
        genero = self.nGen.text()
        codigo = self.nCod.text()

        B.add_livro(titulo, autor, genero, codigo)

        self.limpar_inputs()

    def click_cad_user(self):
        nome = self.nomeCad.text()
        cpf = self.cpfCad.text()
        telefone = self.telCad.text()
        senha = self.senCad.text()
        email = self.emailCad.text()

        if bool(B.add_user(nome, cpf, telefone, senha, email)):
            self.voltar_home()


    def click_del_livro(self):
        codigo = self.id_input.text().strip()

        if not codigo.isdigit():
            QMessageBox.warning(self, "Erro", "Por favor, insira um código numérico válido.")
            return

        status = False
        mensagem = ""

        if self.confirmar(f"Tem certeza que deseja deletar o livro com código {codigo}?"):
            status, mensagem = B.deletar_livro(codigo)

        if status:
            QMessageBox.information(self, "Sucesso", mensagem)
            self.limpar_inputs()
        else:
            QMessageBox.warning(self, "Aviso", mensagem)

        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
