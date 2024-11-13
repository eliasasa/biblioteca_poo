class Livro:
    def __init__(self, titulo, autor, genero, status, codigo):
        self.titulo = titulo
        self.autor = autor
        self.genero = genero
        self.status = status
        self.codigo = codigo

    def to_tuple(self):
        return (self.titulo, self.autor, self.genero, self.status, self.codigo)
    
    def to_tuple_update(self):
        return (self.titulo, self.autor, self.genero, self.status)
