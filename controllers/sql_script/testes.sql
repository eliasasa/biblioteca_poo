-- Active: 1732830022315@@192.168.100.52@3306@biblioteca

-- SELECT * from livro;

DESCRIBE emprestimo;

-- TRUNCATE TABLE livro;

SELECT * from emprestimo;

-- SET FOREIGN_KEY_CHECKS = 1;

DROP DATABASE biblioteca;

SELECT id_emprestimo, status_emprestimo
FROM emprestimo
WHERE id_usuario = 1 AND id_livro = 1;

ALTER TABLE emprestimo ADD COLUMN status BOOLEAN DEFAULT FALSE;
