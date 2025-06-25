import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { CheckSquare } from 'lucide-react'

export default function Tasks() {
  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-foreground">Tasks</h1>
        <p className="text-muted-foreground">Enhanced task management with time tracking and progress monitoring.</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <CheckSquare className="h-5 w-5 mr-2 text-primary" />
            Task Management
          </CardTitle>
          <CardDescription>
            Kanban board, time logging, and detailed task tracking coming soon.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">Enhanced task management interface coming soon...</p>
        </CardContent>
      </Card>
    </div>
  )
}

