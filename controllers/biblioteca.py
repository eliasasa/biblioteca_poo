from config.db import SQL
from config.connect import host
from models.livro import Livro

class Biblioteca:
    sql = SQL(**host)

    @staticmethod
    def listar_livros():
        Biblioteca.sql.conectar()
        Biblioteca.sql.cursor.execute('SELECT titulo, autor, genero, status, codigo FROM livro')
        resultados = Biblioteca.sql.cursor.fetchall()

        if not resultados:
            print("Nenhum livro encontrado.")
            return

        for resultado in resultados:
            titulo, autor, genero, status, codigo = resultado
            print(f"Título: {titulo}, Autor: {autor}, Gênero: {genero}, Status: {status}, Código: {codigo}")

        Biblioteca.sql.desconectar()

    @staticmethod
    def search(tituloS=None, autorS=None, generoS=None, statusS=None, codigoS=None):
        Biblioteca.sql.conectar()
        query = "SELECT titulo, autor, genero, status, codigo FROM livro WHERE 1=1"

        parametros = {
            'titulo': tituloS,
            'autor': autorS,
            'genero': generoS,
            'status': statusS,
            'codigo': codigoS
        }

        query_parametros = []

        for campo, valor in parametros.items():
            if valor is not None:
                if isinstance(valor, str): 
                    query += f" AND {campo} LIKE %s"
                    query_parametros.append('%' + valor.lower() + '%')
                else:
                    query += f" AND {campo} = %s"
                    query_parametros.append(valor)

        Biblioteca.sql.cursor.execute(query, query_parametros)
        resultados = Biblioteca.sql.cursor.fetchall()

        if resultados:
            for resultado in resultados:
                titulo, autor, genero, status, codigo = resultado
                print(f"Título: {titulo}, Autor: {autor}, Gênero: {genero}, Status: {status}, Código: {codigo}")
        else:
            print("Nenhum livro encontrado com os critérios fornecidos.")

        Biblioteca.sql.desconectar()

    @staticmethod
    def add_livro():
        Biblioteca.sql.conectar()
        Livro.create()
        Biblioteca.sql.conector.commit()  # Confirma as alterações no banco
        Biblioteca.sql.desconectar()
