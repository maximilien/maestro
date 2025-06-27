import { useState, useEffect, useRef } from 'react'
import type { KeyboardEvent } from 'react'
import { Send, Paperclip, Mic, ChevronDown, Lightbulb } from 'lucide-react'
import { cn } from '../lib/utils'

interface ChatInputProps {
  onSendMessage: (message: string) => void
}

export function ChatInput({ onSendMessage }: ChatInputProps) {
  const [message, setMessage] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const [showSuggestions, setShowSuggestions] = useState(false)
  const dropdownRef = useRef<HTMLDivElement>(null)

  const suggestions = [
    "Create a simple workflow",
    "Add an OpenAI agent",
    "Build a data processing pipeline",
    "Create a web scraping workflow"
  ]

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setShowSuggestions(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => {
      document.removeEventListener('mousedown', handleClickOutside)
    }
  }, [])

  const handleSend = () => {
    if (message.trim()) {
      onSendMessage(message.trim())
      setMessage('')
      setIsTyping(false)
    }
  }

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  const handleSuggestionClick = (suggestion: string) => {
    onSendMessage(suggestion)
    setShowSuggestions(false)
  }

  return (
    <div className="w-full">
      <div className="relative">
        <div className="flex items-end gap-3 p-4 bg-white border border-gray-200 rounded-2xl shadow-sm hover:shadow-md transition-shadow">
          {/* Attachment Button */}
          <button className="p-2 text-gray-400 hover:text-gray-600 transition-colors rounded-lg hover:bg-gray-50">
            <Paperclip size={20} />
          </button>

          {/* Suggestions Dropdown */}
          <div className="relative" ref={dropdownRef}>
            <button
              onClick={() => setShowSuggestions(!showSuggestions)}
              className="p-2 text-gray-400 hover:text-gray-600 transition-colors rounded-lg hover:bg-gray-50 flex items-center gap-1"
              title="Show suggestions"
            >
              <Lightbulb size={22} />
              <ChevronDown size={18} className={cn("transition-transform", showSuggestions && "rotate-180")} />
            </button>
            
            {showSuggestions && (
              <div className="absolute bottom-full left-0 mb-2 w-64 bg-white border border-gray-200 rounded-xl shadow-lg z-10">
                <div className="p-2">
                  <div className="text-xs font-medium text-gray-500 mb-2 px-2">Suggestions</div>
                  {suggestions.map((suggestion) => (
                    <button
                      key={suggestion}
                      onClick={() => handleSuggestionClick(suggestion)}
                      className="w-full text-left px-3 py-2 text-xs text-gray-700 hover:bg-gray-50 rounded-lg transition-colors"
                    >
                      {suggestion}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Text Input */}
          <div className="flex-1 min-h-[44px] max-h-32">
            <textarea
              value={message}
              onChange={(e) => {
                setMessage(e.target.value)
                setIsTyping(e.target.value.length > 0)
              }}
              onKeyDown={handleKeyDown}
              placeholder="Ask me to help you build your Maestro workflow..."
              className="w-full h-full min-h-[44px] max-h-32 resize-none bg-transparent border-none outline-none text-xs placeholder:text-gray-400 leading-relaxed"
              rows={1}
            />
          </div>

          {/* Voice Button */}
          <button className="p-2 text-gray-400 hover:text-gray-600 transition-colors rounded-lg hover:bg-gray-50">
            <Mic size={20} />
          </button>

          {/* Send Button */}
          <button
            onClick={handleSend}
            disabled={!message.trim()}
            className={cn(
              "p-2 rounded-xl transition-all duration-200",
              message.trim()
                ? "bg-blue-600 text-white hover:bg-blue-700 shadow-sm hover:shadow-md"
                : "bg-gray-100 text-gray-400 cursor-not-allowed"
            )}
          >
            <Send size={20} />
          </button>
        </div>

        {/* Typing Indicator */}
        {isTyping && (
          <div className="absolute -top-8 left-4 text-xs text-gray-400 bg-white px-2 py-1 rounded">
            Press Enter to send, Shift+Enter for new line
          </div>
        )}
      </div>
    </div>
  )
} 