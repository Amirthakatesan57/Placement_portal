#!/usr/bin/env python3
"""
Manual Test Script for Monthly Placement Report
Milestone 7: Backend Jobs - Celery + Redis

Usage:
    python scripts/test_monthly_report.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend import create_app
from backend.tasks.reports import generate_monthly_reports

def test_monthly_report():
    """Manually trigger monthly report generation"""
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("MONTHLY PLACEMENT REPORT - MANUAL TEST")
        print("=" * 60)
        
        print("\n[STEP 1] Triggering monthly report generation...")
        result = generate_monthly_reports()
        
        print(f"\n[RESULT] {result}")
        
        if result['status'] == 'success':
            print(f"\n SUCCESS!")
            print(f"   Reports Generated: {result['reports_generated']}")
            print(f"   Reports Failed: {result['reports_failed']}")
            print(f"   Report Period: {result['report_period']}")
            print(f"\n Check static/reports/ folder for HTML reports")
            print(f" Check email inbox for report notifications")
        else:
            print(f"\n FAILED!")
            print(f"   Error: {result.get('error', 'Unknown error')}")
        
        print("\n" + "=" * 60)
        
        return result

if __name__ == '__main__':
    try:
        test_monthly_report()
    except Exception as e:
        print(f"\n Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)