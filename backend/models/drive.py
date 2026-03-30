from backend.extensions import db
from datetime import datetime, timezone

class Drive(db.Model):
    __tablename__ = 'drives'
    
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False, index=True)
    job_title = db.Column(db.String(150), nullable=False)
    job_description = db.Column(db.Text, nullable=False)
    salary = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(150), nullable=False)
    eligibility_criteria = db.Column(db.Text, nullable=False)
    skills_required = db.Column(db.Text)
    application_deadline = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, approved, active, closed, rejected
    approved_at = db.Column(db.DateTime)
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    applications = db.relationship(
        'Application', 
        backref='drive', 
        lazy='dynamic', 
        cascade='all, delete-orphan',
        foreign_keys='Application.drive_id'
    )
    
    def __repr__(self):
        return f'<Drive {self.job_title} ({self.company_id})>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'company_id': self.company_id,
            'job_title': self.job_title,
            'salary': self.salary,
            'location': self.location,
            'application_deadline': self.application_deadline.isoformat() if self.application_deadline else None,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }