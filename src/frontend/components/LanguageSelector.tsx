import React from 'react'
import { motion } from 'framer-motion'
import { Globe } from 'lucide-react'
import { useLanguageStore } from '../stores/languageStore'

const LanguageSelector: React.FC = () => {
  const { language, setLanguage } = useLanguageStore()

  const languages = [
    { code: 'tr', name: 'Türkçe', flag: '🇹🇷' },
    { code: 'en', name: 'English', flag: '🇺🇸' },
  ]

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.3, duration: 0.5 }}
      className="flex items-center justify-center space-x-4"
    >
      <motion.div
        animate={{ 
          rotate: [0, 10, -10, 0],
          scale: [1, 1.1, 1]
        }}
        transition={{ 
          duration: 4, 
          repeat: Infinity,
          delay: 2
        }}
      >
        <Globe className="w-6 h-6 text-primary-500" />
      </motion.div>
      <div className="flex space-x-3">
        {languages.map((lang, index) => (
          <motion.button
            key={lang.code}
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.5 + index * 0.1, duration: 0.5 }}
            whileHover={{ scale: 1.05, y: -2 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => setLanguage(lang.code as 'tr' | 'en')}
            className={`px-6 py-3 rounded-full text-sm font-semibold transition-all duration-300 flex items-center space-x-2 backdrop-blur-sm shadow-lg ${
              language === lang.code
                ? 'bg-gradient-to-r from-primary-500 to-secondary-500 text-white shadow-xl'
                : 'bg-white/80 text-foreground hover:bg-white hover:shadow-xl border border-primary-200/50'
            }`}
          >
            <motion.span 
              className="text-xl"
              animate={language === lang.code ? { 
                scale: [1, 1.2, 1],
                rotate: [0, 5, -5, 0]
              } : {}}
              transition={{ duration: 0.5 }}
            >
              {lang.flag}
            </motion.span>
            <span>{lang.name}</span>
          </motion.button>
        ))}
      </div>
    </motion.div>
  )
}

export default LanguageSelector
