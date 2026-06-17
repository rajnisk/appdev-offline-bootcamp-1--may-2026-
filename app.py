from flask import Flask, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mad2.db"
db = SQLAlchemy(app)


# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), default='employee')

    def to_json(self):
        return{
            'full_name':self.full_name,
            'email': self.email,
            'role': self.role
        }


with app.app_context():
    db.create_all()


class UserRes(Resource):
    def get(self):
        employee = User.query.filter_by(role='employee').all()
        print(employee)
        return {
            'name':employee[0].full_name
        }
    def put(self):
        data = request.get_json() or {}
        user_id = data.get('user_id')
        full_name = data.get('full_name')

        user = User.query.get(user_id)
        user.full_name = full_name

        db.session.commit()
        return {'msg': f'user name updated to {full_name}!'}
    def delete(self):
        data = request.get_json()
        user_id = data.get('user_id')

        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()


class UserResource(Resource):
    def get(self):
        users = User.query.all()
        data = []
        for user in users:
            data.append(user.to_json())
        return {'msg':data}
    

    def post(self):
        print('inside post')
        data = request.get_json() or {}
        print(data)
        full_name = data['full_name']
        email = data['email']
        password = data['password']

        user = User(full_name=full_name, email=email, password=password)
        db.session.add(user)
        db.session.commit()

        print(full_name, email, password)
        return {"msg":"--"}


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}
    
    def post(self):
        data = request.get_json() or {}
        print(data)
        return {'data': 'from post method'}
    

api.add_resource(HelloWorld, '/')
api.add_resource(UserResource, '/user')
api.add_resource(UserRes, '/usr')

if __name__ == '__main__':
    app.run(port=5001, debug=True)