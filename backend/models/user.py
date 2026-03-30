from backend.extensions import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student')  # admin, company, student
    is_active = db.Column(db.Boolean, default=True)
    is_blacklisted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships - explicitly specify foreign_keys to avoid ambiguity
    company_profile = db.relationship(
        'Company', 
        backref='user', 
        uselist=False, 
        cascade='all, delete-orphan',
        foreign_keys='Company.user_id'  # Specify which FK to use
    )
    student_profile = db.relationship(
        'Student', 
        backref='user', 
        uselist=False, 
        cascade='all, delete-orphan',
        foreign_keys='Student.user_id'  # Specify which FK to use
    )
    
    # Companies approved by this admin
    approved_companies = db.relationship(
        'Company',
        backref='approver',
        lazy='dynamic',
        foreign_keys='Company.approved_by'
    )
    
    # Drives approved by this admin
    approved_drives = db.relationship(
        'Drive',
        backref='approver',
        lazy='dynamic',
        foreign_keys='Drive.approved_by'
    )
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username} ({self.role})>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'is_active': self.is_active,
            'is_blacklisted': self.is_blacklisted,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# Register user loader with login_manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))