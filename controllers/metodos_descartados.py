# @staticmethod
#     def deletar_livro(codigoU):
#         Biblioteca.sql.conectar()

#         try:
#             codigoU = int(codigoU)
#         except ValueError:
#             print("Código inválido. Por favor, insira um número válido.")
#             Biblioteca.sql.desconectar()
#             return

#         Biblioteca.sql.cursor.execute('SELECT * FROM livro WHERE codigo = %s', (codigoU,))
#         resultado = Biblioteca.sql.cursor.fetchone()

#         if not resultado:
#             print('Livro não encontrado.')
#             Biblioteca.sql.desconectar()
#             return

#         print("Livro encontrado:", resultado)

#         if resultado[-2] == 'Indisponível':
#             print('Livro emprestado, não pode ser deletado.')
#             Biblioteca.sql.desconectar() 
#             return
        
#         if Biblioteca.confirmar():
        
#             delet_query = '''
#                 DELETE FROM livro WHERE codigo = %s
#             '''

#             Biblioteca.sql.cursor.execute(delet_query, (codigoU,))
#             Biblioteca.sql.conector.commit()

#             print("Livro deletado com sucesso!")

#         else: pass

#         Biblioteca.sql.desconectar()

