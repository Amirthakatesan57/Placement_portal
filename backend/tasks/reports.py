"""
Placement Report Tasks
Milestone 7: Generate monthly reports for companies (HTML / PDF) with application statistics
"""

from backend.extensions import celery
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
import calendar  
import os
import logging

logger = logging.getLogger(__name__)

@celery.task(bind=True, max_retries=3)
def generate_monthly_reports(self):
    """
    Generate placement reports for all companies with ALL historical data
    Milestone 7: Placement Report Job
    
    This version generates reports with ALL data from database (not date-filtered)
    Perfect for testing and demonstration
    """
    from backend import create_app
    from backend.models.user import User
    from backend.models.company import Company
    from backend.models.drive import Drive
    from backend.models.application import Application
    from backend.models.placement import Placement
    from backend.services.email_service import send_email
    from backend.services.report_service import generate_html_report
    from datetime import datetime, timezone
    import calendar
    
    app = create_app()
    
    with app.app_context():
        try:
            logger.info("Starting placement report generation (ALL DATA)...")
            print("[INFO] Starting placement report generation (ALL DATA)...")
            
            # Get current date for report generation timestamp
            now = datetime.now(timezone.utc)
            
            # Get all approved companies
            companies = Company.query.filter_by(approval_status='approved').all()
            
            logger.info(f"Found {len(companies)} approved companies")
            print(f"[INFO] Found {len(companies)} approved companies")
            
            reports_generated = 0
            reports_failed = 0
            
            for company in companies:
                try:
                    # Get ALL company statistics (not date-filtered)
                    stats = get_company_all_time_stats(company.id)
                    
                    # DEBUG: Log what data was found
                    logger.info(f"Company {company.company_name}: Drives={stats['total_drives']}, Applications={stats['total_applications']}, Placements={stats['total_placements']}")
                    print(f"[DEBUG] Company {company.company_name}: Drives={stats['total_drives']}, Applications={stats['total_applications']}, Placements={stats['total_placements']}")
                    
                    # Generate report
                    user = User.query.get(company.user_id)
                    if not user or not user.email:
                        logger.warning(f"Skipping company {company.company_name} - no email")
                        continue
                    
                    report_data = {
                        'company_name': company.company_name,
                        'report_period': 'All Time (Complete History)',  # Changed from monthly
                        'stats': stats,
                        'generated_at': now.isoformat(),
                        'report_type': 'complete_history'  # Flag for template
                    }
                    
                    # Generate HTML report
                    html_report = generate_html_report('monthly_report.html', report_data)
                    
                    # Save report to file
                    report_filename = f"{company.company_name.replace(' ', '_')}_Complete_History_{now.strftime('%Y%m%d_%H%M%S')}_report.html"
                    report_folder = os.path.join(
                        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 
                        'static', 
                        'reports'
                    )
                    os.makedirs(report_folder, exist_ok=True)
                    report_path = os.path.join(report_folder, report_filename)
                    
                    with open(report_path, 'w', encoding='utf-8') as f:
                        f.write(html_report)
                    
                    logger.info(f"Report saved to: {report_path}")
                    print(f"[INFO] Report saved to: {report_path}")
                    
                    # Send email with report
                    email_sent = send_complete_report_email(
                        company=company,
                        user=user,
                        stats=stats,
                        report_filename=report_filename
                    )
                    
                    if email_sent:
                        reports_generated += 1
                    else:
                        reports_failed += 1
                        
                except Exception as e:
                    logger.error(f"Failed to generate report for company {company.id}: {str(e)}")
                    import traceback
                    traceback.print_exc()
                    reports_failed += 1
                    continue
            
            logger.info(f"Report generation completed. Generated: {reports_generated}, Failed: {reports_failed}")
            print(f"[SUCCESS] Report generation completed. Generated: {reports_generated}, Failed: {reports_failed}")
            
            return {
                'status': 'success',
                'reports_generated': reports_generated,
                'reports_failed': reports_failed,
                'report_period': 'All Time (Complete History)'
            }
            
        except Exception as e:
            logger.error(f"Report generation failed: {str(e)}")
            print(f"[ERROR] Report generation failed: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                'status': 'failed',
                'error': str(e)
            }


def get_company_all_time_stats(company_id):
    """
    Get ALL TIME statistics for a company (not date-filtered)
    This retrieves all historical data from the database
    """
    from backend.models.drive import Drive
    from backend.models.application import Application
    from backend.models.placement import Placement
    
    # Get ALL drives for this company
    drives = Drive.query.filter_by(company_id=company_id).all()
    drive_ids = [drive.id for drive in drives]
    
    if not drive_ids:
        return {
            'total_drives': 0,
            'total_applications': 0,
            'applications_by_status': {},
            'total_placements': 0,
            'total_salary_offered': 0,
            'average_salary': 0
        }
    
    # Get ALL applications for this company's drives
    applications = Application.query.filter(Application.drive_id.in_(drive_ids)).all()
    
    # Get ALL placements for this company
    placements = Placement.query.filter_by(company_id=company_id).all()
    
    # Calculate statistics
    applications_by_status = {}
    for app in applications:
        status = app.status
        applications_by_status[status] = applications_by_status.get(status, 0) + 1
    
    total_salary = sum(p.salary for p in placements)
    
    stats = {
        'total_drives': len(drives),
        'total_applications': len(applications),
        'applications_by_status': applications_by_status,
        'shortlisted': applications_by_status.get('shortlisted', 0),
        'interview': applications_by_status.get('interview', 0),
        'selected': applications_by_status.get('selected', 0),
        'rejected': applications_by_status.get('rejected', 0),
        'applied': applications_by_status.get('applied', 0),
        'total_placements': len(placements),
        'total_salary_offered': total_salary,
        'average_salary': total_salary / len(placements) if placements else 0
    }
    
    logger.info(f"Stats for company {company_id}: {stats}")
    return stats


def send_complete_report_email(company, user, stats, report_filename):
    """Send complete history report email to company"""
    try:
        from backend.services.email_service import send_email
        
        subject = f"Complete Placement History Report - {company.company_name}"
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #0d6efd;">📊 Complete Placement History Report</h2>
                
                <p>Dear {company.company_name} Team,</p>
                
                <p>Your complete placement history report is now available.</p>
                
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h3>Summary Statistics (All Time)</h3>
                    <p><strong>Total Drives:</strong> {stats['total_drives']}</p>
                    <p><strong>Total Applications:</strong> {stats['total_applications']}</p>
                    <p><strong>Shortlisted:</strong> {stats['shortlisted']}</p>
                    <p><strong>Interviews:</strong> {stats['interview']}</p>
                    <p><strong>Selected:</strong> {stats['selected']}</p>
                    <p><strong>Placements:</strong> {stats['total_placements']}</p>
                    <p><strong>Total Salary Offered:</strong> ₹{stats['total_salary_offered']:,}</p>
                </div>
                
                <p>Please log in to the admin dashboard to view and download the full report.</p>
                
                <p>Thank you for using Placement Portal V2!</p>
                
                <hr style="border: 1px solid #dee2e6; margin: 20px 0;">
                <p style="color: #6c757d; font-size: 12px;">
                    This is an automated message from Placement Portal V2.<br>
                    Please do not reply to this email.
                </p>
            </div>
        </body>
        </html>
        """
        
        text_body = f"""
        Complete Placement History Report
        
        Dear {company.company_name} Team,
        
        Your complete placement history report is now available.
        
        Summary Statistics (All Time):
        - Total Drives: {stats['total_drives']}
        - Total Applications: {stats['total_applications']}
        - Shortlisted: {stats['shortlisted']}
        - Interviews: {stats['interview']}
        - Selected: {stats['selected']}
        - Placements: {stats['total_placements']}
        - Total Salary Offered: ₹{stats['total_salary_offered']:,}
        
        Please log in to the admin dashboard to view and download the full report.
        
        Thank you for using Placement Portal V2!
        
        --
        Placement Portal V2
        """
        
        # Send email
        email_sent = send_email(
            to=user.email,
            subject=subject,
            html_body=html_body,
            text_body=text_body
        )
        
        logger.info(f"Complete report email sent to {user.email}")
        return email_sent
        
    except Exception as e:
        logger.error(f"Failed to send complete report email to {user.email}: {str(e)}")
        return False

def get_company_monthly_stats(company_id, month_start, month_end):
    """Get monthly statistics for a company"""
    from backend.models.drive import Drive
    from backend.models.application import Application
    from backend.models.placement import Placement
    
    # Get drives for this company
    drives = Drive.query.filter_by(company_id=company_id).all()
    drive_ids = [drive.id for drive in drives]
    
    if not drive_ids:
        return {
            'total_drives': 0,
            'total_applications': 0,
            'applications_by_status': {},
            'total_placements': 0,
            'total_salary_offered': 0
        }
    
    # Get applications for this month
    applications = Application.query.filter(
        Application.drive_id.in_(drive_ids),
        Application.application_date >= month_start,
        Application.application_date <= month_end
    ).all()
    
    # Get placements for this month
    placements = Placement.query.filter(
        Placement.company_id == company_id,
        Placement.placement_date >= month_start,
        Placement.placement_date <= month_end
    ).all()
    
    # Calculate statistics
    applications_by_status = {}
    for app in applications:
        status = app.status
        applications_by_status[status] = applications_by_status.get(status, 0) + 1
    
    total_salary = sum(p.salary for p in placements)
    
    stats = {
        'total_drives': len(drives),
        'total_applications': len(applications),
        'applications_by_status': applications_by_status,
        'shortlisted': applications_by_status.get('shortlisted', 0),
        'interview': applications_by_status.get('interview', 0),
        'selected': applications_by_status.get('selected', 0),
        'rejected': applications_by_status.get('rejected', 0),
        'total_placements': len(placements),
        'total_salary_offered': total_salary,
        'average_salary': total_salary / len(placements) if placements else 0
    }
    
    return stats


def send_monthly_report_email(company, user, stats, report_period, report_path):
    """Send monthly report email to company"""
    try:
        from backend.services.email_service import send_email
        
        subject = f"Monthly Placement Report - {report_period}"
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #0d6efd;">📊 Monthly Placement Report</h2>
                
                <p>Dear {company.company_name} Team,</p>
                
                <p>Here is your placement activity report for {report_period}:</p>
                
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h3>Summary Statistics</h3>
                    <p><strong>Total Drives:</strong> {stats['total_drives']}</p>
                    <p><strong>Total Applications:</strong> {stats['total_applications']}</p>
                    <p><strong>Shortlisted:</strong> {stats['shortlisted']}</p>
                    <p><strong>Interviews:</strong> {stats['interview']}</p>
                    <p><strong>Selected:</strong> {stats['selected']}</p>
                    <p><strong>Placements:</strong> {stats['total_placements']}</p>
                    <p><strong>Total Salary Offered:</strong> ₹{stats['total_salary_offered']:,}</p>
                </div>
                
                <p>Your detailed report is available in the admin dashboard.</p>
                
                <p>Thank you for using Placement Portal V2!</p>
                
                <hr style="border: 1px solid #dee2e6; margin: 20px 0;">
                <p style="color: #6c757d; font-size: 12px;">
                    This is an automated message from Placement Portal V2.<br>
                    Please do not reply to this email.
                </p>
            </div>
        </body>
        </html>
        """
        
        text_body = f"""
        Monthly Placement Report - {report_period}
        
        Dear {company.company_name} Team,
        
        Here is your placement activity report for {report_period}:
        
        Summary Statistics:
        - Total Drives: {stats['total_drives']}
        - Total Applications: {stats['total_applications']}
        - Shortlisted: {stats['shortlisted']}
        - Interviews: {stats['interview']}
        - Selected: {stats['selected']}
        - Placements: {stats['total_placements']}
        - Total Salary Offered: ₹{stats['total_salary_offered']:,}
        
        Your detailed report is available in the admin dashboard.
        
        Thank you for using Placement Portal V2!
        
        --
        Placement Portal V2
        """
        
        # Send email
        email_sent = send_email(
            to=user.email,
            subject=subject,
            html_body=html_body,
            text_body=text_body
        )
        
        logger.info(f"Monthly report email sent to {user.email}")
        return email_sent
        
    except Exception as e:
        logger.error(f"Failed to send monthly report email to {user.email}: {str(e)}")
        return False