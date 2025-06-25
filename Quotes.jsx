import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { FileText } from 'lucide-react'

export default function Quotes() {
  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-foreground">Quotes</h1>
        <p className="text-muted-foreground">Generate and manage professional quotes and proposals.</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <FileText className="h-5 w-5 mr-2 text-primary" />
            Quote Builder
          </CardTitle>
          <CardDescription>
            Drag-and-drop quote editor with templates and PDF generation.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">Quote builder interface coming soon...</p>
        </CardContent>
      </Card>
    </div>
  )
}

