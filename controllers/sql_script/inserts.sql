USE biblioteca;

-- para adicionar como adm:
INSERT INTO usuario (nome, senha, email, cpf, is_adm, telefone)
VALUES ('Adm', 'Adm', 'adm@email.com', 39033779889, TRUE, 67999999999);

INSERT INTO livro (titulo, autor, genero, codigo)
VALUES 
    ('1984', 'George Orwell', 'Distopia', 101),
    ('O Senhor dos Anéis', 'J.R.R. Tolkien', 'Fantasia', 102),
    ('Dom Quixote', 'Miguel de Cervantes', 'Clássico', 103);


INSERT INTO usuario (nome, senha, email, cpf, telefone, is_adm)
VALUES 
    ('Alice Silva', 'senha123', 'alice@email.com', '123.456.789-01', '(11) 99999-9999', 0),
    ('Carlos Pereira', 'senha456', 'carlos@email.com', '987.654.321-00', '(11) 88888-8888', 0);

INSERT INTO emprestimo (id_livro, id_usuario, status_emprestimo)
VALUES 
    (1, 1, 1), -- Alice empresta "1984"
    (2, 1, 1), -- Alice empresta "O Senhor dos Anéis"
    (3, 1, 1); -- Alice empresta "Dom Quixote"