-- Active: 1725969028064@@10.28.2.62@3306@biblioteca
ALTER TABLE usuario ADD COLUMN senha VARCHAR(30) NOT NULL, ADD COLUMN email VARCHAR(50) NOT NULL;

ALTER Table usuario ADD COLUMN emprestimos TINYINT not null DEFAULT 0;
ALTER TABLE usuario ADD COLUMN is_admin BOOLEAN DEFAULT FALSE;


SELECT * from livro;

DESCRIBE usuario;

TRUNCATE TABLE livro;

SET FOREIGN_KEY_CHECKS = 1;

INSERT INTO usuario (nome, senha, email, cpf, is_admin)
VALUES ('Adm', 'Adm', 'adm@email.com', 39033779889, TRUE);

