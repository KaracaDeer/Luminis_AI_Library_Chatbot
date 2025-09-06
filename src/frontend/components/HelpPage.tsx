import React, { useEffect } from 'react'
import { motion } from 'framer-motion'
import { Sparkles, ArrowLeft, HelpCircle, BookOpen, Search, MessageCircle, Settings } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { useLanguageStore } from '../stores/languageStore'

// Extend Window interface for global route change handler
declare global {
  interface Window {
    handleRouteChange?: (to: string) => void
  }
}

const HelpPage: React.FC = () => {
  const navigate = useNavigate()
  const { language } = useLanguageStore()

  // Translations
  const translations = {
    tr: {
      backToHome: '← Ana Sayfa',
      libraryAssistant: 'Luminis.AI Kütüphane Asistanı',
      help: 'Yardım',
      helpDescription: 'Luminis.AI Kütüphane Asistanı kullanımı hakkında sık sorulan sorular ve yardım konuları.',
      frequentlyAskedQuestions: 'Sık Sorulan Sorular',
      howItWorks: 'Luminis.AI Kütüphane Asistanı nasıl çalışır?',
      howItWorksAnswer: 'Luminis.AI, yapay zeka teknolojisi kullanarak kitap önerileri sunar. Okuma alışkanlıklarınızı analiz eder ve size en uygun kitapları önerir. Ayrıca kütüphane hizmetleri hakkında sorularınızı yanıtlar.',
      howRecommendations: 'Kitap önerileri nasıl oluşturulur?',
      howRecommendationsAnswer: 'Sistem, daha önce okuduğunuz kitapları, tercih ettiğiniz türleri ve okuma alışkanlıklarınızı analiz ederek kişiselleştirilmiş öneriler sunar. Daha fazla kitap ekledikçe öneriler daha da doğru hale gelir.',
      bookTypes: 'Hangi tür kitaplar için öneri alabilirim?',
      bookTypesAnswer: 'Roman, bilim kurgu, tarih, felsefe, bilim, kişisel gelişim, akademik kitaplar ve daha birçok tür için öneri alabilirsiniz. Sistem sürekli olarak yeni kitaplar ekleyerek kütüphanesini genişletir.',
      differentLanguages: 'Farklı dillerde kitap önerisi alabilir miyim?',
      differentLanguagesAnswer: 'Evet, sistem Türkçe ve İngilizce dillerinde kitap önerileri sunar. Dil tercihinizi ayarlar bölümünden değiştirebilirsiniz.',
      helpCategories: 'Yardım Kategorileri',
      bookRecommendations: 'Kitap Önerileri',
      bookRecommendationsDesc: 'Kişiselleştirilmiş kitap önerileri alma ve okuma listeleri oluşturma konusunda yardım.',
      searchAndFilter: 'Arama ve Filtreleme',
      searchAndFilterDesc: 'Kitapları tür, yazar, yıl gibi kriterlere göre arama ve filtreleme işlemleri.',
      chatAssistant: 'Sohbet Asistanı',
      chatAssistantDesc: 'Kütüphane asistanı ile sohbet ederek kitap önerileri alma ve sorularınızı sorma.',
      accountSettings: 'Hesap Ayarları',
      accountSettingsDesc: 'Profil bilgilerinizi düzenleme, dil tercihleri ve gizlilik ayarları.',
      contactSupport: 'Destek İletişim',
      contactSupportDesc: 'Ek yardım için destek ekibimizle iletişime geçebilirsiniz.'
    },
    en: {
      backToHome: '← Home',
      libraryAssistant: 'Luminis.AI Library Assistant',
      help: 'Help',
      helpDescription: 'Frequently asked questions and help topics about using Luminis.AI Library Assistant.',
      frequentlyAskedQuestions: 'Frequently Asked Questions',
      howItWorks: 'How does Luminis.AI Library Assistant work?',
      howItWorksAnswer: 'Luminis.AI provides book recommendations using artificial intelligence technology. It analyzes your reading habits and recommends the most suitable books for you. It also answers your questions about library services.',
      howRecommendations: 'How are book recommendations generated?',
      howRecommendationsAnswer: 'The system provides personalized recommendations by analyzing the books you have read before, the genres you prefer, and your reading habits. As you add more books, the recommendations become more accurate.',
      bookTypes: 'What types of books can I get recommendations for?',
      bookTypesAnswer: 'You can get recommendations for novels, science fiction, history, philosophy, science, personal development, academic books, and many other genres. The system continuously expands its library by adding new books.',
      differentLanguages: 'Can I get book recommendations in different languages?',
      differentLanguagesAnswer: 'Yes, the system provides book recommendations in Turkish and English. You can change your language preference in the settings section.',
      helpCategories: 'Help Categories',
      bookRecommendations: 'Book Recommendations',
      bookRecommendationsDesc: 'Help with getting personalized book recommendations and creating reading lists.',
      searchAndFilter: 'Search and Filtering',
      searchAndFilterDesc: 'Searching and filtering books by criteria such as genre, author, year.',
      chatAssistant: 'Chat Assistant',
      chatAssistantDesc: 'Getting book recommendations and asking questions by chatting with the library assistant.',
      accountSettings: 'Account Settings',
      accountSettingsDesc: 'Editing your profile information, language preferences, and privacy settings.',
      contactSupport: 'Support Contact',
      contactSupportDesc: 'You can contact our support team for additional help.'
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

  const faqItems = [
    {
      question: t.howItWorks,
      answer: t.howItWorksAnswer
    },
    {
      question: t.howRecommendations,
      answer: t.howRecommendationsAnswer
    },
    {
      question: t.bookTypes,
      answer: t.bookTypesAnswer
    },
    {
      question: t.differentLanguages,
      answer: t.differentLanguagesAnswer
    }
  ]

  const helpCategories = [
    {
      icon: BookOpen,
      title: t.bookRecommendations,
      description: t.bookRecommendationsDesc
    },
    {
      icon: Search,
      title: t.searchAndFilter,
      description: t.searchAndFilterDesc
    },
    {
      icon: MessageCircle,
      title: t.chatAssistant,
      description: t.chatAssistantDesc
    },
    {
      icon: Settings,
      title: t.accountSettings,
      description: t.accountSettingsDesc
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
        maxWidth: '900px',
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
              <HelpCircle style={{ width: '40px', height: '40px', color: '#FBF9E4' }} />
            </div>
            <h2 style={{
              fontSize: '32px',
              fontWeight: 'bold',
              color: '#122C4F',
              margin: '0 0 12px'
            }}>
              Yardım Merkezi
            </h2>
            <p style={{
              fontSize: '18px',
              color: '#122C4F',
              opacity: 0.8,
              margin: 0,
              lineHeight: '1.6'
            }}>
              {t.helpDescription}
            </p>
          </div>

          {/* Help Categories */}
          <div style={{ marginBottom: '40px' }}>
            <h3 style={{
              fontSize: '24px',
              fontWeight: 'bold',
              color: '#122C4F',
              margin: '0 0 24px',
              textAlign: 'center'
            }}>
              {t.helpCategories}
            </h3>
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
              gap: '20px'
            }}>
              {helpCategories.map((category, index) => (
                <motion.div
                  key={category.title}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1, duration: 0.5 }}
                  style={{
                    backgroundColor: 'rgba(18, 44, 79, 0.05)',
                    padding: '24px',
                    borderRadius: '16px',
                    border: '1px solid rgba(18, 44, 79, 0.1)',
                    textAlign: 'center',
                    transition: 'all 0.3s ease'
                  }}
                  onMouseOver={(e) => {
                    e.currentTarget.style.backgroundColor = 'rgba(18, 44, 79, 0.1)'
                    e.currentTarget.style.transform = 'translateY(-2px)'
                  }}
                  onMouseOut={(e) => {
                    e.currentTarget.style.backgroundColor = 'rgba(18, 44, 79, 0.05)'
                    e.currentTarget.style.transform = 'translateY(0)'
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
                    <category.icon style={{ width: '28px', height: '28px', color: '#FBF9E4' }} />
                  </div>
                  <h4 style={{
                    fontSize: '18px',
                    fontWeight: 'bold',
                    color: '#122C4F',
                    margin: '0 0 12px'
                  }}>
                    {category.title}
                  </h4>
                  <p style={{
                    fontSize: '14px',
                    color: '#122C4F',
                    opacity: 0.8,
                    lineHeight: '1.6',
                    margin: 0
                  }}>
                    {category.description}
                  </p>
                </motion.div>
              ))}
            </div>
          </div>

          {/* FAQ Section */}
          <div style={{
            backgroundColor: 'rgba(18, 44, 79, 0.05)',
            padding: '32px',
            borderRadius: '16px',
            border: '1px solid rgba(18, 44, 79, 0.1)'
          }}>
            <h3 style={{
              fontSize: '24px',
              fontWeight: 'bold',
              color: '#122C4F',
              margin: '0 0 24px',
              textAlign: 'center'
            }}>
              {t.frequentlyAskedQuestions}
            </h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
              {faqItems.map((item, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1, duration: 0.5 }}
                  style={{
                    backgroundColor: '#FBF9E4',
                    padding: '20px',
                    borderRadius: '12px',
                    border: '1px solid rgba(18, 44, 79, 0.1)'
                  }}
                >
                  <h4 style={{
                    fontSize: '16px',
                    fontWeight: 'bold',
                    color: '#122C4F',
                    margin: '0 0 8px'
                  }}>
                    {item.question}
                  </h4>
                  <p style={{
                    fontSize: '14px',
                    color: '#122C4F',
                    opacity: 0.8,
                    lineHeight: '1.6',
                    margin: 0
                  }}>
                    {item.answer}
                  </p>
                </motion.div>
              ))}
            </div>
          </div>

          {/* Quick Tips */}
          <div style={{
            marginTop: '32px',
            padding: '24px',
            backgroundColor: 'rgba(18, 44, 79, 0.05)',
            borderRadius: '16px',
            border: '1px solid rgba(18, 44, 79, 0.1)'
          }}>
            <h3 style={{
              fontSize: '20px',
              fontWeight: 'bold',
              color: '#122C4F',
              margin: '0 0 16px'
            }}>
              Hızlı İpuçları
            </h3>
            <ul style={{
              listStyle: 'none',
              padding: 0,
              margin: 0
            }}>
              {[
                'Kitap önerilerini daha doğru almak için okuma geçmişinizi güncel tutun.',
                'Arama yaparken yazar adı, kitap adı veya tür kullanabilirsiniz.',
                'Dil tercihlerinizi ayarlar bölümünden değiştirebilirsiniz.',
                'Sohbet asistanı ile doğal dil kullanarak sorularınızı sorabilirsiniz.'
              ].map((tip, index) => (
                <motion.li
                  key={index}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1, duration: 0.5 }}
                  style={{
                    display: 'flex',
                    alignItems: 'flex-start',
                    gap: '12px',
                    marginBottom: '12px',
                    fontSize: '14px',
                    color: '#122C4F',
                    lineHeight: '1.6'
                  }}
                >
                  <div style={{
                    width: '6px',
                    height: '6px',
                    backgroundColor: '#122C4F',
                    borderRadius: '50%',
                    marginTop: '8px',
                    flexShrink: 0
                  }} />
                  {tip}
                </motion.li>
              ))}
            </ul>
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default HelpPage
