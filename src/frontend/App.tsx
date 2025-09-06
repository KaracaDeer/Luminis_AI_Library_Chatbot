import React, { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, useLocation, useNavigate } from 'react-router-dom'
import { AnimatePresence } from 'framer-motion'
import { AuthProvider } from './contexts/AuthContext'
import LandingPage from './components/LandingPage'
import ChatPage from './components/ChatPage'
import RegisterPage from './components/RegisterPage'
import LoginPage from './components/LoginPage'
import AboutPage from './components/AboutPage'
import HelpPage from './components/HelpPage'
import AccountPage from './components/AccountPage'
import HoverEffectsDemo from './components/HoverEffectsDemo'
import Sidebar from './components/Sidebar'
import LanguageButton from './components/LanguageButton'
import PageTransition from './components/PageTransition'
import TransitionOverlay from './components/TransitionOverlay'

const AppContent: React.FC = () => {
  const location = useLocation()
  const navigate = useNavigate()
  const [isOverlayVisible, setIsOverlayVisible] = useState(true) // Start with overlay visible
  const [isInitialLoad, setIsInitialLoad] = useState(true)

  // Initial loading effect
  useEffect(() => {
    if (isInitialLoad) {
      setTimeout(() => {
        setIsOverlayVisible(false)
        setTimeout(() => {
          setIsInitialLoad(false)
        }, 300)
      }, 1000)
    }
  }, [isInitialLoad])

  useEffect(() => {
    const handleRouteChange = (to: string) => {
      setIsOverlayVisible(true)
      
      setTimeout(() => {
        navigate(to)
        setTimeout(() => {
          setIsOverlayVisible(false)
        }, 300)
      }, 400)
    }

    // Global route change handler
    window.handleRouteChange = handleRouteChange
  }, [navigate])

  return (
    <div style={{ position: 'relative', minHeight: '100vh' }}>
      <Sidebar />
      <LanguageButton />
      <TransitionOverlay isVisible={isOverlayVisible} />
      {!isInitialLoad && (
        <AnimatePresence mode="wait">
          <PageTransition key={location.pathname}>
                       <Routes location={location}>
               <Route path="/" element={<LandingPage />} />
               <Route path="/chat" element={<ChatPage />} />
               <Route path="/register" element={<RegisterPage />} />
               <Route path="/login" element={<LoginPage />} />
               <Route path="/about" element={<AboutPage />} />
               <Route path="/help" element={<HelpPage />} />
               <Route path="/account" element={<AccountPage />} />
               <Route path="/hover-demo" element={<HoverEffectsDemo />} />
             </Routes>
          </PageTransition>
        </AnimatePresence>
      )}
    </div>
  )
}

const App: React.FC = () => {
  return (
    <AuthProvider>
      <Router>
        <AppContent />
      </Router>
    </AuthProvider>
  )
}

export default App
