import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card'
import { Button } from '../components/ui/button'
import { Input } from '../components/ui/input'
import { Textarea } from '../components/ui/textarea'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '../components/ui/dialog'
import { Plus, FileText, Eye, Edit, Trash2, DollarSign } from 'lucide-react'

const Quotes = () => {
  const [quotes, setQuotes] = useState([])
  const [clients, setClients] = useState([])
  const [loading, setLoading] = useState(true)
  const [showCreateDialog, setShowCreateDialog] = useState(false)
  const [selectedQuote, setSelectedQuote] = useState(null)
  const [showViewDialog, setShowViewDialog] = useState(false)

  const [newQuote, setNewQuote] = useState({
    client_id: '',
    project_name: '',
    description: '',
    tax_rate: 8.5,
    valid_until: '',
    notes: '',
    items: [{ description: '', quantity: 1, unit_price: 0 }]
  })

  useEffect(() => {
    fetchQuotes()
    fetchClients()
  }, [])

  const fetchQuotes = async () => {
    try {
      const response = await fetch('/api/quotes')
      const data = await response.json()
      setQuotes(data)
    } catch (error) {
      console.error('Error fetching quotes:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchClients = async () => {
    try {
      const response = await fetch('/api/clients')
      const data = await response.json()
      setClients(data)
    } catch (error) {
      console.error('Error fetching clients:', error)
    }
  }

  const fetchQuoteDetails = async (quoteId) => {
    try {
      const response = await fetch(`/api/quotes/${quoteId}`)
      const data = await response.json()
      setSelectedQuote(data)
      setShowViewDialog(true)
    } catch (error) {
      console.error('Error fetching quote details:', error)
    }
  }

  const createQuote = async () => {
    try {
      const response = await fetch('/api/quotes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newQuote)
      })
      
      if (response.ok) {
        setShowCreateDialog(false)
        setNewQuote({
          client_id: '',
          project_name: '',
          description: '',
          tax_rate: 8.5,
          valid_until: '',
          notes: '',
          items: [{ description: '', quantity: 1, unit_price: 0 }]
        })
        fetchQuotes()
      }
    } catch (error) {
      console.error('Error creating quote:', error)
    }
  }

  const updateQuoteStatus = async (quoteId, status) => {
    try {
      await fetch(`/api/quotes/${quoteId}/status`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status })
      })
      fetchQuotes()
    } catch (error) {
      console.error('Error updating quote status:', error)
    }
  }

  const addQuoteItem = () => {
    setNewQuote({
      ...newQuote,
      items: [...newQuote.items, { description: '', quantity: 1, unit_price: 0 }]
    })
  }

  const updateQuoteItem = (index, field, value) => {
    const updatedItems = newQuote.items.map((item, i) => 
      i === index ? { ...item, [field]: value } : item
    )
    setNewQuote({ ...newQuote, items: updatedItems })
  }

  const removeQuoteItem = (index) => {
    if (newQuote.items.length > 1) {
      const updatedItems = newQuote.items.filter((_, i) => i !== index)
      setNewQuote({ ...newQuote, items: updatedItems })
    }
  }

  const calculateSubtotal = () => {
    return newQuote.items.reduce((sum, item) => 
      sum + (parseFloat(item.quantity) * parseFloat(item.unit_price || 0)), 0
    )
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'draft': return 'bg-gray-100 text-gray-800'
      case 'pending': return 'bg-yellow-100 text-yellow-800'
      case 'accepted': return 'bg-green-100 text-green-800'
      case 'rejected': return 'bg-red-100 text-red-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  if (loading) {
    return <div className="flex items-center justify-center h-64">Loading quotes...</div>
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Quotes</h1>
          <p className="text-gray-600 mt-1">Create and manage project quotes for your clients.</p>
        </div>
        <Dialog open={showCreateDialog} onOpenChange={setShowCreateDialog}>
          <DialogTrigger asChild>
            <Button className="bg-teal-600 hover:bg-teal-700">
              <Plus className="w-4 h-4 mr-2" />
              New Quote
            </Button>
          </DialogTrigger>
          <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
            <DialogHeader>
              <DialogTitle>Create New Quote</DialogTitle>
            </DialogHeader>
            <div className="space-y-6">
              {/* Basic Info */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Client</label>
                  <Select value={newQuote.client_id} onValueChange={(value) => setNewQuote({...newQuote, client_id: value})}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select client" />
                    </SelectTrigger>
                    <SelectContent>
                      {clients.map(client => (
                        <SelectItem key={client.id} value={client.id.toString()}>
                          {client.name} - {client.company}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Project Name</label>
                  <Input
                    value={newQuote.project_name}
                    onChange={(e) => setNewQuote({...newQuote, project_name: e.target.value})}
                    placeholder="Enter project name"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Description</label>
                <Textarea
                  value={newQuote.description}
                  onChange={(e) => setNewQuote({...newQuote, description: e.target.value})}
                  placeholder="Project description"
                  rows={3}
                />
              </div>

              {/* Quote Items */}
              <div>
                <div className="flex justify-between items-center mb-4">
                  <h3 className="text-lg font-medium">Quote Items</h3>
                  <Button onClick={addQuoteItem} variant="outline" size="sm">
                    <Plus className="w-4 h-4 mr-2" />
                    Add Item
                  </Button>
                </div>
                
                <div className="space-y-3">
                  {newQuote.items.map((item, index) => (
                    <div key={index} className="grid grid-cols-12 gap-3 items-end">
                      <div className="col-span-5">
                        <label className="block text-sm font-medium mb-1">Description</label>
                        <Input
                          value={item.description}
                          onChange={(e) => updateQuoteItem(index, 'description', e.target.value)}
                          placeholder="Item description"
                        />
                      </div>
                      <div className="col-span-2">
                        <label className="block text-sm font-medium mb-1">Quantity</label>
                        <Input
                          type="number"
                          value={item.quantity}
                          onChange={(e) => updateQuoteItem(index, 'quantity', e.target.value)}
                          min="1"
                        />
                      </div>
                      <div className="col-span-3">
                        <label className="block text-sm font-medium mb-1">Unit Price</label>
                        <Input
                          type="number"
                          value={item.unit_price}
                          onChange={(e) => updateQuoteItem(index, 'unit_price', e.target.value)}
                          placeholder="0.00"
                          step="0.01"
                        />
                      </div>
                      <div className="col-span-1">
                        <label className="block text-sm font-medium mb-1">Total</label>
                        <div className="text-sm font-medium py-2">
                          ${(parseFloat(item.quantity) * parseFloat(item.unit_price || 0)).toFixed(2)}
                        </div>
                      </div>
                      <div className="col-span-1">
                        <Button
                          onClick={() => removeQuoteItem(index)}
                          variant="outline"
                          size="sm"
                          disabled={newQuote.items.length === 1}
                        >
                          <Trash2 className="w-4 h-4" />
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>

                {/* Totals */}
                <div className="mt-6 border-t pt-4">
                  <div className="flex justify-end space-x-8">
                    <div className="text-right">
                      <div className="text-sm text-gray-600">Subtotal: ${calculateSubtotal().toFixed(2)}</div>
                      <div className="text-sm text-gray-600">
                        Tax ({newQuote.tax_rate}%): ${(calculateSubtotal() * newQuote.tax_rate / 100).toFixed(2)}
                      </div>
                      <div className="text-lg font-bold">
                        Total: ${(calculateSubtotal() * (1 + newQuote.tax_rate / 100)).toFixed(2)}
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Additional Info */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Tax Rate (%)</label>
                  <Input
                    type="number"
                    value={newQuote.tax_rate}
                    onChange={(e) => setNewQuote({...newQuote, tax_rate: parseFloat(e.target.value)})}
                    step="0.1"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Valid Until</label>
                  <Input
                    type="date"
                    value={newQuote.valid_until}
                    onChange={(e) => setNewQuote({...newQuote, valid_until: e.target.value})}
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Notes</label>
                <Textarea
                  value={newQuote.notes}
                  onChange={(e) => setNewQuote({...newQuote, notes: e.target.value})}
                  placeholder="Additional notes or terms"
                  rows={3}
                />
              </div>

              <div className="flex justify-end space-x-3">
                <Button variant="outline" onClick={() => setShowCreateDialog(false)}>
                  Cancel
                </Button>
                <Button onClick={createQuote} className="bg-teal-600 hover:bg-teal-700">
                  Create Quote
                </Button>
              </div>
            </div>
          </DialogContent>
        </Dialog>
      </div>

      {/* Quotes List */}
      <div className="grid gap-6">
        {quotes.length === 0 ? (
          <Card>
            <CardContent className="text-center py-12">
              <FileText className="w-12 h-12 mx-auto text-gray-400 mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No quotes yet</h3>
              <p className="text-gray-600 mb-4">Create your first quote to get started.</p>
              <Button onClick={() => setShowCreateDialog(true)} className="bg-teal-600 hover:bg-teal-700">
                <Plus className="w-4 h-4 mr-2" />
                Create Quote
              </Button>
            </CardContent>
          </Card>
        ) : (
          quotes.map(quote => (
            <Card key={quote.id} className="hover:shadow-lg transition-shadow">
              <CardContent className="p-6">
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-2">
                      <h3 className="text-lg font-semibold text-gray-900">{quote.quote_number}</h3>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(quote.status)}`}>
                        {quote.status.charAt(0).toUpperCase() + quote.status.slice(1)}
                      </span>
                    </div>
                    <p className="text-gray-600 mb-1">{quote.project_name}</p>
                    <p className="text-sm text-gray-500">Client: {quote.client}</p>
                    <div className="flex items-center mt-3">
                      <DollarSign className="w-4 h-4 text-green-600 mr-1" />
                      <span className="text-lg font-bold text-green-600">
                        ${quote.total_amount.toLocaleString()}
                      </span>
                    </div>
                  </div>
                  <div className="flex space-x-2">
                    <Button
                      onClick={() => fetchQuoteDetails(quote.id)}
                      variant="outline"
                      size="sm"
                    >
                      <Eye className="w-4 h-4" />
                    </Button>
                    {quote.status === 'pending' && (
                      <>
                        <Button
                          onClick={() => updateQuoteStatus(quote.id, 'accepted')}
                          variant="outline"
                          size="sm"
                          className="text-green-600 hover:text-green-700"
                        >
                          Accept
                        </Button>
                        <Button
                          onClick={() => updateQuoteStatus(quote.id, 'rejected')}
                          variant="outline"
                          size="sm"
                          className="text-red-600 hover:text-red-700"
                        >
                          Reject
                        </Button>
                      </>
                    )}
                  </div>
                </div>
              </CardContent>
            </Card>
          ))
        )}
      </div>

      {/* Quote Details Dialog */}
      <Dialog open={showViewDialog} onOpenChange={setShowViewDialog}>
        <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>Quote Details</DialogTitle>
          </DialogHeader>
          {selectedQuote && (
            <div className="space-y-6">
              {/* Header */}
              <div className="border-b pb-4">
                <div className="flex justify-between items-start">
                  <div>
                    <h2 className="text-2xl font-bold">{selectedQuote.quote_number}</h2>
                    <p className="text-gray-600">{selectedQuote.project_name}</p>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(selectedQuote.status)}`}>
                    {selectedQuote.status.charAt(0).toUpperCase() + selectedQuote.status.slice(1)}
                  </span>
                </div>
              </div>

              {/* Client Info */}
              {selectedQuote.client && (
                <div>
                  <h3 className="font-medium mb-2">Client Information</h3>
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <p className="font-medium">{selectedQuote.client.name}</p>
                    <p>{selectedQuote.client.company}</p>
                    <p>{selectedQuote.client.email}</p>
                    {selectedQuote.client.address && <p>{selectedQuote.client.address}</p>}
                  </div>
                </div>
              )}

              {/* Items */}
              <div>
                <h3 className="font-medium mb-2">Quote Items</h3>
                <div className="border rounded-lg overflow-hidden">
                  <table className="w-full">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="text-left p-3">Description</th>
                        <th className="text-right p-3">Qty</th>
                        <th className="text-right p-3">Unit Price</th>
                        <th className="text-right p-3">Total</th>
                      </tr>
                    </thead>
                    <tbody>
                      {selectedQuote.items.map(item => (
                        <tr key={item.id} className="border-t">
                          <td className="p-3">{item.description}</td>
                          <td className="text-right p-3">{item.quantity}</td>
                          <td className="text-right p-3">${item.unit_price}</td>
                          <td className="text-right p-3">${item.total_price}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* Totals */}
              <div className="border-t pt-4">
                <div className="flex justify-end">
                  <div className="w-64 space-y-2">
                    <div className="flex justify-between">
                      <span>Subtotal:</span>
                      <span>${selectedQuote.subtotal}</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Tax ({selectedQuote.tax_rate}%):</span>
                      <span>${selectedQuote.tax_amount}</span>
                    </div>
                    <div className="flex justify-between font-bold text-lg border-t pt-2">
                      <span>Total:</span>
                      <span>${selectedQuote.total_amount}</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Notes */}
              {selectedQuote.notes && (
                <div>
                  <h3 className="font-medium mb-2">Notes</h3>
                  <p className="text-gray-600 bg-gray-50 p-4 rounded-lg">{selectedQuote.notes}</p>
                </div>
              )}
            </div>
          )}
        </DialogContent>
      </Dialog>
    </div>
  )
}

export default Quotes

