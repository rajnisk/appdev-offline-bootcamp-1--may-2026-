from models import Task, User


def get_dashboard_stats():
    return {
        "total_tasks": Task.query.count(),
        "total_users": User.query.count(),
        "employees": User.query.filter_by(role="employee").count(),
        "admins": User.query.filter_by(role="admin").count(),
        "tasks_by_status": {
            status: Task.query.filter_by(status=status).count()
            for status in ("Pending", "In Progress", "Completed")
        },
    }
