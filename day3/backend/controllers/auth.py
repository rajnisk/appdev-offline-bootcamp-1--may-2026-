from flask import request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask_restful import Resource
from werkzeug.security import check_password_hash, generate_password_hash

from extensions import db
from models import User


class Register(Resource):
    def post(self):
        data = request.get_json() or {}
        username = (data.get("username") or "").strip()
        password = data.get("password") or ""
        email = (data.get("email") or "").strip() or None

        if not username or not password:
            return {"msg": "username and password required"}, 400
        if User.query.filter_by(username=username).first():
            return {"msg": "username already taken"}, 409

        user = User(
            username=username,
            password_hash=generate_password_hash(password),
            role="employee",
            email=email,
        )
        db.session.add(user)
        db.session.commit()
        return {"msg": "created", "user": user.to_dict()}, 201


class Login(Resource):
    def post(self):
        data = request.get_json() or {}
        user = User.query.filter_by(username=(data.get("username") or "")).first()
        if not user or not check_password_hash(
            user.password_hash, data.get("password") or ""
        ):
            return {"msg": "invalid credentials"}, 401

        token = create_access_token(identity=str(user.id))
        return {"token": token, "user": user.to_dict()}


class Me(Resource):
    method_decorators = [jwt_required()]

    def get(self):
        user = db.session.get(User, int(get_jwt_identity()))
        if not user:
            return {"msg": "not found"}, 404
        return user.to_dict()
