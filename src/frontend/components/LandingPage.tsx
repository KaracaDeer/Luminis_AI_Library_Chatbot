import React, { useEffect } from 'react'
import { motion } from 'framer-motion'
import { Sparkles, ArrowRight, BookOpen, User } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { useLanguageStore } from '../stores/languageStore'

// Extend Window interface for global route change handler
declare global {
  interface Window {
    handleRouteChange?: (to: string) => void
  }
}

const LandingPage: React.FC = () => {
  const navigate = useNavigate()
  const { user, isLoggedIn } = useAuth()
  const { language } = useLanguageStore()

  // Translations
  const translations = {
    tr: {
      welcome: 'Hoşgeldin',
      startChat: 'Sohbete Başla',
      exploreBooks: 'Keşfet',
      aboutUs: 'Hakkımızda',
      help: 'Yardım',
      hello: 'Merhaba',
      subtitle: 'Luminis.AI Kütüphane Asistanı ile kitap önerileri alın ve edebiyat dünyasını keşfedin.'
    },
    en: {
      welcome: 'Welcome',
      startChat: 'Start Chat',
      exploreBooks: 'Explore',
      aboutUs: 'About Us',
      help: 'Help',
      hello: 'Hello',
      subtitle: 'Get book recommendations and explore the world of literature with Luminis.AI Library Assistant.'
    }
  }

  const t = translations[language]

  // Ensure component renders correctly when language changes
  useEffect(() => {
    // Force re-render when language changes
  }, [language])

  const handleStartChat = () => {
    if (window.handleRouteChange) {
      window.handleRouteChange('/chat')
    } else {
      navigate('/chat')
    }
  }

  return (
    <div style={{ 
      minHeight: '100vh', 
      background: 'linear-gradient(to bottom, #122C4F 0%, #122C4F 50%, #FBF9E4 50%, #FBF9E4 100%)',
      fontFamily: '"Libertinus Sans", system-ui, sans-serif'
    }}>
      {/* Header */}
      <div style={{
        position: 'absolute',
        top: '32px',
        left: '32px',
        right: '32px',
        zIndex: 20
      }}>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: '48px'
        }}>
                     {/* Welcome Message - Left Side */}
           {isLoggedIn && user && (
             <div style={{
               display: 'flex',
               alignItems: 'center',
               gap: '8px',
               padding: '8px 16px',
               backgroundColor: 'rgba(251, 249, 228, 0.1)',
               borderRadius: '20px',
               border: '1px solid rgba(251, 249, 228, 0.2)',
               marginLeft: '120px'
             }}>
               <User style={{ width: '16px', height: '16px', color: '#FBF9E4' }} />
               <span style={{
                 fontSize: '14px',
                 fontWeight: '500',
                 color: '#FBF9E4'
               }}>
                 {t.welcome}, {user.username}
               </span>
             </div>
           )}

                     {/* Center Logo - Absolutely positioned for perfect centering */}
           <div style={{
             position: 'absolute',
             left: '50%',
             transform: 'translateX(-55%)',
             display: 'flex',
             alignItems: 'center',
             gap: '8px'
           }}>
             <Sparkles style={{ width: '24px', height: '24px', color: '#FBF9E4' }} />
             <h1 style={{
               fontSize: '24px',
               fontWeight: 'bold',
               color: '#FBF9E4',
               margin: 0
             }}>
               Luminis.AI
             </h1>
           </div>

           {/* Light Book Effect - Between Luminis.AI and Merhaba */}
           <motion.div
             initial={{ opacity: 0, scale: 0.8, rotate: -10 }}
             animate={{ opacity: 0.3, scale: 1, rotate: 0 }}
             transition={{ duration: 1, delay: 0.5 }}
             style={{
               position: 'absolute',
               top: '120px',
               left: '47%',
               transform: 'translateX(-50%)',
               zIndex: 5
             }}
           >
             <BookOpen 
               style={{ 
                 width: '80px', 
                 height: '80px', 
                 color: '#FBF9E4',
                 opacity: 0.4
               }} 
             />
           </motion.div>


        </div>
      </div>

                     {/* Main Content */}
        <div style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'flex-start',
          minHeight: '100vh',
          padding: '295px 32px 0 32px',
          textAlign: 'center',
          position: 'relative'
        }}>
                                       {/* Welcome Text - Split colored */}
           <motion.h2
             initial={{ opacity: 0, y: 30 }}
             animate={{ opacity: 1, y: 0 }}
             transition={{ duration: 0.8, delay: 0.2 }}
             style={{
               fontSize: '96px',
               fontWeight: 'bold',
               margin: '0 0 24px',
               position: 'relative',
               zIndex: 10
             }}
           >
             <span style={{
               background: 'linear-gradient(to bottom, #FBF9E4 0%, #FBF9E4 55%, #122C4F 55%, #122C4F 100%)',
               WebkitBackgroundClip: 'text',
               WebkitTextFillColor: 'transparent',
               backgroundClip: 'text'
             }}>
               {t.hello}
             </span>
           </motion.h2>

                   {/* Subtitle - Bottom half */}
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
            style={{
              fontSize: '20px',
              color: '#122C4F',
              margin: '0 0 48px',
              maxWidth: '600px',
              lineHeight: '1.6',
              position: 'relative',
              zIndex: 10
            }}
          >
            {t.subtitle}
          </motion.p>

         {/* Start Button - Bottom half */}
         <motion.button
           initial={{ opacity: 0, y: 30 }}
           animate={{ opacity: 1, y: 0 }}
           transition={{ duration: 0.8, delay: 0.6 }}
           onClick={handleStartChat}
           style={{
             display: 'flex',
             alignItems: 'center',
             gap: '12px',
             padding: '16px 32px',
             backgroundColor: '#122C4F',
             color: '#FBF9E4',
             border: 'none',
             borderRadius: '50px',
             fontSize: '18px',
             fontWeight: '600',
             boxShadow: '0 8px 24px rgba(18, 44, 79, 0.3)',
             transition: 'all 0.3s ease'
           }}
           onMouseOver={(e) => {
             e.currentTarget.style.transform = 'translateY(-2px)'
             e.currentTarget.style.boxShadow = '0 12px 32px rgba(18, 44, 79, 0.4)'
           }}
           onMouseOut={(e) => {
             e.currentTarget.style.transform = 'translateY(0)'
             e.currentTarget.style.boxShadow = '0 8px 24px rgba(18, 44, 79, 0.3)'
           }}
         >
           <span>{t.exploreBooks}</span>
           <ArrowRight style={{ width: '20px', height: '20px' }} />
         </motion.button>
       </div>
    </div>
  )
}

export default LandingPage
