from datetime import datetime

from flask_restful import Resource, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User
from extensions import cache, mail
from flask_mail import Message

class HelloWorld(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user.role != 'admin':
            return {'msg': "you\'re not an admin!"}
        return {"hello": "world!"}


class CacheDemo(Resource):
    @cache.cached()
    def get(self):
        now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return {'data': 'This is a cached response!', 'timestamp': now_time}, 200



class DeleteCache(Resource):
    def get(self):
        cache.clear()
        return {'message': 'Cache cleared successfully!'}, 200


class SendEmail(Resource):
    def get(self):
        email = request.args.get('email')
        if not email:
            return {'message': 'Error: No email provided'}, 400

        msg = Message(
            subject="Test Email from Flask",
            recipients=[email],
            body="This is a test email sent via Flask and SMTP."
        )

        try:
            mail.send(msg)
            return {'message': f'Email sent to {email}!'}, 200
        except Exception as e:
            return {'message': f"Error: {str(e)}"}, 500

