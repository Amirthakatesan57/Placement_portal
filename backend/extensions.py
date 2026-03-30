"""
Flask Extensions Configuration
Milestone 7: Celery + Redis Configuration
Milestone 8: Redis Caching
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from celery import Celery
from celery.schedules import crontab

# Initialize Flask extensions at module level
db = SQLAlchemy()
login_manager = LoginManager()
cors = CORS()

# Celery instance (initialized in app factory)
celery = None

# Cache service instance (Milestone 8)
cache_service = None

def init_celery(app):
    """
    Initialize Celery with Flask app
    Milestone 7: Celery workers, Celery Beat, and Redis server setup
    """
    global celery
    
    class FlaskCelery(Celery):
        def __init__(self, *args, **kwargs):
            kwargs["app"] = app
            super().__init__(*args, **kwargs)
            
            # Celery Configuration
            self.conf.update(
                broker_url=app.config['CELERY_BROKER_URL'],
                result_backend=app.config['CELERY_RESULT_BACKEND'],
                task_serializer='json',
                accept_content=['json'],
                result_serializer='json',
                timezone='UTC',
                enable_utc=True,
                
                # Task execution settings
                task_track_started=True,
                task_time_limit=300,
                task_soft_time_limit=240,
                
                # Result expiration (1 hour)
                result_expires=3600,
                
                # Retry settings
                task_default_retry_delay=60,
                task_max_retries=3,
                
                # FIX: Add these settings for Windows
                worker_prefetch_multiplier=1,
                worker_max_tasks_per_child=1,
                broker_connection_retry_on_startup=True,
            )
            
            # FIX: Explicitly import tasks instead of autodiscover
            self.autodiscover_tasks(['backend.tasks'], force=True)
    
    celery = FlaskCelery('placement_portal')
    
    # Configure Celery Beat Schedule (Scheduled Tasks)
    celery.conf.beat_schedule = {
        # Daily interview reminders at 9:00 AM
        'daily-interview-reminders': {
            'task': 'backend.tasks.reminders.send_interview_reminders',
            'schedule': crontab(hour=9, minute=0),
            'args': ()
        },
        
        # Monthly placement reports on 1st of every month at 10:00 AM
        'monthly-placement-reports': {
            'task': 'backend.tasks.reports.generate_monthly_reports',
            'schedule': crontab(hour=10, minute=0, day_of_month=1),
            'args': ()
        },
        
        # Clean up old export files daily at 2:00 AM
        'cleanup-old-exports': {
            'task': 'backend.tasks.exports.cleanup_old_exports',
            'schedule': crontab(hour=2, minute=0),
            'args': ()
        }
    }
    
    return celery


def init_cache(app):
    """
    Initialize Redis Cache Service
    Milestone 8: API Performance Optimization
    """
    global cache_service
    
    from backend.services.cache_service import init_cache_service as init_cache
    
    cache_service = init_cache(app)
    
    return cache_service