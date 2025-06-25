import os
import sys
# DON'T CHANGE THIS - it's needed for the imports to work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS

# Import database and models
from models.user import db
from models.client import Client
from models.project import Project
from models.task import Task
from models.quote import Quote, QuoteItem
from models.communication import Communication
from models.document import Document
from models.requirement import Requirement
from models.project_update import ProjectUpdate, ProjectUpdateAttachment

from routes.user import user_bp
from routes.client import client_bp
from routes.project import project_bp
from routes.task import task_bp
from routes.quote import quote_bp
from routes.communication import communication_bp
from routes.analytics import analytics_bp
from routes.requirement import requirement_bp
from routes.project_update import project_update_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Database configuration
database_path = os.path.join(os.path.dirname(__file__), 'database', 'app.db')
os.makedirs(os.path.dirname(database_path), exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Enable CORS for all routes
CORS(app)

# Register blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(client_bp, url_prefix='/api')
app.register_blueprint(project_bp, url_prefix='/api')
app.register_blueprint(task_bp, url_prefix='/api')
app.register_blueprint(quote_bp, url_prefix='/api')
app.register_blueprint(communication_bp, url_prefix='/api')
app.register_blueprint(analytics_bp, url_prefix='/api')
app.register_blueprint(requirement_bp, url_prefix='/api')
app.register_blueprint(project_update_bp, url_prefix='/api')

# Create tables
with app.app_context():
    db.create_all()

# Serve React app
@app.route('/')
def serve_react_app():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_react_routes(path):
    # Check if it's an API route
    if path.startswith('api/'):
        return "API endpoint not found", 404
    
    # Check if it's a static file
    if '.' in path:
        try:
            return send_from_directory(app.static_folder, path)
        except:
            return send_from_directory(app.static_folder, 'index.html')
    
    # For all other routes, serve the React app
    try:
        return send_from_directory(app.static_folder, 'index.html')
    except:
        return "index.html not found", 404


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

