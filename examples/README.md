# Examples

This directory contains practical examples and quick-start guides for the Luminis AI Library Assistant.

## 🚀 Quick Start Examples

### 1. Basic Chat Example
Learn how to integrate the chat functionality into your application.

### 2. Voice Integration Example
See how to implement voice recording and transcription features.

### 3. Book Search Example
Example of how to search and retrieve book information.

### 4. User Authentication Example
Learn how to implement user authentication and profile management.

## 📁 Available Examples

| Example | Description | File |
|---------|-------------|------|
| **Basic Chat** | Simple chat integration | `basic_chat.py` |
| **Voice Recording** | Voice input handling | `voice_recording.py` |
| **Book Search** | Book search functionality | `book_search.py` |
| **API Usage** | REST API examples | `api_examples.py` |
| **Frontend Integration** | React component examples | `frontend_examples/` |

## 🛠️ How to Use Examples

1. **Clone the repository**
   ```bash
   git clone https://github.com/KaracaDeer/Luminis_AI_Library_Chatbot.git
   cd Luminis_AI_Library_Chatbot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   cd src/frontend && npm install
   ```

3. **Run examples**
   ```bash
   # Python examples
   python examples/basic_chat.py
   
   # Frontend examples
   cd examples/frontend_examples
   npm start
   ```

## 📚 Example Categories

### Backend Examples
- **API Integration**: How to use the REST API
- **Database Operations**: Working with the database
- **Authentication**: User management examples
- **Vector Search**: Semantic search implementation

### Frontend Examples
- **React Components**: Reusable UI components
- **State Management**: Zustand store examples
- **API Calls**: Frontend-backend communication
- **Voice Integration**: Voice recording components

### Full-Stack Examples
- **Complete Chat Flow**: End-to-end chat implementation
- **User Registration**: Complete user flow
- **Book Management**: Full book lifecycle
- **Search Implementation**: Complete search functionality

## 🔧 Configuration

Before running examples, make sure to:

1. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

2. **Initialize the database**
   ```bash
   python src/database/init_database.py
   ```

3. **Start the backend**
   ```bash
   python -m uvicorn src.backend.main:app --reload
   ```

4. **Start the frontend**
   ```bash
   cd src/frontend && npm run dev
   ```

## 📖 Documentation

For more detailed documentation, see:
- [API Documentation](docs/README.md)
- [Frontend Guide](src/frontend/README.md)
- [Backend Guide](src/backend/README.md)
- [Deployment Guide](docs/DEPLOYMENT.md)

## 🤝 Contributing

Want to add an example? Here's how:

1. Create a new file in the appropriate category
2. Follow the existing naming convention
3. Include clear comments and documentation
4. Test your example thoroughly
5. Submit a pull request
