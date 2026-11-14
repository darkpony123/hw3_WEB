from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Department, Employee, Task

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Company API")


# ---------- Schemas (request validation and responses) ----------

class DepartmentIn(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class DepartmentOut(DepartmentIn):
    model_config = ConfigDict(from_attributes=True)
    id: int


class EmployeeIn(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    position: str = Field(min_length=1, max_length=100)
    department_id: int


class EmployeeOut(EmployeeIn):
    model_config = ConfigDict(from_attributes=True)
    id: int


class TaskIn(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    done: bool = False


class TaskOut(TaskIn):
    model_config = ConfigDict(from_attributes=True)
    id: int
    employee_id: int


def get_or_404(db: Session, model, item_id: int):
    item = db.get(model, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
    return item


# ---------- Departments ----------

@app.get("/departments", response_model=list[DepartmentOut])
def list_departments(db: Session = Depends(get_db)):
    return db.query(Department).all()


@app.post("/departments", response_model=DepartmentOut, status_code=201)
def create_department(data: DepartmentIn, db: Session = Depends(get_db)):
    department = Department(name=data.name)
    db.add(department)
    db.commit()
    db.refresh(department)
    return department


@app.get("/departments/{department_id}/employees", response_model=list[EmployeeOut])
def list_department_employees(department_id: int, db: Session = Depends(get_db)):
    department = get_or_404(db, Department, department_id)
    return department.employees


# ---------- Employees ----------

@app.get("/employees", response_model=list[EmployeeOut])
def list_employees(db: Session = Depends(get_db)):
    return db.query(Employee).all()


@app.get("/employees/{employee_id}", response_model=EmployeeOut)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    return get_or_404(db, Employee, employee_id)


@app.post("/employees", response_model=EmployeeOut, status_code=201)
def create_employee(data: EmployeeIn, db: Session = Depends(get_db)):
    get_or_404(db, Department, data.department_id)
    employee = Employee(**data.model_dump())
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


@app.put("/employees/{employee_id}", response_model=EmployeeOut)
def update_employee(employee_id: int, data: EmployeeIn, db: Session = Depends(get_db)):
    employee = get_or_404(db, Employee, employee_id)
    get_or_404(db, Department, data.department_id)
    employee.name = data.name
    employee.position = data.position
    employee.department_id = data.department_id
    db.commit()
    db.refresh(employee)
    return employee


@app.delete("/employees/{employee_id}", status_code=204)
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = get_or_404(db, Employee, employee_id)
    db.delete(employee)
    db.commit()


# ---------- Tasks ----------

@app.get("/employees/{employee_id}/tasks", response_model=list[TaskOut])
def list_employee_tasks(employee_id: int, db: Session = Depends(get_db)):
    employee = get_or_404(db, Employee, employee_id)
    return employee.tasks


@app.post("/employees/{employee_id}/tasks", response_model=TaskOut, status_code=201)
def create_task(employee_id: int, data: TaskIn, db: Session = Depends(get_db)):
    get_or_404(db, Employee, employee_id)
    task = Task(**data.model_dump(), employee_id=employee_id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task
