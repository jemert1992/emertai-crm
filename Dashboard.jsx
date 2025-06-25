import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { 
  Users, 
  FolderOpen, 
  FileText, 
  CheckSquare, 
  DollarSign, 
  TrendingUp,
  Clock,
  AlertCircle,
  Plus
} from 'lucide-react'

export default function Dashboard() {
  const [metrics, setMetrics] = useState({
    total_clients: 0,
    total_projects: 0,
    active_projects: 0,
    total_quotes: 0,
    pending_quotes: 0,
    total_tasks: 0,
    completed_tasks: 0,
    in_progress_tasks: 0,
    total_revenue: 0,
    task_completion_rate: 0
  })

  const [recentActivity, setRecentActivity] = useState([])

  useEffect(() => {
    // Fetch dashboard metrics
    fetch('http://localhost:5000/api/analytics/dashboard')
      .then(res => res.json())
      .then(data => setMetrics(data))
      .catch(err => console.error('Error fetching metrics:', err))

    // Mock recent activity for now
    setRecentActivity([
      { id: 1, type: 'project', message: 'Document Analyzer project updated', time: '2 hours ago' },
      { id: 2, type: 'quote', message: 'New quote sent to TechCorp', time: '4 hours ago' },
      { id: 3, type: 'task', message: 'API integration task completed', time: '6 hours ago' },
      { id: 4, type: 'client', message: 'New client added: StartupXYZ', time: '1 day ago' },
    ])
  }, [])

  const statCards = [
    {
      title: 'Total Clients',
      value: metrics.total_clients,
      icon: Users,
      description: 'Active client relationships',
      color: 'text-blue-600'
    },
    {
      title: 'Active Projects',
      value: `${metrics.active_projects}/${metrics.total_projects}`,
      icon: FolderOpen,
      description: 'Projects in progress',
      color: 'text-green-600'
    },
    {
      title: 'Pending Quotes',
      value: metrics.pending_quotes,
      icon: FileText,
      description: 'Awaiting client response',
      color: 'text-orange-600'
    },
    {
      title: 'Total Revenue',
      value: `$${metrics.total_revenue.toLocaleString()}`,
      icon: DollarSign,
      description: 'From accepted quotes',
      color: 'text-emerald-600'
    }
  ]

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Dashboard</h1>
          <p className="text-muted-foreground">Welcome back! Here's what's happening with your projects.</p>
        </div>
        <div className="flex space-x-2">
          <Button>
            <Plus className="h-4 w-4 mr-2" />
            New Project
          </Button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statCards.map((stat, index) => (
          <Card key={index} className="hover:shadow-lg transition-shadow">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">{stat.title}</CardTitle>
              <stat.icon className={`h-4 w-4 ${stat.color}`} />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stat.value}</div>
              <p className="text-xs text-muted-foreground">{stat.description}</p>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Task Progress */}
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle className="flex items-center">
              <CheckSquare className="h-5 w-5 mr-2 text-primary" />
              Task Progress
            </CardTitle>
            <CardDescription>
              Overall task completion across all projects
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium">Completion Rate</span>
              <span className="text-sm text-muted-foreground">
                {metrics.completed_tasks}/{metrics.total_tasks} tasks
              </span>
            </div>
            <Progress value={metrics.task_completion_rate} className="h-2" />
            
            <div className="grid grid-cols-3 gap-4 mt-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-green-600">{metrics.completed_tasks}</div>
                <div className="text-xs text-muted-foreground">Completed</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-blue-600">{metrics.in_progress_tasks}</div>
                <div className="text-xs text-muted-foreground">In Progress</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-orange-600">
                  {metrics.total_tasks - metrics.completed_tasks - metrics.in_progress_tasks}
                </div>
                <div className="text-xs text-muted-foreground">To Do</div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Recent Activity */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Clock className="h-5 w-5 mr-2 text-primary" />
              Recent Activity
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {recentActivity.map((activity) => (
                <div key={activity.id} className="flex items-start space-x-3">
                  <div className="flex-shrink-0">
                    {activity.type === 'project' && <FolderOpen className="h-4 w-4 text-blue-600" />}
                    {activity.type === 'quote' && <FileText className="h-4 w-4 text-green-600" />}
                    {activity.type === 'task' && <CheckSquare className="h-4 w-4 text-orange-600" />}
                    {activity.type === 'client' && <Users className="h-4 w-4 text-purple-600" />}
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-foreground">{activity.message}</p>
                    <p className="text-xs text-muted-foreground">{activity.time}</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Quick Actions */}
      <Card>
        <CardHeader>
          <CardTitle>Quick Actions</CardTitle>
          <CardDescription>Common tasks to get you started</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Button variant="outline" className="h-20 flex-col space-y-2">
              <Users className="h-6 w-6" />
              <span>Add New Client</span>
            </Button>
            <Button variant="outline" className="h-20 flex-col space-y-2">
              <FolderOpen className="h-6 w-6" />
              <span>Create Project</span>
            </Button>
            <Button variant="outline" className="h-20 flex-col space-y-2">
              <FileText className="h-6 w-6" />
              <span>Generate Quote</span>
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

