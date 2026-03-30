from backend.extensions import db
from datetime import datetime

class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    roll_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    branch = db.Column(db.String(100), nullable=False)
    year_of_study = db.Column(db.Integer, nullable=False)
    cgpa = db.Column(db.Float, nullable=False)
    phone = db.Column(db.String(20))
    resume_path = db.Column(db.String(255))
    skills = db.Column(db.Text)  # Comma-separated skills
    education_details = db.Column(db.Text)
    experience_details = db.Column(db.Text)
    is_eligible = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    applications = db.relationship(
        'Application', 
        backref='student', 
        lazy='dynamic', 
        cascade='all, delete-orphan',
        foreign_keys='Application.student_id'
    )
    placements = db.relationship(
        'Placement', 
        backref='student', 
        lazy='dynamic', 
        cascade='all, delete-orphan',
        foreign_keys='Placement.student_id'
    )
    
    def __repr__(self):
        return f'<Student {self.full_name} ({self.roll_number})>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'roll_number': self.roll_number,
            'branch': self.branch,
            'year_of_study': self.year_of_study,
            'cgpa': self.cgpa,
            'skills': self.skills,
            'is_eligible': self.is_eligible,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }