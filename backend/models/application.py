from backend.extensions import db
from datetime import datetime, timezone

class Application(db.Model):
    __tablename__ = 'applications'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False, index=True)
    drive_id = db.Column(db.Integer, db.ForeignKey('drives.id'), nullable=False, index=True)
    status = db.Column(db.String(20), default='applied')  # applied, shortlisted, interview, selected, rejected, placed
    application_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    shortlisted_at = db.Column(db.DateTime)
    interview_scheduled_at = db.Column(db.DateTime)
    interview_date = db.Column(db.DateTime)
    feedback = db.Column(db.Text)
    selected_at = db.Column(db.DateTime)
    rejected_at = db.Column(db.DateTime)
    resume_path = db.Column(db.String(255))
    
    # Unique constraint to prevent duplicate applications
    __table_args__ = (
        db.UniqueConstraint('student_id', 'drive_id', name='unique_student_drive_application'),
    )
    
    # Relationships
    placement = db.relationship(
        'Placement', 
        backref='application', 
        uselist=False, 
        cascade='all, delete-orphan',
        foreign_keys='Placement.application_id'
    )
    
    def __repr__(self):
        return f'<Application {self.student_id}-{self.drive_id} ({self.status})>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'drive_id': self.drive_id,
            'status': self.status,
            'application_date': self.application_date.isoformat() if self.application_date else None,
            'feedback': self.feedback,
            'interview_date': self.interview_date.isoformat() if self.interview_date else None
        }