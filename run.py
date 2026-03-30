#!/usr/bin/env python3
"""
Placement Portal Application V2
Application Entry Point
Milestone 4: Company Dashboard and Management
"""

from backend import create_app
from backend.extensions import db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # Ensure database tables exist
        db.create_all()
        
        print("=" * 60)
        print(" Placement Portal Application V2")
        print(" Database: SQLite (Programmatic Creation)")
        print(" Authentication: Enabled")
        print("=" * 60)
        print()
        print(" Server running on: http://localhost:5000")
        print(" Admin Login: admin / Admin@123")
        print(" Company Login: techcorp / Company@123")
        print(" Student Login: student001 / Student@123")
        print()
    
    app.run(debug=True, port=5000, host='0.0.0.0')