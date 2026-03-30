#!/usr/bin/env python3
"""
Demo Data Seeding Script
Milestone 4: Company Dashboard and Management
"""

import sys
import os
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend import create_app
from backend.extensions import db
from backend.models.user import User
from backend.models.student import Student
from backend.models.company import Company
from backend.models.drive import Drive
from backend.models.application import Application

def seed_demo_data():
    """Create demo data for testing Milestone 4"""
    app = create_app()
    
    with app.app_context():
        # Check if demo data already exists
        if User.query.filter_by(username='techcorp').first():
            print("  Demo data already exists. Skipping...")
            return
        
        print(" Seeding demo data for Milestone 4...")
        
        # Create approved company
        company_user = User(
            username='techcorp',
            email='hr@techcorp.com',
            role='company',
            is_active=True
        )
        company_user.set_password('Company@123')
        db.session.add(company_user)
        db.session.commit()
        
        company = Company(
            user_id=company_user.id,
            company_name='Tech Corp Solutions',
            industry='IT Services',
            location='Bangalore',
            approval_status='approved',
            approved_at=datetime.now(timezone.utc),
            approved_by=1,
            created_at=datetime.now(timezone.utc)
        )
        db.session.add(company)
        db.session.commit()
        
        # Create placement drive
        drive = Drive(
            company_id=company.id,
            job_title='Software Developer',
            job_description='Develop and maintain web applications',
            salary=800000,
            location='Bangalore',
            eligibility_criteria='CGPA >= 7.0, Branch: CS/IT',
            skills_required='Python,Java,JavaScript',
            application_deadline=datetime.now(timezone.utc) + timedelta(days=30),
            status='approved',
            approved_at=datetime.now(timezone.utc),
            approved_by=1,
            created_at=datetime.now(timezone.utc)
        )
        db.session.add(drive)
        db.session.commit()
        
        # Create student
        student_user = User(
            username='student001',
            email='student001@college.edu',
            role='student',
            is_active=True
        )
        student_user.set_password('Student@123')
        db.session.add(student_user)
        db.session.commit()
        
        student = Student(
            user_id=student_user.id,
            full_name='Rahul Sharma',
            roll_number='CS2020001',
            branch='Computer Science',
            year_of_study=4,
            cgpa=8.5,
            phone='9876543210',
            skills='Python,Java,JavaScript',
            is_eligible=True,
            created_at=datetime.now(timezone.utc)
        )
        db.session.add(student)
        db.session.commit()
        
        # Create application
        application = Application(
            student_id=student.id,
            drive_id=drive.id,
            status='applied',
            application_date=datetime.now(timezone.utc)
        )
        db.session.add(application)
        db.session.commit()
        
        print(" Demo data seeded successfully!")
        print("=" * 60)
        print("COMPANY:")
        print("  Username: techcorp")
        print("  Password: Company@123")
        print("  Status: Approved")
        print()
        print("STUDENT:")
        print("  Username: student001")
        print("  Password: Student@123")
        print()
        print("DRIVE:")
        print("  Title: Software Developer")
        print("  Status: Approved")
        print("=" * 60)
        
        return True

if __name__ == '__main__':
    try:
        seed_demo_data()
        print("\n Demo Data Seeding - COMPLETE")
    except Exception as e:
        print(f" Error seeding demo data: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)