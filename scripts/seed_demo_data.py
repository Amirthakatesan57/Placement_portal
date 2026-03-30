#!/usr/bin/env python3
"""
Demo Data Seeding Script
Placement Portal Application V2
Creates comprehensive demo data for testing all milestones

Database: placement.db (SQLite)
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
from backend.models.placement import Placement

def seed_demo_data():
    """Create comprehensive demo data for testing"""
    app = create_app()
    
    with app.app_context():
        print("=" * 70)
        print(" PLACEMENT PORTAL V2 - DEMO DATA SEEDING")
        print("=" * 70)
        
        # Check if demo data already exists
        if User.query.filter_by(username='student001').first():
            print("⚠️  Demo data already exists. Skipping...")
            print("   To reset, delete instance/placement.db and run again")
            return
        
        print("📊 Seeding demo data...")
        print()
        
        # ====================================================================
        # 1. CREATE ADMIN USER
        # ====================================================================
        print("1️⃣  Creating Admin User...")
        
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(
                username='admin',
                email='admin@placementportal.edu',
                role='admin',
                is_active=True,
                is_blacklisted=False,
            )
            admin_user.set_password('Admin@123')
            db.session.add(admin_user)
            db.session.commit()
            print("   ✅ Admin created: admin / Admin@123")
        else:
            print("   ⚠️  Admin already exists")
        
        # ====================================================================
        # 2. CREATE COMPANIES (Approved + Pending)
        # ====================================================================
        print()
        print("2️⃣  Creating Companies...")
        
        companies_data = [
            {
                'username': 'techcorp',
                'email': 'hr@techcorp.com',
                'password': 'Company@123',
                'company_name': 'Tech Corp Solutions',
                'industry': 'IT Services',
                'location': 'Bangalore',
                'website': 'www.techcorp.com',
                'hr_contact_name': 'John Doe',
                'hr_contact_email': 'hr@techcorp.com',
                'hr_contact_phone': '9876543210',
                'approval_status': 'approved',
                'description': 'Leading IT services company specializing in web development'
            },
            {
                'username': 'innovatetech',
                'email': 'careers@innovatetech.com',
                'password': 'Company@123',
                'company_name': 'Innovate Tech Pvt Ltd',
                'industry': 'Software Development',
                'location': 'Hyderabad',
                'website': 'www.innovatetech.com',
                'hr_contact_name': 'Sarah Smith',
                'hr_contact_email': 'careers@innovatetech.com',
                'hr_contact_phone': '9123456780',
                'approval_status': 'approved',
                'description': 'Innovative software solutions for enterprise clients'
            },
            {
                'username': 'YAASTECH',
                'email': 'programmerpros6@gmail.com',
                'password': 'Company@123',
                'company_name': 'YASS TECH PVT LTD.',
                'industry': 'IT Services',
                'location': 'Chennai',
                'website': 'www.yasstech.com',
                'hr_contact_name': 'Programmer Pros',
                'hr_contact_email': 'programmerpros6@gmail.com',
                'hr_contact_phone': '9876543211',
                'approval_status': 'approved',
                'description': 'Technology solutions and consulting services'
            },
            {
                'username': 'startup123',
                'email': 'hr@startup123.com',
                'password': 'Company@123',
                'company_name': 'StartUp Innovations',
                'industry': 'Startup',
                'location': 'Pune',
                'website': 'www.startup123.com',
                'hr_contact_name': 'Mike Johnson',
                'hr_contact_email': 'hr@startup123.com',
                'hr_contact_phone': '9988776655',
                'approval_status': 'pending',
                'description': 'Early stage startup looking for talented developers'
            }
        ]
        
        created_companies = []
        for comp_data in companies_data:
            existing_user = User.query.filter_by(username=comp_data['username']).first()
            if not existing_user:
                company_user = User(
                    username=comp_data['username'],
                    email=comp_data['email'],
                    role='company',
                    is_active=True,
                    is_blacklisted=False,
                )
                company_user.set_password(comp_data['password'])
                db.session.add(company_user)
                db.session.commit()
                
                company = Company(
                    user_id=company_user.id,
                    company_name=comp_data['company_name'],
                    industry=comp_data['industry'],
                    location=comp_data['location'],
                    website=comp_data['website'],
                    hr_contact_name=comp_data['hr_contact_name'],
                    hr_contact_email=comp_data['hr_contact_email'],
                    hr_contact_phone=comp_data['hr_contact_phone'],
                    company_description=comp_data['description'],
                    approval_status=comp_data['approval_status'],
                    approved_at=datetime.now(timezone.utc) if comp_data['approval_status'] == 'approved' else None,
                    approved_by=admin_user.id if comp_data['approval_status'] == 'approved' else None,
                )
                db.session.add(company)
                db.session.commit()
                
                created_companies.append(company)
                print(f"   ✅ Company created: {comp_data['username']} / {comp_data['password']} ({comp_data['approval_status']})")
            else:
                print(f"   ⚠️  Company {comp_data['username']} already exists")
        
        # ====================================================================
        # 3. CREATE STUDENTS
        # ====================================================================
        print()
        print("3️⃣  Creating Students...")
        
        students_data = [
            {
                'username': 'student001',
                'email': 'student001@college.edu',
                'password': 'Student@123',
                'full_name': 'Rahul Sharma',
                'roll_number': 'CS2020001',
                'branch': 'Computer Science',
                'year_of_study': 4,
                'cgpa': 8.5,
                'phone': '9876543210',
                'skills': 'Python,Java,JavaScript,React',
                'is_eligible': True
            },
            {
                'username': 'student002',
                'email': 'student002@college.edu',
                'password': 'Student@123',
                'full_name': 'Priya Patel',
                'roll_number': 'CS2020002',
                'branch': 'Computer Science',
                'year_of_study': 4,
                'cgpa': 9.0,
                'phone': '9876543211',
                'skills': 'Python,C++,Machine Learning,AI',
                'is_eligible': True
            },
            {
                'username': 'student003',
                'email': 'akpk47626@gmail.com',
                'password': 'Student@123',
                'full_name': 'Amit Kumar',
                'roll_number': 'CS2020003',
                'branch': 'Computer Science',
                'year_of_study': 4,
                'cgpa': 7.5,
                'phone': '9876543212',
                'skills': 'Java,Spring,MySQL,Docker',
                'is_eligible': True
            },
            {
                'username': 'student004',
                'email': 'student004@college.edu',
                'password': 'Student@123',
                'full_name': 'Sneha Reddy',
                'roll_number': 'IT2020001',
                'branch': 'Information Technology',
                'year_of_study': 4,
                'cgpa': 8.0,
                'phone': '9876543213',
                'skills': 'JavaScript,Node.js,MongoDB,React',
                'is_eligible': True
            },
            {
                'username': 'student005',
                'email': 'student005@college.edu',
                'password': 'Student@123',
                'full_name': 'Vikram Singh',
                'roll_number': 'CS2020005',
                'branch': 'Computer Science',
                'year_of_study': 3,
                'cgpa': 7.0,
                'phone': '9876543214',
                'skills': 'Python,Django,PostgreSQL',
                'is_eligible': True
            }
        ]
        
        created_students = []
        for stud_data in students_data:
            existing_user = User.query.filter_by(username=stud_data['username']).first()
            if not existing_user:
                student_user = User(
                    username=stud_data['username'],
                    email=stud_data['email'],
                    role='student',
                    is_active=True,
                    is_blacklisted=False,
                )
                student_user.set_password(stud_data['password'])
                db.session.add(student_user)
                db.session.commit()
                
                student = Student(
                    user_id=student_user.id,
                    full_name=stud_data['full_name'],
                    roll_number=stud_data['roll_number'],
                    branch=stud_data['branch'],
                    year_of_study=stud_data['year_of_study'],
                    cgpa=stud_data['cgpa'],
                    phone=stud_data['phone'],
                    skills=stud_data['skills'],
                    is_eligible=stud_data['is_eligible'],
                )
                db.session.add(student)
                db.session.commit()
                
                created_students.append(student)
                print(f"   ✅ Student created: {stud_data['username']} / {stud_data['password']} ({stud_data['full_name']})")
            else:
                print(f"   ⚠️  Student {stud_data['username']} already exists")
        
        # ====================================================================
        # 4. CREATE PLACEMENT DRIVES
        # ====================================================================
        print()
        print("4️⃣  Creating Placement Drives...")
        
        drives_data = [
            {
                'company_username': 'techcorp',
                'job_title': 'Software Developer',
                'job_description': 'Develop and maintain web applications using modern technologies. Work with cross-functional teams to deliver high-quality software solutions.',
                'salary': 800000,
                'location': 'Bangalore',
                'eligibility_criteria': 'CGPA >= 7.0, Branch: CS/IT, No active backlogs',
                'skills_required': 'Python,Java,JavaScript',
                'application_deadline': datetime.now(timezone.utc) + timedelta(days=30),
                'status': 'approved'
            },
            {
                'company_username': 'techcorp',
                'job_title': 'Data Scientist',
                'job_description': 'Analyze large datasets and build machine learning models. Work on predictive analytics and data visualization.',
                'salary': 1200000,
                'location': 'Bangalore',
                'eligibility_criteria': 'CGPA >= 8.0, Branch: CS/IT/Statistics, Knowledge of ML/AI',
                'skills_required': 'Python,Machine Learning,AI,SQL',
                'application_deadline': datetime.now(timezone.utc) + timedelta(days=25),
                'status': 'approved'
            },
            {
                'company_username': 'innovatetech',
                'job_title': 'Full Stack Developer',
                'job_description': 'Build end-to-end web applications. Work with React, Node.js, and cloud technologies.',
                'salary': 900000,
                'location': 'Hyderabad',
                'eligibility_criteria': 'CGPA >= 7.5, Branch: CS/IT, Web development experience',
                'skills_required': 'JavaScript,React,Node.js,MongoDB',
                'application_deadline': datetime.now(timezone.utc) + timedelta(days=20),
                'status': 'approved'
            },
            {
                'company_username': 'YAASTECH',
                'job_title': 'Backend Engineer',
                'job_description': 'Design and implement scalable backend services. Work with microservices architecture and cloud platforms.',
                'salary': 1000000,
                'location': 'Chennai',
                'eligibility_criteria': 'CGPA >= 7.0, Branch: CS/IT, Backend development experience',
                'skills_required': 'Python,Django,PostgreSQL,Docker',
                'application_deadline': datetime.now(timezone.utc) + timedelta(days=15),
                'status': 'approved'
            },
            {
                'company_username': 'startup123',
                'job_title': 'Junior Developer',
                'job_description': 'Join our startup as a junior developer. Learn and grow with cutting-edge technologies.',
                'salary': 600000,
                'location': 'Pune',
                'eligibility_criteria': 'CGPA >= 6.5, Branch: Any, Passion for learning',
                'skills_required': 'Python,JavaScript,Git',
                'application_deadline': datetime.now(timezone.utc) + timedelta(days=10),
                'status': 'pending'
            }
        ]
        
        created_drives = []
        for drive_data in drives_data:
            company = Company.query.filter_by(
                user_id=User.query.filter_by(username=drive_data['company_username']).first().id
            ).first()
            
            existing_drive = Drive.query.filter_by(
                company_id=company.id,
                job_title=drive_data['job_title']
            ).first()
            
            if not existing_drive:
                drive = Drive(
                    company_id=company.id,
                    job_title=drive_data['job_title'],
                    job_description=drive_data['job_description'],
                    salary=drive_data['salary'],
                    location=drive_data['location'],
                    eligibility_criteria=drive_data['eligibility_criteria'],
                    skills_required=drive_data['skills_required'],
                    application_deadline=drive_data['application_deadline'],
                    status=drive_data['status'],
                    approved_at=datetime.now(timezone.utc) if drive_data['status'] == 'approved' else None,
                    approved_by=admin_user.id if drive_data['status'] == 'approved' else None,
                )
                db.session.add(drive)
                db.session.commit()
                
                created_drives.append(drive)
                print(f"   ✅ Drive created: {drive_data['job_title']} @ {drive_data['company_username']} ({drive_data['status']})")
            else:
                print(f"   ⚠️  Drive {drive_data['job_title']} already exists")
        
        # ====================================================================
        # 5. CREATE APPLICATIONS (Various Statuses)
        # ====================================================================
        print()
        print("5️⃣  Creating Applications...")
        
        applications_data = [
            {
                'student_username': 'student001',
                'drive_job_title': 'Software Developer',
                'status': 'shortlisted',
                'feedback': 'Good technical skills, shortlisted for interview'
            },
            {
                'student_username': 'student001',
                'drive_job_title': 'Data Scientist',
                'status': 'applied',
                'feedback': None
            },
            {
                'student_username': 'student002',
                'drive_job_title': 'Data Scientist',
                'status': 'interview',
                'feedback': 'Excellent ML knowledge, interview scheduled',
                'interview_date': datetime.now(timezone.utc) + timedelta(days=2)
            },
            {
                'student_username': 'student003',
                'drive_job_title': 'Backend Engineer',
                'status': 'selected',
                'feedback': 'Strong backend skills, selected for position'
            },
            {
                'student_username': 'student004',
                'drive_job_title': 'Full Stack Developer',
                'status': 'applied',
                'feedback': None
            },
            {
                'student_username': 'student005',
                'drive_job_title': 'Junior Developer',
                'status': 'rejected',
                'feedback': 'Does not meet minimum CGPA requirement'
            }
        ]
        
        for app_data in applications_data:
            student = Student.query.filter_by(
                user_id=User.query.filter_by(username=app_data['student_username']).first().id
            ).first()
            
            drive = Drive.query.filter_by(job_title=app_data['drive_job_title']).first()
            
            existing_app = Application.query.filter_by(
                student_id=student.id,
                drive_id=drive.id
            ).first()
            
            if not existing_app:
                application = Application(
                    student_id=student.id,
                    drive_id=drive.id,
                    status=app_data['status'],
                    feedback=app_data['feedback'],
                    interview_date=app_data.get('interview_date'),
                    application_date=datetime.now(timezone.utc) - timedelta(days=5)
                )
                db.session.add(application)
                db.session.commit()
                
                print(f"   ✅ Application: {app_data['student_username']} → {app_data['drive_job_title']} ({app_data['status']})")
            else:
                print(f"   ⚠️  Application already exists")
        
        # ====================================================================
        # 6. CREATE PLACEMENTS
        # ====================================================================
        print()
        print("6️⃣  Creating Placements...")
        
        placements_data = [
            {
                'student_username': 'student003',
                'company_username': 'YAASTECH',
                'drive_job_title': 'Backend Engineer',
                'position': 'Backend Engineer',
                'salary': 1000000,
                'status': 'offered',
                'joining_date': datetime.now(timezone.utc) + timedelta(days=30)
            }
        ]
        
        for placement_data in placements_data:
            student = Student.query.filter_by(
                user_id=User.query.filter_by(username=placement_data['student_username']).first().id
            ).first()
            
            company = Company.query.filter_by(
                user_id=User.query.filter_by(username=placement_data['company_username']).first().id
            ).first()
            
            drive = Drive.query.filter_by(job_title=placement_data['drive_job_title']).first()
            
            existing_placement = Placement.query.filter_by(
                student_id=student.id,
                company_id=company.id
            ).first()
            
            if not existing_placement:
                placement = Placement(
                    student_id=student.id,
                    company_id=company.id,
                    drive_id=drive.id,
                    position=placement_data['position'],
                    salary=placement_data['salary'],
                    status=placement_data['status'],
                    joining_date=placement_data['joining_date'],
                    placement_date=datetime.now(timezone.utc),
                )
                db.session.add(placement)
                db.session.commit()
                
                print(f"   ✅ Placement: {placement_data['student_username']} @ {placement_data['company_username']} (₹{placement_data['salary']:,})")
            else:
                print(f"   ⚠️  Placement already exists")
        
        # ====================================================================
        # SUMMARY
        # ====================================================================
        print()
        print("=" * 70)
        print("✅ DEMO DATA SEEDING COMPLETE!")
        print("=" * 70)
        print()
        print("📊 SUMMARY:")
        print(f"   • Users Created: {User.query.count()}")
        print(f"   • Companies: {Company.query.count()}")
        print(f"   • Students: {Student.query.count()}")
        print(f"   • Drives: {Drive.query.count()}")
        print(f"   • Applications: {Application.query.count()}")
        print(f"   • Placements: {Placement.query.count()}")
        print()
        print("🔑 LOGIN CREDENTIALS:")
        print()
        print("   ADMIN:")
        print("   ┌──────────────────────────────────────┐")
        print("   │ Username: admin                      │")
        print("   │ Password: Admin@123                  │")
        print("   │ URL: http://localhost:5000/#/login   │")
        print("   └──────────────────────────────────────┘")
        print()
        print("   COMPANIES:")
        print("   ┌──────────────────────────────────────┐")
        print("   │ Username: techcorp                   │")
        print("   │ Password: Company@123                │")
        print("   │ Status: Approved                     │")
        print("   ├──────────────────────────────────────┤")
        print("   │ Username: innovatetech               │")
        print("   │ Password: Company@123                │")
        print("   │ Status: Approved                     │")
        print("   ├──────────────────────────────────────┤")
        print("   │ Username: YAASTECH                   │")
        print("   │ Password: Company@123                │")
        print("   │ Status: Approved                     │")
        print("   ├──────────────────────────────────────┤")
        print("   │ Username: startup123                 │")
        print("   │ Password: Company@123                │")
        print("   │ Status: Pending (needs approval)     │")
        print("   └──────────────────────────────────────┘")
        print()
        print("   STUDENTS:")
        print("   ┌──────────────────────────────────────┐")
        print("   │ Username: student001                 │")
        print("   │ Password: Student@123                │")
        print("   │ Name: Rahul Sharma                   │")
        print("   │ Status: Applied to 2 drives          │")
        print("   ├──────────────────────────────────────┤")
        print("   │ Username: student002                 │")
        print("   │ Password: Student@123                │")
        print("   │ Name: Priya Patel                    │")
        print("   │ Status: Interview scheduled          │")
        print("   ├──────────────────────────────────────┤")
        print("   │ Username: student003                 │")
        print("   │ Password: Student@123                │")
        print("   │ Name: Amit Kumar                     │")
        print("   │ Status: SELECTED (Placed!)           │")
        print("   └──────────────────────────────────────┘")
        print()
        print("🌐 ACCESS URLS:")
        print("   • Home: http://localhost:5000/")
        print("   • Admin Dashboard: http://localhost:5000/#/admin/dashboard")
        print("   • Company Dashboard: http://localhost:5000/#/company/dashboard")
        print("   • Student Dashboard: http://localhost:5000/#/student/dashboard")
        print()
        print("=" * 70)
        
        return True

if __name__ == '__main__':
    try:
        seed_demo_data()
        print("\n🎉 Demo Data Seeding - COMPLETE")
    except Exception as e:
        print(f"\n❌ Error seeding demo data: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
