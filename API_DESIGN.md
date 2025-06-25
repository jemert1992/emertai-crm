# Emert.ai CRM API Design

## Database Schema

### Users
- id (Primary Key)
- username (String, unique)
- email (String, unique)
- password_hash (String)
- role (String: 'admin', 'team_member')
- created_at (DateTime)

### Clients
- id (Primary Key)
- company_name (String)
- contact_name (String)
- email (String)
- phone (String)
- address (Text)
- industry (String)
- notes (Text)
- created_at (DateTime)
- updated_at (DateTime)

### Projects
- id (Primary Key)
- client_id (Foreign Key -> Clients)
- name (String)
- description (Text)
- status (String: 'proposal', 'active', 'completed', 'cancelled')
- service_type (String: 'website_redesign', 'seo', 'ai_bot', 'document_analyzer', 'custom')
- start_date (Date)
- end_date (Date)
- budget (Decimal)
- assigned_user_id (Foreign Key -> Users)
- created_at (DateTime)
- updated_at (DateTime)

### Tasks
- id (Primary Key)
- project_id (Foreign Key -> Projects)
- title (String)
- description (Text)
- status (String: 'todo', 'in_progress', 'completed')
- assigned_user_id (Foreign Key -> Users)
- due_date (Date)
- created_at (DateTime)
- updated_at (DateTime)

### Quotes
- id (Primary Key)
- client_id (Foreign Key -> Clients)
- project_id (Foreign Key -> Projects, nullable)
- quote_number (String, unique)
- title (String)
- description (Text)
- total_amount (Decimal)
- status (String: 'draft', 'sent', 'viewed', 'accepted', 'rejected')
- valid_until (Date)
- created_at (DateTime)
- updated_at (DateTime)

### Quote_Items
- id (Primary Key)
- quote_id (Foreign Key -> Quotes)
- service_name (String)
- description (Text)
- quantity (Integer)
- unit_price (Decimal)
- total_price (Decimal)

### Communications
- id (Primary Key)
- client_id (Foreign Key -> Clients)
- project_id (Foreign Key -> Projects, nullable)
- user_id (Foreign Key -> Users)
- type (String: 'email', 'call', 'meeting', 'note')
- subject (String)
- content (Text)
- created_at (DateTime)

### Documents
- id (Primary Key)
- project_id (Foreign Key -> Projects, nullable)
- quote_id (Foreign Key -> Quotes, nullable)
- filename (String)
- file_path (String)
- file_type (String)
- uploaded_by (Foreign Key -> Users)
- created_at (DateTime)

## API Endpoints

### Authentication
- POST /api/auth/login
- POST /api/auth/logout
- GET /api/auth/me

### Clients
- GET /api/clients - List all clients
- POST /api/clients - Create new client
- GET /api/clients/{id} - Get client details
- PUT /api/clients/{id} - Update client
- DELETE /api/clients/{id} - Delete client
- GET /api/clients/{id}/projects - Get client projects
- GET /api/clients/{id}/quotes - Get client quotes
- GET /api/clients/{id}/communications - Get client communications

### Projects
- GET /api/projects - List all projects
- POST /api/projects - Create new project
- GET /api/projects/{id} - Get project details
- PUT /api/projects/{id} - Update project
- DELETE /api/projects/{id} - Delete project
- GET /api/projects/{id}/tasks - Get project tasks
- POST /api/projects/{id}/tasks - Create new task

### Tasks
- GET /api/tasks - List all tasks
- POST /api/tasks - Create new task
- GET /api/tasks/{id} - Get task details
- PUT /api/tasks/{id} - Update task
- DELETE /api/tasks/{id} - Delete task

### Quotes
- GET /api/quotes - List all quotes
- POST /api/quotes - Create new quote
- GET /api/quotes/{id} - Get quote details
- PUT /api/quotes/{id} - Update quote
- DELETE /api/quotes/{id} - Delete quote
- POST /api/quotes/{id}/items - Add quote item
- PUT /api/quotes/{id}/items/{item_id} - Update quote item
- DELETE /api/quotes/{id}/items/{item_id} - Delete quote item
- POST /api/quotes/{id}/send - Send quote to client
- GET /api/quotes/{id}/pdf - Generate quote PDF

### Communications
- GET /api/communications - List all communications
- POST /api/communications - Create new communication
- GET /api/communications/{id} - Get communication details
- PUT /api/communications/{id} - Update communication
- DELETE /api/communications/{id} - Delete communication

### Analytics
- GET /api/analytics/dashboard - Get dashboard metrics
- GET /api/analytics/revenue - Get revenue data
- GET /api/analytics/pipeline - Get pipeline data

### Documents
- POST /api/documents/upload - Upload document
- GET /api/documents/{id} - Download document
- DELETE /api/documents/{id} - Delete document



## Enhanced Project Task Management API Endpoints

### Project Requirements
- GET /api/requirements - List all requirements (with filters)
- POST /api/requirements - Create new requirement
- GET /api/requirements/{id} - Get requirement details
- PUT /api/requirements/{id} - Update requirement
- DELETE /api/requirements/{id} - Delete requirement
- GET /api/projects/{id}/requirements - Get project requirements
- GET /api/projects/{id}/requirements/summary - Get requirements summary

### Project Updates
- GET /api/project-updates - List all project updates
- POST /api/project-updates - Create new project update
- GET /api/project-updates/{id} - Get project update details
- PUT /api/project-updates/{id} - Update project update
- DELETE /api/project-updates/{id} - Delete project update
- GET /api/projects/{id}/updates - Get project updates
- GET /api/projects/{id}/updates/latest - Get latest project update
- GET /api/projects/{id}/next-steps - Get project next steps
- GET /api/projects/{id}/status-overview - Get comprehensive project status

### Enhanced Task Management
- GET /api/tasks/{id}/time-logs - Get task time logs
- POST /api/tasks/{id}/time-logs - Create time log entry
- PUT /api/tasks/{id}/progress - Update task progress
- GET /api/projects/{id}/tasks/kanban - Get tasks in Kanban format

## Enhanced Data Models

### ProjectRequirement
- id, project_id, title, description
- priority (low, medium, high, critical)
- status (pending, in_progress, completed, blocked)
- category (functional, technical, design, business)
- acceptance_criteria, estimated_hours
- assigned_user_id, due_date
- created_by, created_at, updated_at, completed_at

### ProjectUpdate
- id, project_id, title, description
- update_type (progress, milestone, issue, next_steps, requirement_change)
- status_before, status_after
- progress_percentage (0-100)
- next_steps, blockers, estimated_completion
- created_by, created_at

### Enhanced Task Model
- Added: requirement_id, priority, category, created_by
- Added: estimated_hours, actual_hours, progress_percentage
- Added: blockers, notes, started_at, completed_at
- Added: time_logs relationship

### TaskTimeLog
- id, task_id, user_id, description
- hours_worked, work_date, created_at

## Key Features for Document Analyzer Project Example

1. **Requirements Tracking**: Create requirements like "Data extraction module", "PDF parsing capability", "API integration"
2. **Progress Updates**: Regular updates with current status, next steps, and blockers
3. **Task Management**: Break down requirements into specific tasks with time tracking
4. **Status Overview**: Get comprehensive view of where the project stands
5. **Next Steps**: Always know what needs to be done next
6. **Blocker Management**: Track and resolve issues that prevent progress

