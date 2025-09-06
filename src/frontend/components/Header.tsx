import React from 'react'
import { motion } from 'framer-motion'
import { BookOpen, Sparkles } from 'lucide-react'
import { useLanguageStore } from '../stores/languageStore'

const Header: React.FC = () => {
  const { language } = useLanguageStore()

  // Translations
  const translations = {
    tr: {
      libraryAssistant: 'Kütüphane Asistanı',
      online: 'Çevrimiçi'
    },
    en: {
      libraryAssistant: 'Library Assistant',
      online: 'Online'
    }
  }

  const t = translations[language]

  return (
    <motion.header
      initial={{ y: -50, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="sticky top-0 z-50 glass-effect backdrop-blur-md"
    >
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <motion.div
            whileHover={{ scale: 1.05 }}
            className="flex items-center space-x-3"
          >
            <div className="relative">
              <BookOpen className="w-8 h-8 text-primary-600" />
              <Sparkles className="w-4 h-4 text-secondary-500 absolute -top-1 -right-1" />
            </div>
            <div>
              <h1 className="text-xl font-bold gradient-text">Luminis.AI</h1>
              <p className="text-xs text-gray-500">{t.libraryAssistant}</p>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3 }}
            className="hidden md:flex items-center space-x-4"
          >
            <div className="flex items-center space-x-2 text-sm text-gray-600">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              <span>{t.online}</span>
            </div>
          </motion.div>
        </div>
      </div>
    </motion.header>
  )
}

export default Header
