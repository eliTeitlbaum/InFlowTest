from connectMySql import DbManager


workers = """
CREATE TABLE IF NOT EXISTS dim_workers (
      worker_id INT PRIMARY KEY,
      first_name VARCHAR(50),
      last_name VARCHAR(50),
      department_id INT,
      address VARCHAR(100),
      age INT,
      marital_status VARCHAR(50),
      monthly_salary DECIMAL(10, 2)
);
"""

department = """
CREATE TABLE IF NOT EXISTS dim_department (
    department_id INT PRIMARY KEY,
    department_name VARCHAR(50)
);
"""

candidate = """
CREATE TABLE IF NOT EXISTS dim_candidate (
    candidate_id INT PRIMARY KEY,
    name VARCHAR(100),
    submission_date DATETIME
);
"""

recruitment = """
CREATE TABLE IF NOT EXISTS fact_recruitment (
    recruitment_id INT PRIMARY KEY,
    worker_id INT,
    candidate_id INT,
    department_id INT,
    month_id INT,
    salary DECIMAL(10, 2),
    bonus DECIMAL(10, 2),
    FOREIGN KEY (worker_id) REFERENCES dim_workers(worker_id),
    FOREIGN KEY (candidate_id) REFERENCES dim_candidate(candidate_id),
    FOREIGN KEY (department_id) REFERENCES dim_department(department_id)
);
"""

bonus = """
CREATE TABLE IF NOT EXISTS fact_bonus (
    worker_id INT, 
    month_id INT,
    bonus_amount DECIMAL(10, 2),
    PRIMARY KEY (worker_id, month_id),
    FOREIGN KEY (worker_id) REFERENCES dim_workers(worker_id)
);
"""


def main():
    db = DbManager()

    tables_to_create = [
        department, workers, candidate, recruitment, bonus
    ]

    for table in tables_to_create:
        db.insert(query=table)

    db.close()


if __name__ == "__main__":
    main()
