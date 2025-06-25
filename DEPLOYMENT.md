# Emert.ai CRM Deployment Guide

This comprehensive guide will walk you through deploying your Emert.ai CRM application to GitHub and Render.com for production use.

## Prerequisites

Before starting the deployment process, ensure you have:

- A GitHub account
- A Render.com account (free tier available)
- Git installed on your local machine
- The completed CRM application files

## Project Structure Overview

Your CRM application is structured as a full-stack application with the React frontend built and integrated into the Flask backend for single-service deployment:

```
emert-crm/
├── backend/                 # Flask backend (main deployment target)
│   ├── src/
│   │   ├── models/         # Database models (User, Client, Project, etc.)
│   │   ├── routes/         # API endpoints
│   │   ├── static/         # Built React frontend files
│   │   ├── database/       # SQLite database
│   │   └── main.py         # Flask application entry point
│   ├── venv/               # Python virtual environment (excluded from git)
│   └── requirements.txt    # Python dependencies
├── frontend/               # React frontend source (for development)
│   ├── src/               # React source code
│   ├── dist/              # Built files (copied to backend/src/static/)
│   └── package.json       # Node.js dependencies
├── README.md              # Project documentation
├── .gitignore             # Git ignore rules
└── render.yaml            # Render deployment configuration
```

## Step 1: Prepare for GitHub

### 1.1 Initialize Git Repository

Navigate to your project root directory and initialize a Git repository:

```bash
cd emert-crm
git init
```

### 1.2 Add Files to Git

Add all project files to the Git repository:

```bash
git add .
git commit -m "Initial commit: Emert.ai CRM application with enhanced project task management"
```

### 1.3 Create GitHub Repository

1. Go to [GitHub.com](https://github.com) and sign in to your account
2. Click the "+" icon in the top right corner
3. Select "New repository"
4. Fill in the repository details:
   - **Repository name**: `emert-crm` (or your preferred name)
   - **Description**: "Modern CRM and Quote Builder for Emert.ai with enhanced project task management"
   - **Visibility**: Choose Private (recommended for business applications)
   - **Do NOT** initialize with README, .gitignore, or license (we already have these)

5. Click "Create repository"

### 1.4 Connect Local Repository to GitHub

After creating the GitHub repository, connect your local repository:

```bash
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/emert-crm.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

## Step 2: Deploy to Render

### 2.1 Create Render Account

1. Go to [Render.com](https://render.com)
2. Sign up for a free account (you can use your GitHub account for easy integration)
3. Verify your email address

### 2.2 Connect GitHub Repository

1. In your Render dashboard, click "New +"
2. Select "Web Service"
3. Choose "Connect a repository"
4. If this is your first time, you'll need to connect your GitHub account:
   - Click "Connect GitHub"
   - Authorize Render to access your repositories
   - Select the repositories you want to give Render access to (or all repositories)

5. Find and select your `emert-crm` repository
6. Click "Connect"

### 2.3 Configure Deployment Settings

Render will automatically detect that this is a Python application. Configure the following settings:

#### Basic Settings
- **Name**: `emert-crm` (or your preferred service name)
- **Region**: Choose the region closest to your users
- **Branch**: `main`
- **Root Directory**: Leave empty (uses repository root)

#### Build & Deploy Settings
- **Runtime**: `Python 3.11.x` (or latest available)
- **Build Command**: 
  ```bash
  cd backend && pip install -r requirements.txt
  ```
- **Start Command**: 
  ```bash
  cd backend && python src/main.py
  ```

#### Advanced Settings
- **Auto-Deploy**: Yes (recommended - deploys automatically when you push to GitHub)

### 2.4 Environment Variables

Set the following environment variables in Render:

1. Click on "Environment" in the left sidebar
2. Add these variables:
   - **FLASK_ENV**: `production`
   - **PORT**: `5000` (Render will override this automatically)

### 2.5 Deploy

1. Click "Create Web Service"
2. Render will begin the deployment process
3. You can monitor the build logs in real-time
4. The initial deployment typically takes 2-5 minutes

### 2.6 Verify Deployment

Once deployment is complete:

1. Render will provide you with a URL (e.g., `https://emert-crm.onrender.com`)
2. Click the URL to access your deployed CRM application
3. Test the main functionality:
   - Dashboard loads correctly
   - Navigation works
   - Projects page shows the enhanced task management features
   - API endpoints respond correctly

## Step 3: Post-Deployment Configuration

### 3.1 Custom Domain (Optional)

If you want to use a custom domain:

1. In your Render service dashboard, go to "Settings"
2. Scroll down to "Custom Domains"
3. Click "Add Custom Domain"
4. Enter your domain name
5. Follow the DNS configuration instructions provided by Render

### 3.2 SSL Certificate

Render automatically provides SSL certificates for all deployments, including custom domains. Your application will be accessible via HTTPS.

### 3.3 Database Considerations

The application currently uses SQLite, which is perfect for getting started. For production scaling:

#### Upgrade to PostgreSQL (Recommended for high-traffic applications)

1. In Render, create a new PostgreSQL database:
   - Click "New +" → "PostgreSQL"
   - Choose your preferred settings
   - Note the connection string

2. Update your Flask application to use PostgreSQL:
   - Add `psycopg2-binary` to `requirements.txt`
   - Update the database URL in `main.py`
   - Redeploy the application

#### SQLite Limitations
- SQLite works well for small to medium applications
- Data persists between deployments
- Consider PostgreSQL for applications with high concurrency or large datasets

## Step 4: Ongoing Maintenance

### 4.1 Automatic Deployments

With auto-deploy enabled, your application will automatically update when you push changes to GitHub:

```bash
# Make your changes
git add .
git commit -m "Add new feature or fix"
git push origin main
```

Render will automatically detect the changes and redeploy your application.

### 4.2 Monitoring

Render provides built-in monitoring:

1. **Logs**: View application logs in real-time
2. **Metrics**: Monitor CPU, memory, and response times
3. **Health Checks**: Automatic health monitoring
4. **Alerts**: Set up notifications for issues

### 4.3 Scaling

As your business grows, you can easily scale your application:

1. **Vertical Scaling**: Upgrade to higher-tier plans for more CPU/memory
2. **Horizontal Scaling**: Add multiple instances (available on paid plans)
3. **Database Scaling**: Upgrade to larger PostgreSQL instances

## Step 5: Development Workflow

### 5.1 Local Development

For ongoing development:

```bash
# Backend development
cd backend
source venv/bin/activate
python src/main.py

# Frontend development (optional)
cd frontend
pnpm run dev
```

### 5.2 Building and Deploying Changes

When you make frontend changes:

```bash
# Build the frontend
cd frontend
pnpm run build

# Copy to backend static directory
cp -r dist/* ../backend/src/static/

# Commit and push
git add .
git commit -m "Update frontend"
git push origin main
```

The application will automatically redeploy on Render.

## Troubleshooting

### Common Issues and Solutions

#### Build Failures
- **Issue**: Python dependencies fail to install
- **Solution**: Check `requirements.txt` for correct package versions
- **Check**: Ensure Python version compatibility

#### Application Won't Start
- **Issue**: Flask application fails to start
- **Solution**: Check the start command and ensure `main.py` is in the correct location
- **Check**: Review application logs in Render dashboard

#### Frontend Not Loading
- **Issue**: React application shows blank page
- **Solution**: Ensure frontend files are properly built and copied to `backend/src/static/`
- **Check**: Verify the Flask static file serving configuration

#### Database Issues
- **Issue**: Database tables not created
- **Solution**: The application automatically creates tables on first run
- **Check**: Ensure database permissions and SQLite file location

#### API Endpoints Not Working
- **Issue**: Frontend can't connect to backend API
- **Solution**: Verify CORS is properly configured in Flask
- **Check**: Ensure API endpoints are correctly defined and accessible

### Getting Help

If you encounter issues:

1. **Check Render Logs**: Most issues are visible in the deployment logs
2. **Review GitHub Repository**: Ensure all files are properly committed
3. **Test Locally**: Verify the application works in your local environment
4. **Render Documentation**: Comprehensive guides available at [docs.render.com](https://docs.render.com)

## Security Considerations

### Production Security Checklist

- [ ] **Secret Key**: Update Flask secret key for production
- [ ] **Database Security**: Use strong passwords for PostgreSQL
- [ ] **HTTPS**: Ensure all traffic uses HTTPS (automatic with Render)
- [ ] **Environment Variables**: Store sensitive data in environment variables
- [ ] **Input Validation**: Validate all user inputs
- [ ] **Authentication**: Implement proper user authentication (future enhancement)

### Recommended Security Enhancements

1. **User Authentication**: Add login/logout functionality
2. **Role-Based Access**: Implement admin vs. team member permissions
3. **API Rate Limiting**: Prevent abuse of API endpoints
4. **Data Encryption**: Encrypt sensitive client data
5. **Backup Strategy**: Regular database backups
6. **Monitoring**: Set up security monitoring and alerts

## Performance Optimization

### Frontend Optimization
- **Code Splitting**: Implement lazy loading for React components
- **Asset Optimization**: Compress images and optimize bundle size
- **Caching**: Implement proper browser caching strategies

### Backend Optimization
- **Database Indexing**: Add indexes for frequently queried fields
- **Query Optimization**: Optimize database queries for better performance
- **Caching**: Implement Redis for session and data caching
- **CDN**: Use a CDN for static assets

## Backup and Recovery

### Database Backup
- **SQLite**: Regular file backups of the database
- **PostgreSQL**: Automated backups available through Render
- **Export Functionality**: Implement data export features in the application

### Code Backup
- **GitHub**: Your code is automatically backed up in GitHub
- **Multiple Repositories**: Consider maintaining a private backup repository
- **Version Tags**: Use Git tags for release versions

## Conclusion

Your Emert.ai CRM application is now successfully deployed and ready for production use. The enhanced project task management features provide excellent visibility into project progress, requirements completion, and next steps - exactly what you requested for tracking projects like the Document Analyzer.

The deployment architecture is scalable and maintainable, allowing you to easily add new features and handle growing business needs. With automatic deployments from GitHub and Render's reliable infrastructure, you can focus on growing your business while the CRM handles your client and project management needs.

Remember to regularly update your application with new features and security patches, and monitor the performance metrics to ensure optimal user experience for you and your business partner.

