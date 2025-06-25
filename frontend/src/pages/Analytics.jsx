import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { BarChart3 } from 'lucide-react'

export default function Analytics() {
  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-foreground">Analytics</h1>
        <p className="text-muted-foreground">Insights and metrics for your business performance.</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <BarChart3 className="h-5 w-5 mr-2 text-primary" />
            Business Analytics
          </CardTitle>
          <CardDescription>
            Revenue tracking, project pipeline, and performance metrics.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">Analytics dashboard coming soon...</p>
        </CardContent>
      </Card>
    </div>
  )
}

