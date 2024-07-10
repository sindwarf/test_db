CREATE PROCEDURE update_company_phone()
BEGIN
    UPDATE 
        employees
    SET phone = CASE
		WHEN LENGTH(emp_no) = 5 THEN CONCAT('801-60', SUBSTRING(emp_no, 1, 1), '-', SUBSTRING(emp_no, 2))
        ELSE CONCAT('801-6', SUBSTRING(emp_no, 1, 2), '-', SUBSTRING(emp_no, 3))
	END;
END

