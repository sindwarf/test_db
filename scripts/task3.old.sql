ALTER TABLE employees
    ADD COLUMN company_email varchar(64) UNIQUE,
    ADD COLUMN personal_email varchar(64) UNIQUE,
    ADD COLUMN phone smallint
    
DELIMITER //
CREATE TRIGGER update_company_email
BEFORE INSERT
ON employees
FOR EACH ROW
BEGIN
    DECLARE existing_email varchar(64);
    DECLARE new_email varchar(64);
    DECLARE num int;
    
    SELECT 
        company_email
    INTO 
        existing_email
    FROM 
        employees
    WHERE 
        company_email LIKE new.company_email;

    IF existing_email IS NOT NULL THEN
       SET new_email = CONCAT(new.company_email, num);
    END IF;

    SELECT 
        company_email
    INTO 
        existing_email
    FROM 
        employees
    WHERE 
        company_email LIKE new_email;

    WHILE existing_email IS NOT NULL DO
        SET num = num + 1;
        SET new_email = CONCAT(new.company_email, num);
        SELECT 
            company_email
        INTO 
            existing_email
        FROM 
            employees
        WHERE 
            company_email LIKE new_email; 
    END WHILE;

    SET NEW.company_email = new_email;    
    END//
DELIMITER ;


DELIMITER //
CREATE PROCEDURE update_company_emails()
BEGIN
    UPDATE 
        employees
    SET 
        company_email = CONCAT(SUBSTRING(first_name, 1, 1), last_name, '@company.net');
    WHERE emp_no < 10005
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE update_company_emails()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE emp_no_var INT;
    DECLARE cur CURSOR FOR SELECT emp_no FROM employees WHERE emp_no < 10005;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    OPEN cur;

    read_loop: LOOP
        FETCH cur INTO emp_no_var;
        IF done THEN
            LEAVE read_loop;
        END IF;

        BEGIN
            UPDATE employees
            SET company_email = CONCAT(SUBSTRING(first_name, 1, 1), last_name, '@company.net')
            WHERE emp_no = emp_no_var;
        EXCEPTION
            WHEN OTHERS THEN
                -- Handle the exception for this specific row
                UPDATE employees
                SET company_email = CONCAT(SUBSTRING(first_name, 1, 1), last_name, emp_no, '@company.net') -- Default email address
                WHERE emp_no = emp_no_var;
        END;
    END LOOP;

    CLOSE cur;
    UPDATE 
        employees
    SET 
        company_email = CONCAT(SUBSTRING(first_name, 1, 1), last_name, '@company.net');
    WHERE emp_no < 10005
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE update_personal_emails()
BEGIN
    UPDATE 
        employees
    SET 
        personal_email = CONCAT(SUBSTRING(first_name, 1, 1), last_name, '@personal.com');
    WHERE emp_no in (
        SELECT
            emp_no
        FROM
            title
        WHERE 
            title REGEXP 'senior'
    )
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE update_phone()
BEGIN
    UPDATE 
        employees
    SET phone = CASE
		WHEN LENGTH(emp_no) = 5 THEN CONCAT('801-60', SUBSTRING(emp_no, 1, 1), '-', SUBSTRING(emp_no, 2))
        ELSE CONCAT('801-6', SUBSTRING(emp_no, 1, 2), '-', SUBSTRING(emp_no, 3))
	END
    WHERE emp_no < 10005;
END //
DELIMITER ;

