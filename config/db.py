import mysql.connector as sql

class SQL:
    def __init__(self, host, user, password, database) -> None:
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conector = None
        self.cursor = None

    def conectar(self):
        self.conector = sql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        print('Conectou ao banco de dados')
        self.cursor = self.conector.cursor()

    def desconectar(self):
        if self.cursor:
            self.cursor.close()
        if self.conector:
            self.conector.close()
        print('Desconectou do banco de dados')
    
class User:
    max_emprestimo = 3
    
    def __init__(self, nome, cpf):
        self.nome = nome
        self.cpf = cpf
        self.livros_emprestados = 0

SQL.__name__ = 'SQL'