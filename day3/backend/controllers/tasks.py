from datetime import datetime

from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource

from extensions import db
from models import Task, User

STATUSES = ("Pending", "In Progress", "Completed")


def _parse_deadline(value):
    if not value:
        return None, None
    try:
        return datetime.strptime(str(value)[:10], "%Y-%m-%d").date(), None
    except ValueError:
        return None, {"msg": "deadline must be YYYY-MM-DD"}, 400


def _current_user():
    return db.session.get(User, int(get_jwt_identity()))


class TaskList(Resource):
    method_decorators = [jwt_required()]

    def get(self):
        user = _current_user()
        if user.role == "admin":
            rows = Task.query.order_by(Task.id.desc()).all()
        else:
            rows = Task.query.filter_by(user_id=user.id).order_by(Task.id.desc()).all()
        return [row.to_dict() for row in rows]

    def post(self):
        user = _current_user()
        if user.role != "admin":
            return {"msg": "admin only"}, 403

        data = request.get_json() or {}
        title = (data.get("title") or "").strip()
        if not title:
            return {"msg": "title required"}, 400

        employee = db.session.get(User, data.get("user_id"))
        if not employee or employee.role != "employee":
            return {"msg": "pick a valid employee"}, 400

        deadline, err = _parse_deadline(data.get("deadline"))
        if err:
            return err

        task = Task(
            title=title,
            description=data.get("description") or "",
            status=data.get("status") or "Pending",
            deadline=deadline,
            user_id=employee.id,
        )
        db.session.add(task)
        db.session.commit()
        return task.to_dict(), 201


class TaskDetail(Resource):
    method_decorators = [jwt_required()]

    def get(self, task_id):
        task, err = self._get_task(task_id)
        if err:
            return err
        return task.to_dict()

    def put(self, task_id):
        user = _current_user()
        task, err = self._get_task(task_id)
        if err:
            return err

        data = request.get_json() or {}

        if user.role == "admin":
            if "title" in data:
                task.title = (data["title"] or "").strip() or task.title
            if "description" in data:
                task.description = data["description"] or ""
            if "status" in data and data["status"] in STATUSES:
                task.status = data["status"]
            if "deadline" in data:
                deadline, deadline_err = _parse_deadline(data.get("deadline"))
                if deadline_err:
                    return deadline_err
                task.deadline = deadline
            if "user_id" in data:
                employee = db.session.get(User, data.get("user_id"))
                if not employee or employee.role != "employee":
                    return {"msg": "pick a valid employee"}, 400
                task.user_id = employee.id
        else:
            if "status" not in data or data["status"] not in STATUSES:
                return {"msg": "employees can only update status"}, 400
            task.status = data["status"]

        db.session.commit()
        return task.to_dict()

    def delete(self, task_id):
        user = _current_user()
        if user.role != "admin":
            return {"msg": "admin only"}, 403

        task = db.get_or_404(Task, task_id)
        db.session.delete(task)
        db.session.commit()
        return {"msg": "deleted"}

    def _get_task(self, task_id):
        user = _current_user()
        task = db.get_or_404(Task, task_id)
        if user.role != "admin" and task.user_id != user.id:
            return None, ({"msg": "forbidden"}, 403)
        return task, None
