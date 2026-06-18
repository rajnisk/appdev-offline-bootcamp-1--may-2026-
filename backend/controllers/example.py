from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User

class HelloWorld(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user.role != 'admin':
            return {'msg': "you\'re not an admin!"}
        return {"hello": "world!"}