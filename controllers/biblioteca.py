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
    def search_livro(tituloS=None, autorS=None, generoS=None, statusS=None, codigoS=None):
        if not any([tituloS, autorS, generoS, statusS, codigoS]):
            print("Por favor, insira ao menos um critério de busca.")
            return

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
    
        Biblioteca.sql.cursor.execute('SELECT id_usuario, nome, cpf, telefone, senha, email FROM usuario')
        resultados = Biblioteca.sql.cursor.fetchall()

        if not resultados:
            print("Nenhum usuário encontrado.")
            Biblioteca.sql.desconectar()
            return
        
        for resultado in resultados:
            id_usuario, nome, cpf, telefone, senha, email = resultado
            print(f"ID: {id_usuario}, Nome: {nome}, CPF: {cpf}, Telefone: {telefone}, Senha: {senha}, E-mail: {email}")

        Biblioteca.sql.desconectar()

    @staticmethod
    def add_user():
        Biblioteca.sql.conectar()

        nomeA = input('Insira o nome do usuário: ')
        
        while True:
            cpfA = input('CPF: ').strip()

            if len(cpfA) != 11 or not cpfA.isdigit():
                print('CPF inválido. O CPF deve conter exatamente 11 dígitos numéricos.')
                continue

            Biblioteca.sql.cursor.execute('SELECT cpf FROM usuario WHERE cpf = %s', (cpfA,))
            resultado = Biblioteca.sql.cursor.fetchone()

            if resultado:
                print('Já existe um usuário cadastrado com esse CPF. Tente novamente.')
            else:
                break 

        telA = input('Telefone: ')

        while len(telA) > 20 or len(telA) < 10:
            print('Telefone inválido. O telefone deve conter entre 10 e 20 caracteres.')
            telA = input('Telefone: ')

        senhaA = str(input('Senha: '))

        while True:
            emailA = input('E-mail: ').strip()
            Biblioteca.sql.cursor.execute('SELECT email FROM usuario WHERE email = %s', (emailA,))
            resultado = Biblioteca.sql.cursor.fetchone()
            
            if resultado:
                print('E-mail já cadastrado, tente novamente.')
            else:
                break

        query = 'INSERT INTO usuario(nome, cpf, telefone, senha, email) VALUES (%s, %s, %s, %s, %s)'
        Biblioteca.sql.cursor.execute(query, (nomeA, cpfA, telA, senhaA, emailA))
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

    @staticmethod
    def search_usuario(nomeS=None, emailS=None, idS=None):
        if not any([nomeS, emailS, idS]):
            print("Por favor, insira ao menos um critério de busca.")
            return

        Biblioteca.sql.conectar()
        query = "SELECT id_usuario, nome, cpf, telefone, email, senha FROM usuario WHERE 1=1"
        parametros = {
            'nome': nomeS,
            'email': emailS,
            'id_usuario': idS
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
                id_usuario, nome, cpf, telefone, email, senha = resultado
                print(f"ID: {id_usuario}, Nome: {nome}, CPF: {cpf}, Telefone: {telefone}, E-mail: {email}, Senha: {senha} ")
        else:
            print("Nenhum usuário encontrado com os critérios fornecidos.")

        Biblioteca.sql.desconectar()

    @staticmethod
    def atualizar_usuario():
        Biblioteca.sql.conectar()

        id_usuario = input('ID do usuário a ser atualizado: ').strip()

        try:
            id_usuario = int(id_usuario)
        except ValueError:
            print("ID inválido. Por favor, insira um número válido.")
            Biblioteca.sql.desconectar()
            return

        Biblioteca.sql.cursor.execute('SELECT nome, telefone, senha, email, cpf FROM usuario WHERE id_usuario = %s', (id_usuario,))
        resultado = Biblioteca.sql.cursor.fetchone()

        if not resultado:
            print('Usuário não encontrado.')
            Biblioteca.sql.desconectar()
            return

        nome_atual, telefone_atual, senha_atual, email_atual, cpf_atual = resultado
        print("Usuário encontrado:")
        print(f"Nome: {nome_atual}, Telefone: {telefone_atual}, Senha: {senha_atual}, E-mail: {email_atual}, CPF: {cpf_atual}")

        print("\nAtualize os dados (deixe em branco para manter o valor atual):")
        nome = input(f"Nome [{nome_atual}]: ").strip() or nome_atual
        telefone = input(f"Telefone [{telefone_atual}]: ").strip() or telefone_atual
        senha = input(f"Senha [{senha_atual}]: ").strip() or senha_atual
        email = input(f"E-mail [{email_atual}]: ").strip() or email_atual

        update_query = '''
            UPDATE usuario
            SET nome = %s, telefone = %s, senha = %s, email = %s
            WHERE id_usuario = %s
        '''
        parametros = (nome, telefone, senha, email, id_usuario)

        Biblioteca.sql.cursor.execute(update_query, parametros)
        Biblioteca.sql.conector.commit()

        print("Usuário atualizado com sucesso!")

        Biblioteca.sql.desconectar()







    








