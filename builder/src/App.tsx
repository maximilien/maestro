import { useState } from 'react'
import { Sidebar } from './components/Sidebar'
import { ChatCanvas } from './components/ChatCanvas'
import { YamlPanel } from './components/YamlPanel'
import { ChatInput } from './components/ChatInput'

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

  const handleSendMessage = async (content: string) => {
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content,
      timestamp: new Date()
    }
    
    setMessages(prev => [...prev, userMessage])
    
    // Simulate AI response (replace with actual API call)
    setTimeout(() => {
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: `I understand you want to: "${content}". I'll help you build the appropriate Maestro configuration. Let me analyze your requirements and update the YAML files accordingly.`,
        timestamp: new Date()
      }
      setMessages(prev => [...prev, assistantMessage])
      
      // Update YAML files based on the conversation
      // This is where you'd integrate with the Maestro API
      setYamlFiles(prev => prev.map(file => {
        if (file.name === 'agents.yaml') {
          return {
            ...file,
            content: `# Agents configuration generated from conversation
agents:
  example_agent:
    type: openai
    config:
      model: gpt-4
      api_key: ${process.env.OPENAI_API_KEY || 'your-api-key-here'}
    description: "Agent created based on: ${content}"
`
          }
        }
        if (file.name === 'workflow.yaml') {
          return {
            ...file,
            content: `# Workflow configuration generated from conversation
workflow:
  name: "Generated Workflow"
  description: "Workflow created based on: ${content}"
  steps:
    - name: "example_step"
      agent: "example_agent"
      input:
        prompt: "Process the request"
`
          }
        }
        return file
      }))
    }, 1000)
  }

  return (
    <div className="h-screen flex bg-white overflow-hidden">
      {/* Left Sidebar */}
      <Sidebar />
      
      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Chat Canvas */}
        <div className="flex-1 overflow-hidden">
          <ChatCanvas messages={messages} />
        </div>
        
        {/* Chat Input */}
        <div className="border-t border-gray-100 p-6">
          <ChatInput onSendMessage={handleSendMessage} />
        </div>
      </div>
      
      {/* Right Panel - YAML Files */}
      <YamlPanel yamlFiles={yamlFiles} />
    </div>
  )
}

export default App
