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

class Task(db.Model):
    id =db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(250))
    assigned_date = db.Column(db.DateTime, nullable=True)
    due_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(50), default='pending')

    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    
    def to_json(self):
        return{
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'assigned_date': self.assigned_date.isoformat() if self.assigned_date else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'status': self.status,
            'assigned_to': self.assigned_to
        }