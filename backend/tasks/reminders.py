"""
Interview Reminder Tasks
Milestone 7: Send reminders (Email / GChat / SMS) to students with scheduled interviews
"""

# FIX: Import celery from backend.extensions (not from tasks.__init__)
from backend.extensions import celery
from datetime import datetime, timezone, timedelta
import logging

logger = logging.getLogger(__name__)


@celery.task(bind=True, max_retries=3)
def send_interview_reminders(self):
    """
    Send daily interview reminders to students with upcoming interviews
    Milestone 7: Interview Reminder Job
    
    Runs daily at 9:00 AM via Celery Beat
    """
    from backend import create_app
    from backend.models.user import User
    from backend.models.student import Student
    from backend.models.application import Application
    from backend.models.drive import Drive
    from backend.models.company import Company
    from backend.services.email_service import send_email
    from backend.services.webhook_service import send_gchat_notification
    
    # No need to create app here - ContextTask handles it
    try:
        logger.info("Starting daily interview reminder job...")
        print("[INFO] Starting daily interview reminder job...")
        
        now = datetime.now(timezone.utc)
        tomorrow = now + timedelta(days=1)
        
        # Find applications with interviews in next 24 hours
        applications = Application.query.filter(
            Application.status == 'interview',
            Application.interview_date >= now,
            Application.interview_date <= tomorrow
        ).all()
        
        reminders_sent = 0
        reminders_failed = 0
        
        for app in applications:
            try:
                student = Student.query.get(app.student_id)
                if not student:
                    continue
                
                user = User.query.get(student.user_id)
                if not user or not user.email:
                    continue
                
                drive = Drive.query.get(app.drive_id)
                company = Company.query.get(drive.company_id) if drive else None
                
                # Send email reminder
                email_sent = send_interview_email(
                    student=student,
                    user=user,
                    application=app,
                    drive=drive,
                    company=company
                )
                
                if email_sent:
                    reminders_sent += 1
                else:
                    reminders_failed += 1
                    
            except Exception as e:
                logger.error(f"Failed to send reminder: {str(e)}")
                reminders_failed += 1
                continue
        
        logger.info(f"Interview reminder job completed. Sent: {reminders_sent}, Failed: {reminders_failed}")
        print(f"[SUCCESS] Interview reminder job completed. Sent: {reminders_sent}, Failed: {reminders_failed}")
        
        return {
            'status': 'success',
            'reminders_sent': reminders_sent,
            'reminders_failed': reminders_failed
        }
        
    except Exception as e:
        logger.error(f"Interview reminder job failed: {str(e)}")
        print(f"[ERROR] Interview reminder job failed: {str(e)}")
        return {
            'status': 'failed',
            'error': str(e)
        }


def send_interview_email(student, user, application, drive, company):
    """Send interview reminder email to student"""
    try:
        from backend.services.email_service import send_email
        
        subject = f"Interview Reminder: {drive.job_title if drive else 'Job Interview'}"
        
        interview_date = application.interview_date
        if interview_date:
            interview_date_str = interview_date.strftime("%B %d, %Y at %I:%M %p")
        else:
            interview_date_str = "To be scheduled"
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #0d6efd;">📅 Interview Reminder</h2>
                <p>Dear {student.full_name},</p>
                <p>This is a reminder about your upcoming interview:</p>
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <p><strong>Position:</strong> {drive.job_title if drive else 'N/A'}</p>
                    <p><strong>Company:</strong> {company.company_name if company else 'N/A'}</p>
                    <p><strong>Interview Date:</strong> {interview_date_str}</p>
                    <p><strong>Location:</strong> {drive.location if drive else 'N/A'}</p>
                </div>
                <p>Good luck!</p>
            </div>
        </body>
        </html>
        """
        
        email_sent = send_email(
            to=user.email,
            subject=subject,
            html_body=html_body,
            text_body=f"Interview reminder for {drive.job_title if drive else 'N/A'}"
        )
        
        logger.info(f"Interview reminder sent to {user.email}")
        return email_sent
        
    except Exception as e:
        logger.error(f"Failed to send interview email: {str(e)}")
        return False