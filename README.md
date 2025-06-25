# Emert.ai CRM - Client & Project Management System

A modern, sleek CRM system built specifically for Emert.ai to manage clients, projects, tasks, quotes, and communications.

## 🚀 Features

### Core CRM Functionality
- **Client Management**: Store and manage client contact information, company details, and relationship history
- **Project Tracking**: Monitor project progress with detailed task management and status tracking
- **Quote Builder**: Create professional quotes with itemized pricing, tax calculations, and client approval workflow
- **Task Management**: Kanban-style task board with priority levels and assignment tracking
- **Communication Logs**: Track all client interactions including emails, calls, meetings, and notes
- **Analytics Dashboard**: Real-time insights into business performance and project metrics

### Enhanced Project Management
- **Progress Tracking**: Visual progress bars and completion percentages
- **Task Organization**: Todo, In Progress, and Completed task columns
- **Client Relationships**: Link projects to specific clients with full contact integration
- **Budget Management**: Track project budgets and financial performance
- **Timeline Management**: Start and end date tracking with visual indicators

### Professional Quote System
- **Itemized Quotes**: Add multiple line items with quantities and unit prices
- **Tax Calculations**: Automatic tax calculation with customizable rates
- **Quote Status**: Draft, Pending, Accepted, Rejected workflow
- **Client Integration**: Automatically pull client information into quotes
- **Professional Formatting**: Clean, professional quote presentation

## 🛠️ Technology Stack

- **Backend**: Flask (Python) with SQLAlchemy ORM
- **Frontend**: React with Tailwind CSS and shadcn/ui components
- **Database**: SQLite (easily upgradeable to PostgreSQL)
- **Deployment**: Optimized for Render.com deployment

## 📦 Project Structure

```
emert-crm/
├── main.py                 # Flask application (single file for simplicity)
├── requirements.txt        # Python dependencies
├── static/                 # Built React frontend
├── database/              # SQLite database (auto-created)
├── frontend/              # React source code
└── README.md              # This file
```

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/emert-crm.git
   cd emert-crm
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:5000`

5. **Initialize sample data**
   Click "Initialize Sample Data" on the dashboard to populate with example clients, projects, and tasks.

### Render Deployment

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy to Render**
   - Go to [render.com](https://render.com)
   - Create new Web Service
   - Connect your GitHub repository
   - Use these settings:
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `python main.py`
     - **Environment**: `FLASK_ENV=production`

3. **Your CRM is live!**
   Access your CRM at the provided Render URL.

## 📊 Sample Data

The application includes sample data featuring:
- **MortgageCorp**: Example client with document processing project
- **TechStartup**: Example client with e-commerce project
- **Sample Tasks**: Various tasks in different stages of completion
- **Sample Quote**: Professional quote example with multiple line items

## 🎯 Perfect For

- **AI Development Agencies**: Track AI projects like document analyzers, chatbots, and automation systems
- **Software Consultancies**: Manage client projects with detailed task tracking
- **Freelancers**: Professional client management and quote generation
- **Small Teams**: Collaborative project management with clear progress visibility

## 🔧 Customization

The application is built with a single-file Flask backend for easy customization:
- Add new fields to models by modifying the SQLAlchemy classes
- Extend the API by adding new routes
- Customize the frontend by modifying React components
- Add new features by extending the existing structure

## 📈 Business Benefits

- **Professional Image**: Impress clients with polished quotes and project tracking
- **Improved Organization**: Never lose track of project status or client communications
- **Better Collaboration**: Clear task assignments and progress visibility for team members
- **Financial Tracking**: Monitor project budgets and quote acceptance rates
- **Time Savings**: Streamlined workflows for common business operations

## 🔒 Security

- Environment-based configuration for production deployment
- CORS enabled for secure frontend-backend communication
- SQLite database with automatic table creation
- Production-ready Flask configuration

## 📞 Support

Built specifically for Emert.ai's business needs. The system is designed to scale with your growing client base and project complexity.

---

**Emert.ai CRM** - Streamline your client relationships and project management with modern, professional tools.

