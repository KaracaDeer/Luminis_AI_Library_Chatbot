import React from 'react'
import { motion } from 'framer-motion'
import { Volume2, User, Bot } from 'lucide-react'
import { ChatMessage as ChatMessageType } from '../stores/chatStore'

interface ChatMessageProps {
  message: ChatMessageType
  onPlayAudio: () => void
  isPlaying: boolean
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message, onPlayAudio, isPlaying }) => {
  const isUser = message.sender === 'user'

  return (
    <motion.div
      initial={{ opacity: 0, x: isUser ? 20 : -20 }}
      animate={{ opacity: 1, x: 0 }}
      className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}
    >
      <div className={`flex items-start space-x-3 max-w-xs lg:max-w-md ${isUser ? 'flex-row-reverse space-x-reverse' : ''}`}>
        {/* Avatar */}
        <motion.div
          whileHover={{ scale: 1.1 }}
          className={`w-8 h-8 rounded-full flex items-center justify-center ${
            isUser 
              ? 'bg-primary-500 text-white' 
              : 'bg-gradient-to-r from-secondary-400 to-secondary-600 text-white'
          }`}
        >
          {isUser ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
        </motion.div>

        {/* Message Bubble */}
        <div className={`flex flex-col ${isUser ? 'items-end' : 'items-start'}`}>
          <motion.div
            whileHover={{ scale: 1.02 }}
            className={`chat-bubble ${
              isUser ? 'chat-bubble-user' : 'chat-bubble-assistant'
            }`}
          >
            <p className="text-sm leading-relaxed">{message.content}</p>
          </motion.div>

          {/* Audio Play Button (for assistant messages) */}
          {!isUser && (
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={onPlayAudio}
              disabled={isPlaying}
              className={`mt-2 p-2 rounded-full transition-all duration-200 ${
                isPlaying
                  ? 'bg-primary-200 text-primary-600'
                  : 'bg-gray-100 text-gray-600 hover:bg-primary-100 hover:text-primary-600'
              }`}
              title="Sesli Oynat"
            >
              <Volume2 className={`w-4 h-4 ${isPlaying ? 'animate-pulse' : ''}`} />
            </motion.button>
          )}

          {/* Timestamp */}
          <span className="text-xs text-gray-400 mt-1">
            {typeof message.timestamp === 'string' 
              ? new Date(message.timestamp).toLocaleTimeString('tr-TR', {
                  hour: '2-digit',
                  minute: '2-digit'
                })
              : message.timestamp.toLocaleTimeString('tr-TR', {
                  hour: '2-digit',
                  minute: '2-digit'
                })
            }
          </span>
        </div>
      </div>
    </motion.div>
  )
}

export default ChatMessage
