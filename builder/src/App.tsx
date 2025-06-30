import { useState } from 'react'
import { Sidebar } from './components/Sidebar'
import { ChatCanvas } from './components/ChatCanvas'
import { YamlPanel } from './components/YamlPanel'
import { ChatInput } from './components/ChatInput'
import { apiService } from './services/api'

export interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

export interface YamlFile {
  name: string
  content: string
  language: 'yaml'
}

function App() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: 'Hello! I\'m your Maestro AI Builder assistant. I can help you create agents.yaml and workflow.yaml files for your Maestro agents and workflows. What would you like to build today?',
      timestamp: new Date()
    }
  ])
  
  const [yamlFiles, setYamlFiles] = useState<YamlFile[]>([
    {
      name: 'agents.yaml',
      content: '# Agents configuration will be generated here\nagents:\n  # Your agents will appear here',
      language: 'yaml'
    },
    {
      name: 'workflow.yaml',
      content: '# Workflow configuration will be generated here\nworkflow:\n  # Your workflow will appear here',
      language: 'yaml'
    }
  ])

  const [isLoading, setIsLoading] = useState(false)

  const handleSendMessage = async (content: string) => {
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content,
      timestamp: new Date()
    }
    
    setMessages(prev => [...prev, userMessage])
    setIsLoading(true)
    
    try {
      // Send message to API
      const apiResponse = await apiService.sendMessage(content)
      
      // Create assistant message from API response
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: apiResponse.response,
        role: 'assistant',
        timestamp: new Date()
      }
      
      setMessages(prev => [...prev, assistantMessage])
      
      // Update YAML files from API response
      const updatedYamlFiles = yamlFiles.map(file => {
        const apiFile = apiResponse.yaml_files.find(apiFile => apiFile.name === file.name)
        if (apiFile) {
          return {
            ...file,
            content: apiFile.content
          }
        }
        return file
      })
      
      setYamlFiles(updatedYamlFiles)
      
    } catch (error) {
      console.error('Error sending message:', error)
      
      // Add error message
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Sorry, I encountered an error while processing your request. Please try again.',
        timestamp: new Date()
      }
      
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="h-screen flex bg-white overflow-hidden">
      {/* Left Sidebar */}
      <Sidebar />
      
      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Chat Canvas */}
        <div className="flex-1 overflow-hidden">
          <ChatCanvas messages={messages} isLoading={isLoading} />
        </div>
        
        {/* Chat Input */}
        <div className="border-t border-gray-100 p-6">
          <ChatInput onSendMessage={handleSendMessage} disabled={isLoading} />
        </div>
      </div>
      
      {/* Right Panel - YAML Files */}
      <YamlPanel yamlFiles={yamlFiles} isLoading={isLoading} />
    </div>
  )
}

export default App
