import { useState, useEffect } from 'react'
import { FileText, Copy, Download, Eye, EyeOff } from 'lucide-react'
import type { YamlFile } from '../App'
import { cn } from '../lib/utils'
import Prism from 'prismjs'
import 'prismjs/components/prism-yaml'
import 'prismjs/themes/prism.css'

interface YamlPanelProps {
  yamlFiles: YamlFile[]
}

export function YamlPanel({ yamlFiles }: YamlPanelProps) {
  const [activeFile, setActiveFile] = useState(0)
  const [showLineNumbers, setShowLineNumbers] = useState(true)

  // Highlight syntax when content changes
  useEffect(() => {
    Prism.highlightAll()
  }, [yamlFiles, activeFile])

  const handleCopy = async (content: string) => {
    try {
      await navigator.clipboard.writeText(content)
      // You could add a toast notification here
    } catch (err) {
      console.error('Failed to copy: ', err)
    }
  }

  const handleDownload = (file: YamlFile) => {
    const blob = new Blob([file.content], { type: 'text/yaml' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = file.name
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  const renderLineNumbers = (content: string) => {
    const lines = content.split('\n')
    return (
      <div className="flex">
        <div className="w-12 flex-shrink-0 bg-gray-100 text-gray-500 text-[9px] font-mono p-4 border-r border-gray-200 font-['Courier_New']">
          {lines.map((_, index) => (
            <div key={index} className="text-right">
              {index + 1}
            </div>
          ))}
        </div>
        <div className="flex-1">
          <pre className="text-[7px] font-mono p-4 overflow-x-auto bg-white font-['Courier_New'] whitespace-pre">
            <code className="language-yaml whitespace-pre">{content}</code>
          </pre>
        </div>
      </div>
    )
  }

  return (
    <div className="w-1/3 border-l border-gray-100 bg-white flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between p-6 border-b border-gray-100">
        <h2 className="text-lg font-semibold text-gray-900">Generated Files</h2>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setShowLineNumbers(!showLineNumbers)}
            className="p-2 rounded-lg hover:bg-gray-50 hover:text-gray-700 transition-colors"
            title={showLineNumbers ? 'Hide line numbers' : 'Show line numbers'}
          >
            {showLineNumbers ? <EyeOff size={18} /> : <Eye size={18} />}
          </button>
        </div>
      </div>

      {/* File Tabs */}
      <div className="flex border-b border-gray-100">
        {yamlFiles.map((file, index) => (
          <button
            key={file.name}
            onClick={() => setActiveFile(index)}
            className={cn(
              "flex items-center gap-2 px-6 py-4 text-xs border-b-2 transition-all duration-200",
              activeFile === index
                ? "border-blue-600 text-blue-700 bg-blue-50 font-medium"
                : "border-transparent text-gray-500 hover:text-gray-700 hover:bg-gray-50"
            )}
          >
            <FileText size={16} />
            <span>{file.name}</span>
          </button>
        ))}
      </div>

      {/* File Content */}
      <div className="flex-1 overflow-hidden">
        {yamlFiles.length > 0 ? (
          <div className="h-full flex flex-col">
            {/* File Actions */}
            <div className="flex items-center justify-between p-4 border-b border-gray-100 bg-gray-50">
              <span className="text-xs text-gray-500 font-medium">
                {yamlFiles[activeFile].name}
              </span>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => handleCopy(yamlFiles[activeFile].content)}
                  className="p-2 rounded-lg hover:bg-white hover:text-gray-700 transition-colors"
                  title="Copy to clipboard"
                >
                  <Copy size={16} />
                </button>
                <button
                  onClick={() => handleDownload(yamlFiles[activeFile])}
                  className="p-2 rounded-lg hover:bg-white hover:text-gray-700 transition-colors"
                  title="Download file"
                >
                  <Download size={16} />
                </button>
              </div>
            </div>

            {/* YAML Content */}
            <div className="flex-1 overflow-auto">
              {showLineNumbers ? (
                renderLineNumbers(yamlFiles[activeFile].content)
              ) : (
                <pre className="text-[7px] font-mono p-6 overflow-x-auto bg-gray-50 font-['Courier_New'] whitespace-pre">
                  <code className="language-yaml whitespace-pre">{yamlFiles[activeFile].content}</code>
                </pre>
              )}
            </div>
          </div>
        ) : (
          <div className="flex items-center justify-center h-full text-gray-400">
            <div className="text-center max-w-sm">
              <div className="w-12 h-12 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <FileText size={24} className="text-gray-400" />
              </div>
              <h3 className="text-xs font-medium text-gray-900 mb-2">No YAML files generated yet</h3>
              <p className="text-xs text-gray-500">Start a conversation to generate files</p>
            </div>
          </div>
        )}
      </div>
    </div>
  )
} 