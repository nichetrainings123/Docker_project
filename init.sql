CREATE TABLE IF NOT EXISTS emp (
    emp_id SERIAL PRIMARY KEY,
    emp_name VARCHAR(100) NOT NULL,
    department VARCHAR(50),
    salary NUMERIC(10,2),
    age INT,
    gender VARCHAR(20),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(100),
    mobile VARCHAR(15),
    address TEXT
);

INSERT INTO emp (emp_name, department, salary)
VALUES
('John', 'IT', 50000),
('Alice', 'HR', 45000),
('Bob', 'Finance', 60000)
ON CONFLICT DO NOTHING;