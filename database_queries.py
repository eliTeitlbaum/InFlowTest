

def insert_new_departments(insert, name, id_departments=None):
    if id_departments:
        query = "INSERT INTO departments VALUES (%s, %s)"
        insert(query, (id_departments, name))
    else:
        query = "INSERT INTO departments (department_name) VALUES (%s)"
        insert(query, (name, ))


def insert_new_worker(insert, fn, ln, department_id, address=None, date=None, status=None, worker_id=None):
    if worker_id:
        query = "INSERT INTO workers VALUES (%s, %s, %s, %s, %s, %s, %s)"
        insert(query, (worker_id, fn, ln, department_id, address, date, status))
    else:
        ...


def insert_new_candidates(
        insert, fn, ln, enrollment_id, candidate_id, enrollment_ts, worker_id, job_id, enrolled_ts, resume="",
):
    query = "INSERT INTO candidates VALUES (%s, %s, %s, %s)"
    insert(query, (candidate_id, fn, ln, resume))

    query = "INSERT INTO candidate_enrollment VALUES (%s, %s, %s, %s, %s, %s)"
    insert(query, (enrollment_id, candidate_id, enrollment_ts, worker_id, job_id, enrolled_ts))
