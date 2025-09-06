import React, { useState, useRef, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Mic, Square, RotateCcw } from 'lucide-react'
import { useLanguageStore } from '../stores/languageStore'

interface VoiceRecorderProps {
  onRecordingComplete: (audioBlob: Blob) => void
  onCancel: () => void
  isRecording?: boolean
  recordingTime?: number
  language?: string
}

const VoiceRecorder: React.FC<VoiceRecorderProps> = ({ onRecordingComplete, onCancel, isRecording = false, recordingTime = 0 }) => {
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null)
  const { language } = useLanguageStore()

  // Translations
  const translations = {
    tr: {
      recording: 'Kayıt yapılıyor...',
      recordingTime: 'Kayıt Süresi',
      recordingCompleted: 'Kayıt Tamamlandı'
    },
    en: {
      recording: 'Recording...',
      recordingTime: 'Recording Time',
      recordingCompleted: 'Recording Completed'
    }
  }

  const t = translations[language]

  const handleSubmit = () => {
    if (audioBlob) {
      onRecordingComplete(audioBlob)
      setAudioBlob(null)
    }
  }

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
  }

  // Simulate recording completion after 10 seconds
  useEffect(() => {
    if (isRecording && !audioBlob) {
      const timer = setTimeout(() => {
        // Create a dummy blob for demonstration
        const dummyBlob = new Blob(['dummy audio data'], { type: 'audio/webm' })
        setAudioBlob(dummyBlob)
      }, 10000)
      
      return () => clearTimeout(timer)
    }
  }, [isRecording, audioBlob])

  const renderRecordingState = () => (
    <div>
      <div style={{
        width: '40px',
        height: '40px',
        background: '#ef4444',
        borderRadius: '50%',
        margin: '0 auto 12px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        boxShadow: '0 2px 8px rgba(239, 68, 68, 0.4)',
        animation: 'pulse 1s infinite'
      }}>
        <span style={{ fontSize: '16px' }}>⏺️</span>
      </div>
      
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        gap: '8px',
        marginBottom: '12px'
      }}>
        <div style={{
          width: '6px',
          height: '6px',
          background: '#ef4444',
          borderRadius: '50%',
          animation: 'pulse 1s infinite'
        }}></div>
        <span style={{
          fontSize: '16px',
          fontWeight: '700',
          fontFamily: 'monospace',
          color: '#122C4F'
        }}>{formatTime(recordingTime)}</span>
        <div style={{
          width: '6px',
          height: '6px',
          background: '#ef4444',
          borderRadius: '50%',
          animation: 'pulse 1s infinite'
        }}></div>
      </div>
      
      <p style={{
        fontSize: '12px',
        color: '#6B7280',
        marginBottom: '12px',
        textAlign: 'center',
        fontWeight: '500'
      }}>
        {t.recording}
      </p>
    </div>
  )

  const renderCompletedState = () => (
    <div className="text-center">
      <div style={{
        width: '32px',
        height: '32px',
        background: '#10b981',
        borderRadius: '50%',
        margin: '0 auto 12px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        boxShadow: '0 2px 8px rgba(16, 185, 129, 0.3)',
        animation: 'bounce 1s infinite'
      }}>
        <span style={{ fontSize: '14px' }}>✅</span>
      </div>
      
      <h3 style={{
        fontSize: '14px',
        fontWeight: '600',
        color: '#122C4F',
        marginBottom: '12px'
      }}>
        {t.recordingCompleted}
      </h3>
      
      <div className="flex justify-center space-x-2">
        <motion.button
          whileHover={{ scale: 1.05, y: -1 }}
          whileTap={{ scale: 0.95 }}
          onClick={handleSubmit}
          style={{
            background: '#10b981',
            color: 'white',
            padding: '6px 12px',
            borderRadius: '12px',
            border: 'none',
            // Replaced with hover effects
            fontSize: '11px',
            fontWeight: '600',
            transition: 'all 0.3s ease',
            boxShadow: '0 2px 6px rgba(16, 185, 129, 0.4)'
          }}
          onMouseOver={(e) => {
            e.currentTarget.style.transform = 'translateY(-1px)'
            e.currentTarget.style.boxShadow = '0 4px 12px rgba(16, 185, 129, 0.5)'
          }}
          onMouseOut={(e) => {
            e.currentTarget.style.transform = 'translateY(0)'
            e.currentTarget.style.boxShadow = '0 2px 6px rgba(16, 185, 129, 0.4)'
          }}
        >
          {language === 'tr' ? 'Gönder' : 'Send'}
        </motion.button>
        
        <motion.button
          whileHover={{ scale: 1.05, y: -1 }}
          whileTap={{ scale: 0.95 }}
          onClick={onCancel}
          style={{
            background: '#FCA5A5',
            color: '#991B1B',
            padding: '6px 12px',
            borderRadius: '12px',
            border: 'none',
            // Replaced with hover effects
            fontSize: '11px',
            fontWeight: '600',
            transition: 'all 0.3s ease',
            boxShadow: '0 2px 6px rgba(252, 165, 165, 0.4)'
          }}
          onMouseOver={(e) => {
            e.currentTarget.style.transform = 'translateY(-1px)'
            e.currentTarget.style.boxShadow = '0 4px 12px rgba(252, 165, 165, 0.5)'
          }}
          onMouseOut={(e) => {
            e.currentTarget.style.transform = 'translateY(0)'
            e.currentTarget.style.boxShadow = '0 2px 6px rgba(252, 165, 165, 0.4)'
          }}
        >
          {language === 'tr' ? 'İptal' : 'Cancel'}
        </motion.button>
      </div>
    </div>
  )

  return (
    <>
      <style>
        {`
          @keyframes pulse {
            0%, 100% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.05); opacity: 0.8; }
          }
          @keyframes bounce {
            0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
            40% { transform: translateY(-10px); }
            60% { transform: translateY(-5px); }
          }
        `}
      </style>
      
      <div style={{
        width: '100%',
        padding: '0',
        margin: '0'
      }}>
        {!audioBlob ? (
          renderRecordingState()
        ) : (
          renderCompletedState()
        )}
      </div>
    </>
  )
}

export default VoiceRecorder
