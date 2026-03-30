"""
Student Dashboard and Job Application System API Endpoints
Milestone 5 & 6: Student Dashboard, Application History and Status Tracking
"""

import os
import uuid

from flask import Blueprint, jsonify, request, current_app, send_file
from flask_login import login_required, current_user
from datetime import datetime, timezone
from backend.auth.decorators import student_required
from backend.extensions import db
from backend.models.user import User
from backend.models.student import Student
from backend.models.company import Company
from backend.models.drive import Drive
from backend.models.application import Application
from backend.models.placement import Placement
from backend.models.audit_log import AuditLog
from sqlalchemy import or_, and_, func
from backend.services.cache_service import cached, cache_service, invalidate_cache, CACHE_EXPIRY

student_bp = Blueprint('student', __name__, url_prefix='/api/student')


@student_bp.route('/drives', methods=['GET'])
@student_required
@cached('job_listings', expiry=CACHE_EXPIRY['job_listings'])  # ADD THIS DECORATOR
def get_available_drives():
    """
    View and search job postings
    Milestone 6: Ensure students can view only approved placement drives
    Milestone 8: Cached for performance
    """
    try:
        student = get_student_profile()
        
        if not student:
            return jsonify({'error': 'Student profile not found'}), 404
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        per_page = min(per_page, 100)
        
        search = request.args.get('search', '')
        company = request.args.get('company', '')
        skills = request.args.get('skills', '')
        location = request.args.get('location', '')
        
        # Milestone 6: Query ONLY approved drives with approved companies
        query = Drive.query.join(Company).filter(
            Drive.status == 'approved',
            Company.approval_status == 'approved',
            Drive.application_deadline > datetime.now(timezone.utc)
        )
        
        if search:
            query = query.filter(
                or_(
                    Drive.job_title.ilike(f'%{search}%'),
                    Company.company_name.ilike(f'%{search}%')
                )
            )
        
        if company:
            query = query.filter(Company.company_name.ilike(f'%{company}%'))
        
        if skills:
            query = query.filter(Drive.skills_required.ilike(f'%{skills}%'))
        
        if location:
            query = query.filter(Drive.location.ilike(f'%{location}%'))
        
        drives = query.order_by(Drive.created_at.desc()).paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        drive_list = []
        for drive in drives.items:
            existing_application = Application.query.filter_by(
                student_id=student.id,
                drive_id=drive.id
            ).first()
            
            company = Company.query.get(drive.company_id)
            
            drive_list.append({
                'id': drive.id,
                'job_title': drive.job_title,
                'job_description': drive.job_description[:200] + '...' if len(drive.job_description) > 200 else drive.job_description,
                'company_name': company.company_name if company else 'N/A',
                'company_id': drive.company_id,
                'salary': drive.salary,
                'location': drive.location,
                'eligibility_criteria': drive.eligibility_criteria,
                'skills_required': drive.skills_required,
                'application_deadline': drive.application_deadline.isoformat() if drive.application_deadline else None,
                'already_applied': existing_application is not None,
                'application_status': existing_application.status if existing_application else None,
                'is_expired': False,
                'created_at': drive.created_at.isoformat() if drive.created_at else None
            })
        
        return jsonify({
            'drives': drive_list,
            'total': drives.total,
            'pages': drives.pages,
            'current_page': page,
            'per_page': per_page,
            'has_next': drives.has_next,
            'has_prev': drives.has_prev
        }), 200
    
    except Exception as e:
        current_app.logger.error(f"Get available drives error: {str(e)}")
        return jsonify({
            'error': 'Failed to load job postings',
            'details': str(e) if current_app.debug else None
        }), 500


def log_student_action(action, entity_type, entity_id, details=None):
    """Helper function to log student actions for audit trail"""
    try:
        audit_log = AuditLog(
            user_id=current_user.id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            details=details,
            ip_address=request.remote_addr,
            timestamp=datetime.now(timezone.utc)
        )
        db.session.add(audit_log)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Audit log error: {str(e)}")


def get_student_profile():
    """Helper function to get current user's student profile"""
    return Student.query.filter_by(user_id=current_user.id).first()

def make_aware(dt):

    if dt is None:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt

@student_bp.route('/dashboard/stats', methods=['GET'])
@student_required
def get_student_dashboard_stats():
    """
    Get comprehensive dashboard statistics for student
    FIX: Count from Placement table for placed status
    """
    try:
        student = get_student_profile()
        
        if not student:
            return jsonify({
                'error': 'Student profile not found',
                'needs_profile': True
            }), 404
        
        # Get all applications for this student
        applications = Application.query.filter_by(student_id=student.id).all()
        
        # Get all placements for this student
        placements = Placement.query.filter_by(student_id=student.id).all()
        
        # Calculate statistics from applications
        total_applications = len(applications)
        applied = len([a for a in applications if a.status == 'applied'])
        shortlisted = len([a for a in applications if a.status == 'shortlisted'])
        interview = len([a for a in applications if a.status == 'interview'])
        selected = len([a for a in applications if a.status == 'selected'])
        rejected = len([a for a in applications if a.status == 'rejected'])
        
        # FIX: Use placement count for placed status
        placed = len(placements)
        
        # Get current time as timezone-aware
        now = datetime.now(timezone.utc)
        
        # Get upcoming interviews with proper datetime comparison
        upcoming_interviews = []
        for a in applications:
            if a.status == 'interview' and a.interview_date:
                interview_date_aware = make_aware(a.interview_date)
                if interview_date_aware and interview_date_aware > now:
                    upcoming_interviews.append(a)
        
        # Get latest placement status
        latest_placement = placements[0] if placements else None
        placement_status = latest_placement.status if latest_placement else None
        
        stats = {
            'student_id': student.id,
            'student_name': student.full_name,
            'roll_number': student.roll_number,
            'branch': student.branch,
            'cgpa': student.cgpa,
            'total_applications': total_applications,
            'applied': applied,
            'shortlisted': shortlisted,
            'interview_scheduled': interview,
            'selected': selected,
            'rejected': rejected,
            'placed': placed,  # FIX: From Placement table
            'placement_status': placement_status,
            'upcoming_interviews': len(upcoming_interviews),
            'is_eligible': student.is_eligible,
            'has_placement': placed > 0
        }
        
        return jsonify(stats), 200
    
    except Exception as e:
        current_app.logger.error(f"Student dashboard stats error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': 'Failed to load dashboard statistics',
            'details': str(e) if current_app.debug else None
        }), 500

# ============================================================================
# STUDENT PROFILE ENDPOINTS - COMPLETE WITH UPDATE FUNCTIONALITY
# ============================================================================

@student_bp.route('/profile', methods=['GET'])
@student_required
def get_student_profile_endpoint():
    """
    Get student profile details
    Milestone 5: Students can view their profile
    """
    try:
        student = get_student_profile()
        
        if not student:
            return jsonify({
                'error': 'Student profile not found',
                'needs_profile': True
            }), 404
        
        user = User.query.get(student.user_id)
        
        profile_data = {
            'id': student.id,
            'user_id': student.user_id,
            'full_name': student.full_name,
            'roll_number': student.roll_number,
            'branch': student.branch,
            'year_of_study': student.year_of_study,
            'cgpa': student.cgpa,
            'phone': student.phone,
            'email': user.email if user else None,
            'username': user.username if user else None,
            'skills': student.skills,
            'education_details': student.education_details,
            'experience_details': student.experience_details,
            'resume_path': student.resume_path,
            'is_eligible': student.is_eligible,
            'created_at': student.created_at.isoformat() if student.created_at else None,
            'updated_at': student.updated_at.isoformat() if student.updated_at else None
        }
        
        return jsonify(profile_data), 200
    
    except Exception as e:
        current_app.logger.error(f"Get student profile error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': 'Failed to load student profile',
            'details': str(e) if current_app.debug else None
        }), 500


@student_bp.route('/profile', methods=['PUT'])
@student_required
def update_student_profile():
    """
    Update student profile details
    Milestone 5: Students can update profile (education, skills, resume, experience)
    """
    try:
        student = get_student_profile()
        
        if not student:
            return jsonify({
                'error': 'Student profile not found',
                'needs_profile': True
            }), 404
        
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Define allowed update fields (Milestone 5: education, skills, resume, experience)
        update_fields = [
            'phone', 'skills', 'education_details', 'experience_details'
        ]
        
        updated = False
        for field in update_fields:
            if field in data:
                setattr(student, field, data[field])
                updated = True
        
        if not updated:
            return jsonify({'error': 'No valid fields to update'}), 400
        
        student.updated_at = datetime.now(timezone.utc)
        db.session.commit()
        
        log_student_action(
            'profile_updated', 
            'student', 
            student.id, 
            f'Updated student profile: {student.full_name}'
        )
        
        return jsonify({
            'message': 'Student profile updated successfully',
            'student_id': student.id,
            'full_name': student.full_name,
            'updated_at': student.updated_at.isoformat()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Update student profile error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': 'Failed to update student profile',
            'details': str(e) if current_app.debug else None
        }), 500


@student_bp.route('/profile/resume', methods=['POST'])
@student_required
def upload_resume():
    """
    Upload student resume
    Milestone 5: Students can upload resume
    """
    try:
        student = get_student_profile()
        
        if not student:
            return jsonify({'error': 'Student profile not found'}), 404
        
        # Check if file is in request
        if 'resume' not in request.files:
            return jsonify({'error': 'No resume file provided'}), 400
        
        file = request.files['resume']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Validate file type
        allowed_extensions = ['pdf', 'doc', 'docx']
        file_extension = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
        
        if file_extension not in allowed_extensions:
            return jsonify({
                'error': 'Invalid file type. Allowed: PDF, DOC, DOCX'
            }), 400
        
        # Create uploads directory if it doesn't exist
        upload_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 
            'static', 
            'uploads', 
            'resumes'
        )
        os.makedirs(upload_dir, exist_ok=True)
        
        # Generate unique filename
        unique_filename = f"{student.roll_number}_{uuid.uuid4().hex}.{file_extension}"
        file_path = os.path.join(upload_dir, unique_filename)
        
        # Save file
        file.save(file_path)
        
        # Update student record
        student.resume_path = f'/static/uploads/resumes/{unique_filename}'
        student.updated_at = datetime.now(timezone.utc)
        db.session.commit()
        
        log_student_action(
            'resume_uploaded', 
            'student', 
            student.id,
            f'Uploaded resume: {unique_filename}'
        )
        
        return jsonify({
            'message': 'Resume uploaded successfully',
            'resume_path': student.resume_path,
            'student_id': student.id
        }), 200
    
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Upload resume error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': 'Failed to upload resume',
            'details': str(e) if current_app.debug else None
        }), 500


@student_bp.route('/profile/resume', methods=['GET'])
@student_required
def download_resume():
    """Download student resume"""
    try:
        student = get_student_profile()
        
        if not student or not student.resume_path:
            return jsonify({'error': 'No resume uploaded'}), 404
        
        # Get file path
        file_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 
            'static', 
            student.resume_path.lstrip('/')
        )
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'Resume file not found'}), 404
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name=f'{student.roll_number}_resume.pdf'
        )
    
    except Exception as e:
        current_app.logger.error(f"Download resume error: {str(e)}")
        return jsonify({
            'error': 'Failed to download resume',
            'details': str(e) if current_app.debug else None
        }), 500

# ============================================================================
# JOB POSTING ENDPOINTS - MILESTONE 6 VALIDATION
# ============================================================================

@student_bp.route('/drives', methods=['GET'])
@student_bp.route('/drives/<int:drive_id>', methods=['GET'])
@student_required
def get_drive_details(drive_id):
    """
    Get detailed drive information
    Milestone 6: Verify drive and company are approved
    """
    try:
        student = get_student_profile()
        
        if not student:
            return jsonify({'error': 'Student profile not found'}), 404
        
        drive = Drive.query.get(drive_id)
        
        if not drive:
            return jsonify({'error': 'Drive not found'}), 404
        
        # Milestone 6: Verify drive is approved
        if drive.status != 'approved':
            return jsonify({'error': 'Drive not available for applications'}), 403
        
        # Milestone 6: Verify company is approved
        company = Company.query.get(drive.company_id)
        if not company or company.approval_status != 'approved':
            return jsonify({'error': 'Company not approved'}), 403

        if drive.application_deadline:
            deadline_aware = make_aware(drive.application_deadline)  # Convert to aware
            now = datetime.now(timezone.utc)  # Already aware
            if deadline_aware and deadline_aware <= now:  # ✅ Both are aware
                return jsonify({'error': 'Application deadline has passed'}), 403
        
        # Check if student already applied (Milestone 6: Prevent duplicates)
        existing_application = Application.query.filter_by(
            student_id=student.id,
            drive_id=drive_id
        ).first()
        
        drive_data = {
            'id': drive.id,
            'job_title': drive.job_title,
            'job_description': drive.job_description,
            'salary': drive.salary,
            'location': drive.location,
            'eligibility_criteria': drive.eligibility_criteria,
            'skills_required': drive.skills_required,
            'application_deadline': drive.application_deadline.isoformat() if drive.application_deadline else None,
            'company': {
                'id': company.id if company else None,
                'name': company.company_name if company else 'N/A',
                'industry': company.industry if company else 'N/A',
                'website': company.website if company else 'N/A'
            },
            'already_applied': existing_application is not None,
            'application_status': existing_application.status if existing_application else None,
            'application_id': existing_application.id if existing_application else None,
            'is_expired': False
        }
        
        return jsonify(drive_data), 200
    
    except Exception as e:
        current_app.logger.error(f"Get drive details error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': 'Failed to load drive details',
            'details': str(e) if current_app.debug else None
        }), 500

@student_bp.route('/drives/<int:drive_id>/apply', methods=['POST'])
@student_required
@invalidate_cache('ppa_v2:job_listings:*')  # ADD THIS DECORATOR - Invalidate cache on apply
def apply_to_drive(drive_id):
    """
    Apply for a placement drive
    Milestone 6: Prevent duplicate applications, ensure approved drives only
    """
    try:
        student = get_student_profile()
        
        if not student:
            return jsonify({'error': 'Student profile not found'}), 404
        
        # Check if student is eligible
        if not student.is_eligible:
            return jsonify({
                'error': 'You are not eligible to apply. Please contact admin.'
            }), 403
        
        # Get drive
        drive = Drive.query.get(drive_id)
        
        if not drive:
            return jsonify({'error': 'Drive not found'}), 404
        
        # Milestone 6: Verify drive is approved
        if drive.status != 'approved':
            return jsonify({'error': 'Drive not available for applications'}), 403
        
        # Milestone 6: Verify company is approved
        company = Company.query.get(drive.company_id)
        if not company or company.approval_status != 'approved':
            return jsonify({'error': 'Company not approved'}), 403
        
        if drive.application_deadline:
            deadline_aware = make_aware(drive.application_deadline)  # Convert to aware
            now = datetime.now(timezone.utc)  # Already aware
            if deadline_aware and deadline_aware <= now:  # ✅ Both are aware
                return jsonify({'error': 'Application deadline has passed'}), 403
        
        # Milestone 6: PREVENT DUPLICATE APPLICATIONS
        existing_application = Application.query.filter_by(
            student_id=student.id,
            drive_id=drive_id
        ).first()
        
        if existing_application:
            return jsonify({
                'error': 'You have already applied to this drive',
                'application_id': existing_application.id,
                'status': existing_application.status,
                'duplicate': True
            }), 400
        
        # Create application
        application = Application(
            student_id=student.id,
            drive_id=drive_id,
            status='applied',
            application_date=datetime.now(timezone.utc),
            resume_path=student.resume_path
        )
        
        db.session.add(application)
        db.session.commit()
        
        log_student_action(
            'application_submitted', 
            'application', 
            application.id,
            f'Applied to drive: {drive.job_title}'
        )
        
        return jsonify({
            'message': 'Application submitted successfully',
            'application_id': application.id,
            'drive_id': drive_id,
            'status': 'applied',
            'duplicate': False
        }), 201
    
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Apply to drive error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': 'Failed to submit application',
            'details': str(e) if current_app.debug else None
        }), 500


# ============================================================================
# APPLICATION HISTORY ENDPOINTS - MILESTONE 6
# ============================================================================

@student_bp.route('/applications', methods=['GET'])
@student_required
def get_student_applications():
    """
    View applied jobs with detailed application status
    Milestone 6: Complete application history with status tracking
    """
    try:
        student = get_student_profile()
        
        if not student:
            return jsonify({'error': 'Student profile not found'}), 404
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        per_page = min(per_page, 100)
        
        status = request.args.get('status', '')
        
        query = Application.query.filter_by(student_id=student.id)
        
        if status:
            query = query.filter(Application.status == status)
        
        applications = query.order_by(Application.application_date.desc()).paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        app_list = []
        for app in applications.items:
            drive = Drive.query.get(app.drive_id)
            company = Company.query.get(drive.company_id) if drive else None
            
            app_list.append({
                'id': app.id,
                'drive_id': app.drive_id,
                'job_title': drive.job_title if drive else 'N/A',
                'company_name': company.company_name if company else 'N/A',
                'company_id': drive.company_id if drive else None,
                'salary': drive.salary if drive else 'N/A',
                'location': drive.location if drive else 'N/A',
                'status': app.status,
                'application_date': app.application_date.isoformat() if app.application_date else None,
                'shortlisted_at': app.shortlisted_at.isoformat() if app.shortlisted_at else None,
                'interview_date': app.interview_date.isoformat() if app.interview_date else None,
                'feedback': app.feedback,
                'selected_at': app.selected_at.isoformat() if app.selected_at else None,
                'rejected_at': app.rejected_at.isoformat() if app.rejected_at else None
            })
        
        return jsonify({
            'applications': app_list,
            'total': applications.total,
            'pages': applications.pages,
            'current_page': page,
            'per_page': per_page,
            'has_next': applications.has_next,
            'has_prev': applications.has_prev
        }), 200
    
    except Exception as e:
        current_app.logger.error(f"Get student applications error: {str(e)}")
        return jsonify({
            'error': 'Failed to load applications',
            'details': str(e) if current_app.debug else None
        }), 500


@student_bp.route('/applications/<int:application_id>', methods=['GET'])
@student_required
def get_application_details(application_id):
    """Get detailed application information"""
    try:
        student = get_student_profile()
        
        if not student:
            return jsonify({'error': 'Student profile not found'}), 404
        
        # Verify ownership (Milestone 6: Students can view only their own records)
        app = Application.query.filter_by(
            id=application_id,
            student_id=student.id
        ).first()
        
        if not app:
            return jsonify({'error': 'Application not found'}), 404
        
        drive = Drive.query.get(app.drive_id)
        company = Company.query.get(drive.company_id) if drive else None
        
        application_data = {
            'id': app.id,
            'student': {
                'id': student.id,
                'name': student.full_name,
                'roll_number': student.roll_number,
                'branch': student.branch
            },
            'drive': {
                'id': drive.id if drive else None,
                'job_title': drive.job_title if drive else 'N/A',
                'job_description': drive.job_description if drive else 'N/A',
                'salary': drive.salary if drive else 'N/A',
                'location': drive.location if drive else 'N/A'
            },
            'company': {
                'id': company.id if company else None,
                'name': company.company_name if company else 'N/A',
                'industry': company.industry if company else 'N/A'
            },
            'status': app.status,
            'application_date': app.application_date.isoformat() if app.application_date else None,
            'shortlisted_at': app.shortlisted_at.isoformat() if app.shortlisted_at else None,
            'interview_scheduled_at': app.interview_scheduled_at.isoformat() if app.interview_scheduled_at else None,
            'interview_date': app.interview_date.isoformat() if app.interview_date else None,
            'feedback': app.feedback,
            'selected_at': app.selected_at.isoformat() if app.selected_at else None,
            'rejected_at': app.rejected_at.isoformat() if app.rejected_at else None,
            'resume_path': app.resume_path
        }
        
        return jsonify(application_data), 200
    
    except Exception as e:
        current_app.logger.error(f"Get application details error: {str(e)}")
        return jsonify({
            'error': 'Failed to load application details',
            'details': str(e) if current_app.debug else None
        }), 500


@student_bp.route('/history', methods=['GET'])
@student_required
def get_application_history():
    """
    Store and display complete application and placement history
    Milestone 6: Complete history tracking
    """
    try:
        student = get_student_profile()
        
        if not student:
            return jsonify({'error': 'Student profile not found'}), 404
        
        # Get all applications
        applications = Application.query.filter_by(
            student_id=student.id
        ).order_by(Application.application_date.desc()).all()
        
        # Get all placements
        placements = Placement.query.filter_by(
            student_id=student.id
        ).order_by(Placement.placement_date.desc()).all()
        
        history = {
            'applications': [],
            'placements': []
        }
        
        for app in applications:
            drive = Drive.query.get(app.drive_id)
            company = Company.query.get(drive.company_id) if drive else None
            
            history['applications'].append({
                'id': app.id,
                'job_title': drive.job_title if drive else 'N/A',
                'company_name': company.company_name if company else 'N/A',
                'status': app.status,
                'application_date': app.application_date.isoformat() if app.application_date else None,
                'feedback': app.feedback,
                'interview_date': app.interview_date.isoformat() if app.interview_date else None
            })
        
        for placement in placements:
            company = Company.query.get(placement.company_id)
            
            history['placements'].append({
                'id': placement.id,
                'company_name': company.company_name if company else 'N/A',
                'position': placement.position,
                'salary': placement.salary,
                'joining_date': placement.joining_date.isoformat() if placement.joining_date else None,
                'status': placement.status,
                'placement_date': placement.placement_date.isoformat() if placement.placement_date else None
            })
        
        return jsonify({
            'history': history,
            'total_applications': len(history['applications']),
            'total_placements': len(history['placements']),
            'student_id': student.id,
            'student_name': student.full_name,
            'roll_number': student.roll_number
        }), 200
    
    except Exception as e:
        current_app.logger.error(f"Get application history error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': 'Failed to load history',
            'details': str(e) if current_app.debug else None
        }), 500


# ============================================================================
# INTERVIEW SCHEDULE ENDPOINTS
# ============================================================================

@student_bp.route('/interviews', methods=['GET'])
@student_required
def get_student_interviews():
    """View interview schedules"""
    try:
        student = get_student_profile()
        
        if not student:
            return jsonify({'error': 'Student profile not found'}), 404
        
        applications = Application.query.filter_by(
            student_id=student.id,
            status='interview'
        ).order_by(Application.interview_date.desc()).all()
        
        interview_list = []
        for app in applications:
            drive = Drive.query.get(app.drive_id)
            company = Company.query.get(drive.company_id) if drive else None
            
            interview_list.append({
                'application_id': app.id,
                'job_title': drive.job_title if drive else 'N/A',
                'company_name': company.company_name if company else 'N/A',
                'interview_date': app.interview_date.isoformat() if app.interview_date else None,
                'feedback': app.feedback,
                'status': app.status
            })
        
        return jsonify({
            'interviews': interview_list,
            'total': len(interview_list)
        }), 200
    
    except Exception as e:
        current_app.logger.error(f"Get student interviews error: {str(e)}")
        return jsonify({
            'error': 'Failed to load interviews',
            'details': str(e) if current_app.debug else None
        }), 500


# ============================================================================
# PLACEMENT & OFFER LETTER ENDPOINTS
# ============================================================================

@student_bp.route('/placements', methods=['GET'])
@student_required
def get_student_placements():
    """View placement history"""
    try:
        student = get_student_profile()
        
        if not student:
            return jsonify({'error': 'Student profile not found'}), 404
        
        placements = Placement.query.filter_by(
            student_id=student.id
        ).order_by(Placement.placement_date.desc()).all()
        
        placement_list = []
        for placement in placements:
            company = Company.query.get(placement.company_id)
            drive = Drive.query.get(placement.drive_id)
            
            placement_list.append({
                'id': placement.id,
                'company_name': company.company_name if company else 'N/A',
                'position': placement.position,
                'salary': placement.salary,
                'joining_date': placement.joining_date.isoformat() if placement.joining_date else None,
                'status': placement.status,
                'placement_date': placement.placement_date.isoformat() if placement.placement_date else None,
                'offer_letter_path': placement.offer_letter_path
            })
        
        return jsonify({
            'placements': placement_list,
            'total': len(placement_list)
        }), 200
    
    except Exception as e:
        current_app.logger.error(f"Get student placements error: {str(e)}")
        return jsonify({
            'error': 'Failed to load placements',
            'details': str(e) if current_app.debug else None
        }), 500


@student_bp.route('/placements/<int:placement_id>/offer-letter', methods=['GET'])
@student_required
def download_offer_letter(placement_id):
    """Download offer letter or placement confirmation"""
    try:
        student = get_student_profile()
        
        if not student:
            return jsonify({'error': 'Student profile not found'}), 404
        
        placement = Placement.query.filter_by(
            id=placement_id,
            student_id=student.id
        ).first()
        
        if not placement:
            return jsonify({'error': 'Placement not found'}), 404
        
        company = Company.query.get(placement.company_id)
        drive = Drive.query.get(placement.drive_id)
        
        offer_data = {
            'student_name': student.full_name,
            'student_roll': student.roll_number,
            'company_name': company.company_name if company else 'N/A',
            'position': placement.position,
            'salary': placement.salary,
            'joining_date': placement.joining_date.isoformat() if placement.joining_date else 'TBD',
            'offer_date': placement.placement_date.isoformat() if placement.placement_date else None,
            'status': placement.status
        }
        
        return jsonify({
            'message': 'Offer letter generated',
            'offer_letter': offer_data
        }), 200
    
    except Exception as e:
        current_app.logger.error(f"Download offer letter error: {str(e)}")
        return jsonify({
            'error': 'Failed to generate offer letter',
            'details': str(e) if current_app.debug else None
        }), 500


@student_bp.route('/export/applications', methods=['POST'])
@student_required
def export_applications():
    """Trigger CSV export of application history"""
    import traceback
    from datetime import datetime, timezone
    from backend.services.csv_service import generate_application_csv
    import os
    
    try:
        current_app.logger.info("=== EXPORT APPLICATIONS API CALLED ===")
        
        student = get_student_profile()
        
        if not student:
            return jsonify({'error': 'Student profile not found'}), 404
        
        current_app.logger.info(f"Student: {student.full_name}")
        
        # Generate CSV
        csv_data, filename = generate_application_csv(
            user_id=current_user.id,
            user_role='student',
            student_id=student.id
        )
        
        current_app.logger.info(f"CSV generated: {filename}, Size: {len(csv_data)} bytes")
        
        # FIX: Save CSV file to project root static/exports/ (not backend/static/exports/)
        export_folder = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),  # Go up 3 levels to project root
            'static', 
            'exports'
        )
        os.makedirs(export_folder, exist_ok=True)
        
        timestamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
        filename_with_timestamp = f"{filename.split('.')[0]}_{timestamp}.csv"
        file_path = os.path.join(export_folder, filename_with_timestamp)
        
        current_app.logger.info(f"Saving to: {file_path}")
        
        with open(file_path, 'w', encoding='utf-8', newline='') as f:
            f.write(csv_data)
        
        current_app.logger.info(f"CSV saved successfully")
        
        download_url = f"/static/exports/{filename_with_timestamp}"
        
        # Send email (optional)
        email_sent = False
        try:
            from backend.tasks.exports import send_export_complete_email
            user = User.query.get(current_user.id)
            if user:
                email_sent = send_export_complete_email(
                    user=user,
                    filename=filename_with_timestamp,
                    download_url=download_url,
                    export_type='applications'
                )
                current_app.logger.info(f"Email sent: {email_sent}")
        except Exception as email_error:
            current_app.logger.warning(f"Failed to send email: {str(email_error)}")
            email_sent = False
        
        current_app.logger.info("=== EXPORT APPLICATIONS COMPLETED ===")
        
        return jsonify({
            'message': 'Export completed successfully.',
            'filename': filename_with_timestamp,
            'download_url': download_url,
            'email_sent': email_sent
        }), 200
    
    except Exception as e:
        current_app.logger.error(f"Export applications error: {str(e)}")
        current_app.logger.error(f"Traceback: {traceback.format_exc()}")
        traceback.print_exc()
        return jsonify({
            'error': 'Failed to export applications',
            'details': str(e) if current_app.debug else None,
            'traceback': traceback.format_exc() if current_app.debug else None
        }), 500


@student_bp.route('/export/placements', methods=['POST'])
@student_required
def export_placements():
    """Trigger CSV export of placement history"""
    import traceback
    from datetime import datetime, timezone
    from backend.services.csv_service import generate_placement_csv
    import os
    
    try:
        current_app.logger.info("=== EXPORT PLACEMENTS API CALLED ===")
        
        student = get_student_profile()
        
        if not student:
            return jsonify({'error': 'Student profile not found'}), 404
        
        current_app.logger.info(f"Student: {student.full_name}")
        
        # Generate CSV
        csv_data, filename = generate_placement_csv(
            user_id=current_user.id,
            user_role='student',
            student_id=student.id
        )
        
        current_app.logger.info(f"CSV generated: {filename}, Size: {len(csv_data)} bytes")
        
        # FIX: Save CSV file to project root static/exports/ (not backend/static/exports/)
        export_folder = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),  # Go up 3 levels to project root
            'static', 
            'exports'
        )
        os.makedirs(export_folder, exist_ok=True)
        
        timestamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
        filename_with_timestamp = f"{filename.split('.')[0]}_{timestamp}.csv"
        file_path = os.path.join(export_folder, filename_with_timestamp)
        
        current_app.logger.info(f"Saving to: {file_path}")
        
        with open(file_path, 'w', encoding='utf-8', newline='') as f:
            f.write(csv_data)
        
        current_app.logger.info(f"CSV saved successfully")
        
        download_url = f"/static/exports/{filename_with_timestamp}"
        
        # Send email (optional)
        email_sent = False
        try:
            from backend.tasks.exports import send_export_complete_email
            user = User.query.get(current_user.id)
            if user:
                email_sent = send_export_complete_email(
                    user=user,
                    filename=filename_with_timestamp,
                    download_url=download_url,
                    export_type='placements'
                )
                current_app.logger.info(f"Email sent: {email_sent}")
        except Exception as email_error:
            current_app.logger.warning(f"Failed to send email: {str(email_error)}")
            email_sent = False
        
        current_app.logger.info("=== EXPORT PLACEMENTS COMPLETED ===")
        
        return jsonify({
            'message': 'Export completed successfully.',
            'filename': filename_with_timestamp,
            'download_url': download_url,
            'email_sent': email_sent
        }), 200
    
    except Exception as e:
        current_app.logger.error(f"Export placements error: {str(e)}")
        current_app.logger.error(f"Traceback: {traceback.format_exc()}")
        traceback.print_exc()
        return jsonify({
            'error': 'Failed to export placements',
            'details': str(e) if current_app.debug else None,
            'traceback': traceback.format_exc() if current_app.debug else None
        }), 500