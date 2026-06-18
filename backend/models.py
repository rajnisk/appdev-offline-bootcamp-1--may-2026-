from extensions import db

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), default='employee')

    def to_json(self):
        return{
            'full_name':self.full_name,
            'email': self.email,
            'role': self.role
        }
