import mysql.connector

class SQL:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conector = None
        self.cursor = None

    def conectar(self):
        try:
            if not self.conector or not self.conector.is_connected():
                self.conector = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database
                )
                print('Conectou ao banco de dados')
            # Sempre recriar o cursor após a conexão
            self.cursor = self.conector.cursor(buffered=True)
        except mysql.connector.Error as e:
            print(f"Erro ao conectar ao banco: {e}")
            raise

    def desconectar(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.conector and self.conector.is_connected():
                self.conector.close()
            print('Desconectou do banco de dados')
        except mysql.connector.Error as e:
            print(f"Erro ao desconectar do banco: {e}")
            raise
