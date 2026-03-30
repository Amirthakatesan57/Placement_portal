"""
Admin Dashboard and Management API Endpoints
Milestone 3: Admin Dashboard and Management
"""

from flask import Blueprint, jsonify, request, current_app
from flask_login import login_required, current_user
from datetime import datetime, timezone
from backend.auth.decorators import admin_required
from backend.extensions import db
from backend.models.user import User
from backend.models.company import Company
from backend.models.student import Student
from backend.models.drive import Drive
from backend.models.application import Application
from backend.models.placement import Placement
from backend.models.audit_log import AuditLog
from sqlalchemy import or_
from backend.services.cache_service import cached, cache_service, invalidate_cache, CACHE_EXPIRY

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

def log_admin_action(action, entity_type, entity_id, details=None):
    """Helper function to log admin actions for audit trail"""
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

# ==================== DASHBOARD STATISTICS ====================
@admin_bp.route('/dashboard/stats', methods=['GET'])
@admin_required
@cached('dashboard_stats', expiry=CACHE_EXPIRY['admin_stats'])  # ADD THIS DECORATOR
def get_dashboard_stats():
    """
    Get dashboard statistics for admin
    Milestone 3: Admin Dashboard
    Milestone 8: Cached for performance
    """
    try:
        total_students = User.query.filter_by(role='student').count()
        total_companies = User.query.filter_by(role='company').count()
        total_drives = Drive.query.count()
        total_applications = Application.query.count()
        
        # Count actual placements from Placement table
        total_placements = Placement.query.count()
        
        pending_companies = Company.query.filter_by(approval_status='pending').count()
        pending_drives = Drive.query.filter_by(status='pending').count()
        active_drives = Drive.query.filter_by(status='approved').count()
        blacklisted_users = User.query.filter_by(is_blacklisted=True).count()
        
        # Count placed students
        placed_students = db.session.query(Placement.student_id).distinct().count()
        
        stats = {
            'total_students': total_students,
            'total_companies': total_companies,
            'total_drives': total_drives,
            'total_applications': total_applications,
            'total_placements': total_placements,
            'placed_students': placed_students,
            'pending_companies': pending_companies,
            'pending_drives': pending_drives,
            'active_drives': active_drives,
            'blacklisted_users': blacklisted_users
        }
        
        return jsonify(stats), 200
    except Exception as e:
        current_app.logger.error(f"Dashboard stats error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Failed to load dashboard statistics'}), 500

# ==================== COMPANY MANAGEMENT ====================

@admin_bp.route('/companies', methods=['GET'])
@admin_required
@cached('company_search', expiry=CACHE_EXPIRY['company_search'])  # ADD THIS DECORATOR
def get_all_companies():
    """
    Search and list all companies with pagination
    Milestone 3 Requirement: Search companies (by name/industry)
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '')
        status = request.args.get('status', '')
        industry = request.args.get('industry', '')
        
        query = Company.query
        
        # Search by company name or industry
        if search:
            query = query.filter(
                or_(
                    Company.company_name.ilike(f'%{search}%'),
                    Company.industry.ilike(f'%{search}%')
                )
            )
        
        # Filter by approval status
        if status:
            query = query.filter(Company.approval_status == status)
        
        # Filter by industry
        if industry:
            query = query.filter(Company.industry.ilike(f'%{industry}%'))
        
        companies = query.order_by(Company.created_at.desc()).paginate(
            page=page, per_page=min(per_page, 100), error_out=False
        )
        
        company_list = []
        for company in companies.items:
            user = User.query.get(company.user_id)
            company_list.append({
                'id': company.id,
                'company_name': company.company_name,
                'industry': company.industry,
                'location': company.location,
                'website': company.website,
                'approval_status': company.approval_status,
                'approved_at': company.approved_at.isoformat() if company.approved_at else None,
                'username': user.username if user else 'N/A',
                'email': user.email if user else 'N/A',
                'is_blacklisted': user.is_blacklisted if user else False,
                'is_active': user.is_active if user else False,
                'created_at': company.created_at.isoformat() if company.created_at else None
            })
        
        return jsonify({
            'companies': company_list,
            'total': companies.total,
            'pages': companies.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
    except Exception as e:
        current_app.logger.error(f"Get companies error: {str(e)}")
        return jsonify({'error': 'Failed to load companies'}), 500

@admin_bp.route('/companies/<int:company_id>', methods=['GET'])
@admin_required
def get_company_details(company_id):
    """Get detailed company information"""
    try:
        company = Company.query.get_or_404(company_id)
        user = User.query.get(company.user_id)
        drives = Drive.query.filter_by(company_id=company_id).count()
        
        return jsonify({
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
            'username': user.username if user else 'N/A',
            'email': user.email if user else 'N/A',
            'is_blacklisted': user.is_blacklisted if user else False,
            'drive_count': drives
        }), 200
    except Exception as e:
        current_app.logger.error(f"Get company details error: {str(e)}")
        return jsonify({'error': 'Failed to load company details'}), 500

@admin_bp.route('/companies/<int:company_id>/blacklist', methods=['POST'])
@admin_required
def blacklist_company(company_id):
    """
    Blacklist a company
    Milestone 3: Admin can blacklist companies
    Milestone 8: Invalidate cache after blacklist
    """
    try:
        from backend.services.cache_service import cache_service
        
        company = Company.query.get(company_id)
        
        if not company:
            return jsonify({'error': 'Company not found'}), 404
        
        # Update company status
        company.approval_status = 'blacklisted'
        company.is_blacklisted = True  # Ensure this field exists
        
        # Commit to database
        db.session.commit()
        
        # INVALIDATE CACHE - Clear company-related cache
        if cache_service and cache_service.enabled:
            cache_service.delete_pattern('ppa_v2:*company*')
            cache_service.delete_pattern('ppa_v2:dashboard_stats:*')
            cache_service.delete_pattern('ppa_v2:company_search:*')
        
        # Log the action
        audit_log = AuditLog(
            user_id=current_user.id,
            action='company_blacklisted',
            entity_type='company',
            entity_id=company_id,
            details=f'Company {company.company_name} blacklisted by admin',
            timestamp=datetime.now(timezone.utc)
        )
        db.session.add(audit_log)
        db.session.commit()
        
        current_app.logger.info(f"Company {company_id} blacklisted by admin {current_user.username}")
        
        return jsonify({
            'message': 'Company blacklisted successfully',
            'company_id': company_id,
            'status': 'blacklisted'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Blacklist company error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': 'Failed to blacklist company',
            'details': str(e) if current_app.debug else None
        }), 500


@admin_bp.route('/companies/<int:company_id>/unblacklist', methods=['POST'])
@admin_required
def unblacklist_company(company_id):
    """
    Remove company from blacklist
    Milestone 3: Admin can restore blacklisted companies
    Milestone 8: Invalidate cache after unblacklist
    """
    try:
        from backend.services.cache_service import cache_service
        
        company = Company.query.get(company_id)
        
        if not company:
            return jsonify({'error': 'Company not found'}), 404
        
        # Update company status
        company.approval_status = 'approved'
        company.is_blacklisted = False
        
        # Commit to database
        db.session.commit()
        
        # INVALIDATE CACHE - Clear company-related cache
        if cache_service and cache_service.enabled:
            cache_service.delete_pattern('ppa_v2:*company*')
            cache_service.delete_pattern('ppa_v2:dashboard_stats:*')
            cache_service.delete_pattern('ppa_v2:company_search:*')
        
        # Log the action
        audit_log = AuditLog(
            user_id=current_user.id,
            action='company_unblacklisted',
            entity_type='company',
            entity_id=company_id,
            details=f'Company {company.company_name} restored from blacklist',
            timestamp=datetime.now(timezone.utc)
        )
        db.session.add(audit_log)
        db.session.commit()
        
        current_app.logger.info(f"Company {company_id} unblacklisted by admin {current_user.username}")
        
        return jsonify({
            'message': 'Company restored successfully',
            'company_id': company_id,
            'status': 'approved'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Unblacklist company error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': 'Failed to restore company',
            'details': str(e) if current_app.debug else None
        }), 500


@admin_bp.route('/companies/<int:company_id>/approve', methods=['POST'])
@admin_required
def approve_company(company_id):
    """
    Approve company registration
    Milestone 3: Admin can approve companies
    Milestone 8: Invalidate cache after approval
    """
    try:
        from backend.services.cache_service import cache_service
        
        company = Company.query.get(company_id)
        
        if not company:
            return jsonify({'error': 'Company not found'}), 404
        
        # Update company status
        company.approval_status = 'approved'
        company.approved_at = datetime.now(timezone.utc)
        company.approved_by = current_user.id
        
        # Commit to database
        db.session.commit()
        
        # INVALIDATE CACHE - Clear company-related cache
        if cache_service and cache_service.enabled:
            cache_service.delete_pattern('ppa_v2:*company*')
            cache_service.delete_pattern('ppa_v2:dashboard_stats:*')
            cache_service.delete_pattern('ppa_v2:company_search:*')
        
        # Log the action
        audit_log = AuditLog(
            user_id=current_user.id,
            action='company_approved',
            entity_type='company',
            entity_id=company_id,
            details=f'Company {company.company_name} approved by admin',
            timestamp=datetime.now(timezone.utc)
        )
        db.session.add(audit_log)
        db.session.commit()
        
        current_app.logger.info(f"Company {company_id} approved by admin {current_user.username}")
        
        return jsonify({
            'message': 'Company approved successfully',
            'company_id': company_id,
            'status': 'approved'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Approve company error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': 'Failed to approve company',
            'details': str(e) if current_app.debug else None
        }), 500


@admin_bp.route('/companies/<int:company_id>/reject', methods=['POST'])
@admin_required
def reject_company(company_id):
    """
    Reject a company registration
    Milestone 3 Requirement: Remove Company profiles
    """
    try:
        company = Company.query.get_or_404(company_id)
        
        if company.approval_status == 'rejected':
            return jsonify({'error': 'Company already rejected'}), 400
        
        company.approval_status = 'rejected'
        
        db.session.commit()
        log_admin_action('company_rejected', 'company', company_id,
                        f'Rejected company: {company.company_name}')
        
        current_app.logger.info(f"Company {company_id} rejected by admin {current_user.id}")
        
        return jsonify({
            'message': 'Company rejected successfully',
            'company_id': company_id
        }), 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Reject company error: {str(e)}")
        return jsonify({'error': 'Failed to reject company'}), 500

@admin_bp.route('/companies/<int:company_id>/remove', methods=['DELETE'])
@admin_required
def remove_company(company_id):
    """
    Remove/Delete a company permanently
    Milestone 3 Requirement: Remove Company profiles
    """
    try:
        company = Company.query.get_or_404(company_id)
        user = User.query.get(company.user_id)
        
        company_name = company.company_name
        
        # Delete company (cascade will handle related drives)
        db.session.delete(company)
        
        # Optionally delete user account too
        if user:
            db.session.delete(user)
        
        db.session.commit()
        log_admin_action('company_removed', 'company', company_id,
                        f'Removed company: {company_name}')
        
        current_app.logger.info(f"Company {company_id} removed by admin {current_user.id}")
        
        return jsonify({
            'message': 'Company removed successfully',
            'company_id': company_id
        }), 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Remove company error: {str(e)}")
        return jsonify({'error': 'Failed to remove company'}), 500

# ==================== STUDENT MANAGEMENT ====================

@admin_bp.route('/students', methods=['GET'])
@admin_required
def get_all_students():
    """
    Search and list all students with pagination
    Milestone 3 Requirement: Search students (by name/ID/contact)
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '')
        branch = request.args.get('branch', '')
        
        query = Student.query
        
        # Search by name, roll number, or contact
        if search:
            query = query.filter(
                or_(
                    Student.full_name.ilike(f'%{search}%'),
                    Student.roll_number.ilike(f'%{search}%'),
                    Student.phone.ilike(f'%{search}%')
                )
            )
        
        # Filter by branch
        if branch:
            query = query.filter(Student.branch.ilike(f'%{branch}%'))
        
        students = query.order_by(Student.created_at.desc()).paginate(
            page=page, per_page=min(per_page, 100), error_out=False
        )
        
        student_list = []
        for student in students.items:
            user = User.query.get(student.user_id)
            student_list.append({
                'id': student.id,
                'full_name': student.full_name,
                'roll_number': student.roll_number,
                'branch': student.branch,
                'year_of_study': student.year_of_study,
                'cgpa': student.cgpa,
                'phone': student.phone,
                'email': user.email if user else 'N/A',
                'is_eligible': student.is_eligible,
                'is_blacklisted': user.is_blacklisted if user else False,
                'is_active': user.is_active if user else False,
                'created_at': student.created_at.isoformat() if student.created_at else None
            })
        
        return jsonify({
            'students': student_list,
            'total': students.total,
            'pages': students.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
    except Exception as e:
        current_app.logger.error(f"Get students error: {str(e)}")
        return jsonify({'error': 'Failed to load students'}), 500

@admin_bp.route('/students/<int:student_id>', methods=['GET'])
@admin_required
def get_student_details(student_id):
    """Get detailed student information"""
    try:
        student = Student.query.get_or_404(student_id)
        user = User.query.get(student.user_id)
        applications = Application.query.filter_by(student_id=student.id).count()
        placements = Placement.query.filter_by(student_id=student.id).count()
        
        return jsonify({
            'id': student.id,
            'full_name': student.full_name,
            'roll_number': student.roll_number,
            'branch': student.branch,
            'year_of_study': student.year_of_study,
            'cgpa': student.cgpa,
            'phone': student.phone,
            'email': user.email if user else 'N/A',
            'skills': student.skills,
            'education_details': student.education_details,
            'is_eligible': student.is_eligible,
            'is_blacklisted': user.is_blacklisted if user else False,
            'application_count': applications,
            'placement_count': placements
        }), 200
    except Exception as e:
        current_app.logger.error(f"Get student details error: {str(e)}")
        return jsonify({'error': 'Failed to load student details'}), 500

@admin_bp.route('/students/<int:student_id>/blacklist', methods=['POST'])
@admin_required
def blacklist_student(student_id):
    """
    Blacklist/Deactivate a student
    Milestone 3 Requirement: Blacklist/Deactivate students
    """
    try:
        student = Student.query.get_or_404(student_id)
        user = User.query.get(student.user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        user.is_blacklisted = True
        user.is_active = False
        
        db.session.commit()
        log_admin_action('student_blacklisted', 'student', student_id,
                        f'Blacklisted student: {student.full_name} ({student.roll_number})')
        
        current_app.logger.warning(f"Student {student_id} blacklisted by admin {current_user.id}")
        
        return jsonify({
            'message': 'Student blacklisted successfully',
            'student_id': student_id
        }), 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Blacklist student error: {str(e)}")
        return jsonify({'error': 'Failed to blacklist student'}), 500

@admin_bp.route('/students/<int:student_id>/unblacklist', methods=['POST'])
@admin_required
def unblacklist_student(student_id):
    """Remove student from blacklist"""
    try:
        student = Student.query.get_or_404(student_id)
        user = User.query.get(student.user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        user.is_blacklisted = False
        user.is_active = True
        
        db.session.commit()
        log_admin_action('student_unblacklisted', 'student', student_id,
                        f'Unblacklisted student: {student.full_name} ({student.roll_number})')
        
        return jsonify({
            'message': 'Student removed from blacklist successfully',
            'student_id': student_id
        }), 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Unblacklist student error: {str(e)}")
        return jsonify({'error': 'Failed to unblacklist student'}), 500

@admin_bp.route('/students/<int:student_id>/remove', methods=['DELETE'])
@admin_required
def remove_student(student_id):
    """
    Remove/Delete a student permanently
    Milestone 3 Requirement: Remove students
    """
    try:
        student = Student.query.get_or_404(student_id)
        user = User.query.get(student.user_id)
        
        student_name = student.full_name
        
        # Delete student (cascade will handle related applications)
        db.session.delete(student)
        
        # Optionally delete user account too
        if user:
            db.session.delete(user)
        
        db.session.commit()
        log_admin_action('student_removed', 'student', student_id,
                        f'Removed student: {student_name}')
        
        current_app.logger.info(f"Student {student_id} removed by admin {current_user.id}")
        
        return jsonify({
            'message': 'Student removed successfully',
            'student_id': student_id
        }), 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Remove student error: {str(e)}")
        return jsonify({'error': 'Failed to remove student'}), 500

# ==================== DRIVE MANAGEMENT ====================

@admin_bp.route('/drives', methods=['GET'])
@admin_required
def get_all_drives():
    """
    View and manage all job postings
    Milestone 3 Requirement: View and manage all job postings
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '')
        status = request.args.get('status', '')
        company_id = request.args.get('company_id', None, type=int)
        
        query = Drive.query
        
        # Search by job title
        if search:
            query = query.filter(Drive.job_title.ilike(f'%{search}%'))
        
        # Filter by status
        if status:
            query = query.filter(Drive.status == status)
        
        # Filter by company
        if company_id:
            query = query.filter(Drive.company_id == company_id)
        
        drives = query.order_by(Drive.created_at.desc()).paginate(
            page=page, per_page=min(per_page, 100), error_out=False
        )
        
        drive_list = []
        for drive in drives.items:
            company = Company.query.get(drive.company_id)
            application_count = Application.query.filter_by(drive_id=drive.id).count()
            
            drive_list.append({
                'id': drive.id,
                'job_title': drive.job_title,
                'company_name': company.company_name if company else 'N/A',
                'company_id': drive.company_id,
                'salary': drive.salary,
                'location': drive.location,
                'status': drive.status,
                'application_deadline': drive.application_deadline.isoformat() if drive.application_deadline else None,
                'approved_at': drive.approved_at.isoformat() if drive.approved_at else None,
                'application_count': application_count,
                'created_at': drive.created_at.isoformat() if drive.created_at else None
            })
        
        return jsonify({
            'drives': drive_list,
            'total': drives.total,
            'pages': drives.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
    except Exception as e:
        current_app.logger.error(f"Get drives error: {str(e)}")
        return jsonify({'error': 'Failed to load drives'}), 500

@admin_bp.route('/drives/<int:drive_id>', methods=['GET'])
@admin_required
def get_drive_details(drive_id):
    """Get detailed drive information"""
    try:
        drive = Drive.query.get_or_404(drive_id)
        company = Company.query.get(drive.company_id)
        applications = Application.query.filter_by(drive_id=drive_id).count()
        
        return jsonify({
            'id': drive.id,
            'job_title': drive.job_title,
            'job_description': drive.job_description,
            'salary': drive.salary,
            'location': drive.location,
            'eligibility_criteria': drive.eligibility_criteria,
            'skills_required': drive.skills_required,
            'application_deadline': drive.application_deadline.isoformat() if drive.application_deadline else None,
            'status': drive.status,
            'approved_at': drive.approved_at.isoformat() if drive.approved_at else None,
            'company_name': company.company_name if company else 'N/A',
            'company_id': drive.company_id,
            'application_count': applications
        }), 200
    except Exception as e:
        current_app.logger.error(f"Get drive details error: {str(e)}")
        return jsonify({'error': 'Failed to load drive details'}), 500

@admin_bp.route('/drives/<int:drive_id>/approve', methods=['POST'])
@admin_required
def approve_drive(drive_id):
    """
    Approve a placement drive
    Milestone 3 Requirement: Approve job posting/placement drives
    """
    try:
        drive = Drive.query.get_or_404(drive_id)
        company = Company.query.get(drive.company_id)
        
        # Check if company is approved
        if not company or company.approval_status != 'approved':
            return jsonify({'error': 'Company must be approved before drive can be approved'}), 400
        
        if drive.status == 'approved':
            return jsonify({'error': 'Drive already approved'}), 400
        
        drive.status = 'approved'
        drive.approved_at = datetime.now(timezone.utc)
        drive.approved_by = current_user.id
        
        db.session.commit()
        log_admin_action('drive_approved', 'drive', drive_id,
                        f'Approved drive: {drive.job_title} at {company.company_name}')
        
        current_app.logger.info(f"Drive {drive_id} approved by admin {current_user.id}")
        
        return jsonify({
            'message': 'Drive approved successfully',
            'drive_id': drive_id,
            'job_title': drive.job_title
        }), 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Approve drive error: {str(e)}")
        return jsonify({'error': 'Failed to approve drive'}), 500

@admin_bp.route('/drives/<int:drive_id>/reject', methods=['POST'])
@admin_required
def reject_drive(drive_id):
    """
    Reject a placement drive
    Milestone 3 Requirement: Remove job posting/placement drives
    """
    try:
        drive = Drive.query.get_or_404(drive_id)
        
        if drive.status == 'rejected':
            return jsonify({'error': 'Drive already rejected'}), 400
        
        drive.status = 'rejected'
        
        db.session.commit()
        log_admin_action('drive_rejected', 'drive', drive_id,
                        f'Rejected drive: {drive.job_title}')
        
        current_app.logger.info(f"Drive {drive_id} rejected by admin {current_user.id}")
        
        return jsonify({
            'message': 'Drive rejected successfully',
            'drive_id': drive_id
        }), 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Reject drive error: {str(e)}")
        return jsonify({'error': 'Failed to reject drive'}), 500

@admin_bp.route('/drives/<int:drive_id>/remove', methods=['DELETE'])
@admin_required
def remove_drive(drive_id):
    """
    Remove/Delete a placement drive permanently
    Milestone 3 Requirement: Remove job posting/placement drives
    """
    try:
        drive = Drive.query.get_or_404(drive_id)
        
        job_title = drive.job_title
        
        # Delete drive (cascade will handle related applications)
        db.session.delete(drive)
        
        db.session.commit()
        log_admin_action('drive_removed', 'drive', drive_id,
                        f'Removed drive: {job_title}')
        
        current_app.logger.info(f"Drive {drive_id} removed by admin {current_user.id}")
        
        return jsonify({
            'message': 'Drive removed successfully',
            'drive_id': drive_id
        }), 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Remove drive error: {str(e)}")
        return jsonify({'error': 'Failed to remove drive'}), 500

# ==================== APPLICATION MANAGEMENT ====================

@admin_bp.route('/applications', methods=['GET'])
@admin_required
def get_all_applications():
    """
    View and manage all applications - FIXES EMPTY PAGE ERROR
    Returns all applications across all students, drives, and companies
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        per_page = min(per_page, 100)
        
        status = request.args.get('status', '')
        student_id = request.args.get('student_id', None, type=int)
        drive_id = request.args.get('drive_id', None, type=int)
        
        # Start query
        query = Application.query
        
        # Filter by status if provided
        if status:
            query = query.filter(Application.status == status)
        
        # Filter by student if provided
        if student_id:
            query = query.filter(Application.student_id == student_id)
        
        # Filter by drive if provided
        if drive_id:
            query = query.filter(Application.drive_id == drive_id)
        
        # Order by application date (newest first)
        query = query.order_by(Application.application_date.desc())
        
        # Paginate results
        applications = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        # Build application list with all related data
        app_list = []
        for app in applications.items:
            # Get student details
            student = Student.query.get(app.student_id)
            # Get drive details
            drive = Drive.query.get(app.drive_id)
            # Get company details
            company = Company.query.get(drive.company_id) if drive else None
            
            app_list.append({
                'id': app.id,
                'student_id': app.student_id,
                'student_name': student.full_name if student else 'N/A',
                'student_roll': student.roll_number if student else 'N/A',
                'student_branch': student.branch if student else 'N/A',
                'student_cgpa': student.cgpa if student else 'N/A',
                'drive_id': app.drive_id,
                'drive_title': drive.job_title if drive else 'N/A',
                'company_id': company.id if company else None,
                'company_name': company.company_name if company else 'N/A',
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
        current_app.logger.error(f"Get applications error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': 'Failed to load applications',
            'details': str(e) if current_app.debug else None
        }), 500


# ==================== AUDIT LOGS ====================

@admin_bp.route('/audit-logs', methods=['GET'])
@admin_required
def get_audit_logs():
    """Get audit logs for admin monitoring"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        action = request.args.get('action', '')
        user_id = request.args.get('user_id', None, type=int)
        
        query = AuditLog.query
        
        if action:
            query = query.filter(AuditLog.action.ilike(f'%{action}%'))
        
        if user_id:
            query = query.filter(AuditLog.user_id == user_id)
        
        logs = query.order_by(AuditLog.timestamp.desc()).paginate(
            page=page, per_page=min(per_page, 100), error_out=False
        )
        
        log_list = []
        for log in logs.items:
            user = User.query.get(log.user_id)
            log_list.append({
                'id': log.id,
                'user_id': log.user_id,
                'username': user.username if user else 'N/A',
                'action': log.action,
                'entity_type': log.entity_type,
                'entity_id': log.entity_id,
                'details': log.details,
                'ip_address': log.ip_address,
                'timestamp': log.timestamp.isoformat() if log.timestamp else None
            })
        
        return jsonify({
            'logs': log_list,
            'total': logs.total,
            'pages': logs.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
    except Exception as e:
        current_app.logger.error(f"Get audit logs error: {str(e)}")
        return jsonify({'error': 'Failed to load audit logs'}), 500
    

@admin_bp.route('/reports/monthly', methods=['GET'])
@admin_required
def get_monthly_reports():
    """Get list of all monthly reports"""
    try:
        import os
        from datetime import datetime
        
        reports_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 
            'static', 
            'reports'
        )
        
        reports = []
        
        if os.path.exists(reports_dir):
            for filename in os.listdir(reports_dir):
                if filename.endswith('_report.html'):
                    file_path = os.path.join(reports_dir, filename)
                    file_stats = os.stat(file_path)
                    
                    parts = filename.replace('_report.html', '').split('_')
                    if len(parts) >= 3:
                        company_name = '_'.join(parts[:-2])
                        year = parts[-2]
                        month = parts[-1]
                        
                        try:
                            month_name = datetime(int(year), int(month), 1).strftime('%B %Y')
                        except:
                            month_name = f"{year}-{month}"
                        
                        reports.append({
                            'filename': filename,
                            'company_name': company_name.replace('_', ' '),
                            'period': month_name,
                            'year': year,
                            'month': month,
                            'created_at': datetime.fromtimestamp(file_stats.st_mtime).isoformat(),
                            'file_size': file_stats.st_size,
                            'download_url': f'/api/admin/reports/monthly/{filename}'
                        })
        
        reports.sort(key=lambda x: x['created_at'], reverse=True)
        
        return jsonify({
            'reports': reports,
            'total': len(reports)
        }), 200
    
    except Exception as e:
        current_app.logger.error(f"Get monthly reports error: {str(e)}")
        return jsonify({
            'error': 'Failed to load monthly reports',
            'details': str(e) if current_app.debug else None
        }), 500


@admin_bp.route('/reports/monthly/<filename>', methods=['GET'])
@admin_required
def download_monthly_report(filename):
    """Download a specific monthly report"""
    try:
        import os
        from flask import send_file
        
        if '..' in filename or filename.startswith('/') or filename.startswith('\\'):
            return jsonify({'error': 'Invalid filename'}), 400
        
        reports_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 
            'static', 
            'reports'
        )
        
        file_path = os.path.join(reports_dir, filename)
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'Report not found'}), 404
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename,
            mimetype='text/html'
        )
    
    except Exception as e:
        current_app.logger.error(f"Download monthly report error: {str(e)}")
        return jsonify({
            'error': 'Failed to download report',
            'details': str(e) if current_app.debug else None
        }), 500


@admin_bp.route('/reports/monthly/generate', methods=['POST'])
@admin_required
def generate_monthly_report_manual():
    """Manually trigger monthly report generation (for testing)"""
    try:
        from backend.tasks.reports import generate_monthly_reports
        
        result = generate_monthly_reports()
        
        if result['status'] == 'success':
            return jsonify({
                'message': 'Monthly report generation completed',
                'reports_generated': result['reports_generated'],
                'reports_failed': result['reports_failed'],
                'report_period': result['report_period']
            }), 200
        else:
            return jsonify({
                'error': 'Report generation failed',
                'details': result.get('error')
            }), 500
    
    except Exception as e:
        current_app.logger.error(f"Manual monthly report error: {str(e)}")
        return jsonify({
            'error': 'Failed to generate monthly report',
            'details': str(e) if current_app.debug else None
        }), 500
    
@admin_bp.route('/cache/stats', methods=['GET'])
@admin_required
def get_cache_stats():
    """
    Get Redis cache statistics
    Milestone 8: API Performance Optimization
    
    Returns cache hit/miss rates, memory usage, and key counts
    """
    try:
        from backend.services.cache_service import cache_service
        
        if not cache_service:
            return jsonify({
                'error': 'Cache service not initialized'
            }), 500
        
        stats = cache_service.get_stats()
        
        return jsonify({
            'cache_stats': stats,
            'cache_expiry_config': CACHE_EXPIRY
        }), 200
    
    except Exception as e:
        current_app.logger.error(f"Get cache stats error: {str(e)}")
        return jsonify({
            'error': 'Failed to get cache statistics',
            'details': str(e) if current_app.debug else None
        }), 500


@admin_bp.route('/cache/clear', methods=['POST'])
@admin_required
def clear_cache():
    """
    Clear all Redis cache
    Milestone 8: API Performance Optimization
    
    Admin can manually clear cache when needed
    """
    try:
        from backend.services.cache_service import cache_service
        
        if not cache_service or not cache_service.enabled:
            return jsonify({
                'error': 'Cache service not enabled'
            }), 500
        
        # Clear all PPA v2 cache keys
        deleted = cache_service.delete_pattern('ppa_v2:*')
        
        current_app.logger.info(f"Cache cleared: {deleted} keys deleted")
        
        return jsonify({
            'message': 'Cache cleared successfully',
            'keys_deleted': deleted
        }), 200
    
    except Exception as e:
        current_app.logger.error(f"Clear cache error: {str(e)}")
        return jsonify({
            'error': 'Failed to clear cache',
            'details': str(e) if current_app.debug else None
        }), 500


@admin_bp.route('/cache/invalidate/job_listings', methods=['POST'])
@admin_required
def invalidate_job_listings_cache():
    """
    Invalidate job listings cache
    Milestone 8: API Performance Optimization
    """
    try:
        from backend.services.cache_service import cache_service
        
        if not cache_service or not cache_service.enabled:
            return jsonify({
                'error': 'Cache service not enabled'
            }), 500
        
        deleted = cache_service.delete_pattern('ppa_v2:job_listings:*')
        
        return jsonify({
            'message': 'Job listings cache invalidated',
            'keys_deleted': deleted
        }), 200
    
    except Exception as e:
        current_app.logger.error(f"Invalidate cache error: {str(e)}")
        return jsonify({
            'error': 'Failed to invalidate cache',
            'details': str(e) if current_app.debug else None
        }), 500