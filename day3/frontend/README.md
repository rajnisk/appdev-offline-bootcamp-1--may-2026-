# Task Manager — Frontend

Vue 3 + Bootstrap + axios. Connects to `../backend`.

## Run

```bash
# terminal 1
cd backend && python app.py

# terminal 2
cd frontend && npm install && npm run dev
```

Open `http://localhost:5173`

## Pages

| Page | Who | What |
|------|-----|------|
| `/` | employee | My tasks — change status only |
| `/admin` | admin | Assign tasks, edit all, delete |
| `/login` | anyone | Login |
| `/register` | anyone | Sign up as employee |

## Try it

1. Register two employees (e.g. `alice`, `bob`)
2. Login as `admin` / `admin123`
3. Go to **Manage Tasks** → assign a task with deadline
4. Login as employee → see task → update status

API URL is in each view: `const API = 'http://127.0.0.1:5000'`
