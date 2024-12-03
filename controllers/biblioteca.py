from config.db import SQL
from models.livro import Livro
from config.connect import host


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

    # @staticmethod
    # def obter_dados_livro(titulo, autor, genero, status, codigo):
    #     titulo = str(input('Título: '))
    #     autor = str(input('Autor: '))
    #     genero = str(input('Gênero: '))
    #     codigo = int(input('Código: '))
    #     status = Biblioteca.definir_status()
    #     return Livro(titulo, autor, genero, status, codigo)

    @staticmethod
    def definir_status():
        while True:
            print('1 - Disponível\n2 - Indisponível')
            try:
                status_opcao = int(input('Status: '))
                if status_opcao == 1:
                    return 'disponível'
                elif status_opcao == 2:
                    return 'indisponível'
                else:
                    print("Opção inválida, escolha 1 ou 2.")
            except ValueError:
                print("Digite um número válido.")

    @staticmethod
    def add_livro(titulo, autor, genero, codigo):
        try:
            Biblioteca.sql.conectar()
            query_verifica = 'SELECT codigo FROM livro WHERE codigo = %s'
            Biblioteca.sql.cursor.execute(query_verifica, (codigo,))
            if Biblioteca.sql.cursor.fetchone():
                print("Já existe um livro cadastrado com este código.")
                return
            
            livro = (titulo, autor, genero, codigo)
            query = 'INSERT INTO livro (titulo, autor, genero, codigo) VALUES (%s, %s, %s, %s)'
            Biblioteca.sql.cursor.execute(query, livro)
            Biblioteca.sql.conector.commit()
            print("Livro adicionado com sucesso!")
        except Exception as e:
            print(f"Erro ao adicionar livro: {e}")
        finally:
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

    # @staticmethod
    # def confirmar():
    #     conf = input(f'Tem certeza que deseja fazer a exclusão? (Y/N): ').strip().upper()

    #     if conf == 'Y':
    #         return True
    #     else:
    #         print('Ação cancelada.')
    #         return False
        
    @staticmethod
    def deletar_livro(codigoU):
        try:
            Biblioteca.sql.conectar()

            if not Biblioteca.sql.cursor:
                return False, "Erro: o cursor do banco de dados não está inicializado."

            Biblioteca.sql.cursor.execute('SELECT * FROM livro WHERE codigo = %s', (codigoU,))
            resultado = Biblioteca.sql.cursor.fetchone()

            if not resultado:
                return False, "Livro não encontrado."

            nome_livro = resultado[1]  
            status_livro = resultado[4]  

            if status_livro and status_livro.lower() == 'indisponível':
                return False, "Livro emprestado, não pode ser deletado."

            Biblioteca.sql.cursor.execute('SET FOREIGN_KEY_CHECKS = 0;')

            delete_query = 'DELETE FROM livro WHERE codigo = %s'
            Biblioteca.sql.cursor.execute(delete_query, (codigoU,))
            Biblioteca.sql.conector.commit()

            Biblioteca.sql.cursor.execute('SET FOREIGN_KEY_CHECKS = 1;')

            return True, f"Livro '{nome_livro}' deletado com sucesso!"

        except Exception as e:
            return False, f"Erro ao deletar livro: {str(e)}"
        
        finally:
            if Biblioteca.sql.cursor:
                Biblioteca.sql.cursor.close()
            if Biblioteca.sql.conector:
                Biblioteca.sql.desconectar()

    @staticmethod
    def logar(nome, senha):
        Biblioteca.sql.conectar()

        try:
            query = 'SELECT id_usuario, nome, senha, is_admin FROM usuario WHERE nome = %s'
            Biblioteca.sql.cursor.execute(query, (nome,))
            usuario = Biblioteca.sql.cursor.fetchone()

            if usuario:
                if usuario[2] == senha:
                    is_admin = usuario[3]
                    
                    return True, is_admin 
                else:
                    print("Senha incorreta.")
                    return False, False
            else:
                print("Usuário não encontrado.")
                return False, False 
        finally:
            Biblioteca.sql.desconectar()

    @staticmethod
    def listar_user():
        Biblioteca.sql.conectar()
    
        Biblioteca.sql.cursor.execute('SELECT id_usuario, nome, cpf, telefone, senha, email, emprestimos FROM usuario')
        resultados = Biblioteca.sql.cursor.fetchall()

        if not resultados:
            print("Nenhum usuário encontrado.")
            Biblioteca.sql.desconectar()
            return
        
        for resultado in resultados:
            id_usuario, nome, cpf, telefone, senha, email, emprestimos = resultado
            print(f"ID: {id_usuario}, Nome: {nome}, CPF: {cpf}, Telefone: {telefone}, Senha: {senha}, E-mail: {email}, Emprestimos: {emprestimos}")

        Biblioteca.sql.desconectar()

    @staticmethod
    def add_user(nomeA, cpfA, telA, senhaA, emailA):
        Biblioteca.sql.conectar()

        try:
            while True:
                cpfA = cpfA.strip()

                if len(cpfA) != 11 or not cpfA.isdigit():
                    print('CPF inválido. O CPF deve conter exatamente 11 dígitos numéricos.')
                    return False

                Biblioteca.sql.cursor.execute('SELECT cpf FROM usuario WHERE cpf = %s', (cpfA,))
                resultado = Biblioteca.sql.cursor.fetchone()

                if resultado:
                    print('Já existe um usuário cadastrado com esse CPF. Tente novamente.')
                    return False
                else:
                    break

            if len(telA) < 10 or len(telA) > 20:
                print('Telefone inválido. O telefone deve conter entre 10 e 20 caracteres.')
                return

            while True:
                Biblioteca.sql.cursor.execute('SELECT email FROM usuario WHERE email = %s', (emailA,))
                resultado = Biblioteca.sql.cursor.fetchone()

                if resultado:
                    print('E-mail já cadastrado, tente novamente.')
                    return False 
                else:
                    break  

            query = 'INSERT INTO usuario(nome, cpf, telefone, senha, email) VALUES (%s, %s, %s, %s, %s)'
            Biblioteca.sql.cursor.execute(query, (nomeA, cpfA, telA, senhaA, emailA))
            Biblioteca.sql.conector.commit()
            print("Usuário adicionado com sucesso!")
            return True

        finally:
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

    @staticmethod
    def consultar_emprestimos_usuario(id_usuario):
        try:
            Biblioteca.sql.conectar()
            
            query = """
            SELECT emprestimos
            FROM usuario
            WHERE id_usuario = %s;
            """
            Biblioteca.sql.cursor.execute(query, (id_usuario,))
            resultado = Biblioteca.sql.cursor.fetchone()
            
            if resultado:
                return resultado[0]
            else:
                print(f"Usuário com ID {id_usuario} não encontrado.")
                return 0

        except Exception as e:
            print(f"Erro ao consultar empréstimos: {e}")
            return None
        
    @staticmethod
    def realizar_emprestimo(id_usuario, codigo_livro):
        try:
            Biblioteca.sql.conectar()

            Biblioteca.sql.cursor.execute('SELECT id_livro, status FROM livro WHERE codigo = %s', (codigo_livro,))
            livro = Biblioteca.sql.cursor.fetchone()

            if not livro:
                return False, "Livro não encontrado com o código fornecido."

            if livro[1] != 'disponível':
                return False, f"O livro com código {codigo_livro} não está disponível para empréstimo."

            query = '''
                INSERT INTO emprestimo (id_usuario, id_livro, status_emprestimo)
                VALUES (%s, %s, %s)
            '''
            Biblioteca.sql.cursor.execute(query, (id_usuario, livro[0], True))
            Biblioteca.sql.conector.commit()

            return True, f"Empréstimo realizado com sucesso para o usuário {id_usuario}, livro {codigo_livro}."

        except Exception as e:
            return False, f"Erro ao realizar o empréstimo: {str(e)}"

        finally:
            Biblioteca.sql.desconectar()


    @staticmethod
    def devolver_livro(id_usuario, codigo_livro):
        try:
            Biblioteca.sql.conectar()

            query_livro = """
            SELECT id_livro, status
            FROM livro
            WHERE codigo = %s;
            """
            Biblioteca.sql.cursor.execute(query_livro, (codigo_livro,))
            resultado_livro = Biblioteca.sql.cursor.fetchone()

            if not resultado_livro:
                print(f"Livro com código {codigo_livro} não encontrado.")
                return False

            id_livro = resultado_livro[0] 

            query_emprestimo = """
            SELECT id_emprestimo, status_emprestimo
            FROM emprestimo
            WHERE id_usuario = %s AND id_livro = %s AND status_emprestimo = 1;
            """
            Biblioteca.sql.cursor.execute(query_emprestimo, (id_usuario, id_livro))
            emprestimo = Biblioteca.sql.cursor.fetchone()

            if not emprestimo:
                print(f"Não há empréstimo ativo para o livro com código {codigo_livro} e o usuário {id_usuario}.")
                return False

            query_atualizar_emprestimo = """
            UPDATE emprestimo
            SET status_emprestimo = 0
            WHERE id_emprestimo = %s;
            """
            Biblioteca.sql.cursor.execute(query_atualizar_emprestimo, (emprestimo[0],))

            query_atualizar_livro = """
            UPDATE livro
            SET status = 'disponível'
            WHERE id_livro = %s;
            """
            Biblioteca.sql.cursor.execute(query_atualizar_livro, (id_livro,))

            Biblioteca.sql.conector.commit()

            print(f"Livro com código {codigo_livro} devolvido com sucesso pelo usuário {id_usuario}.")
            return True

        except Exception as e:
            print(f"Erro ao devolver o livro: {e}")
            return False

        finally:
            Biblioteca.sql.desconectar()

