# app/models/log.py
from app.db import db
import datetime

class DocumentationLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    log_type = db.Column(db.String(50), nullable=False) # e.g., 'Update', 'Issue', 'Maintenance'
    details = db.Column(db.Text, nullable=False)
    project_details = db.Column(db.Text, nullable=True) # Optional field for project context

    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat() + 'Z',
            'log_type': self.log_type,
            'details': self.details,
            'project_details': self.project_details
        }