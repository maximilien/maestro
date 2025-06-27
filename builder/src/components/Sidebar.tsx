import { useState } from 'react'
import { ChevronLeft, ChevronRight, Settings, FileText, Bot, Workflow, History, Star } from 'lucide-react'
import { cn } from '../lib/utils'

export function Sidebar() {
  const [isCollapsed, setIsCollapsed] = useState(true)

  const menuItems = [
    { icon: Bot, label: 'Agents', active: true },
    { icon: Workflow, label: 'Workflows' },
    { icon: FileText, label: 'Templates' },
    { icon: History, label: 'History' },
    { icon: Star, label: 'Favorites' },
    { icon: Settings, label: 'Settings' },
  ]

  return (
    <div className={cn(
      "h-full border-r border-gray-100 bg-white transition-all duration-300 flex-shrink-0",
      isCollapsed ? "w-16" : "w-64"
    )}>
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-gray-100">
        {!isCollapsed && (
          <h2 className="text-sm font-semibold text-gray-900">Menu</h2>
        )}
        <button
          onClick={() => setIsCollapsed(!isCollapsed)}
          className="p-2 rounded-lg hover:bg-gray-50 transition-colors"
          title={isCollapsed ? "Expand menu" : "Collapse menu"}
        >
          {isCollapsed ? <ChevronRight size={16} /> : <ChevronLeft size={16} />}
        </button>
      </div>

      {/* Menu Items */}
      <nav className="p-3 flex-1 overflow-y-auto">
        {menuItems.map((item) => (
          <button
            key={item.label}
            className={cn(
              "w-full flex items-center gap-3 px-3 py-2.5 text-xs rounded-lg transition-all duration-200 mb-1",
              item.active
                ? "bg-blue-50 text-blue-700 font-medium"
                : "text-gray-600 hover:bg-gray-50 hover:text-gray-900"
            )}
          >
            <item.icon size={16} />
            {!isCollapsed && <span className="truncate">{item.label}</span>}
          </button>
        ))}
      </nav>
    </div>
  )
} 