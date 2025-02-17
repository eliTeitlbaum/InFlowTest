from connectMySql import DbManager

departments = """
    CREATE TABLE IF NOT EXISTS departments (
    department_id INT AUTO_INCREMENT PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL
);
"""

workers = """
    CREATE TABLE IF NOT EXISTS workers (
    worker_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    department_id INT,
    address VARCHAR(255),
    date_of_birth DATE,
    marital_status VARCHAR(50),
    FOREIGN KEY (department_id) REFERENCES departments(department_id) ON DELETE SET NULL
);
"""

jobs = """
CREATE TABLE IF NOT EXISTS jobs (
    job_id INT AUTO_INCREMENT PRIMARY KEY,
    job_name VARCHAR(100) NOT NULL,
    department_id INT NOT NULL,
    FOREIGN KEY (department_id) REFERENCES departments(department_id) ON DELETE CASCADE
);
"""

candidates = """
    CREATE TABLE IF NOT EXISTS candidates (
    candidate_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    resume TEXT
);
"""

candidate_enrollment = """
CREATE TABLE IF NOT EXISTS candidate_enrollment (
    enrollment_id INT AUTO_INCREMENT PRIMARY KEY,
    candidate_id INT NOT NULL,
    enrollment_ts DATETIME,
    worker_id INT,
    job_id INT NOT NULL,
    enrolled_ts DATETIME,
    FOREIGN KEY (candidate_id) REFERENCES candidates(candidate_id) ON DELETE CASCADE,
    FOREIGN KEY (worker_id) REFERENCES workers(worker_id) ON DELETE SET NULL
);
"""

salaries = """
CREATE TABLE IF NOT EXISTS salaries (
    salary_id INT AUTO_INCREMENT PRIMARY KEY,
    worker_id INT NOT NULL,
    salary_month DATE,
    base_salary DECIMAL(10, 2),
    bonus DECIMAL(10, 2),
    travel_expense DECIMAL(10, 2),
    total_salary DECIMAL(10, 2),
    FOREIGN KEY (worker_id) REFERENCES workers(worker_id) ON DELETE CASCADE
);
"""

bonus = """
CREATE TABLE IF NOT EXISTS bonus (
    bonus_id INT AUTO_INCREMENT PRIMARY KEY,
    month DATE,
    min_recruits INT NOT NULL,
    max_recruits INT NOT NULL,
    sum DECIMAL(10, 2)
    );
"""


def main():
    db = DbManager()

    tables_to_create = [
        departments, workers, jobs, candidates, candidate_enrollment, salaries, bonus
    ]

    for table in tables_to_create:
        db.insert(query=table)

    db.close()


if __name__ == "__main__":
    main()
