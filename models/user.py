class User:
    def __init__(self, id_usuario, nome, cpf, telefone, senha, email, emprestimos):
        self.id_usuario = id_usuario
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.senha = senha
        self.email = email
        self.emprestimos = emprestimos

    def __repr__(self):
        return f"User(id_usuario={self.id_usuario}, nome='{self.nome}', cpf='{self.cpf}', telefone='{self.telefone}', senha='{self.senha}', email='{self.email}', emprestimos='{self.emprestimos}')"

    def to_tuple(self):
        return (self.id_usuario, self.nome, self.cpf, self.telefone, self.senha, self.email, self.emprestimos)