from models import User
from flask_restful import Resource, request
from extensions import db
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash


class Register(Resource):
    def post(self):
        data = request.get_json() or {}
        full_name = data['full_name']
        email = data['email']
        password = data['password']

        if not full_name:
            return {'msg': 'full name is required'}

        user = User.query.filter_by(email=email).first()

        if user:
            return {'msg': 'email already registered'}, 400
        password_hash = generate_password_hash(password)
        user = User(full_name=full_name, email=email, password=password_hash)
        db.session.add(user)
        db.session.commit()
        return {'msg': 'user registered successfully!'}


class Login(Resource):
    def post(self):
        data = request.get_json() or {}
        email = data['email']
        password = data['password']

        user = User.query.filter_by(email=email).first()
        if not user:
            return {'msg': "no such user exists!"}
        
        print(f"User password hash: {user.password}, Provided password: {password}")  # Debugging line
        # if user.password != password:
        if not check_password_hash(user.password, password):
            return {'msg': "incorrect password!"}
        
        access_token = create_access_token(identity=str(user.id))
        return {'msg': 'loggedin successfully', 'access_token':access_token, 'role': user.role}