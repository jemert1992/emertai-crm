from flask import Blueprint, jsonify
from src.models.client import Client
from src.models.project import Project
from src.models.quote import Quote
from src.models.task import Task
from sqlalchemy import func

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/analytics/dashboard', methods=['GET'])
def get_dashboard_metrics():
    # Basic counts
    total_clients = Client.query.count()
    total_projects = Project.query.count()
    active_projects = Project.query.filter_by(status='active').count()
    total_quotes = Quote.query.count()
    pending_quotes = Quote.query.filter_by(status='sent').count()
    
    # Task statistics
    total_tasks = Task.query.count()
    completed_tasks = Task.query.filter_by(status='completed').count()
    in_progress_tasks = Task.query.filter_by(status='in_progress').count()
    
    # Revenue data
    accepted_quotes = Quote.query.filter_by(status='accepted').all()
    total_revenue = sum(float(quote.total_amount) for quote in accepted_quotes if quote.total_amount)
    
    return jsonify({
        'total_clients': total_clients,
        'total_projects': total_projects,
        'active_projects': active_projects,
        'total_quotes': total_quotes,
        'pending_quotes': pending_quotes,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'in_progress_tasks': in_progress_tasks,
        'total_revenue': total_revenue,
        'task_completion_rate': (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    })

@analytics_bp.route('/analytics/revenue', methods=['GET'])
def get_revenue_data():
    # Revenue by service type
    revenue_by_service = {}
    projects = Project.query.all()
    
    for project in projects:
        service_type = project.service_type or 'Other'
        if service_type not in revenue_by_service:
            revenue_by_service[service_type] = 0
        
        # Get accepted quotes for this project
        accepted_quotes = Quote.query.filter_by(project_id=project.id, status='accepted').all()
        for quote in accepted_quotes:
            if quote.total_amount:
                revenue_by_service[service_type] += float(quote.total_amount)
    
    return jsonify({
        'revenue_by_service': revenue_by_service
    })

@analytics_bp.route('/analytics/pipeline', methods=['GET'])
def get_pipeline_data():
    # Project status distribution
    project_status_counts = {}
    projects = Project.query.all()
    
    for project in projects:
        status = project.status
        if status not in project_status_counts:
            project_status_counts[status] = 0
        project_status_counts[status] += 1
    
    # Quote status distribution
    quote_status_counts = {}
    quotes = Quote.query.all()
    
    for quote in quotes:
        status = quote.status
        if status not in quote_status_counts:
            quote_status_counts[status] = 0
        quote_status_counts[status] += 1
    
    return jsonify({
        'project_status_distribution': project_status_counts,
        'quote_status_distribution': quote_status_counts
    })

