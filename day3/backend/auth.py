from functools import wraps

from flask_jwt_extended import get_jwt_identity, jwt_required

from extensions import db
from models import User


def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user = db.session.get(User, int(get_jwt_identity()))
        if not user or user.role != "admin":
            return {"msg": "admin only"}, 403
        return fn(*args, **kwargs)

    return wrapper
