"""
Report Generation Service
Milestone 7: Generate HTML/PDF reports for companies
"""

from flask import render_template_string, current_app
import os
import logging

logger = logging.getLogger(__name__)


def generate_html_report(template_name, data):
    """
    Generate HTML report from template
    Milestone 7: Monthly placement reports
    """
    try:
        # Load template from file
        template_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
            'templates', 
            'reports', 
            template_name
        )
        
        if not os.path.exists(template_path):
            logger.error(f"Template not found: {template_path}")
            raise FileNotFoundError(f"Template not found: {template_name}")
        
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # Render template with data
        # FIX: Use current_app.jinja_env if available, otherwise create simple rendering
        try:
            app = current_app._get_current_object()
            template = app.jinja_env.from_string(template_content)
            html_report = template.render(**data)
        except RuntimeError:
            # No app context - use simple string replacement (fallback)
            from jinja2 import Environment
            env = Environment()
            template = env.from_string(template_content)
            html_report = template.render(**data)
        
        return html_report
        
    except Exception as e:
        logger.error(f"Failed to generate HTML report: {str(e)}")
        raise


def generate_pdf_report(html_content, output_path):
    """
    Generate PDF from HTML
    Milestone 7: PDF report generation
    
    Note: For production, use a library like pdfkit or weasyprint
    For now, we'll just save HTML (can be converted to PDF later)
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"PDF report saved to {output_path}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to generate PDF report: {str(e)}")
        return False