from models.user import User

class Adm(User):
    def __init__(self, id_usuario, nome, cpf, telefone, senha, email, emprestimos, is_admin=True):
        super().__init__(id_usuario, nome, cpf, telefone, senha, email, emprestimos)
        self.is_admin = is_admin
