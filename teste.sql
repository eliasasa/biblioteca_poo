-- Active: 1725969028064@@10.28.2.62@3306@biblioteca
ALTER TABLE usuario ADD COLUMN senha VARCHAR(30) NOT NULL, ADD COLUMN email VARCHAR(50) NOT NULL;

ALTER Table usuario ADD COLUMN emprestimos TINYINT not null DEFAULT 0;

SELECT * from usuario;