from config.db import SQL
from controllers.biblioteca import Biblioteca
from models.livro import Livro

Biblioteca.listar_livros()

Biblioteca.add_livro()

Biblioteca.atualizar_livro()

Biblioteca.deletar_livro()

Biblioteca.listar_livros()

Biblioteca.add_user()

Biblioteca.listar_user()

Biblioteca.delet_user()

# Lembrar de atualizar a db para a padrão

# Email, Senha -> Lembrar de fazer