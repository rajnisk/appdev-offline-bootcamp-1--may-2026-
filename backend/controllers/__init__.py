from controllers.example import HelloWorld

def register_api(api):
    api.add_resource(HelloWorld, '/')