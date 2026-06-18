from celery import Celery

celery = Celery(__name__)


def _app_context():
    import app as app_module

    return app_module.app.app_context()


def init_celery(app):
    celery.conf.update(
        broker_url=app.config["CELERY_BROKER_URL"],
        result_backend=app.config.get(
            "CELERY_RESULT_BACKEND", app.config["CELERY_BROKER_URL"]
        ),
        timezone=app.config.get("CELERY_TIMEZONE", "UTC"),
    )
    app.extensions["celery"] = celery
    return celery


@celery.task(name="celery_worker.example_async_job")
def example_async_job(user_id: int):
    with _app_context():
        from models import User

        user = User.query.get(user_id)
        if not user:
            return {"msg": "user not found"}
        return {"msg": f"processed user {user.username}", "user_id": user_id}
