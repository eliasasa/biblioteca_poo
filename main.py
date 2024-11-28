from config.db import SQL
from controllers.biblioteca import Biblioteca
from models.livro import Livro
from PyQt6.QtWidgets import QApplication

# Biblioteca.listar_livros()

# Biblioteca.add_livro('132111', 'El13211ias', '32111', '1113221', '1110')

# Biblioteca.atualizar_livro()

# Biblioteca.deletar_livro()

# Biblioteca.listar_livros()

# Biblioteca.add_user()

Biblioteca.listar_user()

# Biblioteca.search_usuario(emailS='elias')

# Biblioteca.atualizar_usuario()

# Biblioteca.delet_user()

# Lembrar de atualizar a db para a padrão

# Não esquecer de -> DELETAR USER precisa de EMPRESTIMO. -> EMPRESTIMO não pode ter mais de 3 por usuário -> Validação de login (return true)

# ctrl shift p / pip install -r requirements.txt / python 3.12.7