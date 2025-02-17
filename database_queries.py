

def insert_new_departments(insert, name, id_departments=None):
    if id_departments:
        query = "INSERT INTO departments VALUES (%s, %s)"
        insert(query, (id_departments, name))
    else:
        query = "INSERT INTO departments (department_name) VALUES (%s)"
        insert(query, (name, ))



