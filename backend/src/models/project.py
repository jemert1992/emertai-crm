from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default='proposal')  # proposal, active, completed, cancelled
    service_type = db.Column(db.String(100))  # website_redesign, seo, ai_bot, document_analyzer, custom
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    budget = db.Column(db.Numeric(10, 2))
    assigned_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tasks = db.relationship('Task', backref='project', lazy=True, cascade='all, delete-orphan')
    quotes = db.relationship('Quote', backref='project', lazy=True)
    communications = db.relationship('Communication', backref='project', lazy=True)
    documents = db.relationship('Document', backref='project', lazy=True, cascade='all, delete-orphan')
    requirements = db.relationship('ProjectRequirement', backref='project', lazy=True, cascade='all, delete-orphan')
    updates = db.relationship('ProjectUpdate', backref='project', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Project {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'client_id': self.client_id,
            'name': self.name,
            'description': self.description,
            'status': self.status,
            'service_type': self.service_type,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'budget': float(self.budget) if self.budget else None,
            'assigned_user_id': self.assigned_user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

