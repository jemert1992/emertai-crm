from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class ProjectUpdate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    update_type = db.Column(db.String(50), default='progress')  # progress, milestone, issue, next_steps, requirement_change
    status_before = db.Column(db.String(50))
    status_after = db.Column(db.String(50))
    progress_percentage = db.Column(db.Integer, default=0)  # 0-100
    next_steps = db.Column(db.Text)
    blockers = db.Column(db.Text)
    estimated_completion = db.Column(db.Date)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    attachments = db.relationship('ProjectUpdateAttachment', backref='update', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<ProjectUpdate {self.title}>'

    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'title': self.title,
            'description': self.description,
            'update_type': self.update_type,
            'status_before': self.status_before,
            'status_after': self.status_after,
            'progress_percentage': self.progress_percentage,
            'next_steps': self.next_steps,
            'blockers': self.blockers,
            'estimated_completion': self.estimated_completion.isoformat() if self.estimated_completion else None,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'attachments': [att.to_dict() for att in self.attachments]
        }

class ProjectUpdateAttachment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    update_id = db.Column(db.Integer, db.ForeignKey('project_update.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_type = db.Column(db.String(50))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ProjectUpdateAttachment {self.filename}>'

    def to_dict(self):
        return {
            'id': self.id,
            'update_id': self.update_id,
            'filename': self.filename,
            'file_path': self.file_path,
            'file_type': self.file_type,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

