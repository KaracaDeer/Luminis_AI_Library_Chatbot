import React, { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { sendChatMessage } from '../services/api'
import VoiceRecorder from './VoiceRecorder'
import { Sparkles } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import { useLanguageStore } from '../stores/languageStore'

// Extend Window interface for SpeechRecognition
declare global {
  interface Window {
    SpeechRecognition: any
    webkitSpeechRecognition: any
  }
}

// Extend Window interface for global route change handler
declare global {
  interface Window {
    handleRouteChange?: (to: string) => void
  }
}

const ChatPage: React.FC = () => {
  const navigate = useNavigate()
  const { saveChat } = useAuth()
  const { language } = useLanguageStore()

  // Translations
  const translations = {
    tr: {
      backToHome: 'Ana Sayfa',
      libraryAssistant: 'Luminis.AI Kütüphane Asistanı',
      saveChat: 'Sohbeti Kaydet',
      saving: 'Kaydediliyor...',
      quickQuestions: 'Hızlı Sorular',
      romanRecommend: 'Roman önerebilir misin?',
      scifiInfo: 'Bilim kurgu kitapları hakkında bilgi ver',
      classicLit: 'Klasik edebiyat eserleri nelerdir?',
      readingHabit: 'Okuma alışkanlığı nasıl geliştirilir?',
      messagePlaceholder: 'Mesajınızı yazın...',
      voiceMessage: 'Sesli mesaj gönder',
      saveChatTooltip: 'Sohbeti Kaydet',
      sendMessage: 'Mesaj gönder',
      welcomeMessage: 'Merhaba! Ben Luminis.AI Kütüphane Asistanı. Size kitap önerileri verebilir, edebiyat hakkında bilgi verebilir ve okuma tavsiyelerinde bulunabilirim. Nasıl yardımcı olabilirim?',
      error: 'Hata:',
      unknownError: 'Bilinmeyen hata',
      voiceTranscriptionComing: 'Ses-metin çevirisi özelliği yakında eklenecek!',
      voiceTranscriptionFailed: 'Ses-metin çevirisi başarısız oldu. Lütfen tekrar deneyin.',
      noChatToSave: 'Kaydedilecek sohbet bulunamadı. Lütfen önce bir soru sorun.',
      chatSavedSuccess: 'Sohbet başarıyla kaydedildi! Hesabım sayfasından görüntüleyebilirsiniz.',
      chatSaveError: 'Sohbet kaydedilirken bir hata oluştu.'
    },
    en: {
      backToHome: 'Home',
      libraryAssistant: 'Luminis.AI Library Assistant',
      saveChat: 'Save Chat',
      saving: 'Saving...',
      quickQuestions: 'Quick Questions',
      romanRecommend: 'Can you recommend a novel?',
      scifiInfo: 'Tell me about science fiction books',
      classicLit: 'What are classic literature works?',
      readingHabit: 'How to develop reading habits?',
      messagePlaceholder: 'Type your message...',
      voiceMessage: 'Send voice message',
      saveChatTooltip: 'Save Chat',
      sendMessage: 'Send Message',
      welcomeMessage: 'Hello! I am Luminis.AI Library Assistant. I can give you book recommendations, provide information about literature and give reading advice. How can I help you?',
      error: 'Error:',
      unknownError: 'Unknown error',
      voiceTranscriptionComing: 'Voice-to-text transcription feature will be added soon!',
      voiceTranscriptionFailed: 'Voice transcription failed. Please try again.',
      noChatToSave: 'No chat found to save. Please ask a question first.',
      chatSavedSuccess: 'Chat saved successfully! You can view it from My Account page.',
      chatSaveError: 'An error occurred while saving the chat.'
    }
  }

  const t = translations[language]

  const [messages, setMessages] = useState<any[]>([
    {
      message: '',
      response: t.welcomeMessage,
      timestamp: new Date().toISOString()
    }
  ])

  // Update welcome message when language changes
  useEffect(() => {
    setMessages(prev => [
      {
        ...prev[0],
        response: t.welcomeMessage
      }
    ])
  }, [language, t.welcomeMessage])

  const [inputMessage, setInputMessage] = useState('')
  
  // Debug inputMessage state
  useEffect(() => {
    console.log('inputMessage state changed:', inputMessage);
    console.log('inputMessage length:', inputMessage.length);
  }, [inputMessage])
  const [isLoading, setIsLoading] = useState(false)
  const [showVoiceRecorder, setShowVoiceRecorder] = useState(false)
  const [isSaving, setIsSaving] = useState(false)
  const [recordingTime, setRecordingTime] = useState(0)
  const [isListening, setIsListening] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const recognitionRef = useRef<any>(null)
  const timeIntervalRef = useRef<NodeJS.Timeout | null>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleBackToHome = () => {
    if (window.handleRouteChange) {
      window.handleRouteChange('/')
    } else {
      navigate('/')
    }
  }

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isLoading) {
      console.log('Message blocked:', { inputMessage: inputMessage.trim(), isLoading })
      return
    }

    const userMessage = inputMessage.trim()
    console.log('Sending message:', userMessage) // Debug log
    
    setInputMessage('')
    setIsLoading(true)

    // Add user message to chat
    const newUserMessage: any = {
      message: userMessage,
      timestamp: new Date().toISOString()
    }
    setMessages(prev => [...prev, newUserMessage])

    try {
      // Send message to AI backend with language information
      const response = await sendChatMessage(userMessage, language)
      console.log('API Response:', response) // Debug log
      console.log('Response type:', typeof response) // Debug log
      console.log('Response keys:', Object.keys(response)) // Debug log
      
      // Create AI response message in correct format
      const aiResponseMessage: any = {
        message: '', // AI doesn't send a message, only responds
        response: response.response,
        timestamp: new Date().toISOString(),
        books: response.books || null // Include book data if available
      }
      
      // Add AI response to chat
      setMessages(prev => [...prev, aiResponseMessage])
    } catch (error) {
      console.error('Chat error:', error)
      // Add error message with more details
      const errorMessage: any = {
        message: '',
        response: `${t.error} ${error instanceof Error ? error.message : t.unknownError}`,
        timestamp: new Date().toISOString()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey && !isLoading) {
      e.preventDefault()
      e.stopPropagation() // Prevent event bubbling
      handleSendMessage()
    }
  }

  const handleQuickQuestion = (question: string) => {
    console.log('Setting input message from quick question:', question);
    setInputMessage(question)
  }


  const handleVoiceButtonClick = async () => {
    try {
      // If already listening, stop the recognition
      if (isListening && recognitionRef.current) {
        recognitionRef.current.stop()
        return
      }

      // Check if SpeechRecognition is supported
      if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        alert('Ses tanıma desteklenmiyor. Lütfen modern bir tarayıcı kullanın.')
        return
      }

      setIsLoading(true)
      setIsListening(true)
      
      // Initialize SpeechRecognition
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
      const recognition = new SpeechRecognition()
      recognitionRef.current = recognition
      
      recognition.continuous = false
      recognition.interimResults = true
      recognition.lang = language === 'tr' ? 'tr-TR' : 'en-US'
      
      recognition.onstart = () => {
        console.log('Ses tanıma başladı')
        setShowVoiceRecorder(true)
        setRecordingTime(0)
        
        // Update recording time every second
        timeIntervalRef.current = setInterval(() => {
          setRecordingTime((prev: number) => prev + 1)
        }, 1000)
      }
      
      recognition.onresult = (event: any) => {
        let finalTranscript = ''
        let interimTranscript = ''
        
        for (let i = event.resultIndex; i < event.results.length; i++) {
          const transcript = event.results[i][0].transcript
          if (event.results[i].isFinal) {
            finalTranscript += transcript
          } else {
            interimTranscript += transcript
          }
        }
        
        // Show interim results in real-time
        if (interimTranscript) {
          setInputMessage(interimTranscript)
        }
        
        // When final result is available
        if (finalTranscript) {
          console.log('Final tanınan metin:', finalTranscript)
          setInputMessage(finalTranscript)
        }
      }
      
      recognition.onerror = (event: any) => {
        console.error('Ses tanıma hatası:', event.error)
        let errorMessage = 'Ses tanıma hatası'
        
        if (event.error === 'no-speech') {
          errorMessage = 'Ses algılanamadı. Lütfen tekrar konuşun.'
        } else if (event.error === 'audio-capture') {
          errorMessage = 'Mikrofon erişimi sağlanamadı.'
        } else if (event.error === 'not-allowed') {
          errorMessage = 'Mikrofon erişimi reddedildi.'
        }
        
        alert(errorMessage)
        stopRecognition()
      }
      
      recognition.onend = () => {
        console.log('Ses tanıma sonlandı')
        stopRecognition()
      }
      
      // Start speech recognition
      recognition.start()
      
    } catch (error) {
      console.error('Error starting speech recognition:', error)
      alert('Ses tanıma başlatılamadı. Lütfen tekrar deneyin.')
      setIsLoading(false)
      setIsListening(false)
    }
  }

  const stopRecognition = () => {
    if (timeIntervalRef.current) {
      clearInterval(timeIntervalRef.current)
      timeIntervalRef.current = null
    }
    
    if (recognitionRef.current) {
      recognitionRef.current.stop()
      recognitionRef.current = null
    }
    
    setIsListening(false)
    setShowVoiceRecorder(false)
    setIsLoading(false)
  }

  const handleSaveChat = () => {
    if (messages.length <= 1) {
      alert(t.noChatToSave)
      return
    }

    setIsSaving(true)
    try {
      // Convert messages to AuthContext ChatMessage format
      const chatMessages = messages.map(msg => ({
        message: msg.content,
        response: msg.sender === 'assistant' ? msg.content : undefined,
        timestamp: msg.timestamp.toISOString()
      }))
      saveChat(chatMessages)
      alert(t.chatSavedSuccess)
    } catch (error) {
      alert(t.chatSaveError)
      console.error('Save chat error:', error)
    } finally {
      setIsSaving(false)
    }
  }

  const handleVoiceRecordingComplete = async (audioBlob: Blob) => {
    try {
      setIsLoading(true)
      
      // Simulate processing the audio and convert to text
      const voiceText = language === 'tr' 
        ? 'Sesli mesaj alındı ve işlendi' 
        : 'Voice message received and processed'
      
      // Put the text in the input field
      setInputMessage(voiceText)
      
      setShowVoiceRecorder(false)
      setIsLoading(false)
      setIsListening(false)
      
      // Clear the time interval
      if (timeIntervalRef.current) {
        clearInterval(timeIntervalRef.current)
        timeIntervalRef.current = null
      }
      
      console.log('Ses kaydı işlendi:', audioBlob.size, 'bytes')
    } catch (error) {
      console.error('Error processing voice recording:', error)
      alert('Ses kaydı işlenirken hata oluştu')
      setIsLoading(false)
      setIsListening(false)
    }
  }

  const handleVoiceRecordingCancel = () => {
    setShowVoiceRecorder(false)
    setIsListening(false)
    if (recognitionRef.current) {
      recognitionRef.current.stop()
    }
    if (timeIntervalRef.current) {
      clearInterval(timeIntervalRef.current)
    }
  }

  return (
    <div style={{ 
      minHeight: '100vh', 
      backgroundColor: '#FBF9E4',
      fontFamily: '"Libertinus Sans", system-ui, sans-serif'
    }}>
      {/* Header */}
      <div style={{
        backgroundColor: '#122C4F',
        padding: '20px 32px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        boxShadow: '0 4px 12px rgba(18, 44, 79, 0.15)'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <button
            onClick={handleBackToHome}
            style={{
              background: 'none',
              border: 'none',
              color: '#FBF9E4',
              padding: '8px',
              borderRadius: '8px',
              transition: 'all 0.3s ease',
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              fontSize: '16px',
              marginLeft: '50px'
            }}
            onMouseOver={(e) => {
              e.currentTarget.style.backgroundColor = 'rgba(251, 249, 228, 0.1)'
            }}
            onMouseOut={(e) => {
              e.currentTarget.style.backgroundColor = 'transparent'
            }}
          >
            ← {t.backToHome}
          </button>
        </div>
        
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginRight: '120px' }}>
          <Sparkles style={{ width: '20px', height: '20px', color: '#FBF9E4' }} />
          <h1 style={{ 
            color: '#FBF9E4', 
            margin: 0, 
            fontSize: '20px',
            fontWeight: '600'
          }}>
            {t.libraryAssistant}
          </h1>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginRight: '20px' }}>
          {/* Sohbeti Kaydet butonu kaldırıldı */}
        </div>
      </div>

      {/* Chat Container */}
      <div style={{
        maxWidth: '1200px',
        margin: '0 auto',
        padding: '32px',
        minHeight: 'calc(100vh - 120px)',
        display: 'flex',
        flexDirection: 'column'
      }}>
        {/* Messages */}
        <div style={{
          flex: 1,
          marginBottom: '20px',
          overflowY: 'auto',
          border: '2px solid #E5E7EB',
          borderRadius: '12px',
          padding: '20px',
          background: '#FBF9E4'
        }}>
          <AnimatePresence>
            {messages.map((message, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20, scale: 0.95 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                exit={{ opacity: 0, y: -20, scale: 0.95 }}
                transition={{ 
                  duration: 0.4, 
                  ease: "easeOut",
                  delay: index * 0.1
                }}
                style={{
                  marginBottom: '24px',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '12px'
                }}
              >
                {message.message && (
                  <motion.div
                    initial={{ opacity: 0, x: 50, scale: 0.9 }}
                    animate={{ opacity: 1, x: 0, scale: 1 }}
                    transition={{ duration: 0.3, ease: "easeOut" }}
                    style={{
                      alignSelf: 'flex-end',
                      maxWidth: '70%',
                      background: '#122C4F',
                      color: '#FBF9E4',
                      padding: '16px 20px',
                      borderRadius: '20px 20px 4px 20px',
                      fontSize: '16px',
                      lineHeight: '1.5',
                      wordWrap: 'break-word'
                    }}
                  >
                    {message.message}
                  </motion.div>
                )}
                
                {message.response && (
                  <motion.div
                    initial={{ opacity: 0, x: -50, scale: 0.9 }}
                    animate={{ opacity: 1, x: 0, scale: 1 }}
                    transition={{ duration: 0.3, ease: "easeOut" }}
                    style={{
                      alignSelf: 'flex-start',
                      maxWidth: '70%',
                      background: 'rgba(18, 44, 79, 0.05)',
                      color: '#1F2937',
                      padding: '16px 20px',
                      borderRadius: '20px 20px 20px 4px',
                      fontSize: '16px',
                      lineHeight: '1.5',
                      wordWrap: 'break-word',
                      boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)'
                    }}
                  >
                    {message.response}
                    
                    {/* Show book recommendations if available */}
                    {message.books && message.books.length > 0 && (
                      <div style={{ marginTop: '16px', paddingTop: '16px', borderTop: '1px solid rgba(18, 44, 79, 0.1)' }}>
                        <h4 style={{ margin: '0 0 12px 0', fontSize: '14px', fontWeight: '600', color: '#122C4F' }}>
                          📚 Önerilen Kitaplar:
                        </h4>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                          {message.books.map((book: any, index: number) => (
                            <div key={index} style={{
                              padding: '8px 12px',
                              background: 'rgba(18, 44, 79, 0.05)',
                              borderRadius: '8px',
                              border: '1px solid rgba(18, 44, 79, 0.1)'
                            }}>
                              <div style={{ fontWeight: '600', fontSize: '14px', color: '#122C4F' }}>
                                {book.title}
                              </div>
                              <div style={{ fontSize: '12px', color: '#6B7280', marginTop: '2px' }}>
                                {book.author} • {book.genre} • ⭐ {book.rating}
                              </div>
                              <div style={{ fontSize: '12px', color: '#6B7280', marginTop: '4px' }}>
                                {book.description}
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </motion.div>
                )}
              </motion.div>
            ))}
          </AnimatePresence>
          <div ref={messagesEndRef} />
        </div>

        {/* Quick Questions Section */}
        <AnimatePresence>
          {messages.length === 1 && (
            <div style={{
              marginBottom: '24px'
            }}>
              <motion.h3
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4, delay: 0.2 }}
                style={{
                  margin: '0 0 12px 0',
                  fontSize: '16px',
                  fontWeight: '600',
                  color: '#122C4F',
                  textAlign: 'center'
                }}
              >
                {t.quickQuestions}
              </motion.h3>
              <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))',
                gap: '8px'
              }}>
                {[
                  t.romanRecommend,
                  t.scifiInfo,
                  t.classicLit,
                  t.readingHabit
                ].map((question, index) => (
                  <motion.button
                    key={index}
                    initial={{ opacity: 0, y: 20, scale: 0.8 }}
                    animate={{ opacity: 1, y: 0, scale: 1 }}
                    transition={{ 
                      duration: 0.3, 
                      delay: 0.3 + index * 0.1,
                      ease: "easeOut"
                    }}
                    whileHover={{ 
                      scale: 1.05, 
                      y: -2,
                      transition: { duration: 0.2 }
                    }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => handleQuickQuestion(question)}
                    style={{
                      background: 'rgba(18, 44, 79, 0.05)',
                      border: '1px solid rgba(18, 44, 79, 0.1)',
                      color: '#122C4F',
                      padding: '8px 12px',
                      borderRadius: '8px',
                      fontSize: '12px',
                      fontWeight: '500',
                      textAlign: 'left',
                      // Replaced with hover effects
                      lineHeight: '1.4',
                      minHeight: '40px'
                    }}
                  >
                    {question}
                  </motion.button>
                ))}
              </div>
            </div>
          )}
        </AnimatePresence>

                 {/* Voice Recorder */}
          {showVoiceRecorder && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              transition={{ duration: 0.3, ease: "easeOut" }}
              style={{
                marginBottom: '16px',
                padding: '16px',
                border: '1px solid rgba(18, 44, 79, 0.1)',
                borderRadius: '12px',
                background: 'rgba(18, 44, 79, 0.02)'
              }}
            >
             <VoiceRecorder
               onRecordingComplete={handleVoiceRecordingComplete}
               onCancel={handleVoiceRecordingCancel}
               language={language}
               recordingTime={recordingTime}
             />
           </motion.div>
         )}

        {/* Input Area */}
        <div style={{
          display: 'flex',
          gap: '16px',
          alignItems: 'flex-end',
          marginTop: '10px',
          position: 'relative',
          zIndex: 1
        }}>
          <div style={{ 
            flex: 1,
            position: 'relative'
          }}>
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => {
                console.log('INPUT CHANGE:', e.target.value);
                setInputMessage(e.target.value);
              }}
              onKeyDown={handleKeyDown}
              placeholder={t.messagePlaceholder}
              style={{
                width: '100%',
                height: '50px',
                padding: '15px',
                border: '2px solid #E5E7EB',
                borderRadius: '8px',
                fontSize: '16px',
                fontFamily: 'inherit',
                backgroundColor: '#FBF9E4',
                color: '#122C4F'
              }}
              onFocus={(e) => {
                console.log('INPUT FOCUSED');
                e.target.style.borderColor = '#122C4F';
              }}
              onBlur={(e) => {
                console.log('INPUT BLURRED');
                e.target.style.borderColor = '#E5E7EB';
              }}
            />
          </div>
          
          <div style={{ display: 'flex', gap: '12px' }}>
            <motion.button
              onClick={handleVoiceButtonClick}
              whileHover={{ scale: 1.1, y: -2 }}
              whileTap={{ scale: 0.95 }}
              transition={{ duration: 0.2 }}
              style={{
                background: '#122C4F',
                border: 'none',
                color: '#FFFFFF',
                padding: '12px',
                borderRadius: '8px',
                fontSize: '16px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                width: '48px',
                height: '48px',
                // Replaced with hover effects
              }}
              title={t.voiceMessage}
            >
              🎙️
            </motion.button>
            
            <motion.button
              onClick={handleSaveChat}
              disabled={isSaving || messages.length <= 1}
              whileHover={!isSaving && messages.length > 1 ? { scale: 1.1, y: -2 } : {}}
              whileTap={!isSaving && messages.length > 1 ? { scale: 0.95 } : {}}
              transition={{ duration: 0.2 }}
              style={{
                background: isSaving || messages.length <= 1 ? '#6B7280' : '#122C4F',
                border: 'none',
                color: isSaving || messages.length <= 1 ? 'white' : '#FFFFFF',
                pointerEvents: isSaving || messages.length <= 1 ? 'none' : 'auto',
                padding: '12px',
                borderRadius: '8px',
                fontSize: '14px',
                fontWeight: '500',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                width: '48px',
                height: '48px',
                /* Hover efektleri ile etkileşim hissi verilir */
              }}
              title={t.saveChatTooltip}
            >
              💾
            </motion.button>
            
            <motion.button
              onClick={handleSendMessage}
              disabled={!inputMessage.trim() || isLoading}
              whileHover={inputMessage.trim() && !isLoading ? { scale: 1.1, y: -2 } : {}}
              whileTap={inputMessage.trim() && !isLoading ? { scale: 0.95 } : {}}
              transition={{ duration: 0.2 }}
              style={{
                background: !inputMessage.trim() || isLoading ? '#6B7280' : '#122C4F',
                border: 'none',
                color: !inputMessage.trim() || isLoading ? 'white' : '#FFFFFF',
                pointerEvents: !inputMessage.trim() || isLoading ? 'none' : 'auto',
                padding: '12px',
                borderRadius: '8px',
                fontSize: '16px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                width: '48px',
                height: '48px',
                /* Hover efektleri ile etkileşim hissi verilir */
              }}
              title={t.sendMessage}
            >
              ➤
            </motion.button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ChatPage
