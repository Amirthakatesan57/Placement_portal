#!/usr/bin/env python3
"""
Manual Test Script for Interview Reminder Job
Milestone 7: Backend Jobs - Interview Reminders (Email / GChat)

This script:
1. Creates test data (student with scheduled interview)
2. Triggers the reminder task manually
3. Verifies email/GChat was sent

Usage:
    python scripts/test_interview_reminder.py
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
from backend.tasks.reminders import send_interview_reminders

def create_test_interview():
    """Create test data for interview reminder testing"""
    print("\n[STEP 1] Creating test interview data...")
    
    # Get or create test student
    student_user = User.query.filter_by(username='student003').first()
    if not student_user:
        print("❌ Student user not found. Please run seed_demo_data.py first")
        return None
    
    student = Student.query.filter_by(user_id=student_user.id).first()
    if not student:
        print("❌ Student profile not found")
        return None
    
    # Get or create test company
    company_user = User.query.filter_by(username='YAASTECH').first()
    if not company_user:
        print("❌ Company user not found. Please run seed_demo_data.py first")
        return None
    
    company = Company.query.filter_by(user_id=company_user.id).first()
    if not company:
        print("❌ Company profile not found")
        return None
    
    # Get or create test drive
    drive = Drive.query.filter_by(company_id=company.id).first()
    if not drive:
        print("❌ Drive not found. Please create a placement drive first")
        return None
    
    # Create or update application with interview status
    application = Application.query.filter_by(
        student_id=student.id,
        drive_id=drive.id
    ).first()
    
    if not application:
        # Create new application
        application = Application(
            student_id=student.id,
            drive_id=drive.id,
            status='interview',
            application_date=datetime.now(timezone.utc)
        )
        db.session.add(application)
        print("    Created new application")
    else:
        # Update existing application
        application.status = 'interview'
        print("    Updated existing application")
    
    # Set interview date to tomorrow (within 24 hours for reminder to trigger)
    interview_date = datetime.now(timezone.utc) + timedelta(hours=2)
    application.interview_date = interview_date
    application.feedback = f'Interview scheduled for {interview_date.strftime("%Y-%m-%d %H:%M")}'
    
    db.session.commit()
    
    print(f"    Student: {student.full_name} ({student.roll_number})")
    print(f"    Company: {company.company_name}")
    print(f"    Drive: {drive.job_title}")
    print(f"    Interview Date: {interview_date.strftime('%Y-%m-%d %H:%M')} (in 2 hours)")
    print(f"    Student Email: {student_user.email}")
    
    return {
        'student': student,
        'company': company,
        'drive': drive,
        'application': application,
        'interview_date': interview_date
    }


def test_interview_reminder():
    """Test interview reminder job"""
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("INTERVIEW REMINDER - MANUAL TEST")
        print("=" * 60)
        
        # Create test data
        test_data = create_test_interview()
        
        if not test_data:
            print("\n Failed to create test data")
            return
        
        print("\n[STEP 2] Triggering interview reminder job...")
        result = send_interview_reminders()
        
        print(f"\n[RESULT] {result}")
        
        if result['status'] == 'success':
            print(f"\n SUCCESS!")
            print(f"   Reminders Sent: {result['reminders_sent']}")
            print(f"   Reminders Failed: {result['reminders_failed']}")
            
            if result['reminders_sent'] > 0:
                print(f"\n Check email inbox: {test_data['student'].user.email}")
                print(f"   Subject: Interview Reminder: {test_data['drive'].job_title}")
                
                print(f"\n Check GChat (if configured)")
                print(f"   Webhook: Check your Google Chat space")
            else:
                print(f"\n  No reminders sent (no interviews in next 24 hours)")
        else:
            print(f"\n FAILED!")
            print(f"   Error: {result.get('error', 'Unknown error')}")
        
        print("\n[STEP 3] Verification Checklist:")
        print("   □ Email received at student email address")
        print("   □ Email subject contains job title")
        print("   □ Email contains interview date and time")
        print("   □ Email contains company name")
        print("   □ GChat notification received (if configured)")
        
        print("\n" + "=" * 60)
        
        return result


def cleanup_test_data():
    """Clean up test data after testing"""
    app = create_app()
    
    with app.app_context():
        print("\n[CLEANUP] Removing test interview data...")
        
        # Find test application
        student_user = User.query.filter_by(username='student003').first()
        if student_user:
            student = Student.query.filter_by(user_id=student_user.id).first()
            if student:
                application = Application.query.filter_by(
                    student_id=student.id,
                    status='interview'
                ).first()
                
                if application:
                    application.status = 'applied'
                    application.interview_date = None
                    application.feedback = None
                    db.session.commit()
                    print("    Test data cleaned up")
                else:
                    print("     No test application found")
            else:
                print("     Student profile not found")
        else:
            print("     Student user not found")


if __name__ == '__main__':
    try:
        # Run test
        result = test_interview_reminder()
        
        # Ask for cleanup
        if result and result['status'] == 'success':
            cleanup = input("\nClean up test data? (y/n): ").strip().lower()
            if cleanup == 'y':
                cleanup_test_data()
        
    except Exception as e:
        print(f"\n Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)