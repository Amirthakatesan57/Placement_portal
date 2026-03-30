from backend.extensions import db
from datetime import datetime

class Placement(db.Model):
    __tablename__ = 'placements'
    
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'), unique=True, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False, index=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False, index=True)
    drive_id = db.Column(db.Integer, db.ForeignKey('drives.id'), nullable=False)
    position = db.Column(db.String(150), nullable=False)
    salary = db.Column(db.Float, nullable=False)
    joining_date = db.Column(db.Date)
    offer_letter_path = db.Column(db.String(255))
    placement_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='offered')  # offered, joined, declined
    
    def __repr__(self):
        return f'<Placement {self.student_id}-{self.company_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'company_id': self.company_id,
            'position': self.position,
            'salary': self.salary,
            'joining_date': self.joining_date.isoformat() if self.joining_date else None,
            'status': self.status,
            'placement_date': self.placement_date.isoformat() if self.placement_date else None
        }