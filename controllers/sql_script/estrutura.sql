create database biblioteca;
use biblioteca;

create table usuario(
        id_usuario int auto_increment primary key,
        nome varchar(100),
        senha varchar(30),
        email varchar(50),
        cpf varchar(14),
        is_adm boolean default false,
        emprestimos tinyint default 0,
        telefone varchar(20)
);


create table livro(
    id_livro int auto_increment primary key,
    titulo varchar(50),
    autor varchar(50),
    genero varchar(50),
    status VARCHAR(50) DEFAULT 'disponível',
    codigo int
);

create table emprestimo(
    id_emprestimo int auto_increment primary key,
	id_livro int,
	id_usuario int,
    status_emprestimo BOOLEAN DEFAULT 1,
	foreign key (id_livro) references livro(id_livro),
	foreign key (id_usuario) references usuario(id_usuario)
);