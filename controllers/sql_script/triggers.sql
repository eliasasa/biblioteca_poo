

DELIMITER $$

CREATE TRIGGER trigger_emprestimo_insert
AFTER INSERT ON emprestimo
FOR EACH ROW
BEGIN
    UPDATE usuario
    SET emprestimos = (
        SELECT COUNT(*)
        FROM emprestimo
        WHERE id_usuario = NEW.id_usuario
          AND status_emprestimo = 1
    )
    WHERE id_usuario = NEW.id_usuario;
END$$

DELIMITER ;


DELIMITER $$

CREATE TRIGGER trigger_emprestimo_update
AFTER UPDATE ON emprestimo
FOR EACH ROW
BEGIN
    UPDATE usuario
    SET emprestimos = (
        SELECT COUNT(*)
        FROM emprestimo
        WHERE id_usuario = NEW.id_usuario
          AND status_emprestimo = 1
    )
    WHERE id_usuario = NEW.id_usuario;
END$$

DELIMITER ;

DELIMITER $$

CREATE TRIGGER atualiza_status_livro
AFTER INSERT ON emprestimo
FOR EACH ROW
BEGIN
    -- Atualiza o status do livro para 'indisponível' após um empréstimo
    UPDATE livro
    SET status = 'indisponível'
    WHERE id_livro = NEW.id_livro;
END $$

DELIMITER ;

DELIMITER $$

CREATE TRIGGER after_emprestimo_devolvido
AFTER UPDATE ON emprestimo
FOR EACH ROW
BEGIN
    -- Verifica se o status do empréstimo foi alterado para 0
    IF NEW.status_emprestimo = 0 THEN
        -- Atualiza o status do livro para 'disponível'
        UPDATE livro
        SET status = 'disponível'
        WHERE id_livro = NEW.id_livro;
    END IF;
END $$

DELIMITER ;
