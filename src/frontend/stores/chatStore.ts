import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export interface ChatMessage {
  id: string
  content: string
  sender: 'user' | 'assistant'
  timestamp: Date
  language: 'tr' | 'en'
}

interface ChatState {
  messages: ChatMessage[]
  isLoading: boolean
  isRecording: boolean
  addMessage: (message: Omit<ChatMessage, 'id' | 'timestamp'>) => void
  setLoading: (loading: boolean) => void
  setRecording: (recording: boolean) => void
  clearMessages: () => void
  initializeChat: () => void
}

export const useChatStore = create<ChatState>()(
  persist(
    (set, get) => ({
      messages: [],
      isLoading: false,
      isRecording: false,
      
      addMessage: (message) => {
        const newMessage: ChatMessage = {
          ...message,
          id: Date.now().toString(),
          timestamp: new Date(),
        }
        set((state) => ({
          messages: [...state.messages, newMessage],
        }))
      },
      
      setLoading: (loading) => set({ isLoading: loading }),
      
      setRecording: (recording) => set({ isRecording: recording }),
      
      clearMessages: () => set({ messages: [] }),
      
      initializeChat: () => {
        const { messages } = get()
        if (messages.length === 0) {
          // Get current language from localStorage or default to 'tr'
          const currentLanguage = localStorage.getItem('luminis-language') || 'tr'
          
          const welcomeMessage: ChatMessage = {
            id: 'welcome',
            content: currentLanguage === 'tr' 
              ? 'Merhaba! Ben Luminis.AI kütüphane asistanınız. Kitap önerileri, kütüphane bilgileri veya herhangi bir konuda size yardımcı olabilirim. Nasıl yardımcı olabilirim?'
              : 'Hello! I am your Luminis.AI library assistant. I can help you with book recommendations, library information, or any other topic. How can I help you?',
            sender: 'assistant',
            timestamp: new Date(),
            language: currentLanguage as 'tr' | 'en'
          }
          set({ messages: [welcomeMessage] })
        }
      },
    }),
    {
      name: 'luminis-chat',
      partialize: (state) => ({ messages: state.messages }),
    }
  )
)
