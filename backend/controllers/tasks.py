from datetime import datetime

from flask_restful import Resource, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Task, User
from extensions import db


class TaskResouce(Resource):
    @jwt_required()
    def get(self, task_id=None):
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        if not user:
            return {'msg': 'user not found'}, 404

        if task_id is not None:
            task = Task.query.get(task_id)
            if not task:
                return {'msg': 'task not found'}, 404

            if user.role != 'admin' and task.assigned_to != user.id:
                return {'msg': 'you are not authorized to view this task'}, 403

            return {'task': task.to_json()}, 200

        if user.role == 'admin':
            tasks = Task.query.all()
        else:
            tasks = Task.query.filter_by(assigned_to=user.id).all()

        return {'tasks': [task.to_json() for task in tasks]}, 200

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        if not user or user.role != 'admin':
            return {'msg': 'you are not authorized'}, 403

        data = request.get_json() or {}
        title = data.get('title')
        description = data.get('description')
        assigned_to = data.get('assigned_to') or None
        due_date = data.get('due_date')

        if not title:
            return {'msg': 'title is required'}, 400

        fixed_due_date = datetime.strptime(due_date, '%Y-%m-%d') if due_date else None

        task = Task(
            title=title,
            description=description,
            assigned_to=int(assigned_to) if assigned_to else None,
            due_date=fixed_due_date,
            assigned_date=datetime.now(),
        )
        db.session.add(task)
        db.session.commit()

        return {'msg': f'Task "{title}" created successfully!', 'task': task.to_json()}, 201

    @jwt_required()
    def put(self, task_id):
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        if not user or user.role != 'admin':
            return {'msg': 'you are not authorized'}, 403

        task = Task.query.get(task_id)
        if not task:
            return {'msg': 'task not found'}, 404

        data = request.get_json() or {}
        task.title = data.get('title', task.title)
        task.description = data.get('description', task.description)
        task.assigned_to = int(data['assigned_to']) if data.get('assigned_to') else task.assigned_to
        task.status = data.get('status', task.status)

        due_date = data.get('due_date')
        if due_date is not None:
            task.due_date = datetime.strptime(due_date, '%Y-%m-%d') if due_date else None

        db.session.commit()
        return {'msg': 'task updated successfully', 'task': task.to_json()}, 200

    @jwt_required()
    def patch(self, task_id):
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        if not user:
            return {'msg': 'user not found'}, 404

        task = Task.query.get(task_id)
        if not task:
            return {'msg': 'task not found'}, 404

        if user.role != 'admin' and task.assigned_to != user.id:
            return {'msg': 'you are not authorized to update this task'}, 403

        data = request.get_json() or {}

        if 'status' in data:
            task.status = data['status']

        if user.role == 'admin':
            if 'title' in data:
                task.title = data['title']
            if 'description' in data:
                task.description = data['description']
            if 'assigned_to' in data:
                task.assigned_to = int(data['assigned_to']) if data['assigned_to'] else None
            if 'due_date' in data:
                due_date = data['due_date']
                task.due_date = datetime.strptime(due_date, '%Y-%m-%d') if due_date else None

        db.session.commit()
        return {'msg': 'task status updated successfully', 'task': task.to_json()}, 200

    @jwt_required()
    def delete(self, task_id):
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        if not user or user.role != 'admin':
            return {'msg': 'you are not authorized'}, 403

        task = Task.query.get(task_id)
        if not task:
            return {'msg': 'task not found'}, 404

        db.session.delete(task)
        db.session.commit()
        return {'msg': 'task deleted successfully'}, 200


class UserResource(Resource):
    def get(self):
        employees = User.query.filter_by(role='employee').all()

        users = []
        for employee in employees:
            users.append(employee.to_json())

        return {'msg':"user fetched successfully!", 'users':users}