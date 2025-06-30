# Maestro Builder

A modern web-based interface for building Maestro agents and workflows using AI assistance.

## Features

- **AI-Powered Chat Interface**: Chat with an AI assistant to help you create Maestro configurations
- **Real-time YAML Generation**: Automatically generates and updates `agents.yaml` and `workflow.yaml` files
- **Live Preview**: See your YAML configurations update in real-time as you chat
- **Modern UI**: Clean, responsive interface built with React and Tailwind CSS
- **API Integration**: Connects to the Maestro Builder API for intelligent responses

## Quick Start

### Option 1: Start Both API and Frontend (Recommended)

```bash
# From the builder directory
./start-dev.sh
```

This will start both the API server and the frontend development server automatically.

### Option 2: Start Components Separately

#### Start the API Server

```bash
# From the api directory
cd ../api
./run.sh
```

The API will be available at `http://localhost:8000`

#### Start the Frontend

```bash
# From the builder directory
npm install
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Usage

1. **Open the Builder**: Navigate to `http://localhost:5173` in your browser
2. **Start Chatting**: Type your requirements in the chat input at the bottom
3. **Watch YAML Generation**: See your `agents.yaml` and `workflow.yaml` files update in real-time
4. **Use Suggestions**: Click the lightbulb icon for quick suggestions
5. **Download Files**: Use the download buttons in the YAML panel to save your configurations

## Example Conversations

### Creating an OpenAI Agent
```
User: "Create an OpenAI agent for text summarization"
AI: "I'll help you create an OpenAI agent for text summarization. Here's the configuration..."
```

### Building a Workflow
```
User: "Build a workflow that processes data and generates reports"
AI: "I'll create a workflow with multiple steps for data processing and report generation..."
```

### Complex Requirements
```
User: "Create a multi-agent system with a data processor, analyzer, and reporter"
AI: "I'll design a comprehensive multi-agent system with specialized roles..."
```

## API Integration

The builder connects to the Maestro Builder API which provides:

- **Intelligent Responses**: AI-powered chat responses using OpenAI (when API key is configured)
- **Fallback Mode**: Works without OpenAI API key using keyword-based responses
- **Session Management**: Maintains conversation context across messages
- **YAML Validation**: Ensures generated configurations follow Maestro schemas

### API Endpoints

- `POST /api/chat_builder_agent` - Send chat messages and get responses
- `GET /api/get_yamls/{chat_id}` - Retrieve YAML files for a session
- `GET /api/chat_history` - Get chat history

## Configuration

### Environment Variables

Set these in the API directory:

```bash
export OPENAI_API_KEY="your-openai-api-key"
```

### API Configuration

The API runs on `http://localhost:8000` by default. You can modify the URL in `src/services/api.ts` if needed.

## Development

### Project Structure

```
builder/
├── src/
│   ├── components/
│   │   ├── ChatCanvas.tsx      # Chat message display
│   │   ├── ChatInput.tsx       # Message input component
│   │   ├── Sidebar.tsx         # Left sidebar
│   │   └── YamlPanel.tsx       # YAML file display
│   ├── services/
│   │   └── api.ts             # API integration service
│   └── App.tsx                # Main application
├── start-dev.sh               # Development startup script
└── package.json
```

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `./start-dev.sh` - Start both API and frontend

## Troubleshooting

### API Connection Issues

1. Ensure the API server is running on `http://localhost:8000`
2. Check that CORS is properly configured in the API
3. Verify the API endpoint in `src/services/api.ts`

### YAML Not Updating

1. Check the browser console for errors
2. Verify the API response format
3. Ensure the YAML panel is properly connected

### OpenAI Integration

1. Set your `OPENAI_API_KEY` environment variable
2. Restart the API server after setting the key
3. Check API logs for authentication errors

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test the integration
5. Submit a pull request

## License

This project is part of the Maestro framework and follows the same license terms.
