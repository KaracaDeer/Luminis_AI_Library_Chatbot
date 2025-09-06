import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Menu, X, UserPlus, LogIn, HelpCircle, Info, Sparkles, User } from 'lucide-react'
import { useAuth } from '../contexts/AuthContext'
import { useLanguageStore } from '../stores/languageStore'

// Extend Window interface for global route change handler
declare global {
  interface Window {
    handleRouteChange?: (to: string) => void
  }
}

const Sidebar: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false)
  const { isLoggedIn } = useAuth()
  const { language } = useLanguageStore()

  // Translations
  const translations = {
    tr: {
      myAccount: 'Hesabım',
      register: 'Kayıt Ol',
      login: 'Giriş Yap',
      help: 'Yardım',
      about: 'Hakkında'
    },
    en: {
      myAccount: 'My Account',
      register: 'Register',
      login: 'Login',
      help: 'Help',
      about: 'About'
    }
  }

  const t = translations[language]

  // Ensure component re-renders when language changes
  useEffect(() => {
    // Force re-render when language changes
  }, [language])

  const toggleSidebar = () => {
    setIsOpen(!isOpen)
  }

      const menuItems = [
        ...(isLoggedIn ? [
          { icon: User, label: t.myAccount, action: () => {
            if (window.handleRouteChange) {
              window.handleRouteChange('/account')
            }
          }}
        ] : [
          { icon: UserPlus, label: t.register, action: () => {
            if (window.handleRouteChange) {
              window.handleRouteChange('/register')
            }
          }},
          { icon: LogIn, label: t.login, action: () => {
            if (window.handleRouteChange) {
              window.handleRouteChange('/login')
            }
          }}
        ]),
        { icon: HelpCircle, label: t.help, action: () => {
          if (window.handleRouteChange) {
            window.handleRouteChange('/help')
          }
        }},
        { icon: Info, label: t.about, action: () => {
          if (window.handleRouteChange) {
            window.handleRouteChange('/about')
          }
        }}
      ]

  return (
    <div className="relative">
      {/* Hamburger Menu Button */}
      <button
        onClick={toggleSidebar}
        style={{
          position: 'absolute',
          top: '16px',
          left: '32px',
          zIndex: 50,
          padding: '8px',
          backgroundColor: '#122C4F',
          color: '#FBF9E4',
          borderRadius: '8px',
          border: 'none',
          boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
          transition: 'all 0.3s ease'
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
        {isOpen ? (
          <X style={{ width: '24px', height: '24px' }} />
        ) : (
          <Menu style={{ width: '24px', height: '24px' }} />
        )}
      </button>

      {/* Bubble Menu */}
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
              top: '64px',
              left: '32px',
              zIndex: 50,
              backgroundColor: '#FBF9E4',
              borderRadius: '16px',
              padding: '16px',
              boxShadow: '0 8px 32px rgba(0, 0, 0, 0.2)',
              border: '1px solid rgba(18, 44, 79, 0.1)',
              minWidth: '200px'
            }}
          >
            {/* Header */}
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              marginBottom: '12px',
              paddingBottom: '8px',
              borderBottom: '1px solid rgba(18, 44, 79, 0.1)'
            }}>
              <Sparkles style={{ width: '20px', height: '20px', color: '#122C4F' }} />
              <span style={{ 
                fontSize: '14px', 
                fontWeight: 'bold', 
                color: '#122C4F' 
              }}>
                Luminis.AI
              </span>
            </div>

            {/* Menu Items */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
              {menuItems.map((item, index) => (
                <motion.button
                  key={item.label}
                  initial={{ x: -20, opacity: 0 }}
                  animate={{ x: 0, opacity: 1 }}
                  transition={{ 
                    delay: index * 0.1,
                    duration: 0.3 
                  }}
                  onClick={() => {
                    item.action()
                    setIsOpen(false)
                  }}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '12px',
                    padding: '12px',
                    backgroundColor: 'transparent',
                    border: 'none',
                    borderRadius: '8px',
                    color: '#122C4F',
                    fontSize: '14px',
                    fontWeight: '500',
                    transition: 'all 0.2s ease',
                    width: '100%',
                    textAlign: 'left'
                  }}
                  onMouseOver={(e) => {
                    e.currentTarget.style.backgroundColor = 'rgba(18, 44, 79, 0.1)'
                  }}
                  onMouseOut={(e) => {
                    e.currentTarget.style.backgroundColor = 'transparent'
                  }}
                >
                  <div style={{
                    padding: '6px',
                    backgroundColor: 'rgba(18, 44, 79, 0.1)',
                    borderRadius: '6px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center'
                  }}>
                    <item.icon style={{ width: '16px', height: '16px' }} />
                  </div>
                  <span>{item.label}</span>
                </motion.button>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

export default Sidebar
