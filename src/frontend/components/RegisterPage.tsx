import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Sparkles, ArrowLeft, User, Mail, Lock, Eye, EyeOff } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { useLanguageStore } from '../stores/languageStore'

// Extend Window interface for global route change handler
declare global {
  interface Window {
    handleRouteChange?: (to: string) => void
  }
}

const RegisterPage: React.FC = () => {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    username: '',
    email: '',
    password: '',
    confirmPassword: ''
  })
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()
  const { register } = useAuth()
  const { language } = useLanguageStore()

  // Translations
  const translations = {
    tr: {
      backToHome: '← Ana Sayfa',
      register: 'Kayıt Ol',
      firstName: 'Ad',
      lastName: 'Soyad',
      username: 'Kullanıcı Adı',
      email: 'E-posta',
      password: 'Şifre',
      confirmPassword: 'Şifre Tekrar',
      registerButton: 'Kayıt Ol',
      registering: 'Kayıt yapılıyor...',
      haveAccount: 'Zaten hesabınız var mı?',
      login: 'Giriş Yap',
      registerError: 'Kayıt işlemi başarısız oldu. Lütfen tekrar deneyin.',
      generalError: 'Kayıt olurken bir hata oluştu.',
      showPassword: 'Şifreyi göster',
      hidePassword: 'Şifreyi gizle',
      showConfirmPassword: 'Şifre tekrarını göster',
      hideConfirmPassword: 'Şifre tekrarını gizle'
    },
    en: {
      backToHome: '← Home',
      register: 'Register',
      firstName: 'First Name',
      lastName: 'Last Name',
      username: 'Username',
      email: 'Email',
      password: 'Password',
      confirmPassword: 'Confirm Password',
      registerButton: 'Register',
      registering: 'Registering...',
      haveAccount: 'Already have an account?',
      login: 'Login',
      registerError: 'Registration failed. Please try again.',
      generalError: 'An error occurred while registering.',
      showPassword: 'Show password',
      hidePassword: 'Hide password',
      showConfirmPassword: 'Show confirm password',
      hideConfirmPassword: 'Hide confirm password'
    }
  }

  const t = translations[language]

  // Ensure component re-renders when language changes
  useEffect(() => {
    // Force re-render when language changes
  }, [language])

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setError('')

    try {
      const result = await register({
        firstName: formData.firstName,
        lastName: formData.lastName,
        username: formData.username,
        email: formData.email,
        password: formData.password
      })
      
      if (result.success) {
        // Navigate to account page after successful registration
        if (window.handleRouteChange) {
          window.handleRouteChange('/account')
        } else {
          navigate('/account')
        }
      } else {
        setError(result.error || t.registerError)
      }
    } catch (err) {
      setError(t.generalError)
    } finally {
      setIsLoading(false)
    }
  }

  const handleBackToHome = () => {
    if (window.handleRouteChange) {
      window.handleRouteChange('/')
    } else {
      navigate('/')
    }
  }

  const isFormValid = () => {
    return (
      formData.firstName.trim() &&
      formData.lastName.trim() &&
      formData.username.trim() &&
      formData.email.trim() &&
      formData.password.length >= 6 &&
      formData.password === formData.confirmPassword
    )
  }

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
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginLeft: '80px' }}>
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
             Luminis.AI Kütüphane Asistanı
           </h1>
         </div>
        
        <div style={{ width: '120px' }}></div> {/* Spacer for centering */}
      </div>

      {/* Registration Form */}
      <div style={{
        maxWidth: '500px',
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
            marginBottom: '32px'
          }}>
            <div style={{
              width: '64px',
              height: '64px',
              backgroundColor: '#122C4F',
              borderRadius: '50%',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              margin: '0 auto 16px'
            }}>
              <User style={{ width: '32px', height: '32px', color: '#FBF9E4' }} />
            </div>
            <h2 style={{
              fontSize: '28px',
              fontWeight: 'bold',
              color: '#122C4F',
              margin: '0 0 8px'
            }}>
              {t.register}
            </h2>
            <p style={{
              fontSize: '16px',
              color: '#122C4F',
              opacity: 0.7,
              margin: 0
            }}>
              Luminis.AI Kütüphane Asistanı'na hoş geldiniz
            </p>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
            {/* Error Message */}
            {error && (
              <div style={{
                padding: '12px 16px',
                backgroundColor: '#FEE2E2',
                border: '1px solid #FCA5A5',
                borderRadius: '8px',
                color: '#DC2626',
                fontSize: '14px',
                textAlign: 'center'
              }}>
                {error}
              </div>
            )}
            {/* Name Fields */}
            <div style={{ display: 'flex', gap: '16px' }}>
              <div style={{ flex: 1 }}>
                <label style={{
                  display: 'block',
                  fontSize: '14px',
                  fontWeight: '500',
                  color: '#122C4F',
                  marginBottom: '8px'
                }}>
                  {t.firstName}
                </label>
                                 <input
                   type="text"
                   name="firstName"
                   value={formData.firstName}
                   onChange={handleInputChange}
                   style={{
                     width: '100%',
                     padding: '12px 16px',
                     border: '1px solid rgba(18, 44, 79, 0.2)',
                     borderRadius: '12px',
                     fontSize: '16px',
                     backgroundColor: '#FBF9E4',
                     color: '#122C4F',
                     outline: 'none',
                     transition: 'all 0.3s ease'
                   }}
                  onFocus={(e) => {
                    e.target.style.borderColor = '#122C4F'
                    e.target.style.boxShadow = '0 0 0 3px rgba(18, 44, 79, 0.1)'
                  }}
                  onBlur={(e) => {
                    e.target.style.borderColor = 'rgba(18, 44, 79, 0.2)'
                    e.target.style.boxShadow = 'none'
                  }}
                  placeholder="Adınız"
                  required
                />
              </div>
              <div style={{ flex: 1 }}>
                <label style={{
                  display: 'block',
                  fontSize: '14px',
                  fontWeight: '500',
                  color: '#122C4F',
                  marginBottom: '8px'
                }}>
                  {t.lastName}
                </label>
                                 <input
                   type="text"
                   name="lastName"
                   value={formData.lastName}
                   onChange={handleInputChange}
                   style={{
                     width: '100%',
                     padding: '12px 16px',
                     border: '1px solid rgba(18, 44, 79, 0.2)',
                     borderRadius: '12px',
                     fontSize: '16px',
                     backgroundColor: '#FBF9E4',
                     color: '#122C4F',
                     outline: 'none',
                     transition: 'all 0.3s ease'
                   }}
                  onFocus={(e) => {
                    e.target.style.borderColor = '#122C4F'
                    e.target.style.boxShadow = '0 0 0 3px rgba(18, 44, 79, 0.1)'
                  }}
                  onBlur={(e) => {
                    e.target.style.borderColor = 'rgba(18, 44, 79, 0.2)'
                    e.target.style.boxShadow = 'none'
                  }}
                  placeholder="Soyadınız"
                  required
                />
              </div>
            </div>

            {/* Username */}
            <div>
              <label style={{
                display: 'block',
                fontSize: '14px',
                fontWeight: '500',
                color: '#122C4F',
                marginBottom: '8px'
              }}>
                {t.username}
              </label>
              <div style={{ position: 'relative' }}>
                <User style={{
                  position: 'absolute',
                  left: '16px',
                  top: '50%',
                  transform: 'translateY(-50%)',
                  width: '20px',
                  height: '20px',
                  color: '#122C4F',
                  opacity: 0.6
                }} />
                <input
                  type="text"
                  name="username"
                  value={formData.username}
                  onChange={handleInputChange}
                  style={{
                    width: '100%',
                    padding: '12px 16px 12px 48px',
                    border: '1px solid rgba(18, 44, 79, 0.2)',
                    borderRadius: '12px',
                    fontSize: '16px',
                    backgroundColor: '#FBF9E4',
                    color: '#122C4F',
                    outline: 'none',
                    transition: 'all 0.3s ease'
                  }}
                  onFocus={(e) => {
                    e.target.style.borderColor = '#122C4F'
                    e.target.style.boxShadow = '0 0 0 3px rgba(18, 44, 79, 0.1)'
                  }}
                  onBlur={(e) => {
                    e.target.style.borderColor = 'rgba(18, 44, 79, 0.2)'
                    e.target.style.boxShadow = 'none'
                  }}
                  placeholder="Kullanıcı adınızı belirleyin"
                  required
                />
              </div>
            </div>

            {/* Email */}
            <div>
              <label style={{
                display: 'block',
                fontSize: '14px',
                fontWeight: '500',
                color: '#122C4F',
                marginBottom: '8px'
              }}>
                {t.email}
              </label>
              <div style={{ position: 'relative' }}>
                <Mail style={{
                  position: 'absolute',
                  left: '16px',
                  top: '50%',
                  transform: 'translateY(-50%)',
                  width: '20px',
                  height: '20px',
                  color: '#122C4F',
                  opacity: 0.5
                }} />
                                 <input
                   type="email"
                   name="email"
                   value={formData.email}
                   onChange={handleInputChange}
                   style={{
                     width: '100%',
                     padding: '12px 16px 12px 48px',
                     border: '1px solid rgba(18, 44, 79, 0.2)',
                     borderRadius: '12px',
                     fontSize: '16px',
                     backgroundColor: '#FBF9E4',
                     color: '#122C4F',
                     outline: 'none',
                     transition: 'all 0.3s ease'
                   }}
                  onFocus={(e) => {
                    e.target.style.borderColor = '#122C4F'
                    e.target.style.boxShadow = '0 0 0 3px rgba(18, 44, 79, 0.1)'
                  }}
                  onBlur={(e) => {
                    e.target.style.borderColor = 'rgba(18, 44, 79, 0.2)'
                    e.target.style.boxShadow = 'none'
                  }}
                  placeholder="ornek@email.com"
                  required
                />
              </div>
            </div>

            {/* Password */}
            <div>
              <label style={{
                display: 'block',
                fontSize: '14px',
                fontWeight: '500',
                color: '#122C4F',
                marginBottom: '8px'
              }}>
                {t.password}
              </label>
              <div style={{ position: 'relative' }}>
                <Lock style={{
                  position: 'absolute',
                  left: '16px',
                  top: '50%',
                  transform: 'translateY(-50%)',
                  width: '20px',
                  height: '20px',
                  color: '#122C4F',
                  opacity: 0.5
                }} />
                                 <input
                   type={showPassword ? 'text' : 'password'}
                   name="password"
                   value={formData.password}
                   onChange={handleInputChange}
                   style={{
                     width: '100%',
                     padding: '12px 16px 12px 48px',
                     border: '1px solid rgba(18, 44, 79, 0.2)',
                     borderRadius: '12px',
                     fontSize: '16px',
                     backgroundColor: '#FBF9E4',
                     color: '#122C4F',
                     outline: 'none',
                     transition: 'all 0.3s ease'
                   }}
                  onFocus={(e) => {
                    e.target.style.borderColor = '#122C4F'
                    e.target.style.boxShadow = '0 0 0 3px rgba(18, 44, 79, 0.1)'
                  }}
                  onBlur={(e) => {
                    e.target.style.borderColor = 'rgba(18, 44, 79, 0.2)'
                    e.target.style.boxShadow = 'none'
                  }}
                  placeholder="En az 6 karakter"
                  required
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  style={{
                    position: 'absolute',
                    right: '16px',
                    top: '50%',
                    transform: 'translateY(-50%)',
                    background: 'none',
                    border: 'none',
                    color: '#122C4F',
                    opacity: 0.5
                  }}
                >
                  {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                </button>
              </div>
            </div>

            {/* Confirm Password */}
            <div>
              <label style={{
                display: 'block',
                fontSize: '14px',
                fontWeight: '500',
                color: '#122C4F',
                marginBottom: '8px'
              }}>
                {t.confirmPassword}
              </label>
              <div style={{ position: 'relative' }}>
                <Lock style={{
                  position: 'absolute',
                  left: '16px',
                  top: '50%',
                  transform: 'translateY(-50%)',
                  width: '20px',
                  height: '20px',
                  color: '#122C4F',
                  opacity: 0.5
                }} />
                                 <input
                   type={showConfirmPassword ? 'text' : 'password'}
                   name="confirmPassword"
                   value={formData.confirmPassword}
                   onChange={handleInputChange}
                   style={{
                     width: '100%',
                     padding: '12px 16px 12px 48px',
                     border: '1px solid rgba(18, 44, 79, 0.2)',
                     borderRadius: '12px',
                     fontSize: '16px',
                     backgroundColor: '#FBF9E4',
                     color: '#122C4F',
                     outline: 'none',
                     transition: 'all 0.3s ease'
                   }}
                  onFocus={(e) => {
                    e.target.style.borderColor = '#122C4F'
                    e.target.style.boxShadow = '0 0 0 3px rgba(18, 44, 79, 0.1)'
                  }}
                  onBlur={(e) => {
                    e.target.style.borderColor = 'rgba(18, 44, 79, 0.2)'
                    e.target.style.boxShadow = 'none'
                  }}
                  placeholder="Şifrenizi tekrar girin"
                  required
                />
                <button
                  type="button"
                  onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                  style={{
                    position: 'absolute',
                    right: '16px',
                    top: '50%',
                    transform: 'translateY(-50%)',
                    background: 'none',
                    border: 'none',
                    color: '#122C4F',
                    opacity: 0.5
                  }}
                >
                  {showConfirmPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                </button>
              </div>
            </div>

            {/* Submit Button */}
            <motion.button
              type="submit"
              disabled={!isFormValid() || isLoading}
              style={{
                width: '100%',
                padding: '16px',
                backgroundColor: isFormValid() && !isLoading ? '#122C4F' : '#E5E7EB',
                color: isFormValid() && !isLoading ? '#FBF9E4' : '#9CA3AF',
                border: 'none',
                borderRadius: '12px',
                fontSize: '16px',
                fontWeight: '600',
                pointerEvents: isFormValid() && !isLoading ? 'auto' : 'none',
                transition: 'all 0.3s ease',
                marginTop: '8px'
              }}
              whileHover={isFormValid() && !isLoading ? { scale: 1.02 } : {}}
              whileTap={isFormValid() && !isLoading ? { scale: 0.98 } : {}}
            >
              {isLoading ? t.registering : t.registerButton}
            </motion.button>
          </form>

          {/* Login Link */}
          <div style={{
            textAlign: 'center',
            marginTop: '24px',
            paddingTop: '24px',
            borderTop: '1px solid rgba(18, 44, 79, 0.1)'
          }}>
            <p style={{
              fontSize: '14px',
              color: '#122C4F',
              opacity: 0.7,
              margin: 0
            }}>
              {t.haveAccount}{' '}
              <button
                onClick={() => {
                  if (window.handleRouteChange) {
                    window.handleRouteChange('/login')
                  } else {
                    navigate('/login')
                  }
                }}
                style={{
                  background: 'none',
                  border: 'none',
                  color: '#122C4F',
                  fontSize: '14px',
                  fontWeight: '600',
                  textDecoration: 'underline',
                  // Replaced with hover effects
                  transition: 'all 0.3s ease'
                }}
                onMouseOver={(e) => {
                  e.currentTarget.style.color = '#1a3a5f'
                }}
                onMouseOut={(e) => {
                  e.currentTarget.style.color = '#122C4F'
                }}
              >
                {t.login}
              </button>
            </p>
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default RegisterPage
