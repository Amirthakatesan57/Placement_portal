from flask import current_app, jsonify, request, session, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime, timezone
from backend.auth import auth_bp
from backend.extensions import db
from backend.models.user import User
from backend.models.student import Student
from backend.models.company import Company
from backend.auth.utils import (
    validate_registration_data, 
    check_duplicate_username, 
    check_duplicate_email,
    check_duplicate_roll_number,
    log_audit_action
)
from backend.auth.decorators import role_required

# ==================== LOGIN ====================

@auth_bp.route('/login', methods=['POST'])
def login():
    """Handle user login"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    # Find user
    user = User.query.filter_by(username=username).first()
    
    if not user:
        return jsonify({'error': 'Invalid username or password'}), 401
    
    if not user.check_password(password):
        return jsonify({'error': 'Invalid username or password'}), 401
    
    if not user.is_active:
        return jsonify({'error': 'Account is deactivated'}), 403
    
    if user.is_blacklisted:
        return jsonify({'error': 'Account is blacklisted. Contact admin.'}), 403
    
    # Check company approval status
    if user.role == 'company':
        company = Company.query.filter_by(user_id=user.id).first()
        if company and company.approval_status != 'approved':
            return jsonify({
                'error': 'Company account pending admin approval',
                'approval_status': company.approval_status
            }), 403
    
    # Login successful
    login_user(user)
    user.last_login = datetime.utcnow()
    db.session.commit()
    
    # Log audit action
    log_audit_action(user.id, 'login', 'user', user.id)
    
    # Return user info with role
    return jsonify({
        'message': 'Login successful',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role
        },
        'redirect_url': get_dashboard_url(user.role)
    }), 200

def get_dashboard_url(role):
    """Get dashboard URL based on role - USE HASH ROUTES FOR VUE CDN"""
    if role == 'admin':
        return '#/admin/dashboard'
    elif role == 'company':
        return '#/company/dashboard'
    elif role == 'student':
        return '#/student/dashboard'
    return '#/'


# ==================== LOGOUT ====================

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """Handle user logout"""
    log_audit_action(current_user.id, 'logout', 'user', current_user.id)
    logout_user()
    return jsonify({'message': 'Logout successful'}), 200

# ==================== STUDENT REGISTRATION ====================

@auth_bp.route('/register/student', methods=['POST'])
def register_student():
    """Handle student registration"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Validate data
    errors = validate_registration_data(data, 'student')
    if errors:
        return jsonify({'errors': errors}), 400
    
    # Check duplicates
    if check_duplicate_username(data['username']):
        return jsonify({'error': 'Username already exists'}), 400
    if check_duplicate_email(data['email']):
        return jsonify({'error': 'Email already registered'}), 400
    if check_duplicate_roll_number(data['roll_number']):
        return jsonify({'error': 'Roll number already registered'}), 400
    
    try:
        # Create user
        user = User(
            username=data['username'],
            email=data['email'],
            role='student',
            is_active=True,
            is_blacklisted=False,
            created_at=datetime.utcnow()
        )
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        
        # Create student profile
        student = Student(
            user_id=user.id,
            full_name=data['full_name'],
            roll_number=data['roll_number'],
            branch=data['branch'],
            year_of_study=int(data.get('year_of_study', 4)),
            cgpa=float(data['cgpa']),
            phone=data.get('phone', ''),
            skills=data.get('skills', ''),
            education_details=data.get('education_details', ''),
            experience_details=data.get('experience_details', ''),
            is_eligible=True,
            created_at=datetime.utcnow()
        )
        db.session.add(student)
        db.session.commit()
        
        # Log audit action
        log_audit_action(user.id, 'student_registration', 'user', user.id)
        
        # Auto-login after registration
        login_user(user)
        
        return jsonify({
            'message': 'Student registration successful',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role
            },
            'redirect_url': get_dashboard_url('student')
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Registration failed: {str(e)}'}), 500

# ==================== COMPANY REGISTRATION ====================

@auth_bp.route('/register/company', methods=['POST'])
def register_company():
    """Handle company registration"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Validate data
    errors = validate_registration_data(data, 'company')
    if errors:
        return jsonify({'errors': errors}), 400
    
    # Check duplicates
    if check_duplicate_username(data['username']):
        return jsonify({'error': 'Username already exists'}), 400
    if check_duplicate_email(data['email']):
        return jsonify({'error': 'Email already registered'}), 400
    
    try:
        # Create user
        user = User(
            username=data['username'],
            email=data['email'],
            role='company',
            is_active=True,
            is_blacklisted=False,
            created_at=datetime.utcnow()
        )
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        
        # Create company profile (pending approval)
        company = Company(
            user_id=user.id,
            company_name=data['company_name'],
            industry=data['industry'],
            location=data.get('location', ''),
            website=data.get('website', ''),
            hr_contact_name=data.get('hr_contact_name', ''),
            hr_contact_email=data.get('hr_contact_email', ''),
            hr_contact_phone=data.get('hr_contact_phone', ''),
            company_description=data.get('company_description', ''),
            approval_status='pending',  # Requires admin approval
            created_at=datetime.utcnow()
        )
        db.session.add(company)
        db.session.commit()
        
        # Log audit action
        log_audit_action(user.id, 'company_registration', 'user', user.id)
        
        # Don't auto-login - company needs admin approval first
        return jsonify({
            'message': 'Company registration successful. Pending admin approval.',
            'approval_status': 'pending',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Registration failed: {str(e)}'}), 500

# ==================== CHECK AUTH STATUS ====================

@auth_bp.route('/me', methods=['GET'])
@login_required
def get_current_user():
    """Get current authenticated user info"""
    user_data = {
        'id': current_user.id,
        'username': current_user.username,
        'email': current_user.email,
        'role': current_user.role,
        'is_active': current_user.is_active,
        'is_blacklisted': current_user.is_blacklisted
    }
    
    # Add role-specific data
    if current_user.role == 'student':
        student = Student.query.filter_by(user_id=current_user.id).first()
        if student:
            user_data['student_profile'] = student.to_dict()
    elif current_user.role == 'company':
        company = Company.query.filter_by(user_id=current_user.id).first()
        if company:
            user_data['company_profile'] = company.to_dict()
            user_data['approval_status'] = company.approval_status
    
    return jsonify(user_data), 200

# ==================== PASSWORD RESET ====================

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    """Handle forgot password request"""
    data = request.get_json()
    email = data.get('email')
    
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    
    user = User.query.filter_by(email=email).first()
    
    if not user:
        # Don't reveal if email exists for security
        return jsonify({'message': 'If email exists, reset link will be sent'}), 200
    
    # TODO: Implement email sending with reset token
    # For now, just return success message
    log_audit_action(user.id, 'password_reset_request', 'user', user.id)
    
    return jsonify({'message': 'If email exists, reset link will be sent'}), 200

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    """Handle password reset with token"""
    data = request.get_json()
    token = data.get('token')
    new_password = data.get('new_password')
    
    if not token or not new_password:
        return jsonify({'error': 'Token and new password required'}), 400
    
    if len(new_password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
    
    # TODO: Implement token validation and password reset
    # For now, return placeholder
    return jsonify({'message': 'Password reset functionality coming soon'}), 200

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Universal registration endpoint for both Student and Company
    Milestone 2: Authentication and Role-Based Access
    """
    try:
        data = request.get_json()
        
        if not data :
            return jsonify({'error': 'No data provided'}), 400
        
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        role = data.get('role', '').strip()
        
        # Validate required fields
        if not username or not email or not password or not role:
            return jsonify({'error': 'All fields are required'}), 400
        
        # Validate role
        if role not in ['student', 'company']:
            return jsonify({'error': 'Invalid role. Must be student or company'}), 400
        
        # Check if username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({'error': 'Username already exists'}), 400
        
        # Check if email already exists
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            return jsonify({'error': 'Email already registered'}), 400
        
        # Create new user
        user = User(
            username=username,
            email=email,
            role=role,
            is_active=True,
            is_blacklisted=False,
            created_at=datetime.now(timezone.utc)
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.flush()  # Get user ID before commit
        
        # Create role-specific profile
        if role == 'student':
            student_data = data.get('student_data', {})
            student = Student(
                user_id=user.id,
                full_name=student_data.get('full_name', username),
                roll_number=student_data.get('roll_number', ''),
                branch=student_data.get('branch', ''),
                year_of_study=student_data.get('year_of_study', 4),
                cgpa=student_data.get('cgpa', 0.0),
                phone=student_data.get('phone', ''),
                skills=student_data.get('skills', ''),
                is_eligible=True,
                created_at=datetime.now(timezone.utc)
            )
            db.session.add(student)
            
            db.session.commit()
            
            current_app.logger.info(f"Student registration successful: {username}")
            
            return jsonify({
                'message': 'Student registration successful',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': user.role,
                    'full_name': student.full_name
                },
                'redirect_url': '/student/dashboard'
            }), 201
            
        elif role == 'company':
            company_data = data.get('company_data', {})
            company = Company(
                user_id=user.id,
                company_name=company_data.get('company_name', username),
                industry=company_data.get('industry', ''),
                location=company_data.get('location', ''),
                website=company_data.get('website', ''),
                hr_contact_name=company_data.get('hr_contact_name', ''),
                hr_contact_email=company_data.get('hr_contact_email', email),
                hr_contact_phone=company_data.get('hr_contact_phone', ''),
                company_description=company_data.get('company_description', ''),
                approval_status='pending',  # Requires admin approval
                created_at=datetime.now(timezone.utc)
            )
            db.session.add(company)
            
            db.session.commit()
            
            current_app.logger.info(f"Company registration successful: {username} (pending approval)")
            
            return jsonify({
                'message': 'Company registration successful. Pending admin approval.',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': user.role,
                    'company_name': company.company_name
                },
                'redirect_url': '/login'
            }), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Registration error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': 'Registration failed. Please try again.',
            'details': str(e) if current_app.debug else None
        }), 500