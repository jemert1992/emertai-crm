import os
from flask import Flask, jsonify, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime, date
import json

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'emert-crm-secret-key-2024'

# Database configuration
database_path = os.path.join(os.path.dirname(__file__), 'database', 'app.db')
os.makedirs(os.path.dirname(database_path), exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

# Models
class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    company = db.Column(db.String(100))
    address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    status = db.Column(db.String(50), default='active')
    progress = db.Column(db.Integer, default=0)
    budget = db.Column(db.Numeric(10, 2))
    description = db.Column(db.Text)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    client = db.relationship('Client', backref='projects')

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    status = db.Column(db.String(50), default='todo')
    priority = db.Column(db.String(20), default='medium')
    assigned_to = db.Column(db.String(100))
    due_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    project = db.relationship('Project', backref='tasks')

class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quote_number = db.Column(db.String(50), unique=True, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    project_name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default='draft')
    subtotal = db.Column(db.Numeric(10, 2), default=0)
    tax_rate = db.Column(db.Numeric(5, 2), default=0)
    tax_amount = db.Column(db.Numeric(10, 2), default=0)
    total_amount = db.Column(db.Numeric(10, 2), default=0)
    valid_until = db.Column(db.Date)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    client = db.relationship('Client', backref='quotes')

class QuoteItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quote_id = db.Column(db.Integer, db.ForeignKey('quote.id'))
    description = db.Column(db.String(500), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    
    quote = db.relationship('Quote', backref='items')

class Communication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=True)
    type = db.Column(db.String(50), nullable=False)  # email, call, meeting, note
    subject = db.Column(db.String(200))
    content = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    
    client = db.relationship('Client', backref='communications')
    project = db.relationship('Project', backref='communications')

# API Routes

# Clients
@app.route('/api/clients', methods=['GET'])
def get_clients():
    clients = Client.query.all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'email': c.email,
        'phone': c.phone,
        'company': c.company,
        'address': c.address,
        'project_count': len(c.projects),
        'quote_count': len(c.quotes)
    } for c in clients])

@app.route('/api/clients', methods=['POST'])
def create_client():
    data = request.json
    client = Client(
        name=data['name'],
        email=data.get('email'),
        phone=data.get('phone'),
        company=data.get('company'),
        address=data.get('address')
    )
    db.session.add(client)
    db.session.commit()
    return jsonify({'id': client.id, 'message': 'Client created successfully'})

@app.route('/api/clients/<int:client_id>', methods=['GET'])
def get_client(client_id):
    client = Client.query.get_or_404(client_id)
    return jsonify({
        'id': client.id,
        'name': client.name,
        'email': client.email,
        'phone': client.phone,
        'company': client.company,
        'address': client.address,
        'projects': [{
            'id': p.id,
            'name': p.name,
            'status': p.status,
            'progress': p.progress
        } for p in client.projects],
        'quotes': [{
            'id': q.id,
            'quote_number': q.quote_number,
            'project_name': q.project_name,
            'status': q.status,
            'total_amount': float(q.total_amount)
        } for q in client.quotes]
    })

# Projects
@app.route('/api/projects', methods=['GET'])
def get_projects():
    projects = Project.query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'client': p.client.name if p.client else 'No Client',
        'client_id': p.client_id,
        'status': p.status,
        'progress': p.progress,
        'budget': float(p.budget) if p.budget else 0,
        'description': p.description,
        'start_date': p.start_date.isoformat() if p.start_date else None,
        'end_date': p.end_date.isoformat() if p.end_date else None,
        'task_count': len(p.tasks),
        'completed_tasks': len([t for t in p.tasks if t.status == 'completed'])
    } for p in projects])

@app.route('/api/projects', methods=['POST'])
def create_project():
    data = request.json
    project = Project(
        name=data['name'],
        client_id=data.get('client_id'),
        description=data.get('description'),
        budget=data.get('budget'),
        start_date=datetime.strptime(data['start_date'], '%Y-%m-%d').date() if data.get('start_date') else None,
        end_date=datetime.strptime(data['end_date'], '%Y-%m-%d').date() if data.get('end_date') else None
    )
    db.session.add(project)
    db.session.commit()
    return jsonify({'id': project.id, 'message': 'Project created successfully'})

# Tasks
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    project_id = request.args.get('project_id')
    if project_id:
        tasks = Task.query.filter_by(project_id=project_id).all()
    else:
        tasks = Task.query.all()
    
    return jsonify([{
        'id': t.id,
        'title': t.title,
        'description': t.description,
        'project': t.project.name if t.project else 'No Project',
        'project_id': t.project_id,
        'status': t.status,
        'priority': t.priority,
        'assigned_to': t.assigned_to,
        'due_date': t.due_date.isoformat() if t.due_date else None
    } for t in tasks])

@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.json
    task = Task(
        title=data['title'],
        description=data.get('description'),
        project_id=data.get('project_id'),
        priority=data.get('priority', 'medium'),
        assigned_to=data.get('assigned_to'),
        due_date=datetime.strptime(data['due_date'], '%Y-%m-%d').date() if data.get('due_date') else None
    )
    db.session.add(task)
    db.session.commit()
    return jsonify({'id': task.id, 'message': 'Task created successfully'})

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.json
    
    task.status = data.get('status', task.status)
    task.priority = data.get('priority', task.priority)
    task.assigned_to = data.get('assigned_to', task.assigned_to)
    
    db.session.commit()
    return jsonify({'message': 'Task updated successfully'})

# Quotes
@app.route('/api/quotes', methods=['GET'])
def get_quotes():
    quotes = Quote.query.all()
    return jsonify([{
        'id': q.id,
        'quote_number': q.quote_number,
        'client': q.client.name if q.client else 'No Client',
        'client_id': q.client_id,
        'project_name': q.project_name,
        'status': q.status,
        'total_amount': float(q.total_amount),
        'valid_until': q.valid_until.isoformat() if q.valid_until else None,
        'created_at': q.created_at.isoformat()
    } for q in quotes])

@app.route('/api/quotes', methods=['POST'])
def create_quote():
    data = request.json
    
    # Generate quote number
    quote_count = Quote.query.count() + 1
    quote_number = f"Q{quote_count:04d}"
    
    quote = Quote(
        quote_number=quote_number,
        client_id=data['client_id'],
        project_name=data['project_name'],
        description=data.get('description'),
        tax_rate=data.get('tax_rate', 0),
        valid_until=datetime.strptime(data['valid_until'], '%Y-%m-%d').date() if data.get('valid_until') else None,
        notes=data.get('notes')
    )
    
    db.session.add(quote)
    db.session.flush()  # Get the quote ID
    
    # Add quote items
    subtotal = 0
    for item_data in data.get('items', []):
        total_price = float(item_data['quantity']) * float(item_data['unit_price'])
        item = QuoteItem(
            quote_id=quote.id,
            description=item_data['description'],
            quantity=item_data['quantity'],
            unit_price=item_data['unit_price'],
            total_price=total_price
        )
        db.session.add(item)
        subtotal += total_price
    
    # Calculate totals
    quote.subtotal = subtotal
    quote.tax_amount = subtotal * (float(quote.tax_rate) / 100)
    quote.total_amount = subtotal + quote.tax_amount
    
    db.session.commit()
    return jsonify({'id': quote.id, 'quote_number': quote_number, 'message': 'Quote created successfully'})

@app.route('/api/quotes/<int:quote_id>', methods=['GET'])
def get_quote(quote_id):
    quote = Quote.query.get_or_404(quote_id)
    return jsonify({
        'id': quote.id,
        'quote_number': quote.quote_number,
        'client': {
            'id': quote.client.id,
            'name': quote.client.name,
            'email': quote.client.email,
            'company': quote.client.company,
            'address': quote.client.address
        } if quote.client else None,
        'project_name': quote.project_name,
        'description': quote.description,
        'status': quote.status,
        'subtotal': float(quote.subtotal),
        'tax_rate': float(quote.tax_rate),
        'tax_amount': float(quote.tax_amount),
        'total_amount': float(quote.total_amount),
        'valid_until': quote.valid_until.isoformat() if quote.valid_until else None,
        'notes': quote.notes,
        'created_at': quote.created_at.isoformat(),
        'items': [{
            'id': item.id,
            'description': item.description,
            'quantity': item.quantity,
            'unit_price': float(item.unit_price),
            'total_price': float(item.total_price)
        } for item in quote.items]
    })

@app.route('/api/quotes/<int:quote_id>/status', methods=['PUT'])
def update_quote_status(quote_id):
    quote = Quote.query.get_or_404(quote_id)
    data = request.json
    quote.status = data['status']
    db.session.commit()
    return jsonify({'message': 'Quote status updated successfully'})

# Communications
@app.route('/api/communications', methods=['GET'])
def get_communications():
    client_id = request.args.get('client_id')
    project_id = request.args.get('project_id')
    
    query = Communication.query
    if client_id:
        query = query.filter_by(client_id=client_id)
    if project_id:
        query = query.filter_by(project_id=project_id)
    
    communications = query.order_by(Communication.date.desc()).all()
    
    return jsonify([{
        'id': c.id,
        'client': c.client.name if c.client else 'No Client',
        'project': c.project.name if c.project else None,
        'type': c.type,
        'subject': c.subject,
        'content': c.content,
        'date': c.date.isoformat()
    } for c in communications])

@app.route('/api/communications', methods=['POST'])
def create_communication():
    data = request.json
    communication = Communication(
        client_id=data['client_id'],
        project_id=data.get('project_id'),
        type=data['type'],
        subject=data.get('subject'),
        content=data['content']
    )
    db.session.add(communication)
    db.session.commit()
    return jsonify({'id': communication.id, 'message': 'Communication logged successfully'})

# Analytics
@app.route('/api/analytics/dashboard', methods=['GET'])
def get_dashboard():
    total_clients = Client.query.count()
    total_projects = Project.query.count()
    active_projects = Project.query.filter_by(status='active').count()
    total_tasks = Task.query.count()
    completed_tasks = Task.query.filter_by(status='completed').count()
    total_quotes = Quote.query.count()
    pending_quotes = Quote.query.filter_by(status='pending').count()
    accepted_quotes = Quote.query.filter_by(status='accepted').count()
    
    # Calculate total revenue from accepted quotes
    accepted_quote_objects = Quote.query.filter_by(status='accepted').all()
    total_revenue = sum(float(q.total_amount) for q in accepted_quote_objects)
    
    return jsonify({
        'total_clients': total_clients,
        'total_projects': total_projects,
        'active_projects': active_projects,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'task_completion_rate': (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0,
        'total_quotes': total_quotes,
        'pending_quotes': pending_quotes,
        'accepted_quotes': accepted_quotes,
        'total_revenue': total_revenue,
        'in_progress_tasks': Task.query.filter_by(status='in_progress').count()
    })

# Initialize sample data
@app.route('/api/init-data', methods=['POST'])
def init_sample_data():
    if Client.query.first():
        return jsonify({'message': 'Data already exists'})
    
    # Create sample clients
    client1 = Client(
        name='MortgageCorp',
        email='contact@mortgagecorp.com',
        phone='555-0123',
        company='MortgageCorp Inc.',
        address='123 Finance St, New York, NY 10001'
    )
    
    client2 = Client(
        name='TechStartup',
        email='hello@techstartup.com',
        phone='555-0456',
        company='TechStartup LLC',
        address='456 Innovation Ave, San Francisco, CA 94105'
    )
    
    db.session.add(client1)
    db.session.add(client2)
    db.session.commit()
    
    # Create sample projects
    project1 = Project(
        name='Document Processing System',
        client_id=client1.id,
        status='active',
        progress=65,
        budget=25000,
        description='AI-powered document analysis system for mortgage processing',
        start_date=date(2024, 1, 15),
        end_date=date(2024, 4, 15)
    )
    
    project2 = Project(
        name='E-commerce Website',
        client_id=client2.id,
        status='active',
        progress=40,
        budget=15000,
        description='Modern e-commerce platform with payment integration',
        start_date=date(2024, 2, 1),
        end_date=date(2024, 5, 1)
    )
    
    db.session.add(project1)
    db.session.add(project2)
    db.session.commit()
    
    # Create sample tasks
    tasks = [
        Task(title='PDF parsing module', project_id=project1.id, status='completed', priority='high'),
        Task(title='OCR functionality', project_id=project1.id, status='in_progress', priority='high'),
        Task(title='API integration', project_id=project1.id, status='todo', priority='medium'),
        Task(title='Frontend design', project_id=project2.id, status='completed', priority='high'),
        Task(title='Payment integration', project_id=project2.id, status='in_progress', priority='high'),
        Task(title='Testing and deployment', project_id=project2.id, status='todo', priority='medium')
    ]
    
    for task in tasks:
        db.session.add(task)
    
    # Create sample quote
    quote = Quote(
        quote_number='Q0001',
        client_id=client1.id,
        project_name='Document Processing System',
        description='AI-powered document analysis system for mortgage processing',
        status='accepted',
        tax_rate=8.5,
        valid_until=date(2024, 12, 31),
        notes='Payment terms: 50% upfront, 50% on completion'
    )
    
    db.session.add(quote)
    db.session.flush()
    
    # Add quote items
    quote_items = [
        QuoteItem(quote_id=quote.id, description='System Development', quantity=1, unit_price=20000, total_price=20000),
        QuoteItem(quote_id=quote.id, description='Testing & QA', quantity=1, unit_price=3000, total_price=3000),
        QuoteItem(quote_id=quote.id, description='Deployment & Training', quantity=1, unit_price=2000, total_price=2000)
    ]
    
    for item in quote_items:
        db.session.add(item)
    
    # Calculate quote totals
    quote.subtotal = 25000
    quote.tax_amount = 25000 * 0.085
    quote.total_amount = 25000 + quote.tax_amount
    
    # Create sample communication
    communication = Communication(
        client_id=client1.id,
        project_id=project1.id,
        type='email',
        subject='Project Update - Document Processing System',
        content='Hi team, just wanted to update you on the progress. The PDF parsing module is complete and we are now working on the OCR functionality. Expected completion by end of month.'
    )
    
    db.session.add(communication)
    db.session.commit()
    
    return jsonify({'message': 'Sample data created successfully'})

# Serve React app
@app.route('/')
def serve_react_app():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_react_routes(path):
    if path.startswith('api/'):
        return "API endpoint not found", 404
    
    if '.' in path:
        try:
            return send_from_directory(app.static_folder, path)
        except:
            return send_from_directory(app.static_folder, 'index.html')
    
    try:
        return send_from_directory(app.static_folder, 'index.html')
    except:
        return "index.html not found", 404

# Create tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

