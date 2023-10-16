-- Write a SQL script that creates a trigger that resets the attribute valid_email
-- only when the email has been changed.

DROP TRIGGER IF EXISTS validate_email;

DELIMITER $$
CREATE TRIGGER validate_email
BEFORE UPDATE ON `users`
FOR EACH ROW
BEGIN
	IF (OLD.email != NEW.email) THEN
		IF (OLD.valid_email = 1) THEN
			SET NEW.valid_email = 0;
		ELSE
			SET NEW.valid_email = 1;
		END IF;
	END IF;
END;
$$
DELIMITER ;
