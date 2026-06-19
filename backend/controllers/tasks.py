from datetime import datetime

from flask_restful import Resource, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Task, User
from extensions import db


class TaskResouce(Resource):
    def get(self):
        return {"hello": "world!"}, 200
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user.role != "admin":
            return {'msg': 'you\'re not authrized'}
        
        data = request.get_json()
        title = data.get('title')
        description = data.get('description')
        assigned_to = data.get('assigned_to')
        assigned_date = datetime.now()
        due_date = data.get('due_date')

        print(f"Received due_date: {due_date}")  # Debugging line
        fixed_due_date = datetime.strptime(due_date, '%Y-%m-%d') if due_date else None

        task = Task(title=title, description=description, assigned_to=assigned_to, due_date=fixed_due_date, assigned_date=assigned_date)
        db.session.add(task)
        db.session.commit()

        return {'msg':f'Task "{title}" created successfully!'}, 201
    


class UserResource(Resource):
    def get(self):
        employees = User.query.filter_by(role='employee').all()

        users = []
        for employee in employees:
            users.append(employee.to_json())

        return {'msg':"user fetched successfully!", 'users':users}