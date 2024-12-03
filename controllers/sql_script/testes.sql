-- Active: 1733180775390@@127.0.0.1@3306@biblioteca

SELECT * from livro;

DESCRIBE emprestimo;

-- TRUNCATE TABLE livro;

SELECT * from emprestimo;

SET FOREIGN_KEY_CHECKS = 1;

DROP DATABASE biblioteca;

SELECT id_emprestimo, status_emprestimo
FROM emprestimo
WHERE id_usuario = 1 AND id_livro = 1;

GRANT ALL PRIVILEGES ON *.* TO 'usuario'@'%' WITH GRANT OPTION;
