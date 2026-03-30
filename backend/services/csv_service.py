"""
CSV Export Service
Milestone 7: Generate CSV files for application and placement history
"""

from backend.models.student import Student
from backend.models.company import Company
from backend.models.drive import Drive
from backend.models.application import Application
from backend.models.placement import Placement
import csv
import io
import logging

logger = logging.getLogger(__name__)


def generate_application_csv(user_id, user_role, student_id=None, company_id=None):
    """
    Generate CSV for application history
    Milestone 7: User-triggered CSV Export
    """
    try:
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow([
            'Application ID',
            'Student Name',
            'Student Roll Number',
            'Company Name',
            'Job Title',
            'Status',
            'Application Date',
            'Interview Date',
            'Feedback'
        ])
        
        # Get applications based on user role
        if user_role == 'student':
            applications = Application.query.filter_by(student_id=student_id).all()
        elif user_role == 'company':
            # Get all drives for this company
            drives = Drive.query.filter_by(company_id=company_id).all()
            drive_ids = [drive.id for drive in drives]
            if drive_ids:
                applications = Application.query.filter(Application.drive_id.in_(drive_ids)).all()
            else:
                applications = []
        else:
            applications = []
        
        # Write data rows
        for app in applications:
            student = Student.query.get(app.student_id)
            drive = Drive.query.get(app.drive_id)
            company = Company.query.get(drive.company_id) if drive else None
            
            writer.writerow([
                app.id,
                student.full_name if student else 'N/A',
                student.roll_number if student else 'N/A',
                company.company_name if company else 'N/A',
                drive.job_title if drive else 'N/A',
                app.status,
                app.application_date.strftime('%Y-%m-%d %H:%M:%S') if app.application_date else 'N/A',
                app.interview_date.strftime('%Y-%m-%d %H:%M:%S') if app.interview_date else 'N/A',
                app.feedback or 'N/A'
            ])
        
        filename = f"applications_export.csv"
        return output.getvalue(), filename
        
    except Exception as e:
        logger.error(f"Failed to generate application CSV: {str(e)}")
        raise


def generate_placement_csv(user_id, user_role, student_id=None, company_id=None):
    """
    Generate CSV for placement history
    Milestone 7: User-triggered CSV Export
    """
    try:
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow([
            'Placement ID',
            'Student Name',
            'Student Roll Number',
            'Company Name',
            'Position',
            'Salary',
            'Joining Date',
            'Status',
            'Placement Date'
        ])
        
        # Get placements based on user role
        if user_role == 'student':
            placements = Placement.query.filter_by(student_id=student_id).all()
        elif user_role == 'company':
            placements = Placement.query.filter_by(company_id=company_id).all()
        else:
            placements = []
        
        # Write data rows
        for placement in placements:
            student = Student.query.get(placement.student_id)
            company = Company.query.get(placement.company_id)
            
            writer.writerow([
                placement.id,
                student.full_name if student else 'N/A',
                student.roll_number if student else 'N/A',
                company.company_name if company else 'N/A',
                placement.position,
                placement.salary,
                placement.joining_date.strftime('%Y-%m-%d') if placement.joining_date else 'N/A',
                placement.status,
                placement.placement_date.strftime('%Y-%m-%d %H:%M:%S') if placement.placement_date else 'N/A'
            ])
        
        filename = f"placements_export.csv"
        return output.getvalue(), filename
        
    except Exception as e:
        logger.error(f"Failed to generate placement CSV: {str(e)}")
        raise