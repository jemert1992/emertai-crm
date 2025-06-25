from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    requirement_id = db.Column(db.Integer, db.ForeignKey('project_requirement.id'))  # Link to requirement
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default='todo')  # todo, in_progress, completed, blocked, cancelled
    priority = db.Column(db.String(20), default='medium')  # low, medium, high, critical
    category = db.Column(db.String(100))  # development, testing, design, research, documentation
    assigned_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    due_date = db.Column(db.Date)
    estimated_hours = db.Column(db.Integer)
    actual_hours = db.Column(db.Integer)
    progress_percentage = db.Column(db.Integer, default=0)  # 0-100
    blockers = db.Column(db.Text)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    
    # Relationships
    time_logs = db.relationship('TaskTimeLog', backref='task', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Task {self.title}>'

    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'requirement_id': self.requirement_id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'category': self.category,
            'assigned_user_id': self.assigned_user_id,
            'created_by': self.created_by,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'estimated_hours': self.estimated_hours,
            'actual_hours': self.actual_hours,
            'progress_percentage': self.progress_percentage,
            'blockers': self.blockers,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'time_logs': [log.to_dict() for log in self.time_logs]
        }

class TaskTimeLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    description = db.Column(db.Text)
    hours_worked = db.Column(db.Numeric(4, 2), nullable=False)  # Allow decimal hours
    work_date = db.Column(db.Date, default=datetime.utcnow().date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<TaskTimeLog {self.hours_worked}h on {self.work_date}>'

    def to_dict(self):
        return {
            'id': self.id,
            'task_id': self.task_id,
            'user_id': self.user_id,
            'description': self.description,
            'hours_worked': float(self.hours_worked) if self.hours_worked else 0,
            'work_date': self.work_date.isoformat() if self.work_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

