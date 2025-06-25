import { Link, useLocation } from 'react-router-dom'
import { 
  LayoutDashboard, 
  Users, 
  FolderOpen, 
  CheckSquare, 
  FileText, 
  MessageSquare, 
  BarChart3, 
  Menu,
  Bot
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'

const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
  { name: 'Clients', href: '/clients', icon: Users },
  { name: 'Projects', href: '/projects', icon: FolderOpen },
  { name: 'Tasks', href: '/tasks', icon: CheckSquare },
  { name: 'Quotes', href: '/quotes', icon: FileText },
  { name: 'Communications', href: '/communications', icon: MessageSquare },
  { name: 'Analytics', href: '/analytics', icon: BarChart3 },
]

export default function Sidebar({ isOpen, setIsOpen }) {
  const location = useLocation()

  return (
    <div className={cn(
      "fixed left-0 top-0 z-40 h-screen bg-sidebar border-r border-sidebar-border transition-all duration-300",
      isOpen ? "w-64" : "w-16"
    )}>
      <div className="flex h-full flex-col">
        {/* Header */}
        <div className="flex h-16 items-center justify-between px-4 border-b border-sidebar-border">
          <div className={cn(
            "flex items-center space-x-3 transition-opacity duration-300",
            isOpen ? "opacity-100" : "opacity-0"
          )}>
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary">
              <Bot className="h-5 w-5 text-primary-foreground" />
            </div>
            <div className="flex flex-col">
              <span className="text-sm font-semibold text-sidebar-foreground">Emert.ai</span>
              <span className="text-xs text-sidebar-foreground/60">CRM</span>
            </div>
          </div>
          
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setIsOpen(!isOpen)}
            className="h-8 w-8 p-0 hover:bg-sidebar-accent"
          >
            <Menu className="h-4 w-4" />
          </Button>
        </div>

        {/* Navigation */}
        <nav className="flex-1 space-y-1 p-4">
          {navigation.map((item) => {
            const isActive = location.pathname === item.href
            return (
              <Link
                key={item.name}
                to={item.href}
                className={cn(
                  "flex items-center space-x-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors",
                  isActive
                    ? "bg-sidebar-primary text-sidebar-primary-foreground"
                    : "text-sidebar-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground"
                )}
              >
                <item.icon className="h-5 w-5 flex-shrink-0" />
                <span className={cn(
                  "transition-opacity duration-300",
                  isOpen ? "opacity-100" : "opacity-0"
                )}>
                  {item.name}
                </span>
              </Link>
            )
          })}
        </nav>

        {/* Footer */}
        <div className="border-t border-sidebar-border p-4">
          <div className={cn(
            "flex items-center space-x-3 transition-opacity duration-300",
            isOpen ? "opacity-100" : "opacity-0"
          )}>
            <div className="h-8 w-8 rounded-full bg-primary/10 flex items-center justify-center">
              <span className="text-xs font-medium text-primary">U</span>
            </div>
            <div className="flex flex-col">
              <span className="text-sm font-medium text-sidebar-foreground">User</span>
              <span className="text-xs text-sidebar-foreground/60">Admin</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

