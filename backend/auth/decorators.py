"""
Authentication and Authorization Decorators
Milestone 4: Company Dashboard and Management
"""

from functools import wraps
from flask import jsonify
from flask_login import login_required, current_user
from backend.models.company import Company

def role_required(*roles):
    """Decorator to restrict access based on user role"""
    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            if current_user.role not in roles:
                return jsonify({'error': 'Access denied. Insufficient permissions.'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    """Decorator for admin-only access"""
    @wraps(f)
    @login_required
    @role_required('admin')
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)
    return decorated_function

def company_required(f):
    """Decorator for company-only access"""
    @wraps(f)
    @login_required
    @role_required('company')
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)
    return decorated_function

def student_required(f):
    """Decorator for student-only access"""
    @wraps(f)
    @login_required
    @role_required('student')
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)
    return decorated_function

def approved_company_required(f):
    """
    Decorator to check if company is approved by admin
    Milestone 4 Requirement: Companies can only access dashboard when approved by admin
    """
    @wraps(f)
    @login_required
    @role_required('company')
    def decorated_function(*args, **kwargs):
        company = Company.query.filter_by(user_id=current_user.id).first()
        
        if not company:
            return jsonify({'error': 'Company profile not found. Please complete registration.'}), 400
        
        if company.approval_status != 'approved':
            return jsonify({
                'error': 'Company account pending admin approval.',
                'approval_status': company.approval_status
            }), 403
        
        return f(*args, **kwargs)
    return decorated_function