# Task Manager — Backend

Flask-RESTful JSON API. Admin assigns tasks to employees with a deadline.

## Roles

| Role | Can do |
|------|--------|
| **admin** | See all tasks, assign, edit, delete |
| **employee** | See own tasks, update status only |

## Quick start

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python app.py
```

Default admin: `admin` / `admin123`

If you had an old database, delete `app.db` and restart.

## Endpoints

| Method | URL | Who | Action |
|--------|-----|-----|--------|
| POST | `/register` | anyone | Sign up as employee |
| POST | `/login` | anyone | Get JWT |
| GET | `/tasks` | all | Employee: own tasks. Admin: all tasks |
| POST | `/tasks` | admin | Assign task (`title`, `user_id`, `deadline`, optional `description`) |
| PUT | `/tasks/<id>` | employee | Update `status` only |
| PUT | `/tasks/<id>` | admin | Update anything |
| DELETE | `/tasks/<id>` | admin | Delete task |
| GET | `/admin/employees` | admin | List employees (for assign dropdown) |
| GET | `/admin/stats` | admin | Dashboard counts |

Task status values: `Pending`, `In Progress`, `Completed`

Deadline format: `YYYY-MM-DD`

## Layout

```
backend/
├── models.py           # User, Task
├── controllers/
│   ├── tasks.py        # main task API
│   ├── admin.py        # stats + employee list
│   └── auth.py
└── services/stats.py
```

Frontend: `../frontend`
