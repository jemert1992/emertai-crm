from flask import Blueprint, jsonify, request
from src.models.project import Project, db
from src.models.task import Task
from datetime import datetime

project_bp = Blueprint('project', __name__)

@project_bp.route('/projects', methods=['GET'])
def get_projects():
    status = request.args.get('status')
    if status:
        projects = Project.query.filter_by(status=status).all()
    else:
        projects = Project.query.all()
    return jsonify([project.to_dict() for project in projects])

@project_bp.route('/projects', methods=['POST'])
def create_project():
    data = request.json
    project = Project(
        client_id=data['client_id'],
        name=data['name'],
        description=data.get('description'),
        status=data.get('status', 'proposal'),
        service_type=data.get('service_type'),
        start_date=datetime.fromisoformat(data['start_date']).date() if data.get('start_date') else None,
        end_date=datetime.fromisoformat(data['end_date']).date() if data.get('end_date') else None,
        budget=data.get('budget'),
        assigned_user_id=data.get('assigned_user_id')
    )
    db.session.add(project)
    db.session.commit()
    return jsonify(project.to_dict()), 201

@project_bp.route('/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    project = Project.query.get_or_404(project_id)
    return jsonify(project.to_dict())

@project_bp.route('/projects/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    project = Project.query.get_or_404(project_id)
    data = request.json
    
    project.name = data.get('name', project.name)
    project.description = data.get('description', project.description)
    project.status = data.get('status', project.status)
    project.service_type = data.get('service_type', project.service_type)
    project.budget = data.get('budget', project.budget)
    project.assigned_user_id = data.get('assigned_user_id', project.assigned_user_id)
    
    if data.get('start_date'):
        project.start_date = datetime.fromisoformat(data['start_date']).date()
    if data.get('end_date'):
        project.end_date = datetime.fromisoformat(data['end_date']).date()
    
    db.session.commit()
    return jsonify(project.to_dict())

@project_bp.route('/projects/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    return '', 204

@project_bp.route('/projects/<int:project_id>/tasks', methods=['GET'])
def get_project_tasks(project_id):
    project = Project.query.get_or_404(project_id)
    tasks = Task.query.filter_by(project_id=project_id).all()
    return jsonify([task.to_dict() for task in tasks])

@project_bp.route('/projects/<int:project_id>/tasks', methods=['POST'])
def create_project_task(project_id):
    project = Project.query.get_or_404(project_id)
    data = request.json
    task = Task(
        project_id=project_id,
        title=data['title'],
        description=data.get('description'),
        status=data.get('status', 'todo'),
        assigned_user_id=data.get('assigned_user_id'),
        due_date=datetime.fromisoformat(data['due_date']).date() if data.get('due_date') else None
    )
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201

