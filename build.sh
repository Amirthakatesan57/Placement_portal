#!/usr/bin/env bash
# Exit on error
set -o errexit

# 1. Install dependencies
pip install -r requirements.txt

# 2. Run database setup scripts
python scripts/init_db.py
python scripts/create_admin.py

# Optional: Comment this out if you don't want fake test data in your live app
# python scripts/seed_demo_data.py
