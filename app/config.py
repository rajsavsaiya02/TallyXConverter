# app/config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'a_hard_to_guess_string')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///../instance/app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Hardcoded as per requirement, but sourced from config for best practice.
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin@123')