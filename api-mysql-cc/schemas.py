from pydantic import BaseModel
class Employee(BaseModel):
    name: str
    cargo: str
    correo: str
    edad: int

class Local(BaseModel):
    nombre: str
    direccion: str

class AssignEmployeeToLocal(BaseModel):
    ID_local: int
    ID_empleado: int
