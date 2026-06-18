import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from werkzeug.security import generate_password_hash

load_dotenv()

from controllers import register_api
from celery_worker import init_celery
from extensions import cache, db, mail
from models import User


def ensure_admin():
    if User.query.filter_by(role="admin").first():
        return
    username = os.getenv("ADMIN_USERNAME", "admin")
    password = os.getenv("ADMIN_PASSWORD", "admin123")
    email = os.getenv("ADMIN_EMAIL", "").strip() or None
    user = User(
        username=username,
        password_hash=generate_password_hash(password),
        role="admin",
        email=email,
    )
    db.session.add(user)
    db.session.commit()


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-change-me")
    
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "jwt-dev-change-me")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "sqlite:///app.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False



    app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT", "587"))
    app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS", "true").lower() in (
        "1",
        "true",
        "yes",
    )
    app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME", "")
    app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD", "")
    app.config["MAIL_DEFAULT_SENDER"] = os.getenv(
        "MAIL_DEFAULT_SENDER", app.config["MAIL_USERNAME"] or "noreply@localhost"
    )



    app.config["CACHE_TYPE"] = os.getenv("CACHE_TYPE", "SimpleCache")
    app.config["CACHE_REDIS_URL"] = os.getenv(
        "CACHE_REDIS_URL", "redis://127.0.0.1:6379/1"
    )
    app.config["CACHE_DEFAULT_TIMEOUT"] = int(
        os.getenv("CACHE_DEFAULT_TIMEOUT", "300")
    )



    app.config["CELERY_BROKER_URL"] = os.getenv(
        "CELERY_BROKER_URL", "redis://127.0.0.1:6379/0"
    )
    app.config["CELERY_RESULT_BACKEND"] = os.getenv(
        "CELERY_RESULT_BACKEND", app.config["CELERY_BROKER_URL"]
    )
    app.config["CELERY_TIMEZONE"] = os.getenv("CELERY_TIMEZONE", "UTC")


    db.init_app(app)
    mail.init_app(app)
    cache.init_app(app)

    
    CORS(app, supports_credentials=True)
    JWTManager(app)

    api = Api(app)
    register_api(api)
    init_celery(app)

    with app.app_context():
        db.create_all()
        ensure_admin()

    return app


app = create_app()
celery_app = app.extensions["celery"]

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=int(os.getenv("PORT", "5000")))
