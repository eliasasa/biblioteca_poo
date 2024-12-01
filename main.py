from config.db import SQL
from controllers.biblioteca import Biblioteca
from models.livro import Livro
import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox

# Biblioteca.listar_livros()

# Biblioteca.add_livro('132111', 'El13211ias', '32111', '1113221', '1110')

# Biblioteca.atualizar_livro()

# Biblioteca.deletar_livro()

# Biblioteca.listar_livros()

# Biblioteca.add_user()

# Biblioteca.listar_user()

# total = Biblioteca.consultar_emprestimos_usuario(1)
# print(total)

# Biblioteca.realizar_emprestimo(2, 103)

Biblioteca.devolver_livro(2, 103)

# Biblioteca.realizar_emprestimo(2, 103)

# Biblioteca.search_usuario(emailS='elias')

# Biblioteca.atualizar_usuario()

# Biblioteca.delet_user()

# Lembrar de atualizar a db para a padrão

# Não esquecer de -> DELETAR USER precisa de EMPRESTIMO. -> EMPRESTIMO não pode ter mais de 3 por usuário -> Validação de login (return true)

# ctrl shift p / pip install -r requirements.txt / python 3.12.7