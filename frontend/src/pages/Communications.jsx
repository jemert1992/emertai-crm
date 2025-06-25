import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card'
import { MessageSquare, Mail, Phone, Calendar, User } from 'lucide-react'

const Communications = () => {
  const [communications, setCommunications] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchCommunications()
  }, [])

  const fetchCommunications = async () => {
    try {
      const response = await fetch('/api/communications')
      const data = await response.json()
      setCommunications(data)
    } catch (error) {
      console.error('Error fetching communications:', error)
    } finally {
      setLoading(false)
    }
  }

  const getTypeIcon = (type) => {
    switch (type) {
      case 'email': return Mail
      case 'call': return Phone
      case 'meeting': return Calendar
      default: return MessageSquare
    }
  }

  const getTypeColor = (type) => {
    switch (type) {
      case 'email': return 'text-blue-600 bg-blue-50'
      case 'call': return 'text-green-600 bg-green-50'
      case 'meeting': return 'text-purple-600 bg-purple-50'
      default: return 'text-gray-600 bg-gray-50'
    }
  }

  if (loading) {
    return <div className="flex items-center justify-center h-64">Loading communications...</div>
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Communications</h1>
        <p className="text-gray-600 mt-1">Track all client communications and project updates.</p>
      </div>

      {/* Communications List */}
      <div className="space-y-4">
        {communications.length === 0 ? (
          <Card>
            <CardContent className="text-center py-12">
              <MessageSquare className="w-12 h-12 mx-auto text-gray-400 mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No communications yet</h3>
              <p className="text-gray-600">Communication logs will appear here.</p>
            </CardContent>
          </Card>
        ) : (
          communications.map(comm => {
            const TypeIcon = getTypeIcon(comm.type)
            return (
              <Card key={comm.id} className="hover:shadow-md transition-shadow">
                <CardContent className="p-6">
                  <div className="flex items-start space-x-4">
                    <div className={`p-2 rounded-full ${getTypeColor(comm.type)}`}>
                      <TypeIcon className="w-5 h-5" />
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center justify-between mb-2">
                        <h3 className="font-semibold text-gray-900">
                          {comm.subject || `${comm.type.charAt(0).toUpperCase() + comm.type.slice(1)} with ${comm.client}`}
                        </h3>
                        <span className="text-sm text-gray-500">
                          {new Date(comm.date).toLocaleDateString()}
                        </span>
                      </div>
                      <div className="flex items-center space-x-4 mb-3 text-sm text-gray-600">
                        <div className="flex items-center">
                          <User className="w-4 h-4 mr-1" />
                          {comm.client}
                        </div>
                        {comm.project && (
                          <div>
                            Project: {comm.project}
                          </div>
                        )}
                        <div className="capitalize">
                          {comm.type}
                        </div>
                      </div>
                      <p className="text-gray-700">{comm.content}</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )
          })
        )}
      </div>
    </div>
  )
}

export default Communications

