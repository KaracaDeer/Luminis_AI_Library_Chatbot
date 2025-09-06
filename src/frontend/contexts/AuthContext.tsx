import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react'

export interface ChatMessage {
  message: string
  response?: string
  timestamp: string
}

export interface ChatHistory {
  id: string
  title: string
  messages: ChatMessage[]
  createdAt: string
  lastUpdated: string
}

interface User {
  id: string
  firstName: string
  lastName: string
  username: string
  email: string
  joinDate: string
  password: string
}

interface AuthContextType {
  user: User | null
  isLoggedIn: boolean
  chatHistory: ChatHistory[]
  login: (identifier: string, password: string) => Promise<{ success: boolean; error?: string }>
  register: (userData: {
    firstName: string
    lastName: string
    username: string
    email: string
    password: string
  }) => Promise<{ success: boolean; error?: string }>
  logout: () => void
  deleteAccount: () => Promise<{ success: boolean; error?: string }>
  saveChat: (messages: ChatMessage[]) => void
  deleteChat: (chatId: string) => void
  getChatHistory: () => ChatHistory[]
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

interface AuthProviderProps {
  children: ReactNode
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(() => {
    const savedUser = localStorage.getItem('luminis_current_user')
    return savedUser ? JSON.parse(savedUser) : null
  })
  
  // Initialize users from localStorage or default
  const [users, setUsers] = useState<User[]>(() => {
    const savedUsers = localStorage.getItem('luminis_users')
    if (savedUsers) {
      return JSON.parse(savedUsers)
    }
    // Default user
    const defaultUsers = [
      {
        id: '1',
        firstName: 'Ahmet',
        lastName: 'Yılmaz',
        username: 'ahmetyilmaz',
        email: 'test@example.com',
        joinDate: '15 Mart 2024',
        password: '123456'
      }
    ]
    localStorage.setItem('luminis_users', JSON.stringify(defaultUsers))
    return defaultUsers
  })

  // Initialize chat history from localStorage
  const [chatHistory, setChatHistory] = useState<ChatHistory[]>(() => {
    if (!user) return []
    const savedHistory = localStorage.getItem(`luminis_chat_history_${user.id}`)
    return savedHistory ? JSON.parse(savedHistory) : []
  })

  // Save users to localStorage whenever users state changes
  useEffect(() => {
    localStorage.setItem('luminis_users', JSON.stringify(users))
  }, [users])

  // Save current user to localStorage whenever user state changes
  useEffect(() => {
    if (user) {
      localStorage.setItem('luminis_current_user', JSON.stringify(user))
    } else {
      localStorage.removeItem('luminis_current_user')
    }
  }, [user])

  // Save chat history to localStorage whenever it changes
  useEffect(() => {
    if (user && chatHistory.length > 0) {
      localStorage.setItem(`luminis_chat_history_${user.id}`, JSON.stringify(chatHistory))
    }
  }, [chatHistory, user])

  const login = async (identifier: string, password: string): Promise<{ success: boolean; error?: string }> => {
    return new Promise((resolve) => {
      setTimeout(() => {
        // Check if identifier is email or username
        const foundUser = users.find(user => 
          user.email === identifier || user.username === identifier
        )
        
        if (!foundUser) {
          resolve({ 
            success: false, 
            error: 'Kullanıcı hesabı bulunamadı. Lütfen e-posta adresinizi veya kullanıcı adınızı kontrol edin.' 
          })
          return
        }
        
        // Mock password validation (in real app, this would be hashed)
        if (password === foundUser.password) {
          setUser(foundUser)
          resolve({ success: true })
        } else {
          resolve({ 
            success: false, 
            error: 'Şifre hatalı. Lütfen tekrar deneyin.' 
          })
        }
      }, 1000)
    })
  }

  const register = async (userData: {
    firstName: string
    lastName: string
    username: string
    email: string
    password: string
  }): Promise<{ success: boolean; error?: string }> => {
    return new Promise((resolve) => {
      setTimeout(() => {
        // Check if username already exists
        const existingUsername = users.find(user => user.username === userData.username)
        if (existingUsername) {
          resolve({ 
            success: false, 
            error: 'Bu kullanıcı adı zaten kullanılıyor. Lütfen farklı bir kullanıcı adı seçin.' 
          })
          return
        }
        
        // Check if email already exists
        const existingEmail = users.find(user => user.email === userData.email)
        if (existingEmail) {
          resolve({ 
            success: false, 
            error: 'Bu e-posta adresi zaten kayıtlı. Lütfen farklı bir e-posta adresi kullanın.' 
          })
          return
        }
        
        const newUser: User = {
          id: Date.now().toString(),
          firstName: userData.firstName,
          lastName: userData.lastName,
          username: userData.username,
          email: userData.email,
          password: userData.password,
          joinDate: new Date().toLocaleDateString('tr-TR', {
            day: 'numeric',
            month: 'long',
            year: 'numeric'
          })
        }
        
        setUsers(prev => [...prev, newUser])
        setUser(newUser)
        resolve({ success: true })
      }, 1000)
    })
  }

  const logout = () => {
    setUser(null)
    // localStorage'dan da temizle
    localStorage.removeItem('luminis_current_user')
  }

  const deleteAccount = async (): Promise<{ success: boolean; error?: string }> => {
    return new Promise((resolve) => {
      setTimeout(() => {
        if (user) {
          // Remove user from users list
          setUsers(prev => prev.filter(u => u.id !== user.id))
          // Clear current user
          setUser(null)
          // Clear chat history
          localStorage.removeItem(`luminis_chat_history_${user.id}`)
          resolve({ success: true })
        } else {
          resolve({ 
            success: false, 
            error: 'Kullanıcı bulunamadı.' 
          })
        }
      }, 1000)
    })
  }

  const saveChat = (messages: ChatMessage[]) => {
    if (!user || messages.length === 0) return

    const now = new Date().toISOString()
    const firstMessage = messages.find(m => m.message)?.message || 'Yeni Sohbet'
    const title = firstMessage.length > 30 ? firstMessage.substring(0, 30) + '...' : firstMessage

    const newChat: ChatHistory = {
      id: Date.now().toString(),
      title,
      messages,
      createdAt: now,
      lastUpdated: now
    }

    setChatHistory(prev => [newChat, ...prev])
  }

  const deleteChat = (chatId: string) => {
    setChatHistory(prev => prev.filter(chat => chat.id !== chatId))
  }

  const getChatHistory = (): ChatHistory[] => {
    return chatHistory
  }

  const value: AuthContextType = {
    user,
    isLoggedIn: !!user,
    chatHistory,
    login,
    register,
    logout,
    deleteAccount,
    saveChat,
    deleteChat,
    getChatHistory
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}
