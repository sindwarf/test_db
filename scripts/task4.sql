CREATE PROCEDURE update_terminated_employee_dates()
BEGIN
    UPDATE titles 
    SET 
        to_date = CURDATE()
    WHERE
        to_date = '9999-01-01'
            AND emp_no IN (SELECT 
                emp_no
            FROM
                employees
            WHERE
                employment_status = 'T'); 
    
    UPDATE salaries 
    SET 
        to_date = CURDATE()
    WHERE
        to_date = '9999-01-01'
        
            AND emp_no IN (SELECT 
                emp_no
            FROM
                employees
            WHERE
                employment_status = 'T'); 

    UPDATE dept_emp 
    SET 
        to_date = CURDATE()
    WHERE
        to_date = '9999-01-01'
            AND emp_no IN (SELECT 
                emp_no
            FROM
                employees
            WHERE
                employment_status = 'T'); 

    UPDATE dept_manager 
    SET 
        to_date = CURDATE()
    WHERE
        to_date = '9999-01-01'
            AND emp_no IN (SELECT 
                emp_no
            FROM
                employees
            WHERE
                employment_status = 'T'); 
END

