"""
Celery Tasks Package
Milestone 7: Backend Jobs - Interview Reminders, Placement Reports, and CSV Export
"""

# Import celery instance from extensions
from backend.extensions import celery

# Export celery instance
__all__ = ['celery']