import React from 'react'
import { motion } from 'framer-motion'

interface PageTransitionProps {
  children: React.ReactNode
}

const PageTransition: React.FC<PageTransitionProps> = ({ children }) => {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95, y: 20 }}
      animate={{ opacity: 1, scale: 1, y: 0 }}
      exit={{ opacity: 0, scale: 0.95, y: -20 }}
      transition={{ 
        duration: 0.5,
        ease: [0.4, 0.0, 0.2, 1]
      }}
      style={{ width: '100%', height: '100%' }}
    >
      {children}
    </motion.div>
  )
}

export default PageTransition
