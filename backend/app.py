import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from werkzeug.security import generate_password_hash
from celery import Celery
from celery_app import init_celery

load_dotenv()

from controllers import register_api
from extensions import db, jwt, cache, mail
from models import User

def ensure_admin():
    admin = User.query.filter_by(role='admin').first()
    if not admin:
        password = generate_password_hash('admin')
        admin = User(full_name="admin", role="admin", password=password, email="admin@mail.com")
        db.session.add(admin)
        db.session.commit()

    
def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "sqlite:///app.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["JWT_SECRET_KEY"] = "not-super-secret"  


    # ============================
    # Celery Configuration
    # ============================
    app.config['broker_url'] = os.getenv('BROKER_URL', 'redis://localhost:6379/0')
    app.config['result_backend'] = os.getenv('RESULT_BACKEND', 'redis://localhost:6379/0')

    celery = Celery(app.name, broker=app.config['broker_url'], backend=app.config['result_backend'])
    celery.conf.broker_connection_retry_on_startup = True




    # ============================
    # Flask-Caching with Redis
    # ============================
    app.config['CACHE_TYPE'] = 'RedisCache'
    app.config['CACHE_REDIS_HOST'] = 'localhost'
    app.config['CACHE_REDIS_PORT'] = 6379
    app.config['CACHE_REDIS_DB'] = 1
    app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/1'
    app.config['CACHE_DEFAULT_TIMEOUT'] = 60

    # ============================
    # Flask-Mail Configuration
    # ============================
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USER')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASS')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USER')


    CORS(app)

    db.init_app(app)
    jwt.init_app(app)
    cache.init_app(app)
    mail.init_app(app)
    api = Api(app)
    celery = init_celery(app)


    register_api(api)


    with app.app_context():
        db.drop_all()
        db.create_all()
        ensure_admin()
    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=int(os.getenv("PORT", "5000")))
