import React, { useEffect } from 'react'
import { motion } from 'framer-motion'
import { Sparkles, ArrowLeft, BookOpen, Users, Zap, Heart } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { useLanguageStore } from '../stores/languageStore'

// Extend Window interface for global route change handler
declare global {
  interface Window {
    handleRouteChange?: (to: string) => void
  }
}

const AboutPage: React.FC = () => {
  const navigate = useNavigate()
  const { language } = useLanguageStore()

  // Translations
  const translations = {
    tr: {
      backToHome: '← Ana Sayfa',
      libraryAssistant: 'Luminis.AI Kütüphane Asistanı',
      about: 'Hakkında',
      aboutDescription: 'Luminis.AI Kütüphane Asistanı, yapay zeka teknolojisi kullanarak kütüphane ve kitap hakkında kapsamlı bilgi sağlayan modern bir platformdur.',
      features: 'Özellikler',
      bookRecommendations: 'Kitap Önerileri',
      bookRecommendationsDesc: 'Kişiselleştirilmiş kitap önerileri alın.',
      researchSupport: 'Araştırma Desteği',
      researchSupportDesc: 'Akademik araştırmalarınız için kapsamlı kaynak önerileri alın.',
      quickResponses: 'Hızlı Yanıtlar',
      quickResponsesDesc: 'Kütüphane ve kitap hakkında anında yanıtlar alın.',
      personalizedExperience: 'Kişiselleştirilmiş Deneyim',
      personalizedExperienceDesc: 'Okuma alışkanlıklarınıza göre özelleştirilmiş öneriler.',
      mission: 'Misyonumuz',
      missionDescription: 'Okuma ve öğrenmeyi herkes için erişilebilir kılmak, kütüphane kaynaklarını en etkili şekilde kullanmanıza yardımcı olmak.',
      technology: 'Teknoloji',
      technologyDescription: 'En son yapay zeka teknolojilerini kullanarak, kütüphane kaynaklarını akıllı bir şekilde analiz eder ve size en uygun bilgileri sunar.',
      contact: 'İletişim',
      contactDescription: 'Sorularınız veya önerileriniz için bizimle iletişime geçebilirsiniz.'
    },
    en: {
      backToHome: '← Home',
      libraryAssistant: 'Luminis.AI Library Assistant',
      about: 'About',
      aboutDescription: 'Luminis.AI Library Assistant is a modern platform that provides comprehensive information about libraries and books using artificial intelligence technology.',
      features: 'Features',
      bookRecommendations: 'Book Recommendations',
      bookRecommendationsDesc: 'Get personalized book recommendations.',
      researchSupport: 'Research Support',
      researchSupportDesc: 'Get comprehensive resource recommendations for your academic research.',
      quickResponses: 'Quick Responses',
      quickResponsesDesc: 'Get instant answers about libraries and books.',
      personalizedExperience: 'Personalized Experience',
      personalizedExperienceDesc: 'Customized recommendations based on your reading habits.',
      mission: 'Our Mission',
      missionDescription: 'To make reading and learning accessible to everyone, helping you use library resources most effectively.',
      technology: 'Technology',
      technologyDescription: 'Using the latest artificial intelligence technologies, it intelligently analyzes library resources and provides you with the most suitable information.',
      contact: 'Contact',
      contactDescription: 'You can contact us for your questions or suggestions.'
    }
  }

  const t = translations[language]

  // Ensure component re-renders when language changes
  useEffect(() => {
    // Force re-render when language changes
  }, [language])

  const handleBackToHome = () => {
    if (window.handleRouteChange) {
      window.handleRouteChange('/')
    } else {
      navigate('/')
    }
  }

  const features = [
    {
      icon: BookOpen,
      title: t.bookRecommendations,
      description: t.bookRecommendationsDesc
    },
    {
      icon: Users,
      title: t.researchSupport,
      description: t.researchSupportDesc
    },
    {
      icon: Zap,
      title: t.quickResponses,
      description: t.quickResponsesDesc
    },
    {
      icon: Heart,
      title: t.personalizedExperience,
      description: t.personalizedExperienceDesc
    }
  ]

  return (
    <div style={{ 
      minHeight: '100vh', 
      backgroundColor: '#FBF9E4',
      fontFamily: '"Libertinus Sans", system-ui, sans-serif'
    }}>
      {/* Header */}
      <div style={{
        backgroundColor: '#122C4F',
        padding: '20px 32px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        boxShadow: '0 4px 12px rgba(18, 44, 79, 0.15)'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginLeft: '120px' }}>
          <button
            onClick={handleBackToHome}
            style={{
              background: 'none',
              border: 'none',
              color: '#FBF9E4',
              padding: '8px',
              borderRadius: '8px',
              transition: 'all 0.3s ease',
              display: 'flex',
              alignItems: 'center',
              gap: '8px'
            }}
            onMouseOver={(e) => {
              e.currentTarget.style.backgroundColor = 'rgba(251, 249, 228, 0.1)'
            }}
            onMouseOut={(e) => {
              e.currentTarget.style.backgroundColor = 'transparent'
            }}
          >
            <ArrowLeft style={{ width: '20px', height: '20px' }} />
            <span style={{ fontSize: '14px', fontWeight: '500' }}>{t.backToHome}</span>
          </button>
        </div>
        
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginRight: '80px' }}>
          <Sparkles style={{ width: '24px', height: '24px', color: '#FBF9E4' }} />
          <h1 style={{ 
            fontSize: '20px', 
            fontWeight: 'bold', 
            color: '#FBF9E4',
            margin: 0
          }}>
            {t.libraryAssistant}
          </h1>
        </div>
        
        <div style={{ width: '120px' }}></div> {/* Spacer for centering */}
      </div>

      {/* Content */}
      <div style={{
        maxWidth: '800px',
        margin: '40px auto',
        padding: '40px',
        backgroundColor: '#FBF9E4',
        borderRadius: '20px',
        boxShadow: '0 8px 32px rgba(0, 0, 0, 0.1)',
        border: '2px solid rgba(18, 44, 79, 0.1)'
      }}>
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          {/* Header */}
          <div style={{
            textAlign: 'center',
            marginBottom: '40px'
          }}>
            <div style={{
              width: '80px',
              height: '80px',
              backgroundColor: '#122C4F',
              borderRadius: '50%',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              margin: '0 auto 20px'
            }}>
              <Sparkles style={{ width: '40px', height: '40px', color: '#FBF9E4' }} />
            </div>
            <h2 style={{
              fontSize: '32px',
              fontWeight: 'bold',
              color: '#122C4F',
              margin: '0 0 12px'
            }}>
              {t.about}
            </h2>
            <p style={{
              fontSize: '18px',
              color: '#122C4F',
              opacity: 0.8,
              margin: 0,
              lineHeight: '1.6'
            }}>
              {t.aboutDescription}
            </p>
          </div>

          {/* Mission */}
          <div style={{
            backgroundColor: 'rgba(18, 44, 79, 0.05)',
            padding: '24px',
            borderRadius: '16px',
            marginBottom: '40px',
            border: '1px solid rgba(18, 44, 79, 0.1)'
          }}>
            <h3 style={{
              fontSize: '24px',
              fontWeight: 'bold',
              color: '#122C4F',
              margin: '0 0 16px'
            }}>
              {t.mission}
            </h3>
            <p style={{
              fontSize: '16px',
              color: '#122C4F',
              lineHeight: '1.7',
              margin: 0
            }}>
              {t.missionDescription}
            </p>
          </div>

          {/* Features */}
          <div style={{ marginBottom: '40px' }}>
            <h3 style={{
              fontSize: '24px',
              fontWeight: 'bold',
              color: '#122C4F',
              margin: '0 0 24px',
              textAlign: 'center'
            }}>
              {t.features}
            </h3>
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
              gap: '20px'
            }}>
              {features.map((feature, index) => (
                <motion.div
                  key={feature.title}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1, duration: 0.5 }}
                  style={{
                    backgroundColor: 'rgba(18, 44, 79, 0.05)',
                    padding: '24px',
                    borderRadius: '16px',
                    border: '1px solid rgba(18, 44, 79, 0.1)',
                    textAlign: 'center'
                  }}
                >
                  <div style={{
                    width: '60px',
                    height: '60px',
                    backgroundColor: '#122C4F',
                    borderRadius: '50%',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    margin: '0 auto 16px'
                  }}>
                    <feature.icon style={{ width: '28px', height: '28px', color: '#FBF9E4' }} />
                  </div>
                  <h4 style={{
                    fontSize: '18px',
                    fontWeight: 'bold',
                    color: '#122C4F',
                    margin: '0 0 12px'
                  }}>
                    {feature.title}
                  </h4>
                  <p style={{
                    fontSize: '14px',
                    color: '#122C4F',
                    opacity: 0.8,
                    lineHeight: '1.6',
                    margin: 0
                  }}>
                    {feature.description}
                  </p>
                </motion.div>
              ))}
            </div>
          </div>

          {/* Technology */}
          <div style={{
            backgroundColor: 'rgba(18, 44, 79, 0.05)',
            padding: '24px',
            borderRadius: '16px',
            marginBottom: '40px',
            border: '1px solid rgba(18, 44, 79, 0.1)'
          }}>
            <h3 style={{
              fontSize: '24px',
              fontWeight: 'bold',
              color: '#122C4F',
              margin: '0 0 16px'
            }}>
              {t.technology}
            </h3>
            <p style={{
              fontSize: '16px',
              color: '#122C4F',
              lineHeight: '1.7',
              margin: '0 0 16px'
            }}>
              {t.technologyDescription}
            </p>
            <div style={{
              display: 'flex',
              flexWrap: 'wrap',
              gap: '8px'
            }}>
              {['React', 'TypeScript', 'AI/ML', 'Modern UI/UX'].map((tech) => (
                <span
                  key={tech}
                  style={{
                    backgroundColor: '#122C4F',
                    color: '#FBF9E4',
                    padding: '6px 12px',
                    borderRadius: '20px',
                    fontSize: '12px',
                    fontWeight: '500'
                  }}
                >
                  {tech}
                </span>
              ))}
            </div>
          </div>

          {/* Contact */}
          <div style={{
            backgroundColor: 'rgba(18, 44, 79, 0.05)',
            padding: '24px',
            borderRadius: '16px',
            marginBottom: '40px',
            border: '1px solid rgba(18, 44, 79, 0.1)'
          }}>
            <h3 style={{
              fontSize: '24px',
              fontWeight: 'bold',
              color: '#122C4F',
              margin: '0 0 16px'
            }}>
              {t.contact}
            </h3>
            <p style={{
              fontSize: '16px',
              color: '#122C4F',
              lineHeight: '1.7',
              margin: '0 0 16px'
            }}>
              {t.contactDescription}
            </p>
          </div>
          
        </motion.div>
      </div>
    </div>
  )
}

export default AboutPage
