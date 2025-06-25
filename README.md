# Emert.ai CRM - Client & Project Management System

A modern, sleek CRM and Quote Builder application built specifically for Emert.ai's AI-forward business operations. This system provides comprehensive client management, enhanced project task tracking, quote generation, and business analytics.

## 🚀 Features

### Enhanced Project Task Management
- **Detailed Progress Tracking**: Visual progress bars for requirements and tasks
- **Next Steps Visibility**: Always know what needs to be done next
- **Blocker Management**: Track and resolve issues preventing progress
- **Requirements Tracking**: Organize project requirements by priority and category
- **Time Logging**: Track actual hours worked vs estimates
- **Project Updates**: Regular progress updates with status changes

### Core CRM Functionality
- **Client Management**: Comprehensive client profiles and relationship tracking
- **Project Lifecycle**: From proposal to completion with detailed status tracking
- **Quote Builder**: Professional quote generation with templates
- **Communication Logs**: Track all client interactions and project communications
- **Analytics Dashboard**: Business insights and performance metrics

### Modern Design
- **AI-Inspired UI**: Clean, professional design with Emert.ai branding
- **Responsive Layout**: Works seamlessly on desktop and mobile
- **Teal Color Scheme**: Matches Emert.ai's brand identity
- **Intuitive Navigation**: Collapsible sidebar with smooth animations

## 🛠️ Technology Stack

### Backend
- **Flask**: Python web framework
- **SQLAlchemy**: Database ORM
- **SQLite**: Database (easily upgradeable to PostgreSQL)
- **Flask-CORS**: Cross-origin resource sharing

### Frontend
- **React**: Modern JavaScript framework
- **Vite**: Fast build tool and development server
- **Tailwind CSS**: Utility-first CSS framework
- **shadcn/ui**: High-quality React components
- **Lucide Icons**: Beautiful icon library
- **React Router**: Client-side routing

## 📁 Project Structure

```
emert-crm/
├── backend/                 # Flask backend application
│   ├── src/
│   │   ├── models/         # Database models
│   │   ├── routes/         # API endpoints
│   │   ├── static/         # Built frontend files
│   │   ├── database/       # SQLite database
│   │   └── main.py         # Flask application entry point
│   ├── venv/               # Python virtual environment
│   └── requirements.txt    # Python dependencies
├── frontend/               # React frontend application
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   └── App.jsx         # Main application component
│   ├── dist/               # Built frontend files
│   └── package.json        # Node.js dependencies
├── README.md               # This file
├── .gitignore              # Git ignore rules
└── render.yaml             # Render deployment configuration
```

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd emert-crm
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python src/main.py
   ```

3. **Frontend Development** (Optional - for development only)
   ```bash
   cd frontend
   pnpm install
   pnpm run dev
   ```

The application will be available at `http://localhost:5000`

### Production Deployment

The application is configured for easy deployment to Render.com:

1. **Push to GitHub**
2. **Connect to Render**
3. **Deploy automatically**

See the [Deployment Guide](#deployment-guide) below for detailed instructions.

## 📊 API Documentation

The backend provides a comprehensive REST API for all CRM operations:

### Core Endpoints
- `GET /api/clients` - List all clients
- `GET /api/projects` - List all projects
- `GET /api/tasks` - List all tasks
- `GET /api/quotes` - List all quotes
- `GET /api/analytics/dashboard` - Dashboard metrics

### Enhanced Project Management
- `GET /api/requirements` - Project requirements
- `GET /api/project-updates` - Project progress updates
- `GET /api/projects/{id}/next-steps` - Get next steps for a project
- `GET /api/projects/{id}/status-overview` - Comprehensive project status

### Task Management
- `GET /api/tasks/{id}/time-logs` - Task time tracking
- `PUT /api/tasks/{id}/progress` - Update task progress
- `GET /api/projects/{id}/tasks/kanban` - Kanban board data

## 🎯 Use Cases

### Document Analyzer Project Example
Perfect for tracking AI development projects like document analyzers:

1. **Requirements**: "PDF parsing module", "OCR functionality", "API integration"
2. **Progress Updates**: Regular status updates with completion percentages
3. **Task Breakdown**: Specific development tasks with time estimates
4. **Blocker Tracking**: Issues like "Waiting for client sample documents"
5. **Next Steps**: Always visible priorities like "Implement OCR testing"

### Website Redesign Projects
Ideal for web development projects:

1. **Design Phase**: Wireframes, mockups, client approval
2. **Development Phase**: Frontend, backend, testing
3. **Launch Phase**: Deployment, training, handover

## 🔧 Configuration

### Environment Variables
- `FLASK_ENV`: Set to `production` for deployment
- `DATABASE_URL`: Database connection string (optional, defaults to SQLite)

### Database
The application uses SQLite by default, which is perfect for small to medium businesses. For larger deployments, easily upgrade to PostgreSQL by updating the database URL.

## 🚀 Deployment Guide

### GitHub Setup
1. Create a new repository on GitHub
2. Push your code:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

### Render Deployment
1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Use these settings:
   - **Build Command**: `cd backend && pip install -r requirements.txt`
   - **Start Command**: `cd backend && python src/main.py`
   - **Environment**: Python 3.11+

The application will be automatically deployed and available at your Render URL.

## 📈 Scaling

The application is designed to scale with your business:

- **Database**: Easily upgrade from SQLite to PostgreSQL
- **File Storage**: Add cloud storage for document uploads
- **Authentication**: Integrate with OAuth providers
- **Email Integration**: Connect with Gmail/Outlook APIs
- **Payment Processing**: Add Stripe integration for invoicing

## 🤝 Contributing

This CRM system is specifically designed for Emert.ai's workflow and requirements. For customizations or enhancements, please follow the existing code patterns and maintain the modern, clean design aesthetic.

## 📄 License

Proprietary software for Emert.ai. All rights reserved.

---

Built with ❤️ by Manus AI for Emert.ai's modern business operations.

