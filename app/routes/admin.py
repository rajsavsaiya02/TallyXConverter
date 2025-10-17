# app/routes/admin.py
from flask import Blueprint, request, jsonify
from app.models.log import DocumentationLog
from app.utils.auth import password_required
from app.db import db

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/log', methods=['POST'])
@password_required
def add_log_entry():
    data = request.get_json()
    if not data or not data.get('log_type') or not data.get('details'):
        return jsonify({"error": "Missing required fields: log_type, details"}), 400

    new_entry = DocumentationLog(
        log_type=data['log_type'],
        details=data['details'],
        project_details=data.get('project_details')
    )
    db.session.add(new_entry)
    db.session.commit()
    return jsonify(new_entry.to_dict()), 201

@admin_bp.route('/log', methods=['GET'])
@password_required
def get_log_entries():
    logs = DocumentationLog.query.order_by(DocumentationLog.timestamp.desc()).all()
    return jsonify([log.to_dict() for log in logs]), 200