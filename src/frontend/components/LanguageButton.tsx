import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Globe, ChevronDown } from 'lucide-react'
import { useLanguageStore } from '../stores/languageStore'

const LanguageButton: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false)
  const { language, setLanguage } = useLanguageStore()

  const languages = [
    { code: 'tr', name: 'Türkçe' },
    { code: 'en', name: 'English' }
  ]

  const toggleLanguageMenu = () => {
    setIsOpen(!isOpen)
  }

  const selectLanguage = (langCode: 'tr' | 'en') => {
    setLanguage(langCode)
    setIsOpen(false)
    console.log(`Language changed to: ${langCode}`)
  }

  const currentLanguageName = languages.find(lang => lang.code === language)?.name || 'TR'

  return (
    <div className="relative">
      {/* Language Button */}
      <button
        onClick={toggleLanguageMenu}
        style={{
          position: 'absolute',
          top: '24px',
          right: '32px',
          zIndex: 50,
          padding: '8px 12px',
          backgroundColor: '#122C4F',
          color: '#FBF9E4',
          borderRadius: '8px',
          border: 'none',
          boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
          transition: 'all 0.3s ease',
          display: 'flex',
          alignItems: 'center',
          gap: '6px',
          fontSize: '14px',
          fontWeight: '500'
        }}
        onMouseOver={(e) => {
          e.currentTarget.style.backgroundColor = '#1a3a5f'
          e.currentTarget.style.transform = 'scale(1.05)'
        }}
        onMouseOut={(e) => {
          e.currentTarget.style.backgroundColor = '#122C4F'
          e.currentTarget.style.transform = 'scale(1)'
        }}
      >
        <Globe style={{ width: '16px', height: '16px' }} />
        <span>{language.toUpperCase()}</span>
        <ChevronDown style={{ 
          width: '14px', 
          height: '14px',
          transform: isOpen ? 'rotate(180deg)' : 'rotate(0deg)',
          transition: 'transform 0.3s ease'
        }} />
      </button>

      {/* Language Dropdown */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, scale: 0.8, y: -20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.8, y: -20 }}
            transition={{ 
              type: "spring", 
              damping: 25, 
              stiffness: 200 
            }}
            style={{
              position: 'absolute',
              top: '72px',
              right: '32px',
              zIndex: 50,
              backgroundColor: '#FBF9E4',
              borderRadius: '16px',
              padding: '12px',
              boxShadow: '0 8px 32px rgba(0, 0, 0, 0.2)',
              border: '1px solid rgba(18, 44, 79, 0.1)',
              minWidth: '160px'
            }}
          >
            {/* Language Options */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '2px' }}>
              {languages.map((lang, index) => (
                <motion.button
                  key={lang.code}
                  initial={{ x: 20, opacity: 0 }}
                  animate={{ x: 0, opacity: 1 }}
                  transition={{ 
                    delay: index * 0.05,
                    duration: 0.3 
                  }}
                  onClick={() => selectLanguage(lang.code as 'tr' | 'en')}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px',
                    padding: '10px 12px',
                    backgroundColor: language === lang.code ? 'rgba(18, 44, 79, 0.1)' : 'transparent',
                    border: 'none',
                    borderRadius: '8px',
                    color: '#122C4F',
                    fontSize: '14px',
                    fontWeight: language === lang.code ? '600' : '500',
                    transition: 'all 0.2s ease',
                    width: '100%',
                    textAlign: 'left'
                  }}
                  onMouseOver={(e) => {
                    if (language !== lang.code) {
                      e.currentTarget.style.backgroundColor = 'rgba(18, 44, 79, 0.05)'
                    }
                  }}
                  onMouseOut={(e) => {
                    if (language !== lang.code) {
                      e.currentTarget.style.backgroundColor = 'transparent'
                    }
                  }}
                >
                  <span style={{ 
                    width: '8px', 
                    height: '8px', 
                    borderRadius: '50%',
                    backgroundColor: language === lang.code ? '#122C4F' : 'transparent',
                    border: language === lang.code ? 'none' : '1px solid rgba(18, 44, 79, 0.3)'
                  }} />
                  <span>{lang.name}</span>
                </motion.button>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

export default LanguageButton
