from backend.extensions import db
from datetime import datetime

class Company(db.Model):
    __tablename__ = 'companies'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    company_name = db.Column(db.String(150), nullable=False)
    industry = db.Column(db.String(100))
    location = db.Column(db.String(150))
    website = db.Column(db.String(200))
    hr_contact_name = db.Column(db.String(100))
    hr_contact_email = db.Column(db.String(120))
    hr_contact_phone = db.Column(db.String(20))
    company_description = db.Column(db.Text)
    approval_status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    approved_at = db.Column(db.DateTime)
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'))  # Admin who approved
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships - explicitly specify foreign_keys
    drives = db.relationship(
        'Drive', 
        backref='company', 
        lazy='dynamic', 
        cascade='all, delete-orphan',
        foreign_keys='Drive.company_id'
    )
    
    def __repr__(self):
        return f'<Company {self.company_name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'company_name': self.company_name,
            'industry': self.industry,
            'location': self.location,
            'website': self.website,
            'approval_status': self.approval_status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }