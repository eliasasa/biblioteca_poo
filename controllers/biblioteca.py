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
            Biblioteca.sql.desconectar()
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
    def obter_dados_livro():
        titulo = str(input('Título: '))
        autor = str(input('Autor: '))
        genero = str(input('Gênero: '))
        codigo = int(input('Código: '))
        status = Biblioteca.definir_status()
        return Livro(titulo, autor, genero, status, codigo)

    @staticmethod
    def definir_status():
        while True:
            print('1 - Disponível\n2 - Indisponível')
            try:
                status_opcao = int(input('Status: '))
                if status_opcao == 1:
                    return 'Disponível'
                elif status_opcao == 2:
                    return 'Indisponível'
                else:
                    print("Opção inválida, escolha 1 ou 2.")
            except ValueError:
                print("Digite um número válido.")

    @staticmethod
    def add_livro():
        Biblioteca.sql.conectar()
        livro = Biblioteca.obter_dados_livro()
        query = 'INSERT INTO livro(titulo, autor, genero, status, codigo) VALUES (%s, %s, %s, %s, %s)'
        Biblioteca.sql.cursor.execute(query, livro.to_tuple())
        Biblioteca.sql.conector.commit()
        print("Livro adicionado com sucesso!")
        Biblioteca.sql.desconectar()

    @staticmethod
    def atualizar_livro():
        Biblioteca.sql.conectar()

        codigoU = input('Código do livro a ser atualizado: ').strip()

        try:
            codigoU = int(codigoU)
        except ValueError:
            print("Código inválido. Por favor, insira um número válido.")
            Biblioteca.sql.desconectar()
            return

        Biblioteca.sql.cursor.execute('SELECT * FROM livro WHERE codigo = %s', (codigoU,))
        resultado = Biblioteca.sql.cursor.fetchone()

        if not resultado:
            print('Livro não encontrado.')
            Biblioteca.sql.desconectar()
            return

        print("Livro encontrado:", resultado)


        livro_atualizado = Biblioteca.obter_dados_livro()

        update_query = '''
            UPDATE livro
            SET titulo = %s, autor = %s, genero = %s, status = %s, codigo = %s
            WHERE codigo = %s
        '''

        Biblioteca.sql.cursor.execute(update_query, (*livro_atualizado.to_tuple(), codigoU))

        Biblioteca.sql.conector.commit()

        print("Livro atualizado com sucesso!")

        Biblioteca.sql.desconectar()

    @staticmethod
    def confirmar():
        conf = input(f'Tem certeza que deseja fazer a exclusão? (Y/N): ').strip().upper()

        if conf == 'Y':
            return True
        else:
            print('Ação cancelada.')
            return False

    @staticmethod
    def deletar_livro():
        Biblioteca.sql.conectar()

        codigoU = input('Código do livro a ser deletado: ').strip()

        try:
            codigoU = int(codigoU)
        except ValueError:
            print("Código inválido. Por favor, insira um número válido.")
            Biblioteca.sql.desconectar()
            return

        Biblioteca.sql.cursor.execute('SELECT * FROM livro WHERE codigo = %s', (codigoU,))
        resultado = Biblioteca.sql.cursor.fetchone()

        if not resultado:
            print('Livro não encontrado.')
            Biblioteca.sql.desconectar()
            return

        print("Livro encontrado:", resultado)

        if resultado[-2] == 'Indisponível':
            print('Livro emprestado, não pode ser deletado.')
            Biblioteca.sql.desconectar() 
            return
        
        if Biblioteca.confirmar():
        
            delet_query = '''
                DELETE FROM livro WHERE codigo = %s
            '''

            Biblioteca.sql.cursor.execute(delet_query, (codigoU,))
            Biblioteca.sql.conector.commit()

            print("Livro deletado com sucesso!")

        else: pass

        Biblioteca.sql.desconectar()
    
    @staticmethod
    def listar_user():
        Biblioteca.sql.conectar()
    
        Biblioteca.sql.cursor.execute('SELECT id_usuario, nome, cpf, telefone FROM usuario')
        resultados = Biblioteca.sql.cursor.fetchall()

        if not resultados:
            print("Nenhum usuário encontrado.")
            Biblioteca.sql.desconectar()
            return
        
        for resultado in resultados:
            id_usuario, nome, cpf, telefone = resultado
            print(f"ID: {id_usuario}, Nome: {nome}, CPF: {cpf}, Telefone: {telefone}")

        Biblioteca.sql.desconectar()

    @staticmethod
    def add_user():
        Biblioteca.sql.conectar()

        nomeA = input('Insira o nome do usuário: ')
        cpfA = input('CPF: ')

        while len(cpfA) != 11 or not cpfA.isdigit():
            print('CPF inválido. O CPF deve conter exatamente 11 dígitos numéricos.')
            cpfA = input('CPF: ')

        telA = input('Telefone: ')

        while len(telA) > 20 or len(telA) < 10:
            print('Telefone inválido. O telefone deve conter entre 10 e 20 caracteres.')
            telA = input('Telefone: ')

        Biblioteca.sql.cursor.execute('SELECT cpf FROM usuario WHERE cpf = %s', (cpfA,))
        resultado = Biblioteca.sql.cursor.fetchone()

        if resultado:
            print('Já existe um usuário cadastrado com esse CPF.')
            Biblioteca.sql.desconectar()
            return

        query = 'INSERT INTO usuario(nome, cpf, telefone) VALUES (%s, %s, %s)'
        Biblioteca.sql.cursor.execute(query, (nomeA, cpfA, telA))
        Biblioteca.sql.conector.commit()
        print("Usuário adicionado com sucesso!")

        Biblioteca.sql.desconectar()

    @staticmethod
    def delet_user():
        Biblioteca.sql.conectar()

        try:
            idD = int(input('ID do usuário a ser deletado: ').strip())
        except ValueError:
            print("ID inválido. O ID deve ser um número inteiro.")
            Biblioteca.sql.desconectar()
            return

        Biblioteca.sql.cursor.execute('SELECT * FROM usuario WHERE id_usuario = %s', (idD,))
        resultado = Biblioteca.sql.cursor.fetchone()

        if not resultado:
            print('Usuário não encontrado.')
            Biblioteca.sql.desconectar()
            return

        print("Usuário encontrado:", resultado)

        if Biblioteca.confirmar():
            delet_query = 'DELETE FROM usuario WHERE id_usuario = %s'
            Biblioteca.sql.cursor.execute(delet_query, (idD,))
            Biblioteca.sql.conector.commit()

            print("Usuário deletado com sucesso!")
                
        else: pass
            
        Biblioteca.sql.desconectar()



    








