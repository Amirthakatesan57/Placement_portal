#!/usr/bin/env python3
"""
Database Initialization Script
Creates all tables programmatically as per Milestone 1 requirements
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend import create_app
from backend.extensions import db

def init_database():
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        
        print(" Database tables created successfully!")
        print(" Tables created:")
        print("   - users")
        print("   - companies")
        print("   - students")
        print("   - drives")
        print("   - applications")
        print("   - placements")
        print("   - audit_logs")
        
        return True

if __name__ == '__main__':
    try:
        init_database()
        print("\n Milestone 1: Database Models and Schema Setup - COMPLETE")
    except Exception as e:
        print(f" Error initializing database: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)