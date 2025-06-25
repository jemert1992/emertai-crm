from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Communication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # email, call, meeting, note
    subject = db.Column(db.String(200))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Communication {self.type}: {self.subject}>'

    def to_dict(self):
        return {
            'id': self.id,
            'client_id': self.client_id,
            'project_id': self.project_id,
            'user_id': self.user_id,
            'type': self.type,
            'subject': self.subject,
            'content': self.content,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

