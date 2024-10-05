from fastapi import FastAPI
import mysql.connector
import schemas

app = FastAPI()

host_name = "3.82.58.28"
port_number = "8020"
user_name = "root"
password_db = "utec"
database_name = "api-mysql-cc"

# Get echo test for load balancer's health check
@app.get("/")
def get_echo_test():
    return {"message": "Echo Test OK"}

# Get all employees
@app.get("/employees")
def get_employees():
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM Empleados")
    result = cursor.fetchall()
    cursor.close()
    mydb.close()
    return {"employees": result}

# Get an employee by ID
@app.get("/employees/{id}")
def get_employee(id: int):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM Empleados WHERE ID_empleado = {id}")
    result = cursor.fetchone()
    cursor.close()
    mydb.close()
    return {"employee": result}

# Add a new employee
@app.post("/employees")
def add_employee(item:schemas.Item):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    name = item.name
    cargo = item.cargo
    correo = item.correo
    edad = item.edad
    cursor = mydb.cursor()
    sql = "INSERT INTO Empleados (nombre, cargo, correo, edad) VALUES (%s, %s, %s, %s)"
    val = (name, cargo, correo, edad)
    cursor.execute(sql, val)
    mydb.commit()
    cursor.close()
    mydb.close()
    return {"message": "Employee added successfully"}

# Modify an employee
@app.put("/employees/{id}")
def update_employee(id: int, item: schemas.Item):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    name = item.name
    cargo = item.cargo
    correo = item.correo
    edad = item.edad
    cursor = mydb.cursor()
    sql = "UPDATE Empleados SET nombre=%s, cargo=%s, correo=%s, edad=%s WHERE ID_empleado=%s"
    val = (name, cargo, correo, edad, id)
    cursor.execute(sql, val)
    mydb.commit()
    cursor.close()
    mydb.close()
    return {"message": "Employee modified successfully"}

# Delete an employee by ID
@app.delete("/employees/{id}")
def delete_employee(id: int):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute(f"DELETE FROM Empleados WHERE ID_empleado = {id}")
    mydb.commit()
    cursor.close()
    mydb.close()
    return {"message": "Employee deleted successfully"}

# Get all locals
@app.get("/locals")
def get_locals():
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM Local")
    result = cursor.fetchall()
    cursor.close()
    mydb.close()
    return {"locals": result}

# Get a local by ID
@app.get("/locals/{id}")
def get_local(id: int):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM Local WHERE ID_local = {id}")
    result = cursor.fetchone()
    cursor.close()
    mydb.close()
    return {"local": result}

# Assign employee to local
@app.post("/assign_employee_to_local")
def assign_employee_to_local(local_id: int, employee_id: int):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    sql = "INSERT INTO Trabajan (ID_local, ID_empleado) VALUES (%s, %s)"
    val = (local_id, employee_id)
    cursor.execute(sql, val)
    mydb.commit()
    cursor.close()
    mydb.close()
    return {"message": f"Employee {employee_id} assigned to local {local_id} successfully"}

# Get employees by local
@app.get("/local/{id}/employees")
def get_employees_by_local(id: int):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    sql = """
    SELECT Empleados.ID_empleado, Empleados.nombre, Empleados.cargo, Empleados.correo, Empleados.edad
    FROM Empleados
    INNER JOIN Trabajan ON Empleados.ID_empleado = Trabajan.ID_empleado
    WHERE Trabajan.ID_local = %s
    """
    cursor.execute(sql, (id,))
    result = cursor.fetchall()
    cursor.close()
    mydb.close()
    return {"employees": result}
