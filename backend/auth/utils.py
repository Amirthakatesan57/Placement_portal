from flask import session, request
from datetime import datetime
from backend.models.user import User
from backend.models.audit_log import AuditLog
from backend.extensions import db
import hashlib
import os

def get_client_ip():
    """Get client IP address for audit logging"""
    if request.headers.getlist("X-Forwarded-For"):
        return request.headers.getlist("X-Forwarded-For")[0]
    return request.remote_addr

def log_audit_action(user_id, action, entity_type=None, entity_id=None, details=None):
    """Log user actions for audit trail"""
    try:
        audit_log = AuditLog(
            user_id=user_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            details=details,
            ip_address=get_client_ip()
        )
        db.session.add(audit_log)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Audit log error: {e}")

def validate_registration_data(data, role):
    """Validate registration data based on role"""
    errors = []
    
    # Common validations
    if not data.get('username') or len(data.get('username', '')) < 3:
        errors.append('Username must be at least 3 characters')
    if not data.get('email') or '@' not in data.get('email', ''):
        errors.append('Valid email is required')
    if not data.get('password') or len(data.get('password', '')) < 6:
        errors.append('Password must be at least 6 characters')
    
    # Role-specific validations
    if role == 'student':
        if not data.get('full_name'):
            errors.append('Full name is required')
        if not data.get('roll_number'):
            errors.append('Roll number is required')
        if not data.get('branch'):
            errors.append('Branch is required')
        if not data.get('cgpa'):
            errors.append('CGPA is required')
    
    elif role == 'company':
        if not data.get('company_name'):
            errors.append('Company name is required')
        if not data.get('industry'):
            errors.append('Industry is required')
    
    return errors

def check_duplicate_username(username):
    """Check if username already exists"""
    return User.query.filter_by(username=username).first() is not None

def check_duplicate_email(email):
    """Check if email already exists"""
    return User.query.filter_by(email=email).first() is not None

def check_duplicate_roll_number(roll_number):
    """Check if roll number already exists (for students)"""
    from backend.models.student import Student
    return Student.query.filter_by(roll_number=roll_number).first() is not None