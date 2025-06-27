# Maestro AI Builder

A modern TypeScript React application for building Maestro workflows with AI assistance. The interface is inspired by Google Gemini and provides an intuitive way to create `agents.yaml` and `workflow.yaml` files through natural language conversation.

## Features

- **Chat Interface**: Natural language conversation with AI to build workflows
- **Real-time YAML Generation**: See your `agents.yaml` and `workflow.yaml` files being built in real-time
- **Collapsible Sidebar**: Navigation menu with search functionality (collapsed by default)
- **YAML Syntax Highlighting**: Beautiful color-coded YAML display with Prism.js
- **File Management**: Copy, download, and manage generated YAML files
- **Line Numbers**: Toggle line numbers for better code navigation
- **Modern UI**: Clean, responsive design inspired by Google Gemini
- **TypeScript**: Full type safety and modern development experience
- **Smart Suggestions**: Dropdown menu with suggested prompts for quick workflow creation

## Layout

The application features a three-pane layout:

1. **Left Sidebar**: Collapsible navigation with search and menu items (Agents, Workflows, Templates, History, Favorites, Settings)
2. **Center Canvas**: Chat interface showing conversation history and YAML building process
3. **Right Panel**: Generated YAML files with syntax highlighting, line numbers, and file management tools

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn

### Installation

1. Navigate to the builder directory:
   ```bash
   cd builder
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Open your browser and navigate to `http://localhost:5173`

### Building for Production

```bash
npm run build
```

The built files will be in the `dist` directory.

## Development

### Project Structure

```
src/
├── components/          # React components
│   ├── Sidebar.tsx     # Left navigation sidebar with search
│   ├── ChatCanvas.tsx  # Main chat interface with message history
│   ├── ChatInput.tsx   # Message input with suggestions dropdown
│   └── YamlPanel.tsx   # Right panel for YAML files with syntax highlighting
├── lib/
│   └── utils.ts        # Utility functions (cn helper)
├── App.tsx             # Main application component with state management
├── main.tsx           # Application entry point
└── index.css          # Global styles and Tailwind imports
```

### Key Technologies

- **React 19** with TypeScript
- **Vite** for fast development and building
- **Tailwind CSS v4** for styling
- **Lucide React** for icons
- **Radix UI** components for accessibility
- **Prism.js** for YAML syntax highlighting
- **class-variance-authority** and **clsx** for conditional styling

### Current Functionality

The application currently includes:

- **Simulated AI Responses**: Placeholder AI responses that update YAML files based on user input
- **YAML File Generation**: Real-time generation of `agents.yaml` and `workflow.yaml` files
- **File Operations**: Copy to clipboard and download functionality for generated files
- **Syntax Highlighting**: Beautiful YAML syntax highlighting with line numbers
- **Responsive Design**: Optimized for different screen sizes
- **Modern UI Components**: Dropdown menus, collapsible sidebar, and clean typography

### API Integration

The application is designed to integrate with a Maestro API (to be built). The chat interface will send messages to the API and receive responses that update the YAML files in real-time.

Current placeholder functionality:
- Simulated AI responses with 1-second delay
- Basic YAML file generation based on user input
- File download and copy functionality
- Syntax highlighting for YAML content

## UI Features

### Chat Interface
- Clean message bubbles with user/assistant avatars
- Timestamp display for each message
- Auto-scroll to latest messages
- YAML preview in messages when applicable

### YAML Panel
- Syntax highlighting with Prism.js
- Toggle line numbers on/off
- Copy to clipboard functionality
- Download files as .yaml
- Tabbed interface for multiple files
- Compact 7px font size for maximum content visibility

### Sidebar
- Collapsible design (collapsed by default)
- Search functionality with proper spacing
- Navigation menu items with icons
- Smooth transitions and hover effects

### Chat Input
- Clean input field with send button
- Suggestions dropdown with lightbulb icon
- Attach file button
- Responsive design

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is part of the Maestro ecosystem and follows the same licensing terms.
