#!/usr/bin/env python3
"""
Admin User Creation Script
Milestone 3: Admin Dashboard and Management
"""

import sys
import os
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend import create_app
from backend.extensions import db
from backend.models.user import User
from backend.models.audit_log import AuditLog

def create_admin_user():
    """Create default admin user programmatically"""
    app = create_app()
    
    with app.app_context():
        # Check if admin already exists
        existing_admin = User.query.filter_by(role='admin').first()
        
        if existing_admin:
            print(f"⚠️  Admin user already exists: {existing_admin.username}")
            print(f"   Email: {existing_admin.email}")
            print(f"   ID: {existing_admin.id}")
            return existing_admin
        
        # Create admin user
        admin = User(
            username='admin',
            email='admin@placementportal.edu',
            role='admin',
            is_active=True,
            is_blacklisted=False,
            created_at=datetime.now(timezone.utc)
        )
        admin.set_password('Admin@123')
        
        db.session.add(admin)
        db.session.commit()
        
        # Create audit log entry
        audit_log = AuditLog(
            user_id=admin.id,
            action='admin_created',
            entity_type='user',
            entity_id=admin.id,
            details='Default admin user created programmatically for Milestone 3',
            timestamp=datetime.now(timezone.utc)
        )
        
        db.session.add(audit_log)
        db.session.commit()
        
        print("Admin user created successfully!")
        print("=" * 60)
        print("   Username: admin")
        print("   Email: admin@placementportal.edu")
        print("   Role: admin")
        print("   Password: Admin@123")
        print("   ID: {}".format(admin.id))
        print("=" * 60)
        print("\n IMPORTANT: Change the default password after first login!")
        
        return admin

if __name__ == '__main__':
    try:
        create_admin_user()
        print("\nAdmin Creation Script - COMPLETE")
    except Exception as e:
        print(f"Error creating admin: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)