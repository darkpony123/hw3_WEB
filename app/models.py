from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Department(Base):
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

    employees: Mapped[list["Employee"]] = relationship(back_populates="department")


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    position: Mapped[str] = mapped_column(String(100))
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"))

    department: Mapped["Department"] = relationship(back_populates="employees")
    tasks: Mapped[list["Task"]] = relationship(back_populates="employee", cascade="all, delete-orphan")


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    done: Mapped[bool] = mapped_column(default=False)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"))

    employee: Mapped["Employee"] = relationship(back_populates="tasks")
