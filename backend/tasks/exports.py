"""
CSV Export Tasks
Milestone 7: User-triggered CSV Export
"""

# FIX: Import celery from backend.extensions
from backend.extensions import celery
from datetime import datetime, timezone, timedelta
import os
import logging

logger = logging.getLogger(__name__)


@celery.task(bind=True, max_retries=3)
def export_applications_csv(self, user_id, user_role, export_type='all'):
    """Export application history to CSV"""
    from backend.models.user import User
    from backend.models.student import Student
    from backend.models.company import Company
    from backend.models.audit_log import AuditLog
    from backend.extensions import db
    from backend.services.csv_service import generate_application_csv
    from backend.services.email_service import send_email
    
    try:
        logger.info(f"Starting CSV export for user {user_id} (role: {user_role})...")
        print(f"[INFO] Starting CSV export for user {user_id} (role: {user_role})...")
        
        user = User.query.get(user_id)
        if not user or not user.email:
            return {'status': 'failed', 'error': 'User not found'}
        
        # Generate CSV based on role
        if user_role == 'student':
            student = Student.query.filter_by(user_id=user_id).first()
            if not student:
                return {'status': 'failed', 'error': 'Student profile not found'}
            
            csv_data, filename = generate_application_csv(
                user_id=user_id,
                user_role='student',
                student_id=student.id
            )
        elif user_role == 'company':
            company = Company.query.filter_by(user_id=user_id).first()
            if not company:
                return {'status': 'failed', 'error': 'Company profile not found'}
            
            csv_data, filename = generate_application_csv(
                user_id=user_id,
                user_role='company',
                company_id=company.id
            )
        else:
            return {'status': 'failed', 'error': 'Invalid user role'}
        
        # Save CSV
        export_folder = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 
            'static', 
            'exports'
        )
        os.makedirs(export_folder, exist_ok=True)
        
        timestamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
        filename_with_timestamp = f"{filename.split('.')[0]}_{timestamp}.csv"
        file_path = os.path.join(export_folder, filename_with_timestamp)
        
        with open(file_path, 'w', encoding='utf-8', newline='') as f:
            f.write(csv_data)
        
        download_url = f"/static/exports/{filename_with_timestamp}"
        
        # Send email (optional)
        email_sent = False
        try:
            from backend.tasks.exports import send_export_complete_email
            email_sent = send_export_complete_email(
                user=user,
                filename=filename_with_timestamp,
                download_url=download_url,
                export_type='applications'
            )
        except:
            email_sent = False
        
        # Log the export action
        try:
            audit_log = AuditLog(
                user_id=user_id,
                action='csv_export_completed',
                entity_type='export',
                entity_id=user_id,
                details=f'Application CSV export completed: {filename_with_timestamp}',
                timestamp=datetime.now(timezone.utc)
            )
            db.session.add(audit_log)
            db.session.commit()
        except:
            pass
        
        logger.info(f"CSV export completed: {filename_with_timestamp}")
        print(f"[SUCCESS] CSV export completed: {filename_with_timestamp}")
        
        return {
            'status': 'success',
            'filename': filename_with_timestamp,
            'download_url': download_url,
            'email_sent': email_sent
        }
        
    except Exception as e:
        logger.error(f"CSV export failed: {str(e)}")
        print(f"[ERROR] CSV export failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return {'status': 'failed', 'error': str(e)}


@celery.task(bind=True, max_retries=3)
def export_placements_csv(self, user_id, user_role):
    """Export placement history to CSV"""
    from backend.models.user import User
    from backend.models.student import Student
    from backend.models.company import Company
    from backend.models.audit_log import AuditLog
    from backend.extensions import db
    from backend.services.csv_service import generate_placement_csv
    
    try:
        logger.info(f"Starting placement CSV export for user {user_id}...")
        print(f"[INFO] Starting placement CSV export for user {user_id}...")
        
        user = User.query.get(user_id)
        if not user or not user.email:
            return {'status': 'failed', 'error': 'User not found'}
        
        # Generate CSV based on role
        if user_role == 'student':
            student = Student.query.filter_by(user_id=user_id).first()
            if not student:
                return {'status': 'failed', 'error': 'Student profile not found'}
            
            csv_data, filename = generate_placement_csv(
                user_id=user_id,
                user_role='student',
                student_id=student.id
            )
        elif user_role == 'company':
            company = Company.query.filter_by(user_id=user_id).first()
            if not company:
                return {'status': 'failed', 'error': 'Company profile not found'}
            
            csv_data, filename = generate_placement_csv(
                user_id=user_id,
                user_role='company',
                company_id=company.id
            )
        else:
            return {'status': 'failed', 'error': 'Invalid user role'}
        
        # Save CSV
        export_folder = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 
            'static', 
            'exports'
        )
        os.makedirs(export_folder, exist_ok=True)
        
        timestamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
        filename_with_timestamp = f"{filename.split('.')[0]}_{timestamp}.csv"
        file_path = os.path.join(export_folder, filename_with_timestamp)
        
        with open(file_path, 'w', encoding='utf-8', newline='') as f:
            f.write(csv_data)
        
        download_url = f"/static/exports/{filename_with_timestamp}"
        
        # Send email (optional)
        email_sent = False
        try:
            from backend.tasks.exports import send_export_complete_email
            email_sent = send_export_complete_email(
                user=user,
                filename=filename_with_timestamp,
                download_url=download_url,
                export_type='placements'
            )
        except:
            email_sent = False
        
        # Log the export action
        try:
            audit_log = AuditLog(
                user_id=user_id,
                action='csv_export_completed',
                entity_type='export',
                entity_id=user_id,
                details=f'Placement CSV export completed: {filename_with_timestamp}',
                timestamp=datetime.now(timezone.utc)
            )
            db.session.add(audit_log)
            db.session.commit()
        except:
            pass
        
        logger.info(f"Placement CSV export completed: {filename_with_timestamp}")
        print(f"[SUCCESS] Placement CSV export completed: {filename_with_timestamp}")
        
        return {
            'status': 'success',
            'filename': filename_with_timestamp,
            'download_url': download_url,
            'email_sent': email_sent
        }
        
    except Exception as e:
        logger.error(f"Placement CSV export failed: {str(e)}")
        print(f"[ERROR] Placement CSV export failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return {'status': 'failed', 'error': str(e)}


@celery.task
def cleanup_old_exports():
    """Clean up old export files"""
    try:
        logger.info("Starting cleanup of old export files...")
        
        export_folder = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 
            'static', 
            'exports'
        )
        
        retention_days = 7
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=retention_days)
        
        files_deleted = 0
        
        if os.path.exists(export_folder):
            for filename in os.listdir(export_folder):
                file_path = os.path.join(export_folder, filename)
                
                if os.path.isfile(file_path):
                    file_mtime = datetime.fromtimestamp(
                        os.path.getmtime(file_path), 
                        tz=timezone.utc
                    )
                    
                    if file_mtime < cutoff_date:
                        os.remove(file_path)
                        files_deleted += 1
        
        logger.info(f"Cleanup completed. Deleted {files_deleted} files.")
        
        return {
            'status': 'success',
            'files_deleted': files_deleted
        }
        
    except Exception as e:
        logger.error(f"Cleanup failed: {str(e)}")
        return {'status': 'failed', 'error': str(e)}


def send_export_complete_email(user, filename, download_url, export_type):
    """Send email notification when export is complete"""
    try:
        from backend.services.email_service import send_email
        
        subject = f"Your {export_type.title()} Export is Ready"
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h2>Export Complete</h2>
            <p>Dear {user.username},</p>
            <p>Your {export_type} export is ready for download.</p>
            <p><strong>Filename:</strong> {filename}</p>
            <p><a href="http://localhost:5000{download_url}">Download CSV</a></p>
        </body>
        </html>
        """
        
        email_sent = send_email(
            to=user.email,
            subject=subject,
            html_body=html_body,
            text_body=f"Your {export_type} export is ready. Download: http://localhost:5000{download_url}"
        )
        
        return email_sent
        
    except Exception as e:
        logger.error(f"Failed to send export email: {str(e)}")
        return False