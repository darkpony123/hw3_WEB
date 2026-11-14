# Company API

REST API for departments, employees and their tasks.

**Stack:** FastAPI, PostgreSQL, SQLAlchemy (ORM), Docker Compose.

## Run

```
docker compose up --build
```

API: `http://localhost:8000`, Swagger: `http://localhost:8000/docs`.
Tables are created automatically on startup.

## Models

- **Department**: id, name
- **Employee**: id, name, position, department_id
- **Task**: id, title, done, employee_id

Relationships:
- Department → Employees: **one-to-many**
- Employee → Tasks: **one-to-many** (tasks are deleted together with the employee)

## Endpoints

| # | Method | URL | Body | Response |
|---|---|---|---|---|
| 1 | GET | `/departments` | | 200, list of departments |
| 2 | POST | `/departments` | `{"name": "IT"}` | 201, created department |
| 3 | GET | `/departments/{id}/employees` | | 200, employees of the department |
| 4 | GET | `/employees` | | 200, list of employees |
| 5 | GET | `/employees/{id}` | | 200, employee |
| 6 | POST | `/employees` | `{"name": "Aidos", "position": "Developer", "department_id": 1}` | 201, created employee |
| 7 | PUT | `/employees/{id}` | same as POST | 200, updated employee |
| 8 | DELETE | `/employees/{id}` | | 204, no content |
| 9 | GET | `/employees/{id}/tasks` | | 200, tasks of the employee |
| 10 | POST | `/employees/{id}/tasks` | `{"title": "Fix bug", "done": false}` | 201, created task |

Response examples:
```json
{"id": 1, "name": "IT"}
{"id": 1, "name": "Aidos", "position": "Developer", "department_id": 1}
{"id": 1, "title": "Fix bug", "done": false, "employee_id": 1}
```

## Validation and errors

- `name`, `position`, `title` are required and can't be empty
- Wrong or missing fields → **422**
- Department, employee or task not found (also a wrong `department_id` in the body) → **404** `{"detail": "Employee not found"}`

## Postman

Import `postman_collection.json` and run the requests top to bottom on a fresh database (they use id 1).
