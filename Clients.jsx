import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Plus, Users } from 'lucide-react'

export default function Clients() {
  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Clients</h1>
          <p className="text-muted-foreground">Manage your client relationships and contacts.</p>
        </div>
        <Button>
          <Plus className="h-4 w-4 mr-2" />
          Add Client
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Users className="h-5 w-5 mr-2 text-primary" />
            Client Management
          </CardTitle>
          <CardDescription>
            This page will contain client management features including search, filtering, and detailed client profiles.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">Client management interface coming soon...</p>
        </CardContent>
      </Card>
    </div>
  )
}

