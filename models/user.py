class User:
    def __init__(self, id_usuario, nome, cpf, telefone):
        self.id_usuario = id_usuario
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone

    def __repr__(self):
        return f"User(id_usuario={self.id_usuario}, nome='{self.nome}', cpf='{self.cpf}', telefone='{self.telefone}')"

    def to_tuple(self):
        return (self.id_usuario, self.nome, self.cpf, self.telefone)