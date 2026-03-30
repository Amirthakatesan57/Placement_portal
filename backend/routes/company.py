"""
Company Dashboard and Job/Application Management API Endpoints
Milestone 4: Company Dashboard and Management

This module handles all company-related functionality including:
- Company profile management
- Placement drive creation and management
- Application review and status updates
- Interview scheduling
- Placement record creation

All endpoints require company authentication and admin approval.
"""

from flask import Blueprint, jsonify, request, current_app
from flask_login import login_required, current_user
from datetime import datetime, timezone, timedelta
from backend.auth.decorators import company_required, approved_company_required
from backend.extensions import db
from backend.models.user import User
from backend.models.company import Company
from backend.models.student import Student
from backend.models.drive import Drive
from backend.models.application import Application
from backend.models.placement import Placement
from backend.models.audit_log import AuditLog
from sqlalchemy import or_, and_
from backend.services.cache_service import cached, cache_service, invalidate_cache, CACHE_EXPIRY

# Create Blueprint for company routes
company_bp = Blueprint('company', __name__, url_prefix='/api/company')


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def log_company_action(action, entity_type, entity_id, details=None):
    """
    Helper function to log company actions for audit trail
    
    Args:
        action (str): Type of action performed
        entity_type (str): Type of entity affected (drive, application, etc.)
        entity_id (int): ID of the entity
        details (str, optional): Additional details about the action
    """
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


def get_company_profile():
    """
    Helper function to get current user's company profile
    
    Returns:
        Company: Company object or None
    """
    return Company.query.filter_by(user_id=current_user.id).first()


# COMPANY DASHBOARD ENDPOINTS

@company_bp.route('/dashboard/stats', methods=['GET'])
@approved_company_required
def get_company_dashboard_stats():
    """
    Get comprehensive dashboard statistics for company
    FIX: Count placements from Placement table
    """
    try:
        company = get_company_profile()
        
        if not company:
            return jsonify({'error': 'Company profile not found'}), 404
        
        drives = Drive.query.filter_by(company_id=company.id).all()
        drive_ids = [drive.id for drive in drives]
        
        applications = []
        if drive_ids:
            applications = Application.query.filter(Application.drive_id.in_(drive_ids)).all()
        
        # FIX: Get placements for this company
        placements = Placement.query.filter_by(company_id=company.id).all()
        
        total_drives = len(drives)
        active_drives = len([d for d in drives if d.status in ['approved', 'active']])
        closed_drives = len([d for d in drives if d.status == 'closed'])
        pending_drives = len([d for d in drives if d.status == 'pending'])
        total_applications = len(applications)
        shortlisted = len([a for a in applications if a.status == 'shortlisted'])
        selected = len([a for a in applications if a.status == 'selected'])
        rejected = len([a for a in applications if a.status == 'rejected'])
        pending = len([a for a in applications if a.status == 'applied'])
        interview = len([a for a in applications if a.status == 'interview'])
        
        # FIX: Use placement count
        total_placements = len(placements)
        
        stats = {
            'company_id': company.id,
            'company_name': company.company_name,
            'industry': company.industry,
            'location': company.location,
            'total_drives': total_drives,
            'active_drives': active_drives,
            'closed_drives': closed_drives,
            'pending_drives': pending_drives,
            'total_applications': total_applications,
            'shortlisted': shortlisted,
            'selected': selected,
            'rejected_applicants': rejected,
            'pending_applicants': pending,
            'interview_scheduled': interview,
            'total_placements': total_placements,  # FIX: From Placement table
            'approval_status': company.approval_status,
            'approved_at': company.approved_at.isoformat() if company.approved_at else None,
            'created_at': company.created_at.isoformat() if company.created_at else None
        }
        
        return jsonify(stats), 200
    
    except Exception as e:
        current_app.logger.error(f"Company dashboard stats error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Failed to load dashboard statistics'}), 500

# ============================================================================
# COMPANY PROFILE ENDPOINTS
# ============================================================================

@company_bp.route('/profile', methods=['GET'])
@company_required
def get_company_profile_endpoint():
    """
    Get company profile details
    
    Returns:
        JSON: Complete company profile information
    """
    try:
        company = get_company_profile()
        
        if not company:
            return jsonify({
                'error': 'Company profile not found',
                'needs_profile': True
            }), 404
        
        user = User.query.get(company.user_id)
        
        profile_data = {
            'id': company.id,
            'company_name': company.company_name,
            'industry': company.industry,
            'location': company.location,
            'website': company.website,
            'hr_contact_name': company.hr_contact_name,
            'hr_contact_email': company.hr_contact_email,
            'hr_contact_phone': company.hr_contact_phone,
            'company_description': company.company_description,
            'approval_status': company.approval_status,
            'approved_at': company.approved_at.isoformat() if company.approved_at else None,
            'approved_by': company.approved_by,
            'created_at': company.created_at.isoformat() if company.created_at else None,
            'updated_at': company.updated_at.isoformat() if company.updated_at else None,
            'user_email': user.email if user else None,
            'user_username': user.username if user else None
        }
        
        return jsonify(profile_data), 200
    
    except Exception as e:
        current_app.logger.error(f"Get company profile error: {str(e)}")
        return jsonify({
            'error': 'Failed to load company profile',
            'details': str(e) if current_app.debug else None
        }), 500


@company_bp.route('/profile', methods=['PUT'])
@company_required
def update_company_profile():
    """
    Update company profile details
    
    Milestone 4 Requirement: Companies will register their profile
    
    Returns:
        JSON: Success message and updated company ID
    """
    try:
        company = get_company_profile()
        
        if not company:
            return jsonify({
                'error': 'Company profile not found',
                'needs_profile': True
            }), 404
        
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Define allowed update fields
        update_fields = [
            'company_name', 'industry', 'location', 'website',
            'hr_contact_name', 'hr_contact_email', 'hr_contact_phone',
            'company_description'
        ]
        
        # Update allowed fields
        updated = False
        for field in update_fields:
            if field in data:
                setattr(company, field, data[field])
                updated = True
        
        if not updated:
            return jsonify({'error': 'No valid fields to update'}), 400
        
        company.updated_at = datetime.now(timezone.utc)
        db.session.commit()
        
        log_company_action(
            'profile_updated', 
            'company', 
            company.id,
            f'Updated company profile: {company.company_name}'
        )
        
        return jsonify({
            'message': 'Company profile updated successfully',
            'company_id': company.id,
            'company_name': company.company_name
        }), 200
    
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Update company profile error: {str(e)}")
        return jsonify({
            'error': 'Failed to update company profile',
            'details': str(e) if current_app.debug else None
        }), 500


# ============================================================================
# PLACEMENT DRIVE MANAGEMENT ENDPOINTS
# ============================================================================

@company_bp.route('/drives', methods=['GET'])
@approved_company_required
@cached('job_listings', expiry=CACHE_EXPIRY['job_listings'])  # ADD THIS DECORATOR
def get_company_drives():
    """
    Get all placement drives for this company
    
    Milestone 4 Requirement: Dashboard showing job postings
    
    Query Parameters:
        page (int): Page number for pagination (default: 1)
        per_page (int): Items per page (default: 10, max: 100)
        status (str): Filter by drive status
    
    Returns:
        JSON: Paginated list of company drives with statistics
    """
    try:
        company = get_company_profile()
        
        if not company:
            return jsonify({'error': 'Company profile not found'}), 404
        
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        per_page = min(per_page, 100)  # Limit max per_page
        
        # Get filter parameters
        status = request.args.get('status', '')
        
        # Build query
        query = Drive.query.filter_by(company_id=company.id)
        
        if status:
            query = query.filter(Drive.status == status)
        
        # Execute paginated query
        drives = query.order_by(Drive.created_at.desc()).paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        # Build drive list with statistics
        drive_list = []
        for drive in drives.items:
            application_count = Application.query.filter_by(drive_id=drive.id).count()
            shortlisted_count = Application.query.filter_by(
                drive_id=drive.id, 
                status='shortlisted'
            ).count()
            selected_count = Application.query.filter_by(
                drive_id=drive.id, 
                status='selected'
            ).count()
            
            drive_list.append({
                'id': drive.id,
                'job_title': drive.job_title,
                'job_description': drive.job_description,
                'salary': drive.salary,
                'location': drive.location,
                'eligibility_criteria': drive.eligibility_criteria,
                'skills_required': drive.skills_required,
                'application_deadline': drive.application_deadline.isoformat() 
                    if drive.application_deadline else None,
                'status': drive.status,
                'application_count': application_count,
                'shortlisted_count': shortlisted_count,
                'selected_count': selected_count,
                'created_at': drive.created_at.isoformat() 
                    if drive.created_at else None,
                'updated_at': drive.updated_at.isoformat() 
                    if drive.updated_at else None,
                'approved_at': drive.approved_at.isoformat() 
                    if drive.approved_at else None
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
        current_app.logger.error(f"Get company drives error: {str(e)}")
        return jsonify({
            'error': 'Failed to load drives',
            'details': str(e) if current_app.debug else None
        }), 500


@company_bp.route('/drives/<int:drive_id>', methods=['GET'])
@approved_company_required
def get_drive_details(drive_id):
    """
    Get detailed drive information
    
    Returns:
        JSON: Complete drive details with application statistics
    """
    try:
        company = get_company_profile()
        
        if not company:
            return jsonify({'error': 'Company profile not found'}), 404
        
        # Get drive and verify ownership
        drive = Drive.query.filter_by(
            id=drive_id, 
            company_id=company.id
        ).first()
        
        if not drive:
            return jsonify({'error': 'Drive not found'}), 404
        
        # Calculate application statistics
        application_count = Application.query.filter_by(drive_id=drive_id).count()
        shortlisted_count = Application.query.filter_by(
            drive_id=drive_id, 
            status='shortlisted'
        ).count()
        selected_count = Application.query.filter_by(
            drive_id=drive_id, 
            status='selected'
        ).count()
        rejected_count = Application.query.filter_by(
            drive_id=drive_id, 
            status='rejected'
        ).count()
        pending_count = Application.query.filter_by(
            drive_id=drive_id, 
            status='applied'
        ).count()
        interview_count = Application.query.filter_by(
            drive_id=drive_id, 
            status='interview'
        ).count()
        
        drive_data = {
            'id': drive.id,
            'job_title': drive.job_title,
            'job_description': drive.job_description,
            'salary': drive.salary,
            'location': drive.location,
            'eligibility_criteria': drive.eligibility_criteria,
            'skills_required': drive.skills_required,
            'application_deadline': drive.application_deadline.isoformat() 
                if drive.application_deadline else None,
            'status': drive.status,
            'application_count': application_count,
            'shortlisted_count': shortlisted_count,
            'selected_count': selected_count,
            'rejected_count': rejected_count,
            'pending_count': pending_count,
            'interview_count': interview_count,
            'created_at': drive.created_at.isoformat() 
                if drive.created_at else None,
            'updated_at': drive.updated_at.isoformat() 
                if drive.updated_at else None,
            'approved_at': drive.approved_at.isoformat() 
                if drive.approved_at else None,
            'approved_by': drive.approved_by
        }
        
        return jsonify(drive_data), 200
    
    except Exception as e:
        current_app.logger.error(f"Get drive details error: {str(e)}")
        return jsonify({
            'error': 'Failed to load drive details',
            'details': str(e) if current_app.debug else None
        }), 500

@company_bp.route('/drives/<int:drive_id>', methods=['PUT'])
@approved_company_required
def update_drive(drive_id):
    """
    Update placement drive details
    
    Note: Cannot update closed drives
    
    Returns:
        JSON: Success message and drive ID
    """
    try:
        company = get_company_profile()
        
        if not company:
            return jsonify({'error': 'Company profile not found'}), 404
        
        # Get drive and verify ownership
        drive = Drive.query.filter_by(
            id=drive_id, 
            company_id=company.id
        ).first()
        
        if not drive:
            return jsonify({'error': 'Drive not found'}), 404
        
        # Cannot update if drive is closed
        if drive.status == 'closed':
            return jsonify({
                'error': 'Cannot update closed drive'
            }), 400
        
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Define allowed update fields
        update_fields = [
            'job_title', 'job_description', 'salary', 'location',
            'eligibility_criteria', 'skills_required', 'application_deadline'
        ]
        
        # Update allowed fields
        for field in update_fields:
            if field in data:
                if field == 'salary':
                    try:
                        setattr(drive, field, float(data[field]))
                    except (ValueError, TypeError):
                        return jsonify({'error': f'Invalid {field} format'}), 400
                
                elif field == 'application_deadline':
                    try:
                        deadline_str = data[field]
                        if deadline_str.endswith('Z'):
                            deadline_str = deadline_str[:-1] + '+00:00'
                        setattr(drive, field, datetime.fromisoformat(deadline_str))
                    except (ValueError, TypeError):
                        return jsonify({'error': f'Invalid {field} format'}), 400
                
                else:
                    setattr(drive, field, data[field])
        
        drive.updated_at = datetime.now(timezone.utc)
        db.session.commit()
        
        log_company_action(
            'drive_updated', 
            'drive', 
            drive_id,
            f'Updated drive: {drive.job_title}'
        )
        
        return jsonify({
            'message': 'Drive updated successfully',
            'drive_id': drive.id,
            'job_title': drive.job_title
        }), 200
    
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Update drive error: {str(e)}")
        return jsonify({
            'error': 'Failed to update drive',
            'details': str(e) if current_app.debug else None
        }), 500


@company_bp.route('/drives/<int:drive_id>/status', methods=['PUT'])
@approved_company_required
def update_drive_status(drive_id):
    """
    Manage job posting status (Active/Closed)
    
    Milestone 4 Requirement: Manage job posting status
    
    Allowed Status Values:
        - active: Drive is open for applications
        - closed: Drive is closed for applications
    
    Returns:
        JSON: Success message and updated status
    """
    try:
        company = get_company_profile()
        
        if not company:
            return jsonify({'error': 'Company profile not found'}), 404
        
        # Get drive and verify ownership
        drive = Drive.query.filter_by(
            id=drive_id, 
            company_id=company.id
        ).first()
        
        if not drive:
            return jsonify({'error': 'Drive not found'}), 404
        
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        status = data.get('status')
        
        # Validate status
        if status not in ['active', 'closed']:
            return jsonify({
                'error': 'Invalid status. Must be active or closed',
                'valid_statuses': ['active', 'closed']
            }), 400
        
        # Can only close approved drives
        if drive.status != 'approved' and status == 'closed':
            return jsonify({
                'error': 'Can only close approved drives',
                'current_status': drive.status
            }), 400
        
        drive.status = status
        drive.updated_at = datetime.now(timezone.utc)
        db.session.commit()
        
        log_company_action(
            'drive_status_updated', 
            'drive', 
            drive_id,
            f'Drive status changed to {status}'
        )
        
        return jsonify({
            'message': f'Drive status updated to {status}',
            'drive_id': drive.id,
            'status': status,
            'job_title': drive.job_title
        }), 200
    
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Update drive status error: {str(e)}")
        return jsonify({
            'error': 'Failed to update drive status',
            'details': str(e) if current_app.debug else None
        }), 500


@company_bp.route('/drives/<int:drive_id>', methods=['DELETE'])
@approved_company_required
def delete_drive(drive_id):
    """
    Delete placement drive
    
    Note: Cannot delete drive with existing applications
    
    Returns:
        JSON: Success message and deleted drive ID
    """
    try:
        company = get_company_profile()
        
        if not company:
            return jsonify({'error': 'Company profile not found'}), 404
        
        # Get drive and verify ownership
        drive = Drive.query.filter_by(
            id=drive_id, 
            company_id=company.id
        ).first()
        
        if not drive:
            return jsonify({'error': 'Drive not found'}), 404
        
        # Cannot delete drive with applications
        application_count = Application.query.filter_by(
            drive_id=drive_id
        ).count()
        
        if application_count > 0:
            return jsonify({
                'error': 'Cannot delete drive with existing applications',
                'application_count': application_count,
                'note': 'Please close the drive or remove applications first'
            }), 400
        
        job_title = drive.job_title
        db.session.delete(drive)
        db.session.commit()
        
        log_company_action(
            'drive_deleted', 
            'drive', 
            drive_id,
            f'Deleted drive: {job_title}'
        )
        
        return jsonify({
            'message': 'Drive deleted successfully',
            'drive_id': drive_id,
            'job_title': job_title
        }), 200
    
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Delete drive error: {str(e)}")
        return jsonify({
            'error': 'Failed to delete drive',
            'details': str(e) if current_app.debug else None
        }), 500


# ============================================================================
# APPLICATION MANAGEMENT ENDPOINTS
# ============================================================================

@company_bp.route('/drives/<int:drive_id>/applications', methods=['GET'])
@approved_company_required
def get_drive_applications(drive_id):
    """
    View list of applicants for each job
    
    Milestone 4 Requirement: View list of applicants for each job
    
    Query Parameters:
        page (int): Page number for pagination
        per_page (int): Items per page
        status (str): Filter by application status
    
    Returns:
        JSON: Paginated list of applications with student details
    """
    try:
        company = get_company_profile()
        
        if not company:
            return jsonify({'error': 'Company profile not found'}), 404
        
        # Verify drive belongs to company
        drive = Drive.query.filter_by(
            id=drive_id, 
            company_id=company.id
        ).first()
        
        if not drive:
            return jsonify({'error': 'Drive not found'}), 404
        
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        per_page = min(per_page, 100)
        
        # Get filter parameters
        status = request.args.get('status', '')
        
        # Build query
        query = Application.query.filter_by(drive_id=drive_id)
        
        if status:
            query = query.filter(Application.status == status)
        
        # Execute paginated query
        applications = query.order_by(
            Application.application_date.desc()
        ).paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        # Build application list with student details
        app_list = []
        for app in applications.items:
            student = Student.query.get(app.student_id)
            user = User.query.get(student.user_id) if student else None
            
            app_list.append({
                'id': app.id,
                'student_id': app.student_id,
                'student_name': student.full_name if student else 'N/A',
                'student_roll': student.roll_number if student else 'N/A',
                'student_branch': student.branch if student else 'N/A',
                'student_cgpa': student.cgpa if student else 'N/A',
                'student_year': student.year_of_study if student else 'N/A',
                'student_email': user.email if user else 'N/A',
                'student_phone': student.phone if student else 'N/A',
                'student_skills': student.skills if student else 'N/A',
                'status': app.status,
                'application_date': app.application_date.isoformat() 
                    if app.application_date else None,
                'shortlisted_at': app.shortlisted_at.isoformat() 
                    if app.shortlisted_at else None,
                'interview_date': app.interview_date.isoformat() 
                    if app.interview_date else None,
                'feedback': app.feedback,
                'resume_path': app.resume_path
            })
        
        return jsonify({
            'applications': app_list,
            'total': applications.total,
            'pages': applications.pages,
            'current_page': page,
            'per_page': per_page,
            'has_next': applications.has_next,
            'has_prev': applications.has_prev,
            'drive_id': drive_id,
            'drive_title': drive.job_title
        }), 200
    
    except Exception as e:
        current_app.logger.error(f"Get drive applications error: {str(e)}")
        return jsonify({
            'error': 'Failed to load applications',
            'details': str(e) if current_app.debug else None
        }), 500

@company_bp.route('/applications', methods=['GET'])
@approved_company_required
# @cached('company_applications', expiry=CACHE_EXPIRY['default'])  # ADD THIS DECORATOR
def get_company_applications():
    """
    Get all applications for this company's drives - FIXES LOAD ERROR
    Returns all applications across all drives owned by this company
    """
    try:
        company = get_company_profile()
        
        if not company:
            return jsonify({'error': 'Company profile not found'}), 404
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        per_page = min(per_page, 100)
        
        status = request.args.get('status', '')
        
        # Get all drives for this company
        drives = Drive.query.filter_by(company_id=company.id).all()
        drive_ids = [drive.id for drive in drives]
        
        # If company has no drives, return empty list (NOT an error)
        if not drive_ids:
            return jsonify({
                'applications': [],
                'total': 0,
                'pages': 0,
                'current_page': page,
                'per_page': per_page,
                'has_next': False,
                'has_prev': False
            }), 200
        
        # Get all applications for this company's drives
        query = Application.query.filter(Application.drive_id.in_(drive_ids))
        
        if status:
            query = query.filter(Application.status == status)
        
        applications = query.order_by(Application.application_date.desc()).paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        app_list = []
        for app in applications.items:
            student = Student.query.get(app.student_id)
            drive = Drive.query.get(app.drive_id)
            user = User.query.get(student.user_id) if student else None
            
            app_list.append({
                'id': app.id,
                'student_id': app.student_id,
                'student_name': student.full_name if student else 'N/A',
                'student_roll': student.roll_number if student else 'N/A',
                'student_branch': student.branch if student else 'N/A',
                'student_cgpa': student.cgpa if student else 'N/A',
                'student_email': user.email if user else 'N/A',
                'student_phone': student.phone if student else 'N/A',
                'drive_id': app.drive_id,
                'drive_title': drive.job_title if drive else 'N/A',
                'company_id': company.id,
                'company_name': company.company_name,
                'status': app.status,
                'application_date': app.application_date.isoformat() if app.application_date else None,
                'interview_date': app.interview_date.isoformat() if app.interview_date else None,
                'feedback': app.feedback
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
        current_app.logger.error(f"Get company applications error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': 'Failed to load applications',
            'details': str(e) if current_app.debug else None
        }), 500


@company_bp.route('/applications/<int:application_id>', methods=['GET'])
@approved_company_required
def get_application_details(application_id):
    """
    Get detailed application information
    
    Returns:
        JSON: Complete application details with student and drive information
    """
    try:
        company = get_company_profile()
        
        if not company:
            return jsonify({'error': 'Company profile not found'}), 404
        
        # Get application
        app = Application.query.get(application_id)
        
        if not app:
            return jsonify({'error': 'Application not found'}), 404
        
        # Verify this application belongs to company's drive
        drive = Drive.query.get(app.drive_id)
        
        if not drive or drive.company_id != company.id:
            return jsonify({'error': 'Access denied'}), 403
        
        # Get student details
        student = Student.query.get(app.student_id)
        user = User.query.get(student.user_id) if student else None
        
        application_data = {
            'id': app.id,
            'student': {
                'id': student.id if student else None,
                'full_name': student.full_name if student else 'N/A',
                'roll_number': student.roll_number if student else 'N/A',
                'branch': student.branch if student else 'N/A',
                'cgpa': student.cgpa if student else 'N/A',
                'year_of_study': student.year_of_study if student else 'N/A',
                'email': user.email if user else 'N/A',
                'phone': student.phone if student else 'N/A',
                'skills': student.skills if student else 'N/A',
                'education_details': student.education_details if student else 'N/A',
                'experience_details': student.experience_details if student else 'N/A',
                'resume_path': student.resume_path if student else None
            },
            'drive': {
                'id': drive.id if drive else None,
                'job_title': drive.job_title if drive else 'N/A',
                'company_name': company.company_name,
                'salary': drive.salary if drive else 'N/A',
                'location': drive.location if drive else 'N/A'
            },
            'status': app.status,
            'application_date': app.application_date.isoformat() 
                if app.application_date else None,
            'shortlisted_at': app.shortlisted_at.isoformat() 
                if app.shortlisted_at else None,
            'interview_scheduled_at': app.interview_scheduled_at.isoformat() 
                if app.interview_scheduled_at else None,
            'interview_date': app.interview_date.isoformat() 
                if app.interview_date else None,
            'feedback': app.feedback,
            'selected_at': app.selected_at.isoformat() 
                if app.selected_at else None,
            'rejected_at': app.rejected_at.isoformat() 
                if app.rejected_at else None,
            'resume_path': app.resume_path
        }
        
        return jsonify(application_data), 200
    
    except Exception as e:
        current_app.logger.error(f"Get application details error: {str(e)}")
        return jsonify({
            'error': 'Failed to load application details',
            'details': str(e) if current_app.debug else None
        }), 500

@company_bp.route('/applications/<int:application_id>/status', methods=['PUT'])
@approved_company_required
def update_application_status(application_id):
    """
    Update application status (Shortlist/Reject/Select)
    FIX: Create Placement record when status = selected
    """
    try:
        company = get_company_profile()
        
        if not company:
            return jsonify({'error': 'Company profile not found'}), 404
        
        app = Application.query.get(application_id)
        
        if not app:
            return jsonify({'error': 'Application not found'}), 404
        
        # Verify this application belongs to company's drive
        drive = Drive.query.get(app.drive_id)
        
        if not drive or drive.company_id != company.id:
            return jsonify({'error': 'Access denied'}), 403
        
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        status = data.get('status')
        feedback = data.get('feedback', '')
        interview_date = data.get('interview_date')
        
        valid_statuses = ['applied', 'shortlisted', 'interview', 'selected', 'rejected']
        
        if status not in valid_statuses:
            return jsonify({
                'error': f'Invalid status',
                'valid_statuses': valid_statuses,
                'provided_status': status
            }), 400
        
        # Store old status to check if we need to create placement
        old_status = app.status
        app.status = status
        
        now = datetime.now(timezone.utc)
        
        if status == 'shortlisted':
            app.shortlisted_at = now
        elif status == 'selected':
            app.selected_at = now
            
            # FIX: Create Placement record when status changes to selected
            if old_status != 'selected':
                # Check if placement already exists
                existing_placement = Placement.query.filter_by(
                    application_id=application_id
                ).first()
                
                if not existing_placement:
                    placement = Placement(
                        application_id=application_id,
                        student_id=app.student_id,
                        company_id=company.id,
                        drive_id=drive.id,
                        position=drive.job_title,
                        salary=drive.salary,
                        joining_date=None,
                        status='offered',
                        placement_date=now
                    )
                    db.session.add(placement)
                    current_app.logger.info(f"Placement created for student {app.student_id}")
                    
        elif status == 'rejected':
            app.rejected_at = now
        
        if interview_date:
            try:
                interview_str = interview_date
                if interview_str.endswith('Z'):
                    interview_str = interview_str[:-1] + '+00:00'
                app.interview_date = datetime.fromisoformat(interview_str)
                app.interview_scheduled_at = now
            except (ValueError, TypeError):
                return jsonify({'error': 'Invalid interview date format'}), 400
        
        if feedback:
            app.feedback = feedback
        
        db.session.commit()
        
        log_company_action(
            'application_status_updated', 
            'application', 
            application_id,
            f'Updated application {application_id} status to {status}'
        )
        
        return jsonify({
            'message': 'Application status updated successfully',
            'application_id': application_id,
            'status': status,
            'student_id': app.student_id,
            'drive_id': app.drive_id,
            'placement_created': status == 'selected' and old_status != 'selected',
            'updated_at': now.isoformat()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Update application status error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': 'Failed to update application status',
            'details': str(e) if current_app.debug else None
        }), 500

@company_bp.route('/applications/<int:application_id>/interview', methods=['POST'])
@approved_company_required
def schedule_interview(application_id):
    """
    Schedule interviews with shortlisted candidates
    
    Milestone 4 Requirement: Schedule interviews with shortlisted candidates
    
    Required Fields:
        interview_date (ISO 8601 format)
    
    Optional Fields:
        interview_type (default: In-Person)
        interview_location
    
    Returns:
        JSON: Success message and interview details
    """
    try:
        company = get_company_profile()
        
        if not company:
            return jsonify({'error': 'Company profile not found'}), 404
        
        # Get application
        app = Application.query.get(application_id)
        
        if not app:
            return jsonify({'error': 'Application not found'}), 404
        
        # Verify this application belongs to company's drive
        drive = Drive.query.get(app.drive_id)
        
        if not drive or drive.company_id != company.id:
            return jsonify({'error': 'Access denied'}), 403
        
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        interview_date = data.get('interview_date')
        interview_type = data.get('interview_type', 'In-Person')
        interview_location = data.get('interview_location', '')
        
        # Validate interview date
        if not interview_date:
            return jsonify({'error': 'Interview date is required'}), 400
        
        try:
            interview_str = interview_date
            if interview_str.endswith('Z'):
                interview_str = interview_str[:-1] + '+00:00'
            
            interview_datetime = datetime.fromisoformat(interview_str)
            
            if interview_datetime <= datetime.now(timezone.utc):
                return jsonify({
                    'error': 'Interview date must be in the future'
                }), 400
                
        except (ValueError, TypeError) as e:
            return jsonify({
                'error': 'Invalid interview date format. Use ISO 8601 format',
                'details': str(e) if current_app.debug else None
            }), 400
        
        # Update application
        app.interview_date = interview_datetime
        app.interview_scheduled_at = datetime.now(timezone.utc)
        app.status = 'interview'
        
        # Build feedback message
        feedback_msg = f'Interview scheduled: {interview_type}'
        feedback_msg += f' on {interview_datetime.strftime("%Y-%m-%d %H:%M")}'
        
        if interview_location:
            feedback_msg += f' at {interview_location}'
        
        app.feedback = feedback_msg
        
        db.session.commit()
        
        log_company_action(
            'interview_scheduled', 
            'application', 
            application_id,
            f'Scheduled interview for {interview_datetime}'
        )
        
        return jsonify({
            'message': 'Interview scheduled successfully',
            'application_id': application_id,
            'interview_date': interview_datetime.isoformat(),
            'interview_type': interview_type,
            'interview_location': interview_location,
            'student_id': app.student_id,
            'drive_id': app.drive_id
        }), 200
    
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Schedule interview error: {str(e)}")
        return jsonify({
            'error': 'Failed to schedule interview',
            'details': str(e) if current_app.debug else None
        }), 500


# ============================================================================
# PLACEMENT MANAGEMENT ENDPOINTS
# ============================================================================

@company_bp.route('/applications/<int:application_id>/placement', methods=['POST'])
@approved_company_required
def create_placement(application_id):
    """
    Create placement record for selected student
    
    Prerequisites:
        - Application must be in 'selected' status
    
    Returns:
        JSON: Success message and placement ID
    """
    try:
        company = get_company_profile()
        
        if not company:
            return jsonify({'error': 'Company profile not found'}), 404
        
        # Get application
        app = Application.query.get(application_id)
        
        if not app:
            return jsonify({'error': 'Application not found'}), 404
        
        # Verify this application belongs to company's drive
        drive = Drive.query.get(app.drive_id)
        
        if not drive or drive.company_id != company.id:
            return jsonify({'error': 'Access denied'}), 403
        
        # Application must be selected
        if app.status != 'selected':
            return jsonify({
                'error': 'Application must be in selected status',
                'current_status': app.status
            }), 400
        
        # Check if placement already exists
        existing_placement = Placement.query.filter_by(
            application_id=application_id
        ).first()
        
        if existing_placement:
            return jsonify({
                'error': 'Placement already exists for this application',
                'placement_id': existing_placement.id
            }), 400
        
        data = request.get_json()
        
        # Create placement record
        placement = Placement(
            application_id=application_id,
            student_id=app.student_id,
            company_id=company.id,
            drive_id=drive.id,
            position=drive.job_title,
            salary=drive.salary,
            joining_date=data.get('joining_date'),
            status='offered',
            placement_date=datetime.now(timezone.utc)
        )
        
        db.session.add(placement)
        db.session.commit()
        
        log_company_action(
            'placement_created', 
            'placement', 
            placement.id,
            f'Created placement for student {app.student_id}'
        )
        
        return jsonify({
            'message': 'Placement record created successfully',
            'placement_id': placement.id,
            'student_id': app.student_id,
            'company_id': company.id,
            'position': drive.job_title,
            'salary': drive.salary
        }), 201
    
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Create placement error: {str(e)}")
        return jsonify({
            'error': 'Failed to create placement',
            'details': str(e) if current_app.debug else None
        }), 500

@company_bp.route('/placements', methods=['GET'])
@approved_company_required
def get_company_placements():
    """
    Get all placements for this company
    FIX: Return actual placement data from Placement table
    """
    try:
        company = get_company_profile()
        
        if not company:
            return jsonify({'error': 'Company profile not found'}), 404
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        per_page = min(per_page, 100)
        
        # Get all placements for this company
        placements = Placement.query.filter_by(
            company_id=company.id
        ).order_by(
            Placement.placement_date.desc()
        ).paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        placement_list = []
        for placement in placements.items:
            student = Student.query.get(placement.student_id)
            drive = Drive.query.get(placement.drive_id)
            
            placement_list.append({
                'id': placement.id,
                'student_id': placement.student_id,
                'student_name': student.full_name if student else 'N/A',
                'student_roll': student.roll_number if student else 'N/A',
                'student_branch': student.branch if student else 'N/A',
                'student_cgpa': student.cgpa if student else 'N/A',
                'drive_id': placement.drive_id,
                'drive_title': drive.job_title if drive else 'N/A',
                'position': placement.position,
                'salary': placement.salary,
                'joining_date': placement.joining_date.isoformat() if placement.joining_date else None,
                'status': placement.status,
                'placement_date': placement.placement_date.isoformat() if placement.placement_date else None,
                'offer_letter_path': placement.offer_letter_path
            })
        
        return jsonify({
            'placements': placement_list,
            'total': placements.total,
            'pages': placements.pages,
            'current_page': page,
            'per_page': per_page,
            'has_next': placements.has_next,
            'has_prev': placements.has_prev,
            'company_id': company.id,
            'company_name': company.company_name
        }), 200
    
    except Exception as e:
        current_app.logger.error(f"Get company placements error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': 'Failed to load placements',
            'details': str(e) if current_app.debug else None
        }), 500

@company_bp.route('/drives', methods=['POST'])
@approved_company_required
@invalidate_cache('ppa_v2:job_listings:*')  # ADD THIS - Invalidate on create
@invalidate_cache('ppa_v2:dashboard_stats:*')
def create_drive():
    """
    Create new placement drive
    Milestone 6: Ensure only approved companies can create placement drives
    """
    try:
        company = get_company_profile()
        
        if not company:
            return jsonify({'error': 'Company profile not found'}), 404
        
        # Milestone 6: Verify company is approved
        if company.approval_status != 'approved':
            return jsonify({
                'error': 'Company must be approved by admin before creating drives',
                'approval_status': company.approval_status
            }), 403
        
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        required_fields = [
            'job_title', 'job_description', 'salary', 
            'location', 'eligibility_criteria', 'application_deadline'
        ]
        
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        try:
            salary = float(data['salary'])
            if salary <= 0:
                return jsonify({'error': 'Salary must be positive'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid salary format'}), 400
        
        try:
            deadline_str = data['application_deadline']
            if deadline_str.endswith('Z'):
                deadline_str = deadline_str[:-1] + '+00:00'
            deadline = datetime.fromisoformat(deadline_str)
            
            if deadline <= datetime.now(timezone.utc):
                return jsonify({'error': 'Application deadline must be in the future'}), 400
        except (ValueError, TypeError) as e:
            return jsonify({'error': 'Invalid deadline format'}), 400
        
        drive = Drive(
            company_id=company.id,
            job_title=data['job_title'],
            job_description=data['job_description'],
            salary=salary,
            location=data['location'],
            eligibility_criteria=data['eligibility_criteria'],
            skills_required=data.get('skills_required', ''),
            application_deadline=deadline,
            status='pending',  # Requires admin approval
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        
        db.session.add(drive)
        db.session.commit()
        
        log_company_action('drive_created', 'drive', drive.id, 
                          f'Created drive: {drive.job_title}')
        
        return jsonify({
            'message': 'Drive created successfully. Pending admin approval.',
            'drive_id': drive.id,
            'job_title': drive.job_title,
            'status': drive.status
        }), 201
    
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Create drive error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': 'Failed to create drive',
            'details': str(e) if current_app.debug else None
        }), 500

@company_bp.route('/export/applications', methods=['POST'])
@approved_company_required
def export_applications():
    """Trigger CSV export of application history"""
    import traceback
    from datetime import datetime, timezone
    from backend.services.csv_service import generate_application_csv
    import os
    
    try:
        current_app.logger.info("=== EXPORT APPLICATIONS API CALLED ===")
        
        company = get_company_profile()
        
        if not company:
            return jsonify({'error': 'Company profile not found'}), 404
        
        current_app.logger.info(f"Company: {company.company_name}")
        
        # Generate CSV
        csv_data, filename = generate_application_csv(
            user_id=current_user.id,
            user_role='company',
            company_id=company.id
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


@company_bp.route('/export/placements', methods=['POST'])
@approved_company_required
def export_placements():
    """Trigger CSV export of placement history"""
    import traceback
    from datetime import datetime, timezone
    from backend.services.csv_service import generate_placement_csv
    import os
    
    try:
        current_app.logger.info("=== EXPORT PLACEMENTS API CALLED ===")
        
        company = get_company_profile()
        
        if not company:
            return jsonify({'error': 'Company profile not found'}), 404
        
        current_app.logger.info(f"Company: {company.company_name}")
        
        # Generate CSV
        csv_data, filename = generate_placement_csv(
            user_id=current_user.id,
            user_role='company',
            company_id=company.id
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