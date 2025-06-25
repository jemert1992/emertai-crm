from flask import Blueprint, jsonify, request
from src.models.requirement import ProjectRequirement, db
from datetime import datetime

requirement_bp = Blueprint('requirement', __name__)

@requirement_bp.route('/requirements', methods=['GET'])
def get_requirements():
    project_id = request.args.get('project_id')
    status = request.args.get('status')
    priority = request.args.get('priority')
    assigned_user_id = request.args.get('assigned_user_id')
    
    query = ProjectRequirement.query
    if project_id:
        query = query.filter_by(project_id=project_id)
    if status:
        query = query.filter_by(status=status)
    if priority:
        query = query.filter_by(priority=priority)
    if assigned_user_id:
        query = query.filter_by(assigned_user_id=assigned_user_id)
    
    requirements = query.order_by(ProjectRequirement.created_at.desc()).all()
    return jsonify([req.to_dict() for req in requirements])

@requirement_bp.route('/requirements', methods=['POST'])
def create_requirement():
    data = request.json
    requirement = ProjectRequirement(
        project_id=data['project_id'],
        title=data['title'],
        description=data.get('description'),
        priority=data.get('priority', 'medium'),
        status=data.get('status', 'pending'),
        category=data.get('category'),
        acceptance_criteria=data.get('acceptance_criteria'),
        estimated_hours=data.get('estimated_hours'),
        assigned_user_id=data.get('assigned_user_id'),
        due_date=datetime.fromisoformat(data['due_date']).date() if data.get('due_date') else None,
        created_by=data['created_by']
    )
    db.session.add(requirement)
    db.session.commit()
    return jsonify(requirement.to_dict()), 201

@requirement_bp.route('/requirements/<int:req_id>', methods=['GET'])
def get_requirement(req_id):
    requirement = ProjectRequirement.query.get_or_404(req_id)
    return jsonify(requirement.to_dict())

@requirement_bp.route('/requirements/<int:req_id>', methods=['PUT'])
def update_requirement(req_id):
    requirement = ProjectRequirement.query.get_or_404(req_id)
    data = request.json
    
    requirement.title = data.get('title', requirement.title)
    requirement.description = data.get('description', requirement.description)
    requirement.priority = data.get('priority', requirement.priority)
    requirement.status = data.get('status', requirement.status)
    requirement.category = data.get('category', requirement.category)
    requirement.acceptance_criteria = data.get('acceptance_criteria', requirement.acceptance_criteria)
    requirement.estimated_hours = data.get('estimated_hours', requirement.estimated_hours)
    requirement.assigned_user_id = data.get('assigned_user_id', requirement.assigned_user_id)
    
    if data.get('due_date'):
        requirement.due_date = datetime.fromisoformat(data['due_date']).date()
    
    # Mark as completed if status changed to completed
    if data.get('status') == 'completed' and requirement.status != 'completed':
        requirement.completed_at = datetime.utcnow()
    elif data.get('status') != 'completed':
        requirement.completed_at = None
    
    db.session.commit()
    return jsonify(requirement.to_dict())

@requirement_bp.route('/requirements/<int:req_id>', methods=['DELETE'])
def delete_requirement(req_id):
    requirement = ProjectRequirement.query.get_or_404(req_id)
    db.session.delete(requirement)
    db.session.commit()
    return '', 204

@requirement_bp.route('/projects/<int:project_id>/requirements', methods=['GET'])
def get_project_requirements(project_id):
    requirements = ProjectRequirement.query.filter_by(project_id=project_id).order_by(ProjectRequirement.priority.desc(), ProjectRequirement.created_at.desc()).all()
    return jsonify([req.to_dict() for req in requirements])

@requirement_bp.route('/projects/<int:project_id>/requirements/summary', methods=['GET'])
def get_project_requirements_summary(project_id):
    requirements = ProjectRequirement.query.filter_by(project_id=project_id).all()
    
    total = len(requirements)
    completed = len([r for r in requirements if r.status == 'completed'])
    in_progress = len([r for r in requirements if r.status == 'in_progress'])
    pending = len([r for r in requirements if r.status == 'pending'])
    blocked = len([r for r in requirements if r.status == 'blocked'])
    
    # Priority breakdown
    high_priority = len([r for r in requirements if r.priority in ['high', 'critical']])
    
    return jsonify({
        'total_requirements': total,
        'completed': completed,
        'in_progress': in_progress,
        'pending': pending,
        'blocked': blocked,
        'high_priority': high_priority,
        'completion_percentage': (completed / total * 100) if total > 0 else 0
    })

