const API_BASE_URL = 'http://localhost:8000/api';

export interface ChatMessage {
  message: string;
  response?: string;
  timestamp?: string;
}

export interface BookRecommendation {
  title: string;
  author: string;
  genre: string;
  description: string;
  rating: number;
  year: number;
}

export interface UserPreferences {
  genre?: string;
  mood?: string;
  readingLevel?: string;
}

export interface ReadingAnalysis {
  analysis: string;
  recommendations: string[];
}

// Chat API
export const sendChatMessage = async (message: string, language?: string): Promise<ChatMessage> => {
  try {
    console.log('Sending request to:', `${API_BASE_URL}/chat`);
    console.log('Request body:', { message, language });
    
    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message, language }),
    });

    console.log('Response status:', response.status);
    console.log('Response headers:', response.headers);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    console.log('Response data:', data);
    
    if (!data.success) {
      throw new Error(data.error || 'Chat mesajı gönderilemedi');
    }

    return {
      message: data.user_message,
      response: data.response,
      timestamp: new Date().toISOString(),
    };
  } catch (error) {
    console.error('Chat API Error:', error);
    throw error;
  }
};

// Book Recommendations API
export const getBookRecommendations = async (preferences: UserPreferences): Promise<{
  recommendations: string;
  books: BookRecommendation[];
}> => {
  try {
    const response = await fetch(`${API_BASE_URL}/book-recommendations`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ preferences }),
    });

    const data = await response.json();
    
    if (!data.success) {
      throw new Error(data.error || 'Kitap önerileri alınamadı');
    }

    return {
      recommendations: data.recommendations,
      books: data.books,
    };
  } catch (error) {
    console.error('Book Recommendations API Error:', error);
    throw error;
  }
};

// Get All Books API
export const getAllBooks = async (): Promise<BookRecommendation[]> => {
  try {
    const response = await fetch(`${API_BASE_URL}/books`);
    const data = await response.json();
    
    if (!data.success) {
      throw new Error(data.error || 'Kitaplar alınamadı');
    }

    return data.books;
  } catch (error) {
    console.error('Get Books API Error:', error);
    throw error;
  }
};

// Reading Analysis API
export const analyzeReadingList = async (readingList: BookRecommendation[]): Promise<ReadingAnalysis> => {
  try {
    const response = await fetch(`${API_BASE_URL}/analyze-reading`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ reading_list: readingList }),
    });

    const data = await response.json();
    
    if (!data.success) {
      throw new Error(data.error || 'Okuma analizi yapılamadı');
    }

    return {
      analysis: data.analysis,
      recommendations: [],
    };
  } catch (error) {
    console.error('Reading Analysis API Error:', error);
    throw error;
  }
};

// Audio Transcription API
export const transcribeAudio = async (audioBlob: Blob): Promise<string> => {
  try {
    const formData = new FormData();
    formData.append('file', audioBlob, 'audio.wav');

    const response = await fetch(`${API_BASE_URL}/transcribe`, {
      method: 'POST',
      body: formData,
    });

    const data = await response.json();
    
    if (!data.success) {
      throw new Error(data.error || 'Ses-metin çevirisi başarısız');
    }

    return data.text;
  } catch (error) {
    console.error('Transcription API Error:', error);
    throw error;
  }
};

// Mock data for development
export const mockBooks: BookRecommendation[] = [
  {
    title: "Suç ve Ceza",
    author: "Fyodor Dostoyevski",
    genre: "Roman",
    description: "Psikolojik gerilim ve ahlaki sorgulama",
    rating: 4.8,
    year: 1866
  },
  {
    title: "1984",
    author: "George Orwell",
    genre: "Distopya",
    description: "Totaliter rejim eleştirisi",
    rating: 4.7,
    year: 1949
  },
  {
    title: "Küçük Prens",
    author: "Antoine de Saint-Exupéry",
    genre: "Çocuk Edebiyatı",
    description: "Felsefi masal",
    rating: 4.9,
    year: 1943
  },
  {
    title: "Dune",
    author: "Frank Herbert",
    genre: "Bilim Kurgu",
    description: "Epik bilim kurgu romanı",
    rating: 4.6,
    year: 1965
  },
  {
    title: "Hobbit",
    author: "J.R.R. Tolkien",
    genre: "Fantastik",
    description: "Macera dolu fantastik roman",
    rating: 4.8,
    year: 1937
  }
];
