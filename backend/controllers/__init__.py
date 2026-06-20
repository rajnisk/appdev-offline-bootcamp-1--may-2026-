from controllers.example import HelloWorld
from controllers.auth import Login, Register
from controllers.tasks import TaskResouce, UserResource

def register_api(api):
    api.add_resource(HelloWorld, '/')
    api.add_resource(Register, '/register')
    api.add_resource(Login, '/login')
    api.add_resource(TaskResouce, '/task', '/task/<int:task_id>')
    api.add_resource(UserResource, '/users')