import datetime
import os
from flask import Flask, request
from flask_restful import Api, Resource
from flask_mail import Mail, Message
from flask_caching import Cache
from celery import Celery
from dotenv import load_dotenv
from celery.schedules import crontab

# Load .env
load_dotenv()

app = Flask(__name__)
api = Api(app)

# ============================
# Flask-Mail Configuration
# ============================
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USER')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASS')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USER')
mail = Mail(app)

# ============================
# Flask-Caching with Redis
# ============================
app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_REDIS_HOST'] = 'localhost'
app.config['CACHE_REDIS_PORT'] = 6379
app.config['CACHE_REDIS_DB'] = 1
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/1'
app.config['CACHE_DEFAULT_TIMEOUT'] = 60
cache = Cache(app)

# ============================
# Celery Configuration
# ============================
app.config['broker_url'] = os.getenv('BROKER_URL', 'redis://localhost:6379/0')
app.config['result_backend'] = os.getenv('RESULT_BACKEND', 'redis://localhost:6379/0')

celery = Celery(app.name, broker=app.config['broker_url'], backend=app.config['result_backend'])
celery.conf.broker_connection_retry_on_startup = True

# ============================
# Celery Context Setup
# ============================
def init_celery(flask_app):
    celery_app = Celery(
        flask_app.import_name,
        broker=flask_app.config['broker_url'],
        backend=flask_app.config['result_backend']
    )
    celery_app.conf.update(flask_app.config)

    class ContextTask(celery_app.Task):
        def __call__(self, *args, **kwargs):
            with flask_app.app_context():
                return super().__call__(*args, **kwargs)

    celery_app.Task = ContextTask
    return celery_app

celery = init_celery(app)


class SendEmail(Resource):
    def get(self):
        email = request.args.get('email')
        if not email:
            return {'message': 'Error: No email provided'}, 400

        msg = Message(
            subject="Test Email from Flask",
            recipients=[email],
            body="This is a test email sent via Flask and SMTP."
        )

        try:
            mail.send(msg)
            return {'message': f'Email sent to {email}!'}, 200
        except Exception as e:
            return {'message': f"Error: {str(e)}"}, 500

api.add_resource(SendEmail, '/send-email')


class CacheDemo(Resource):
    @cache.cached()
    def get(self):
        now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return {'data': 'This is a cached response!', 'timestamp': now_time}, 200

api.add_resource(CacheDemo, '/cache')


class DeleteCache(Resource):
    def get(self):
        cache.clear()
        return {'message': 'Cache cleared successfully!'}, 200

api.add_resource(DeleteCache, '/delete-cache')



@celery.task(name="tasks.background_task")
def background_task():
    return 'Background task completed'

class QueuedTask(Resource):
    def get(self):
        task = background_task.apply_async()
        return {'task_id': task.id}, 202

api.add_resource(QueuedTask, '/queued-task')


celery.conf.timezone = 'Asia/Kolkata'
celery.conf.beat_schedule = {
    'daily-reminder': {
        'task': 'tasks.send_reminders',
        'schedule': crontab(hour=17, minute=20),
    },
}

@celery.task(name="tasks.send_reminders")
def send_reminders():
    print("Reminder sent at 7:00 AM IST!")
    return "Reminder triggered"




if __name__ == '__main__':
    app.run(debug=True, port=5001)