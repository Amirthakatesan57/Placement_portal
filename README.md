#  Placement Portal Application V2

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.x-brightgreen.svg)](https://vuejs.org/)
[![Redis](https://img.shields.io/badge/Redis-5.0+-red.svg)](https://redis.io/)
[![Celery](https://img.shields.io/badge/Celery-5.3.4-orange.svg)](https://docs.celeryq.dev/)
[![SQLite](https://img.shields.io/badge/SQLite-3.x-lightgrey.svg)](https://www.sqlite.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.0-purple.svg)](https://getbootstrap.com/)

> **A comprehensive campus recruitment management system built with Flask (Backend API) and Vue.js (Frontend UI) that connects Admins, Companies, and Students for streamlined placement processes.**

---

##  Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Running the Application](#-running-the-application)
- [Default Credentials](#-default-credentials)
- [Testing](#-testing)
- [Git Commit History](#-git-commit-history)

---

##  Overview

The **Placement Portal Application V2** is a full-stack web application designed to automate and streamline campus recruitment processes for educational institutions. It provides a unified platform for:

- **Admin (Institute Placement Cell)**: Manage companies, students, and placement drives with complete oversight
- **Companies**: Post job drives, review applications, schedule interviews, and manage hiring pipelines
- **Students**: Browse opportunities, apply for drives, track application status, and view placement history

This project demonstrates the features like asynchronous task processing (Celery), caching (Redis), role-based access control, email notifications, CSV exports, and automated reporting.

---

##  Features

###  Admin (Institute Placement Cell)
-  **Dashboard Analytics** - Real-time statistics on students, companies, drives, and applications
-  **Company Management** - Approve/reject company registrations, blacklist/deactivate accounts
-  **Drive Management** - Approve/reject placement drives created by companies
-  **Student Management** - View, search, and manage all student records
-  **Application Tracking** - Monitor all applications across all drives
-  **Monthly Reports** - Generate and view HTML placement reports for companies
-  **Cache Monitoring** - View Redis cache statistics and clear cache manually
-  **Search Functionality** - Search companies and students by various criteria

###  Company
-  **Company Registration** - Self-registration with admin approval workflow
-  **Dashboard Analytics** - View drive statistics, applications, and placements
-  **Drive Creation** - Post new placement drives with job details, eligibility, and deadlines
-  **Application Management** - View, shortlist, reject applicants with feedback
-  **Interview Scheduling** - Schedule interviews with shortlisted candidates
-  **Status Updates** - Update application status (Applied → Shortlisted → Interview → Selected → Rejected)
-  **Drive Status** - Manage drive status (Active/Closed)
-  **CSV Export** - Export application and placement history asynchronously
-  **Email Notifications** - Receive monthly activity reports via email

###  Student
-  **Self Registration** - Create account with complete profile (education, skills, resume)
-  **Resume Upload** - Upload and manage resume (PDF/DOC)
-  **Job Search** - Browse and search approved placement drives by company, position, skills
-  **Application System** - Apply for drives with eligibility validation
-  **Status Tracking** - Real-time application status updates
-  **Interview Schedules** - View upcoming interview schedules
-  **Placement History** - Complete application and placement history
-  **Offer Letters** - Download offer letters for selected positions
-  **CSV Export** - Export personal application and placement history
-  **Email Reminders** - Receive interview reminders via email/GChat

###  Backend Jobs (Celery + Redis)
-  **Daily Interview Reminders** - Automated reminders to students with upcoming interviews (9:00 AM daily)
-  **Monthly Placement Reports** - Generate HTML reports for companies with statistics (1st of every month, 10:00 AM)
-  **CSV Export Jobs** - Asynchronous export of application/placement history with email notifications
-  **Cleanup Old Exports** - Remove old export files older than 7 days (2:00 AM daily)

###  Performance & Caching 
-  **Redis Caching** - Cache frequently accessed endpoints (job listings, searches, stats)
-  **Configurable Expiry** - Different cache expiry policies for different data types
-  **Cache Monitoring** - Admin dashboard for cache hit/miss rates, memory usage
-  **Manual Invalidation** - Clear cache manually when needed
-  **Performance Optimization** - 80-90% faster response times for cached endpoints

---

##  Tech Stack

| Layer | Technology | Version | Purpose |
|-------|------------|---------|---------|
| **Backend Framework** | Flask | 3.0.0 | REST API development |
| **Frontend Framework** | Vue.js | 3.x | Reactive UI components |
| **Database** | SQLite | 3.x | Relational data storage |
| **ORM** | SQLAlchemy | 3.1.1 | Database object mapping |
| **Cache** | Redis | 5.0+ | API response caching |
| **Task Queue** | Celery | 5.3.4 | Async background jobs |
| **Authentication** | Flask-Login | 0.6.3 | Session management |
| **Email** | SMTP (Gmail) | - | Email notifications |
| **Styling** | Bootstrap | 5.3.0 | Responsive UI design |
| **Icons** | Bootstrap Icons | 1.10.0 | UI icons |
| **HTTP Client** | Axios | 1.6.0 | API requests |
| **Routing** | Vue Router | 4.x | Frontend routing |

---

##  Project Structure

```
MAD_2P_Placement-Portal-Application/
├── backend/
│   ├── __init__.py              # Flask app factory
│   ├── config.py                # Configuration settings
│   ├── extensions.py            # Extensions (DB, Celery, Cache)
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── routes.py            # Auth endpoints (login, register, logout)
│   │   └── decorators.py        # Role-based access decorators
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py              # User model (Admin/Company/Student)
│   │   ├── company.py           # Company profile model
│   │   ├── student.py           # Student profile model
│   │   ├── drive.py             # Placement drive model
│   │   ├── application.py       # Application model
│   │   ├── placement.py         # Placement model
│   │   └── audit_log.py         # Audit log model
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── admin.py             # Admin endpoints
│   │   ├── company.py           # Company endpoints
│   │   └── student.py           # Student endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   ├── email_service.py     # Email sending service
│   │   ├── webhook_service.py   # GChat webhook service
│   │   ├── csv_service.py       # CSV generation service
│   │   ├── report_service.py    # HTML/PDF report generation
│   │   └── cache_service.py     # Redis cache service (Milestone 8)
│   ├── tasks/
│   │   ├── __init__.py
│   │   ├── reminders.py         # Interview reminder tasks
│   │   ├── reports.py           # Monthly report tasks
│   │   └── exports.py           # CSV export tasks
│   └── templates/
│       └── reports/
│           └── monthly_report.html  # Monthly report template
├── frontend/
│   ├── index.html               # Entry point (Vue CDN)
│   ├── css/
│   │   └── custom.css           # Custom styles
│   └── js/
│       ├── app.js               # Main Vue app
│       ├── router.js            # Vue Router configuration
│       ├── api.js               # API service layer
│       └── auth.js              # Authentication helper
├── scripts/
│   ├── init_db.py               # Database initialization
│   ├── create_admin.py          # Create admin user
│   ├── seed_demo_data.py        # Seed demo data
│   ├── test_monthly_report.py   # Test monthly report generation
│   ├── test_interview_reminder.py # Test interview reminders
│   └── create_test_data_for_reports.py # Create test data
├── static/
│   ├── exports/                 # CSV export files
│   ├── reports/                 # HTML/PDF reports
│   └── uploads/
│       └── resumes/             # Uploaded resumes
├── instance/
│   └── placement_portal.db      # SQLite database (auto-created)
├── logs/
│   └── app.log                  # Application logs
├── .env                         # Environment variables
├── .gitignore                   # Git ignore rules
├── requirements.txt             # Python dependencies
├── celery_worker.py             # Celery worker entry point
├── run.py                       # Flask app entry point
└── README.md                    # This file
```

---

##  Installation

### Prerequisites

- Python 3.10 or higher
- Redis Server 5.0 or higher
- Git
- Modern web browser (Chrome, Firefox, Edge)

### Step 1: Clone Repository

```bash
git clone https://github.com/23F1002688/MAD_2P_Placement-Portal-Application.git
cd MAD_2P_Placement-Portal-Application
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Install Redis

**Windows (WSL2):**
```bash
wsl
sudo apt update
sudo apt install redis-server -y
sudo service redis-server start
redis-cli ping  # Should return: PONG
```

**Windows (Native):**
- Download from: https://github.com/microsoftarchive/redis/releases
- Extract and run: `redis-server.exe`

**Linux:**
```bash
sudo apt install redis-server
sudo systemctl start redis
```

**Docker:**
```bash
docker run -d -p 6379:6379 --name redis redis:latest
```

### Step 5: Initialize Database

```bash
# Create instance directory
mkdir instance

# Initialize database
python scripts/init_db.py

# Create admin user
python scripts/create_admin.py

# Seed demo data (optional)
python scripts/seed_demo_data.py
```

---

##  Configuration

### Environment Variables (.env)

Create a `.env` file in the project root:

```bash
# Flask Configuration
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-change-in-production

# Database
DATABASE_URI=sqlite:///instance/placement_portal.db

# Redis & Celery Configuration
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP=True

# Email Configuration (Gmail)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com

# Google Chat Webhook (Optional)
GOOGLE_CHAT_WEBHOOK_URL=

# Base URL for email links
BASE_URL=http://localhost:5000

# Export Configuration
EXPORT_FOLDER=static/exports
REPORT_FOLDER=static/reports
EXPORT_RETENTION_DAYS=7
```

### Gmail App Password Setup

1. Go to: https://myaccount.google.com/
2. Enable 2-Factor Authentication
3. Generate App Password: https://myaccount.google.com/apppasswords
4. Select App: **Mail**, Device: **Windows Computer**
5. Copy the 16-character password to `.env`

---

##  Running the Application

### Terminal 1: Start Redis

```bash
# Windows (WSL)
wsl
sudo service redis-server start

# Or native Windows
redis-server

# Verify
redis-cli ping  # Should return: PONG
```

### Terminal 2: Start Celery Worker

```bash
cd placement_portal
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

celery -A celery_worker worker --loglevel=info --pool=solo
```

### Terminal 3: Start Celery Beat (Optional - for scheduled tasks)

```bash
celery -A celery_worker beat --loglevel=info
```

### Terminal 4: Start Flask Application

```bash
python run.py
```

### Access the Application

Open browser: **http://localhost:5000**

---

##  Default Credentials

| Role | Username | Password | Email |
|------|----------|----------|-------|
| **Admin** | `admin` | `Admin@123` | admin@placement.com |
| **Company** | `techcorp` | `Company@123` | hr@techcorp.com |
| **Student** | `student001` | `Student@123` | student001@college.edu |


---

##  Testing

### Test Monthly Report Generation

```bash
python scripts/test_monthly_report.py
```

### Test Interview Reminders

```bash
python scripts/test_interview_reminder.py
```

### Test Cache Performance

1. Login as admin
2. Go to: http://localhost:5000/#/admin/cache_stats
3. Check hit rate, memory usage, keys count

### Test CSV Export

1. Login as student or company
2. Go to History or Placements page
3. Click "Export CSV"
4. Check email for download link

---

##  Git Commit History

```bash
# Milestone 0: Repository Setup
git commit -m "Milestone-0 PPA-V2 Setup"

# Milestone 1: Database Models
git commit -m "Milestone-PPA-V2 DB-Relationship"

# Milestone 2: Authentication
git commit -m "Milestone-PPA-V2 Auth-RBAC"

# Milestone 3: Admin Dashboard
git commit -m "Milestone-PPA-V2 Admin-Dashboard-Management"

# Milestone 4: Company Dashboard
git commit -m "Milestone-PPA-V2 Company-Dashboard-Management"

# Milestone 5: Student Dashboard
git commit -m "Milestone-PPA-V2 Student-Dashboard-Management"

# Milestone 6: Placement Tracking
git commit -m "Milestone-PPA-V2 Placement-Tracking"

# Milestone 7: Celery Jobs
git commit -m "Milestone-PPA-V2 Celery-Jobs"

# Milestone 8: Redis Caching
git commit -m "Milestone-PPA-V2 Redis-Caching"
```

---

<div align="center">

**Built with ❤️ using Flask + Vue.js**

[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.x-brightgreen.svg)](https://vuejs.org/)
[![Redis](https://img.shields.io/badge/Redis-5.0+-red.svg)](https://redis.io/)
[![Celery](https://img.shields.io/badge/Celery-5.3.4-orange.svg)](https://docs.celeryq.dev/)

**Made for Modern Application Development II**

</div>