import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from werkzeug.security import generate_password_hash

load_dotenv()

from controllers import register_api
from extensions import db, jwt
from models import User

def ensure_admin():
    admin = User.query.filter_by(role='admin').first()
    if not admin:
        admin = User(full_name="admin", role="admin", password="admin", email="admin@mail.com")
        db.session.add(admin)
        db.session.commit()

    
def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "sqlite:///app.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["JWT_SECRET_KEY"] = "not-super-secret"  

    CORS(app)

    db.init_app(app)
    jwt.init_app(app)

    api = Api(app)
    register_api(api)


    with app.app_context():
        # db.drop_all()
        db.create_all()
        ensure_admin()
    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=int(os.getenv("PORT", "5000")))
