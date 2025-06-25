from flask import Blueprint, jsonify, request
from src.models.task import Task, TaskTimeLog, db
from datetime import datetime

task_bp = Blueprint('task', __name__)

@task_bp.route('/tasks', methods=['GET'])
def get_tasks():
    status = request.args.get('status')
    assigned_user_id = request.args.get('assigned_user_id')
    project_id = request.args.get('project_id')
    priority = request.args.get('priority')
    
    query = Task.query
    if status:
        query = query.filter_by(status=status)
    if assigned_user_id:
        query = query.filter_by(assigned_user_id=assigned_user_id)
    if project_id:
        query = query.filter_by(project_id=project_id)
    if priority:
        query = query.filter_by(priority=priority)
    
    tasks = query.order_by(Task.due_date.asc()).all()
    return jsonify([task.to_dict() for task in tasks])

@task_bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    task = Task(
        project_id=data['project_id'],
        requirement_id=data.get('requirement_id'),
        title=data['title'],
        description=data.get('description'),
        status=data.get('status', 'todo'),
        priority=data.get('priority', 'medium'),
        category=data.get('category'),
        assigned_user_id=data.get('assigned_user_id'),
        created_by=data['created_by'],
        due_date=datetime.fromisoformat(data['due_date']).date() if data.get('due_date') else None,
        estimated_hours=data.get('estimated_hours'),
        progress_percentage=data.get('progress_percentage', 0),
        blockers=data.get('blockers'),
        notes=data.get('notes')
    )
    
    # Set started_at if status is in_progress
    if task.status == 'in_progress':
        task.started_at = datetime.utcnow()
    
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201

@task_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    return jsonify(task.to_dict())

@task_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.json
    
    old_status = task.status
    
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.status = data.get('status', task.status)
    task.priority = data.get('priority', task.priority)
    task.category = data.get('category', task.category)
    task.assigned_user_id = data.get('assigned_user_id', task.assigned_user_id)
    task.estimated_hours = data.get('estimated_hours', task.estimated_hours)
    task.actual_hours = data.get('actual_hours', task.actual_hours)
    task.progress_percentage = data.get('progress_percentage', task.progress_percentage)
    task.blockers = data.get('blockers', task.blockers)
    task.notes = data.get('notes', task.notes)
    
    if data.get('due_date'):
        task.due_date = datetime.fromisoformat(data['due_date']).date()
    
    # Handle status changes
    if old_status != task.status:
        if task.status == 'in_progress' and not task.started_at:
            task.started_at = datetime.utcnow()
        elif task.status == 'completed':
            task.completed_at = datetime.utcnow()
            task.progress_percentage = 100
        elif task.status in ['todo', 'blocked']:
            task.completed_at = None
    
    db.session.commit()
    return jsonify(task.to_dict())

@task_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return '', 204

@task_bp.route('/tasks/<int:task_id>/time-logs', methods=['GET'])
def get_task_time_logs(task_id):
    task = Task.query.get_or_404(task_id)
    time_logs = TaskTimeLog.query.filter_by(task_id=task_id).order_by(TaskTimeLog.work_date.desc()).all()
    return jsonify([log.to_dict() for log in time_logs])

@task_bp.route('/tasks/<int:task_id>/time-logs', methods=['POST'])
def create_time_log(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.json
    
    time_log = TaskTimeLog(
        task_id=task_id,
        user_id=data['user_id'],
        description=data.get('description'),
        hours_worked=data['hours_worked'],
        work_date=datetime.fromisoformat(data['work_date']).date() if data.get('work_date') else datetime.utcnow().date()
    )
    
    db.session.add(time_log)
    
    # Update task actual hours
    total_hours = db.session.query(db.func.sum(TaskTimeLog.hours_worked)).filter_by(task_id=task_id).scalar() or 0
    task.actual_hours = int(float(total_hours) + float(data['hours_worked']))
    
    db.session.commit()
    return jsonify(time_log.to_dict()), 201

@task_bp.route('/tasks/<int:task_id>/progress', methods=['PUT'])
def update_task_progress(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.json
    
    task.progress_percentage = data.get('progress_percentage', task.progress_percentage)
    task.notes = data.get('notes', task.notes)
    
    # Auto-update status based on progress
    if task.progress_percentage == 100 and task.status != 'completed':
        task.status = 'completed'
        task.completed_at = datetime.utcnow()
    elif task.progress_percentage > 0 and task.status == 'todo':
        task.status = 'in_progress'
        if not task.started_at:
            task.started_at = datetime.utcnow()
    
    db.session.commit()
    return jsonify(task.to_dict())

@task_bp.route('/projects/<int:project_id>/tasks/kanban', methods=['GET'])
def get_project_tasks_kanban(project_id):
    tasks = Task.query.filter_by(project_id=project_id).all()
    
    kanban_data = {
        'todo': [task.to_dict() for task in tasks if task.status == 'todo'],
        'in_progress': [task.to_dict() for task in tasks if task.status == 'in_progress'],
        'completed': [task.to_dict() for task in tasks if task.status == 'completed'],
        'blocked': [task.to_dict() for task in tasks if task.status == 'blocked']
    }
    
    return jsonify(kanban_data)

