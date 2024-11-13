from config.db import SQL
from config.connect import host

class Livro:
    sql = SQL(**host)

    def __init__(self, titulo, autor, genero, status, codigo):
        self.titulo = titulo
        self.autor = autor
        self.genero = genero
        self.status = status
        self.codigo = codigo
    
    @staticmethod
    def create():
        # Conecta ao banco antes de inserir
        Livro.sql.conectar()

        # Dados de entrada do usuário
        tituloA = str(input('Título: '))
        autorA = str(input('Autor: '))
        generoA = str(input('Genero: '))
        codigoA = str(input('Código: '))

        # Executa a inserção
        query = 'INSERT INTO livro(titulo, autor, genero, status, codigo) VALUES (%s, %s, %s, %s, %s)'
        Livro.sql.cursor.execute(query, (tituloA, autorA, generoA, 'Disponível', codigoA))
        Livro.sql.conector.commit()  # Confirma a transação
        print("Livro adicionado com sucesso!")

        # Desconecta após a inserção
        Livro.sql.desconectar()
        
Livro.__name__ = 'Livro'