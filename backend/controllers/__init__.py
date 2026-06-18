from controllers.example import HelloWorld
from controllers.auth import Login, Register

def register_api(api):
    api.add_resource(HelloWorld, '/')
    api.add_resource(Register, '/register')
    api.add_resource(Login, '/login')