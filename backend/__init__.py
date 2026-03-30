"""
Placement Portal Application V2
Backend Application Factory
Milestone 7: Backend Jobs – Celery + Redis
"""

from flask import Flask, app, send_from_directory, jsonify
from backend.config import Config
from backend.extensions import db, init_cache, login_manager, cors, init_celery
import os
import logging
from logging.handlers import RotatingFileHandler

def create_app(config_class=Config):
    """Application factory for creating Flask app"""
    app = Flask(__name__, 
                static_folder='../frontend',
                static_url_path='/frontend')
    app.config.from_object(config_class)
    
    # Configure logging
    if not app.debug:
        file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Placement Portal V2 Startup')
    
    # Ensure instance directory exists
    instance_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'instance')
    if not os.path.exists(instance_dir):
        os.makedirs(instance_dir)
    
    # Ensure logs directory exists
    logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    # Ensure uploads directory exists
    uploads_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static', 'uploads')
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)
    
    # FIX: Ensure exports directory exists (Milestone 7)
    exports_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static', 'exports')
    if not os.path.exists(exports_dir):
        os.makedirs(exports_dir)
    
    # Ensure reports directory exists (Milestone 7)
    reports_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static', 'reports')
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
    
    # Initialize Extensions
    db.init_app(app)
    login_manager.init_app(app)
    cors.init_app(app)
    init_celery(app)
    init_cache(app) 
    
    # Login Manager Configuration
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # Import models AFTER db is initialized (prevents circular imports)
    from backend.models import User, Company, Student, Drive, Application, Placement, AuditLog
    
    # Register Blueprints
    from backend.auth import auth_bp
    app.register_blueprint(auth_bp)
    
    # Register Admin Blueprint (Milestone 3)
    from backend.routes.admin import admin_bp
    app.register_blueprint(admin_bp)
    
    # Register Company Blueprint (Milestone 4)
    from backend.routes.company import company_bp
    app.register_blueprint(company_bp)
    
    # Register Student Blueprint (Milestone 5)
    from backend.routes.student import student_bp
    app.register_blueprint(student_bp)
    
    # Serve frontend index.html
    @app.route('/')
    def serve_frontend():
        return send_from_directory('../frontend', 'index.html')
    
    # FIX: Serve export files (MUST BE BEFORE CATCH-ALL ROUTE) - Milestone 7
    @app.route('/static/exports/<filename>')
    def serve_export_file(filename):
        """Serve CSV export files"""
        exports_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
            'static', 
            'exports'
        )
        
        # Security check - prevent path traversal attacks
        if '..' in filename or filename.startswith('/') or filename.startswith('\\'):
            return jsonify({'error': 'Invalid filename'}), 400
        
        if os.path.exists(os.path.join(exports_dir, filename)):
            return send_from_directory(
                exports_dir, 
                filename, 
                as_attachment=True,
                mimetype='text/csv'
            )
        else:
            return jsonify({'error': 'File not found'}), 404
    
    # Serve frontend for SPA routing (CATCH-ALL ROUTE - MUST BE LAST)
    @app.route('/<path:path>')
    def serve_all_routes(path):
        if path.startswith('api/'):
            return jsonify({'error': 'API route not found', 'path': path}), 404
        return send_from_directory('../frontend', 'index.html')
    
    @app.route('/frontend/<path:filename>')
    def serve_frontend_static(filename):
        return send_from_directory('../frontend', filename)
    
    @app.route('/frontend/css/<path:filename>')
    def serve_css(filename):
        return send_from_directory('../frontend/css', filename)
    
    @app.route('/frontend/js/<path:filename>')
    def serve_js(filename):
        return send_from_directory('../frontend/js', filename)
    
    @app.route('/static/<path:filename>')
    def serve_static(filename):
        return send_from_directory('static', filename)
    
    # Create Database Tables
    with app.app_context():
        db.create_all()
    
    # Health check endpoint - Updated for Milestone 7
    @app.route('/api/health')
    def health_check():
        return jsonify({
            'status': 'healthy', 
            'database': 'connected', 
            'auth': 'enabled',
            'celery': 'configured',
            'redis': 'connected',
            'milestone': '7 - Celery Jobs',
            'version': '2.0.0'
        }), 200
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({'error': 'Not Found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'error': 'Internal Server Error'}), 500
    
    return app