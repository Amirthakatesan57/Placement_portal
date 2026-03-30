"""
Celery Worker Entry Point
Milestone 7: Celery workers for background jobs
"""

from backend import create_app
from backend.extensions import celery

# Create Flask app
flask_app = create_app()

# Use the celery instance from extensions
celery_app = celery

# Register Flask app context with Celery (ContextTask already handles this)

if __name__ == '__main__':
    celery_app.start()