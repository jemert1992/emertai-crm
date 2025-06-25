import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card'
import { CheckSquare, Clock, AlertCircle, User } from 'lucide-react'

const Tasks = () => {
  const [tasks, setTasks] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchTasks()
  }, [])

  const fetchTasks = async () => {
    try {
      const response = await fetch('/api/tasks')
      const data = await response.json()
      setTasks(data)
    } catch (error) {
      console.error('Error fetching tasks:', error)
    } finally {
      setLoading(false)
    }
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed': return 'bg-green-100 text-green-800'
      case 'in_progress': return 'bg-blue-100 text-blue-800'
      case 'todo': return 'bg-gray-100 text-gray-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high': return 'text-red-600'
      case 'medium': return 'text-yellow-600'
      case 'low': return 'text-green-600'
      default: return 'text-gray-600'
    }
  }

  const getPriorityIcon = (priority) => {
    switch (priority) {
      case 'high': return AlertCircle
      case 'medium': return Clock
      case 'low': return CheckSquare
      default: return CheckSquare
    }
  }

  if (loading) {
    return <div className="flex items-center justify-center h-64">Loading tasks...</div>
  }

  const groupedTasks = {
    todo: tasks.filter(task => task.status === 'todo'),
    in_progress: tasks.filter(task => task.status === 'in_progress'),
    completed: tasks.filter(task => task.status === 'completed')
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Tasks</h1>
        <p className="text-gray-600 mt-1">Track and manage tasks across all your projects.</p>
      </div>

      {/* Kanban Board */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* To Do */}
        <div>
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            To Do ({groupedTasks.todo.length})
          </h2>
          <div className="space-y-3">
            {groupedTasks.todo.map(task => {
              const PriorityIcon = getPriorityIcon(task.priority)
              return (
                <Card key={task.id} className="hover:shadow-md transition-shadow">
                  <CardContent className="p-4">
                    <div className="flex items-start justify-between mb-2">
                      <h3 className="font-medium text-gray-900">{task.title}</h3>
                      <PriorityIcon className={`w-4 h-4 ${getPriorityColor(task.priority)}`} />
                    </div>
                    {task.description && (
                      <p className="text-sm text-gray-600 mb-3">{task.description}</p>
                    )}
                    <div className="flex items-center justify-between text-xs text-gray-500">
                      <span>{task.project}</span>
                      {task.assigned_to && (
                        <div className="flex items-center">
                          <User className="w-3 h-3 mr-1" />
                          {task.assigned_to}
                        </div>
                      )}
                    </div>
                  </CardContent>
                </Card>
              )
            })}
            {groupedTasks.todo.length === 0 && (
              <div className="text-center py-8 text-gray-500">
                No tasks to do
              </div>
            )}
          </div>
        </div>

        {/* In Progress */}
        <div>
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            In Progress ({groupedTasks.in_progress.length})
          </h2>
          <div className="space-y-3">
            {groupedTasks.in_progress.map(task => {
              const PriorityIcon = getPriorityIcon(task.priority)
              return (
                <Card key={task.id} className="hover:shadow-md transition-shadow border-l-4 border-blue-500">
                  <CardContent className="p-4">
                    <div className="flex items-start justify-between mb-2">
                      <h3 className="font-medium text-gray-900">{task.title}</h3>
                      <PriorityIcon className={`w-4 h-4 ${getPriorityColor(task.priority)}`} />
                    </div>
                    {task.description && (
                      <p className="text-sm text-gray-600 mb-3">{task.description}</p>
                    )}
                    <div className="flex items-center justify-between text-xs text-gray-500">
                      <span>{task.project}</span>
                      {task.assigned_to && (
                        <div className="flex items-center">
                          <User className="w-3 h-3 mr-1" />
                          {task.assigned_to}
                        </div>
                      )}
                    </div>
                  </CardContent>
                </Card>
              )
            })}
            {groupedTasks.in_progress.length === 0 && (
              <div className="text-center py-8 text-gray-500">
                No tasks in progress
              </div>
            )}
          </div>
        </div>

        {/* Completed */}
        <div>
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            Completed ({groupedTasks.completed.length})
          </h2>
          <div className="space-y-3">
            {groupedTasks.completed.map(task => {
              const PriorityIcon = getPriorityIcon(task.priority)
              return (
                <Card key={task.id} className="hover:shadow-md transition-shadow border-l-4 border-green-500 opacity-75">
                  <CardContent className="p-4">
                    <div className="flex items-start justify-between mb-2">
                      <h3 className="font-medium text-gray-900 line-through">{task.title}</h3>
                      <CheckSquare className="w-4 h-4 text-green-600" />
                    </div>
                    {task.description && (
                      <p className="text-sm text-gray-600 mb-3">{task.description}</p>
                    )}
                    <div className="flex items-center justify-between text-xs text-gray-500">
                      <span>{task.project}</span>
                      {task.assigned_to && (
                        <div className="flex items-center">
                          <User className="w-3 h-3 mr-1" />
                          {task.assigned_to}
                        </div>
                      )}
                    </div>
                  </CardContent>
                </Card>
              )
            })}
            {groupedTasks.completed.length === 0 && (
              <div className="text-center py-8 text-gray-500">
                No completed tasks
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default Tasks

