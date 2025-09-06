# Frontend Examples

This directory contains React/TypeScript examples for integrating with the Luminis AI Library Assistant frontend.

## 🚀 Available Examples

### 1. Chat Component Example
A reusable chat component that can be integrated into any React application.

### 2. Voice Recorder Example
Voice recording component with audio visualization and transcription.

### 3. Book Search Component
Search interface for finding and displaying books.

### 4. User Authentication Example
Complete authentication flow with login, registration, and profile management.

## 📁 File Structure

```
frontend_examples/
├── README.md
├── ChatComponent.tsx
├── VoiceRecorder.tsx
├── BookSearch.tsx
├── AuthExample.tsx
├── ApiService.ts
└── package.json
```

## 🛠️ Setup

1. **Install dependencies**
   ```bash
   cd examples/frontend_examples
   npm install
   ```

2. **Start development server**
   ```bash
   npm start
   ```

3. **Build for production**
   ```bash
   npm run build
   ```

## 📖 Usage Examples

### Chat Component
```tsx
import { ChatComponent } from './ChatComponent';

function App() {
  return (
    <div>
      <h1>My App</h1>
      <ChatComponent 
        apiUrl="http://localhost:8000"
        userId="user123"
      />
    </div>
  );
}
```

### Voice Recorder
```tsx
import { VoiceRecorder } from './VoiceRecorder';

function App() {
  const handleAudioData = (audioData: Blob) => {
    // Handle recorded audio
    console.log('Audio recorded:', audioData);
  };

  return (
    <VoiceRecorder 
      onAudioData={handleAudioData}
      maxDuration={30}
    />
  );
}
```

### Book Search
```tsx
import { BookSearch } from './BookSearch';

function App() {
  return (
    <BookSearch 
      apiUrl="http://localhost:8000"
      onBookSelect={(book) => console.log('Selected:', book)}
    />
  );
}
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the frontend_examples directory:

```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_URL=ws://localhost:8000/ws
```

### API Service
The `ApiService.ts` file provides a centralized way to make API calls:

```typescript
import { ApiService } from './ApiService';

const api = new ApiService('http://localhost:8000');

// Send chat message
const response = await api.sendChatMessage('Hello!');

// Search books
const books = await api.searchBooks('Python programming');

// Get user profile
const profile = await api.getUserProfile();
```

## 🎨 Styling

Examples use TailwindCSS for styling. Make sure to include TailwindCSS in your project:

```bash
npm install -D tailwindcss
npx tailwindcss init
```

## 📱 Responsive Design

All components are designed to be responsive and work on:
- Desktop computers
- Tablets
- Mobile phones

## 🔒 Authentication

The authentication example shows how to:
- Register new users
- Login existing users
- Manage user sessions
- Handle authentication errors
- Protect routes

## 🎤 Voice Features

The voice recorder example includes:
- Audio recording with MediaRecorder API
- Audio visualization
- File upload to backend
- Transcription display
- Error handling

## 📚 Book Search Features

The book search example includes:
- Real-time search
- Filter by genre
- Sort by popularity/rating
- Book details modal
- Pagination
- Loading states

## 🤝 Contributing

To add new examples:

1. Create a new `.tsx` file
2. Follow the existing component structure
3. Include TypeScript types
4. Add proper error handling
5. Update this README
6. Test thoroughly

