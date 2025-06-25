import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { 
  Plus, 
  FolderOpen, 
  Calendar, 
  User, 
  CheckSquare, 
  AlertCircle,
  Clock,
  FileText,
  MessageSquare,
  TrendingUp
} from 'lucide-react'

export default function Projects() {
  const [projects, setProjects] = useState([])
  const [selectedProject, setSelectedProject] = useState(null)

  useEffect(() => {
    // Mock project data for now
    setProjects([
      {
        id: 1,
        name: 'Document Analyzer for MortgageCorp',
        client: 'MortgageCorp',
        status: 'active',
        service_type: 'ai_bot',
        progress: 65,
        start_date: '2024-01-15',
        end_date: '2024-03-15',
        budget: 25000,
        requirements_completed: 8,
        requirements_total: 12,
        tasks_completed: 15,
        tasks_total: 23,
        next_steps: 'Implement OCR functionality and test with sample documents',
        blockers: 'Waiting for client to provide sample document formats'
      },
      {
        id: 2,
        name: 'E-commerce Website Redesign',
        client: 'RetailPlus',
        status: 'active',
        service_type: 'website_redesign',
        progress: 40,
        start_date: '2024-02-01',
        end_date: '2024-04-01',
        budget: 15000,
        requirements_completed: 5,
        requirements_total: 10,
        tasks_completed: 8,
        tasks_total: 18,
        next_steps: 'Complete wireframes and begin development phase',
        blockers: null
      },
      {
        id: 3,
        name: 'SEO Optimization Campaign',
        client: 'TechStartup',
        status: 'proposal',
        service_type: 'seo',
        progress: 0,
        start_date: '2024-03-01',
        end_date: '2024-06-01',
        budget: 8000,
        requirements_completed: 0,
        requirements_total: 6,
        tasks_completed: 0,
        tasks_total: 0,
        next_steps: 'Awaiting client approval to begin project',
        blockers: null
      }
    ])
  }, [])

  const getStatusColor = (status) => {
    switch (status) {
      case 'active': return 'bg-green-100 text-green-800'
      case 'proposal': return 'bg-yellow-100 text-yellow-800'
      case 'completed': return 'bg-blue-100 text-blue-800'
      case 'cancelled': return 'bg-red-100 text-red-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getServiceTypeLabel = (type) => {
    switch (type) {
      case 'website_redesign': return 'Website Redesign'
      case 'seo': return 'SEO'
      case 'ai_bot': return 'AI Bot Development'
      case 'document_analyzer': return 'Document Analyzer'
      default: return 'Custom'
    }
  }

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Projects</h1>
          <p className="text-muted-foreground">Manage your projects with detailed task tracking and progress monitoring.</p>
        </div>
        <Button>
          <Plus className="h-4 w-4 mr-2" />
          New Project
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Project List */}
        <div className="lg:col-span-2 space-y-4">
          {projects.map((project) => (
            <Card 
              key={project.id} 
              className={`cursor-pointer transition-all hover:shadow-lg ${
                selectedProject?.id === project.id ? 'ring-2 ring-primary' : ''
              }`}
              onClick={() => setSelectedProject(project)}
            >
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div className="space-y-1">
                    <CardTitle className="text-lg">{project.name}</CardTitle>
                    <CardDescription className="flex items-center space-x-2">
                      <User className="h-4 w-4" />
                      <span>{project.client}</span>
                      <Badge variant="secondary">{getServiceTypeLabel(project.service_type)}</Badge>
                    </CardDescription>
                  </div>
                  <Badge className={getStatusColor(project.status)}>
                    {project.status}
                  </Badge>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>Progress</span>
                    <span>{project.progress}%</span>
                  </div>
                  <Progress value={project.progress} className="h-2" />
                </div>

                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <span className="text-muted-foreground">Requirements:</span>
                    <span className="ml-2 font-medium">
                      {project.requirements_completed}/{project.requirements_total}
                    </span>
                  </div>
                  <div>
                    <span className="text-muted-foreground">Tasks:</span>
                    <span className="ml-2 font-medium">
                      {project.tasks_completed}/{project.tasks_total}
                    </span>
                  </div>
                </div>

                <div className="flex items-center justify-between text-sm">
                  <div className="flex items-center text-muted-foreground">
                    <Calendar className="h-4 w-4 mr-1" />
                    {new Date(project.end_date).toLocaleDateString()}
                  </div>
                  <div className="font-medium">
                    ${project.budget.toLocaleString()}
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Project Details */}
        <div className="space-y-4">
          {selectedProject ? (
            <>
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Project Details</CardTitle>
                  <CardDescription>{selectedProject.name}</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-sm text-muted-foreground">Client:</span>
                      <span className="text-sm font-medium">{selectedProject.client}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-muted-foreground">Budget:</span>
                      <span className="text-sm font-medium">${selectedProject.budget.toLocaleString()}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-muted-foreground">Timeline:</span>
                      <span className="text-sm font-medium">
                        {new Date(selectedProject.start_date).toLocaleDateString()} - {new Date(selectedProject.end_date).toLocaleDateString()}
                      </span>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center text-lg">
                    <CheckSquare className="h-5 w-5 mr-2 text-primary" />
                    Next Steps
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground mb-3">
                    {selectedProject.next_steps}
                  </p>
                  {selectedProject.blockers && (
                    <div className="flex items-start space-x-2 p-3 bg-orange-50 rounded-lg">
                      <AlertCircle className="h-4 w-4 text-orange-600 mt-0.5" />
                      <div>
                        <p className="text-sm font-medium text-orange-800">Blocker</p>
                        <p className="text-sm text-orange-700">{selectedProject.blockers}</p>
                      </div>
                    </div>
                  )}
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Progress Overview</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span>Requirements</span>
                      <span>{selectedProject.requirements_completed}/{selectedProject.requirements_total}</span>
                    </div>
                    <Progress 
                      value={(selectedProject.requirements_completed / selectedProject.requirements_total) * 100} 
                      className="h-2" 
                    />
                  </div>
                  
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span>Tasks</span>
                      <span>{selectedProject.tasks_completed}/{selectedProject.tasks_total}</span>
                    </div>
                    <Progress 
                      value={(selectedProject.tasks_completed / selectedProject.tasks_total) * 100} 
                      className="h-2" 
                    />
                  </div>
                </CardContent>
              </Card>

              <div className="space-y-2">
                <Button className="w-full" variant="outline">
                  <FileText className="h-4 w-4 mr-2" />
                  View Requirements
                </Button>
                <Button className="w-full" variant="outline">
                  <CheckSquare className="h-4 w-4 mr-2" />
                  Manage Tasks
                </Button>
                <Button className="w-full" variant="outline">
                  <MessageSquare className="h-4 w-4 mr-2" />
                  Add Update
                </Button>
              </div>
            </>
          ) : (
            <Card>
              <CardContent className="flex items-center justify-center h-64">
                <div className="text-center">
                  <FolderOpen className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                  <p className="text-muted-foreground">Select a project to view details</p>
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  )
}

