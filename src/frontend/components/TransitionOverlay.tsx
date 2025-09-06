import React from 'react'
import { motion } from 'framer-motion'
import { Sparkles } from 'lucide-react'

interface TransitionOverlayProps {
  isVisible: boolean
}

const TransitionOverlay: React.FC<TransitionOverlayProps> = ({ isVisible }) => {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: isVisible ? 1 : 0 }}
      transition={{ duration: 0.6 }}
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100vw',
        height: '100vh',
        backgroundColor: '#122C4F',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 9999,
        pointerEvents: isVisible ? 'auto' : 'none'
      }}
    >
      <motion.div
        animate={{ 
          rotate: 360,
          scale: [1, 1.2, 1]
        }}
        transition={{ 
          rotate: { duration: 2, repeat: Infinity, ease: "linear" },
          scale: { duration: 1.5, repeat: Infinity, ease: "easeInOut" }
        }}
        style={{ marginBottom: '24px' }}
      >
        <Sparkles style={{ width: '64px', height: '64px', color: '#FBF9E4' }} />
      </motion.div>
      
      <motion.h1
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3, duration: 0.6 }}
        style={{
          fontSize: '32px',
          fontWeight: 'bold',
          color: '#FBF9E4',
          marginBottom: '16px',
          textAlign: 'center'
        }}
      >
        Luminis.AI
      </motion.h1>
      
      <motion.div
        initial={{ width: 0 }}
        animate={{ width: '200px' }}
        transition={{ delay: 0.6, duration: 1.2, ease: "easeInOut" }}
        style={{
          height: '4px',
          backgroundColor: '#FBF9E4',
          borderRadius: '2px',
          overflow: 'hidden'
        }}
      >
        <motion.div
          initial={{ x: '-100%' }}
          animate={{ x: '100%' }}
          transition={{ 
            delay: 0.6, 
            duration: 1.2, 
            ease: "easeInOut",
            repeat: Infinity,
            repeatDelay: 0.5
          }}
          style={{
            width: '100%',
            height: '100%',
            backgroundColor: 'rgba(251, 249, 228, 0.6)',
            borderRadius: '2px'
          }}
        />
      </motion.div>
    </motion.div>
  )
}

export default TransitionOverlay
