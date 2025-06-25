from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    quote_number = db.Column(db.String(50), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    total_amount = db.Column(db.Numeric(10, 2), default=0)
    status = db.Column(db.String(50), default='draft')  # draft, sent, viewed, accepted, rejected
    valid_until = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    items = db.relationship('QuoteItem', backref='quote', lazy=True, cascade='all, delete-orphan')
    documents = db.relationship('Document', backref='quote', lazy=True, cascade='all, delete-orphan')

    def __init__(self, **kwargs):
        super(Quote, self).__init__(**kwargs)
        if not self.quote_number:
            self.quote_number = f"Q-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"

    def __repr__(self):
        return f'<Quote {self.quote_number}>'

    def to_dict(self):
        return {
            'id': self.id,
            'client_id': self.client_id,
            'project_id': self.project_id,
            'quote_number': self.quote_number,
            'title': self.title,
            'description': self.description,
            'total_amount': float(self.total_amount) if self.total_amount else 0,
            'status': self.status,
            'valid_until': self.valid_until.isoformat() if self.valid_until else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'items': [item.to_dict() for item in self.items]
        }

class QuoteItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quote_id = db.Column(db.Integer, db.ForeignKey('quote.id'), nullable=False)
    service_name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    quantity = db.Column(db.Integer, default=1)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)

    def __repr__(self):
        return f'<QuoteItem {self.service_name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'quote_id': self.quote_id,
            'service_name': self.service_name,
            'description': self.description,
            'quantity': self.quantity,
            'unit_price': float(self.unit_price) if self.unit_price else 0,
            'total_price': float(self.total_price) if self.total_price else 0
        }

