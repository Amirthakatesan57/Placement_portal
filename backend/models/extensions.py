from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from celery import Celery

db = SQLAlchemy()
login_manager = LoginManager()
cors = CORS()
celery_app = None

def init_celery(app):
    global celery_app
    celery_app = Celery(
        'celery_worker',
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_RESULT_BACKEND']
    )
    celery_app.conf.update(
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone='UTC',
        enable_utc=True,
    )
    return celery_app