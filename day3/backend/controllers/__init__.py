from controllers.admin import AdminStats, EmployeeList
from controllers.auth import Login, Me, Register
from controllers.health import Health, HelloWorld
from controllers.tasks import TaskDetail, TaskList


def register_api(api):
    api.add_resource(Health, "/health")
    api.add_resource(HelloWorld, "/")
    api.add_resource(Register, "/register")
    api.add_resource(Login, "/login")
    api.add_resource(Me, "/me")
    api.add_resource(TaskList, "/tasks")
    api.add_resource(TaskDetail, "/tasks/<int:task_id>")
    api.add_resource(AdminStats, "/admin/stats")
    api.add_resource(EmployeeList, "/admin/employees")
