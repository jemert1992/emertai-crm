from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class ProjectRequirement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    priority = db.Column(db.String(20), default='medium')  # low, medium, high, critical
    status = db.Column(db.String(50), default='pending')  # pending, in_progress, completed, blocked
    category = db.Column(db.String(100))  # functional, technical, design, business
    acceptance_criteria = db.Column(db.Text)
    estimated_hours = db.Column(db.Integer)
    assigned_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    due_date = db.Column(db.Date)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = db.Column(db.DateTime)

    def __repr__(self):
        return f'<ProjectRequirement {self.title}>'

    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'status': self.status,
            'category': self.category,
            'acceptance_criteria': self.acceptance_criteria,
            'estimated_hours': self.estimated_hours,
            'assigned_user_id': self.assigned_user_id,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

