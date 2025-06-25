from flask import Blueprint, jsonify, request
from src.models.project_update import ProjectUpdate, ProjectUpdateAttachment, db
from datetime import datetime

project_update_bp = Blueprint('project_update', __name__)

@project_update_bp.route('/project-updates', methods=['GET'])
def get_project_updates():
    project_id = request.args.get('project_id')
    update_type = request.args.get('update_type')
    
    query = ProjectUpdate.query
    if project_id:
        query = query.filter_by(project_id=project_id)
    if update_type:
        query = query.filter_by(update_type=update_type)
    
    updates = query.order_by(ProjectUpdate.created_at.desc()).all()
    return jsonify([update.to_dict() for update in updates])

@project_update_bp.route('/project-updates', methods=['POST'])
def create_project_update():
    data = request.json
    update = ProjectUpdate(
        project_id=data['project_id'],
        title=data['title'],
        description=data.get('description'),
        update_type=data.get('update_type', 'progress'),
        status_before=data.get('status_before'),
        status_after=data.get('status_after'),
        progress_percentage=data.get('progress_percentage', 0),
        next_steps=data.get('next_steps'),
        blockers=data.get('blockers'),
        estimated_completion=datetime.fromisoformat(data['estimated_completion']).date() if data.get('estimated_completion') else None,
        created_by=data['created_by']
    )
    db.session.add(update)
    db.session.commit()
    return jsonify(update.to_dict()), 201

@project_update_bp.route('/project-updates/<int:update_id>', methods=['GET'])
def get_project_update(update_id):
    update = ProjectUpdate.query.get_or_404(update_id)
    return jsonify(update.to_dict())

@project_update_bp.route('/project-updates/<int:update_id>', methods=['PUT'])
def update_project_update(update_id):
    update = ProjectUpdate.query.get_or_404(update_id)
    data = request.json
    
    update.title = data.get('title', update.title)
    update.description = data.get('description', update.description)
    update.update_type = data.get('update_type', update.update_type)
    update.status_before = data.get('status_before', update.status_before)
    update.status_after = data.get('status_after', update.status_after)
    update.progress_percentage = data.get('progress_percentage', update.progress_percentage)
    update.next_steps = data.get('next_steps', update.next_steps)
    update.blockers = data.get('blockers', update.blockers)
    
    if data.get('estimated_completion'):
        update.estimated_completion = datetime.fromisoformat(data['estimated_completion']).date()
    
    db.session.commit()
    return jsonify(update.to_dict())

@project_update_bp.route('/project-updates/<int:update_id>', methods=['DELETE'])
def delete_project_update(update_id):
    update = ProjectUpdate.query.get_or_404(update_id)
    db.session.delete(update)
    db.session.commit()
    return '', 204

@project_update_bp.route('/projects/<int:project_id>/updates', methods=['GET'])
def get_project_updates_for_project(project_id):
    updates = ProjectUpdate.query.filter_by(project_id=project_id).order_by(ProjectUpdate.created_at.desc()).all()
    return jsonify([update.to_dict() for update in updates])

@project_update_bp.route('/projects/<int:project_id>/updates/latest', methods=['GET'])
def get_latest_project_update(project_id):
    update = ProjectUpdate.query.filter_by(project_id=project_id).order_by(ProjectUpdate.created_at.desc()).first()
    if update:
        return jsonify(update.to_dict())
    return jsonify(None)

@project_update_bp.route('/projects/<int:project_id>/next-steps', methods=['GET'])
def get_project_next_steps(project_id):
    # Get the latest update with next steps
    latest_update = ProjectUpdate.query.filter_by(project_id=project_id).filter(ProjectUpdate.next_steps.isnot(None)).order_by(ProjectUpdate.created_at.desc()).first()
    
    # Get pending requirements
    from src.models.requirement import ProjectRequirement
    pending_requirements = ProjectRequirement.query.filter_by(project_id=project_id, status='pending').order_by(ProjectRequirement.priority.desc()).limit(5).all()
    
    # Get in-progress tasks
    from src.models.task import Task
    in_progress_tasks = Task.query.filter_by(project_id=project_id, status='in_progress').order_by(Task.due_date.asc()).limit(5).all()
    
    return jsonify({
        'latest_next_steps': latest_update.next_steps if latest_update else None,
        'latest_update_date': latest_update.created_at.isoformat() if latest_update else None,
        'pending_requirements': [req.to_dict() for req in pending_requirements],
        'in_progress_tasks': [task.to_dict() for task in in_progress_tasks]
    })

@project_update_bp.route('/projects/<int:project_id>/status-overview', methods=['GET'])
def get_project_status_overview(project_id):
    # Get latest update
    latest_update = ProjectUpdate.query.filter_by(project_id=project_id).order_by(ProjectUpdate.created_at.desc()).first()
    
    # Get requirements summary
    from src.models.requirement import ProjectRequirement
    requirements = ProjectRequirement.query.filter_by(project_id=project_id).all()
    req_completed = len([r for r in requirements if r.status == 'completed'])
    req_total = len(requirements)
    
    # Get tasks summary
    from src.models.task import Task
    tasks = Task.query.filter_by(project_id=project_id).all()
    task_completed = len([t for t in tasks if t.status == 'completed'])
    task_total = len(tasks)
    
    # Get blockers
    current_blockers = []
    if latest_update and latest_update.blockers:
        current_blockers.append({
            'source': 'project_update',
            'description': latest_update.blockers,
            'date': latest_update.created_at.isoformat()
        })
    
    blocked_tasks = Task.query.filter_by(project_id=project_id, status='blocked').all()
    for task in blocked_tasks:
        if task.blockers:
            current_blockers.append({
                'source': 'task',
                'task_title': task.title,
                'description': task.blockers,
                'date': task.updated_at.isoformat()
            })
    
    return jsonify({
        'latest_progress': latest_update.progress_percentage if latest_update else 0,
        'requirements_completion': (req_completed / req_total * 100) if req_total > 0 else 0,
        'tasks_completion': (task_completed / task_total * 100) if task_total > 0 else 0,
        'current_blockers': current_blockers,
        'next_steps': latest_update.next_steps if latest_update else None,
        'estimated_completion': latest_update.estimated_completion.isoformat() if latest_update and latest_update.estimated_completion else None
    })

