from flask_restful import Resource

from auth import admin_required
from extensions import cache
from models import User
from services.stats import get_dashboard_stats


class AdminStats(Resource):
    method_decorators = [admin_required]

    def get(self):
        cached = cache.get("admin_stats")
        if cached is not None:
            return cached
        data = get_dashboard_stats()
        cache.set("admin_stats", data, timeout=60)
        return data


class EmployeeList(Resource):
    method_decorators = [admin_required]

    def get(self):
        rows = User.query.filter_by(role="employee").order_by(User.username).all()
        return [u.to_dict() for u in rows]
