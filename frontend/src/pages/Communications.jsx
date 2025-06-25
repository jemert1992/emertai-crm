import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { MessageSquare } from 'lucide-react'

export default function Communications() {
  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-foreground">Communications</h1>
        <p className="text-muted-foreground">Track client communications and project updates.</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <MessageSquare className="h-5 w-5 mr-2 text-primary" />
            Communication Logs
          </CardTitle>
          <CardDescription>
            Email integration and communication timeline.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">Communication management interface coming soon...</p>
        </CardContent>
      </Card>
    </div>
  )
}

