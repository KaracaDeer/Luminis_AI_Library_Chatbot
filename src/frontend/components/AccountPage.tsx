import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Sparkles, ArrowLeft, User, Settings, Edit, LogOut, Trash2, Lock, MessageCircle } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { useAuth, ChatHistory } from '../contexts/AuthContext'
import { useLanguageStore } from '../stores/languageStore'

// Extend Window interface for global route change handler
declare global {
  interface Window {
    handleRouteChange?: (to: string) => void
  }
}

const AccountPage: React.FC = () => {
  const navigate = useNavigate()
  const { user, isLoggedIn, logout, deleteAccount, chatHistory, deleteChat } = useAuth()
  const { language } = useLanguageStore()
  const [activeTab, setActiveTab] = useState<'profile' | 'chat-history' | 'settings'>('profile')
  const [isEditing, setIsEditing] = useState(false)
  const [isDeletingAccount, setIsDeletingAccount] = useState(false)
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false)
  const [showChangePassword, setShowChangePassword] = useState(false)
  const [isChangingPassword, setIsChangingPassword] = useState(false)
  const [passwordData, setPasswordData] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  })
  const [passwordError, setPasswordError] = useState('')
  const [showChatDetails, setShowChatDetails] = useState(false)
  const [selectedChat, setSelectedChat] = useState<ChatHistory | null>(null)

  // Translations
  const translations = {
    tr: {
      backToHome: '← Ana Sayfa',
      redirecting: 'Yönlendiriliyor...',
      redirectingToHome: 'Ana sayfaya yönlendiriliyorsunuz',
      myAccount: 'Hesabım',
      profile: 'Profil',
      chatHistory: 'Eski Sohbetler',
      settings: 'Ayarlar',
      editProfile: 'Profili Düzenle',
      saveChanges: 'Değişiklikleri Kaydet',
      cancel: 'İptal',
      logout: 'Çıkış Yap',
      deleteAccount: 'Hesabı Sil',
      changePassword: 'Şifre Değiştir',
      currentPassword: 'Mevcut Şifre',
      newPassword: 'Yeni Şifre',
      confirmPassword: 'Şifre Tekrar',
      savePassword: 'Şifreyi Kaydet',
      changingPassword: 'Şifre değiştiriliyor...',
      deleteChat: 'Sohbeti Sil',
      chatDate: 'Sohbet Tarihi',
      chatMessages: 'Sohbet Mesajları',
      noChats: 'Henüz sohbet geçmişi yok',
      deleteConfirm: 'Bu hesabı silmek istediğinizden emin misiniz?',
      deleteConfirmChat: 'Bu sohbeti silmek istediğinizden emin misiniz?',
      yes: 'Evet',
      no: 'Hayır',
      deleting: 'Siliniyor...',
      username: 'Kullanıcı Adı',
      email: 'E-posta',
      firstName: 'Ad',
      lastName: 'Soyad',
      accountDeleteError: 'Hesap silinirken bir hata oluştu.',
      passwordChangedSuccess: 'Şifreniz başarıyla değiştirildi!',
      passwordValidationError: 'Yeni şifre en az 6 karakter olmalıdır.',
      passwordMismatchError: 'Yeni şifreler eşleşmiyor.',
      currentPasswordError: 'Mevcut şifre hatalı.',
      passwordChangeError: 'Şifre değiştirilirken bir hata oluştu.'
    },
    en: {
      backToHome: '← Home',
      redirecting: 'Redirecting...',
      redirectingToHome: 'Redirecting to home page',
      myAccount: 'My Account',
      profile: 'Profile',
      chatHistory: 'Chat History',
      settings: 'Settings',
      editProfile: 'Edit Profile',
      saveChanges: 'Save Changes',
      cancel: 'Cancel',
      logout: 'Logout',
      deleteAccount: 'Delete Account',
      changePassword: 'Change Password',
      currentPassword: 'Current Password',
      newPassword: 'New Password',
      confirmPassword: 'Confirm Password',
      savePassword: 'Save Password',
      changingPassword: 'Changing password...',
      deleteChat: 'Delete Chat',
      chatDate: 'Chat Date',
      chatMessages: 'Chat Messages',
      noChats: 'No chat history yet',
      deleteConfirm: 'Are you sure you want to delete this account?',
      deleteConfirmChat: 'Are you sure you want to delete this chat?',
      yes: 'Yes',
      no: 'No',
      deleting: 'Deleting...',
      username: 'Username',
      email: 'Email',
      firstName: 'First Name',
      lastName: 'Last Name',
      accountDeleteError: 'An error occurred while deleting the account.',
      passwordChangedSuccess: 'Your password has been changed successfully!',
      passwordValidationError: 'New password must be at least 6 characters long.',
      passwordMismatchError: 'New passwords do not match.',
      currentPasswordError: 'Current password is incorrect.',
      passwordChangeError: 'An error occurred while changing the password.'
    }
  }

  const t = translations[language]

  // Ensure component re-renders when language changes
  useEffect(() => {
    // Force re-render when language changes
  }, [language])

  // Redirect if not logged in
  useEffect(() => {
    if (!isLoggedIn) {
      if (window.handleRouteChange) {
        window.handleRouteChange('/')
      } else {
        navigate('/')
      }
    }
  }, [isLoggedIn, navigate])

  // Show loading while checking auth status
  if (!isLoggedIn || !user) {
    return (
      <div style={{ 
        minHeight: '100vh', 
        backgroundColor: '#FBF9E4',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontFamily: '"Libertinus Sans", system-ui, sans-serif'
      }}>
        <div style={{
          textAlign: 'center',
          color: '#122C4F'
        }}>
          <div style={{
            width: '64px',
            height: '64px',
            backgroundColor: '#122C4F',
            borderRadius: '50%',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            margin: '0 auto 20px'
          }}>
            <User style={{ width: '32px', height: '32px', color: '#FBF9E4' }} />
          </div>
          <h2 style={{
            fontSize: '24px',
            fontWeight: 'bold',
            margin: '0 0 12px'
          }}>
            {t.redirecting}
          </h2>
          <p style={{
            fontSize: '16px',
            opacity: 0.7,
            margin: 0
          }}>
            {t.redirectingToHome}
          </p>
        </div>
      </div>
    )
  }



  const handleBackToHome = () => {
    if (window.handleRouteChange) {
      window.handleRouteChange('/')
    } else {
      navigate('/')
    }
  }

  const handleLogout = () => {
    // Logout first
    logout()
    // Then navigate to home page
    setTimeout(() => {
      if (window.handleRouteChange) {
        window.handleRouteChange('/')
      } else {
        navigate('/')
      }
    }, 50)
  }

  const handleDeleteAccount = async () => {
    setIsDeletingAccount(true)
    try {
      const result = await deleteAccount()
      if (result.success) {
        // Navigate to home page after successful account deletion
        setTimeout(() => {
          if (window.handleRouteChange) {
            window.handleRouteChange('/')
          } else {
            navigate('/')
          }
        }, 50)
      } else {
        alert(result.error || t.accountDeleteError)
      }
    } catch (err) {
      alert(t.accountDeleteError)
    } finally {
      setIsDeletingAccount(false)
      setShowDeleteConfirm(false)
    }
  }



  const handleChangePassword = async () => {
    setIsChangingPassword(true)
    setPasswordError('')

    // Validasyon
    if (passwordData.newPassword.length < 6) {
      setPasswordError(t.passwordValidationError)
      setIsChangingPassword(false)
      return
    }

    if (passwordData.newPassword !== passwordData.confirmPassword) {
      setPasswordError(t.passwordMismatchError)
      setIsChangingPassword(false)
      return
    }

    if (passwordData.currentPassword !== user.password) {
      setPasswordError(t.currentPasswordError)
      setIsChangingPassword(false)
      return
    }

    try {
      // Password change simulation
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      // For now, just show success message
      
      alert(t.passwordChangedSuccess)
      setShowChangePassword(false)
      setPasswordData({
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      })
    } catch (err) {
      setPasswordError(t.passwordChangeError)
    } finally {
      setIsChangingPassword(false)
    }
  }

  const handlePasswordInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setPasswordData(prev => ({
      ...prev,
      [name]: value
    }))
    setPasswordError('')
  }

  const handleViewChatDetails = (chat: ChatHistory) => {
    setSelectedChat(chat)
    setShowChatDetails(true)
  }

  const tabs = [
    { id: 'profile', label: t.profile, icon: User },
    { id: 'chat-history', label: t.chatHistory, icon: MessageCircle },
    { id: 'settings', label: t.settings, icon: Settings }
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
            Luminis.AI Kütüphane Asistanı
          </h1>
        </div>
        
        <div style={{ width: '120px' }}></div>
      </div>

      {/* Content */}
      <div style={{
        maxWidth: '1000px',
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
              <User style={{ width: '40px', height: '40px', color: '#FBF9E4' }} />
            </div>
            <h2 style={{
              fontSize: '32px',
              fontWeight: 'bold',
              color: '#122C4F',
              margin: '0 0 12px'
            }}>
              {t.myAccount}
            </h2>
                         <p style={{
               fontSize: '18px',
               color: '#122C4F',
               opacity: 0.8,
               margin: 0,
               lineHeight: '1.6'
             }}>
               Profil bilgilerinizi yönetin, sohbet geçmişinizi görüntüleyin ve hesap ayarlarınızı düzenleyin
             </p>
          </div>

          {/* Tabs */}
          <div style={{
            display: 'flex',
            gap: '8px',
            marginBottom: '32px',
            borderBottom: '2px solid rgba(18, 44, 79, 0.1)',
            paddingBottom: '16px'
          }}>
            {tabs.map((tab) => (
              <motion.button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  padding: '12px 20px',
                  backgroundColor: activeTab === tab.id ? '#122C4F' : 'transparent',
                  color: activeTab === tab.id ? '#FBF9E4' : '#122C4F',
                  border: 'none',
                  borderRadius: '12px',
                  fontSize: '14px',
                  fontWeight: '500',
                  transition: 'all 0.3s ease'
                }}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                <tab.icon style={{ width: '18px', height: '18px' }} />
                {tab.label}
              </motion.button>
            ))}
          </div>

          {/* Tab Content */}
          <div style={{ minHeight: '400px' }}>
            {/* Profile Tab */}
            {activeTab === 'profile' && (
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.5 }}
              >
                <div style={{
                  backgroundColor: 'rgba(18, 44, 79, 0.05)',
                  padding: '32px',
                  borderRadius: '16px',
                  border: '1px solid rgba(18, 44, 79, 0.1)'
                }}>
                  <div style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    marginBottom: '24px'
                  }}>
                    <h3 style={{
                      fontSize: '24px',
                      fontWeight: 'bold',
                      color: '#122C4F',
                      margin: 0
                    }}>
                      Profil Bilgileri
                    </h3>
                    <button
                      onClick={() => setIsEditing(!isEditing)}
                      style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '8px',
                        padding: '8px 16px',
                        backgroundColor: '#122C4F',
                        color: '#FBF9E4',
                        border: 'none',
                        borderRadius: '8px',
                        fontSize: '14px',
                        fontWeight: '500'
                      }}
                    >
                      <Edit style={{ width: '16px', height: '16px' }} />
                      {isEditing ? t.saveChanges : t.editProfile}
                    </button>
                  </div>

                  <div style={{ display: 'grid', gap: '20px' }}>
                    <div style={{ display: 'flex', gap: '20px' }}>
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
                           value={user.firstName}
                           disabled={!isEditing}
                          style={{
                            width: '100%',
                            padding: '12px 16px',
                            border: '1px solid rgba(18, 44, 79, 0.2)',
                            borderRadius: '12px',
                            fontSize: '16px',
                            backgroundColor: isEditing ? '#FBF9E4' : 'rgba(18, 44, 79, 0.05)',
                            color: '#122C4F',
                            outline: 'none',
                            transition: 'all 0.3s ease'
                          }}
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
                           value={user.lastName}
                           disabled={!isEditing}
                          style={{
                            width: '100%',
                            padding: '12px 16px',
                            border: '1px solid rgba(18, 44, 79, 0.2)',
                            borderRadius: '12px',
                            fontSize: '16px',
                            backgroundColor: isEditing ? '#FBF9E4' : 'rgba(18, 44, 79, 0.05)',
                            color: '#122C4F',
                            outline: 'none',
                            transition: 'all 0.3s ease'
                          }}
                        />
                      </div>
                    </div>

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
                                             <input
                         type="text"
                         value={user.username}
                         disabled={!isEditing}
                        style={{
                          width: '100%',
                          padding: '12px 16px',
                          border: '1px solid rgba(18, 44, 79, 0.2)',
                          borderRadius: '12px',
                          fontSize: '16px',
                          backgroundColor: isEditing ? '#FBF9E4' : 'rgba(18, 44, 79, 0.05)',
                          color: '#122C4F',
                          outline: 'none',
                          transition: 'all 0.3s ease'
                        }}
                      />
                    </div>

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
                                             <input
                         type="email"
                         value={user.email}
                         disabled={!isEditing}
                        style={{
                          width: '100%',
                          padding: '12px 16px',
                          border: '1px solid rgba(18, 44, 79, 0.2)',
                          borderRadius: '12px',
                          fontSize: '16px',
                          backgroundColor: isEditing ? '#FBF9E4' : 'rgba(18, 44, 79, 0.05)',
                          color: '#122C4F',
                          outline: 'none',
                          transition: 'all 0.3s ease'
                        }}
                      />
                    </div>

                    
                  </div>
                </div>
              </motion.div>
            )}

            {/* Chat History Tab */}
            {activeTab === 'chat-history' && (
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.5 }}
              >
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
                    margin: '0 0 24px'
                  }}>
                    {t.chatHistory} ({chatHistory.length})
                  </h3>

                  {chatHistory.length === 0 ? (
                    <div style={{
                      textAlign: 'center',
                      padding: '40px',
                      color: '#122C4F',
                      opacity: 0.7
                    }}>
                      <MessageCircle style={{ width: '48px', height: '48px', margin: '0 auto 16px', opacity: 0.5 }} />
                      <p>{t.noChats}</p>
                      <p>Chat sayfasında sohbet ettiğinizde burada görünecek.</p>
                    </div>
                  ) : (
                    <div style={{ display: 'grid', gap: '16px' }}>
                      {chatHistory.map((chat) => (
                        <motion.div
                          key={chat.id}
                          initial={{ opacity: 0, y: 20 }}
                          animate={{ opacity: 1, y: 0 }}
                          style={{
                            backgroundColor: '#FBF9E4',
                            padding: '20px',
                            borderRadius: '12px',
                            border: '1px solid rgba(18, 44, 79, 0.1)',
                            transition: 'all 0.3s ease'
                          }}
                          onClick={() => handleViewChatDetails(chat)}
                          onMouseOver={(e) => {
                            e.currentTarget.style.transform = 'translateY(-2px)'
                            e.currentTarget.style.boxShadow = '0 4px 12px rgba(18, 44, 79, 0.15)'
                          }}
                          onMouseOut={(e) => {
                            e.currentTarget.style.transform = 'translateY(0)'
                            e.currentTarget.style.boxShadow = 'none'
                          }}
                        >
                          <div style={{
                            display: 'flex',
                            justifyContent: 'space-between',
                            alignItems: 'flex-start',
                            marginBottom: '12px'
                          }}>
                            <div style={{ flex: 1 }}>
                              <h4 style={{
                                fontSize: '16px',
                                fontWeight: 'bold',
                                color: '#122C4F',
                                margin: '0 0 4px'
                              }}>
                                {chat.title}
                              </h4>
                              <p style={{
                                fontSize: '12px',
                                color: '#122C4F',
                                opacity: 0.7,
                                margin: '0 0 8px'
                              }}>
                                {new Date(chat.lastUpdated).toLocaleDateString('tr-TR', {
                                  day: 'numeric',
                                  month: 'long',
                                  year: 'numeric',
                                  hour: '2-digit',
                                  minute: '2-digit'
                                })}
                              </p>
                              <p style={{
                                fontSize: '14px',
                                color: '#122C4F',
                                opacity: 0.8,
                                margin: 0
                              }}>
                                {chat.messages.length} {t.chatMessages}
                              </p>
                            </div>
                            <button
                              onClick={(e) => {
                                e.stopPropagation()
                                deleteChat(chat.id)
                              }}
                              style={{
                                background: 'none',
                                border: 'none',
                                color: '#E53E3E',
                                padding: '8px',
                                borderRadius: '8px',
                                transition: 'all 0.3s ease'
                              }}
                              onMouseOver={(e) => {
                                e.currentTarget.style.backgroundColor = 'rgba(229, 62, 62, 0.1)'
                              }}
                              onMouseOut={(e) => {
                                e.currentTarget.style.backgroundColor = 'transparent'
                              }}
                            >
                              <Trash2 style={{ width: '18px', height: '18px' }} />
                            </button>
                          </div>
                        </motion.div>
                      ))}
                    </div>
                  )}
                </div>
              </motion.div>
            )}

            {/* Settings Tab */}
            {activeTab === 'settings' && (
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.5 }}
              >
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
                    margin: '0 0 24px'
                  }}>
                    Hesap Ayarları
                  </h3>

                  <div style={{ display: 'grid', gap: '20px' }}>
                    <div>
                      <h4 style={{
                        fontSize: '18px',
                        fontWeight: 'bold',
                        color: '#122C4F',
                        margin: '0 0 12px'
                      }}>
                        {t.changePassword}
                      </h4>
                                             <button
                         onClick={() => setShowChangePassword(true)}
                         style={{
                           padding: '12px 20px',
                           backgroundColor: '#122C4F',
                           color: '#FBF9E4',
                           border: 'none',
                           borderRadius: '8px',
                           fontSize: '14px',
                           fontWeight: '500'
                         }}
                       >
                         {t.changePassword}
                       </button>
                    </div>

                    <div>
                      <h4 style={{
                        fontSize: '18px',
                        fontWeight: 'bold',
                        color: '#122C4F',
                        margin: '0 0 12px'
                      }}>
                        Bildirim Ayarları
                      </h4>
                      <div style={{ display: 'grid', gap: '12px' }}>
                        <label style={{
                          display: 'flex',
                          alignItems: 'center',
                          gap: '12px',
                          pointerEvents: 'none'
                        }}>
                          <input type="checkbox" defaultChecked />
                          <span style={{ color: '#122C4F' }}>Yeni kitap önerileri</span>
                        </label>
                        <label style={{
                          display: 'flex',
                          alignItems: 'center',
                          gap: '12px',
                          pointerEvents: 'none'
                        }}>
                          <input type="checkbox" defaultChecked />
                          <span style={{ color: '#122C4F' }}>Okuma hatırlatıcıları</span>
                        </label>
                        <label style={{
                          display: 'flex',
                          alignItems: 'center',
                          gap: '12px',
                          pointerEvents: 'none'
                        }}>
                          <input type="checkbox" />
                          <span style={{ color: '#122C4F' }}>E-posta bildirimleri</span>
                        </label>
                      </div>
                    </div>

                    <div>
                      <h4 style={{
                        fontSize: '18px',
                        fontWeight: 'bold',
                        color: '#122C4F',
                        margin: '0 0 12px'
                      }}>
                        Hesap İşlemleri
                      </h4>
                      <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                                                 <button
                           onClick={handleLogout}
                           style={{
                             display: 'flex',
                             alignItems: 'center',
                             gap: '8px',
                             padding: '12px 16px',
                             backgroundColor: '#E53E3E',
                             color: '#FBF9E4',
                             border: 'none',
                             borderRadius: '8px',
                             fontSize: '14px',
                             fontWeight: '500',
                             width: 'fit-content'
                           }}
                         >
                           <LogOut style={{ width: '16px', height: '16px' }} />
                           {t.logout}
                         </button>
                        
                                                 <button
                           onClick={() => setShowDeleteConfirm(true)}
                           disabled={isDeletingAccount}
                           style={{
                             display: 'flex',
                             alignItems: 'center',
                             gap: '8px',
                             padding: '12px 16px',
                             backgroundColor: isDeletingAccount ? '#9CA3AF' : '#DC2626',
                             color: '#FBF9E4',
                             border: 'none',
                             borderRadius: '8px',
                             pointerEvents: isDeletingAccount ? 'none' : 'auto',
                             fontSize: '14px',
                             fontWeight: '500',
                             width: 'fit-content'
                           }}
                         >
                           <Trash2 style={{ width: '16px', height: '16px' }} />
                           {isDeletingAccount ? t.deleting : t.deleteAccount}
                         </button>
                      </div>
                    </div>
                  </div>
                </div>
              </motion.div>
            )}
          </div>
        </motion.div>
      </div>

      {/* Delete Account Confirmation Modal */}
      {showDeleteConfirm && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundColor: 'rgba(0, 0, 0, 0.5)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 1000
        }}>
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            style={{
              backgroundColor: '#FBF9E4',
              padding: '32px',
              borderRadius: '16px',
              maxWidth: '400px',
              width: '90%',
              textAlign: 'center',
              border: '2px solid rgba(18, 44, 79, 0.1)'
            }}
          >
            <div style={{
              width: '64px',
              height: '64px',
              backgroundColor: '#DC2626',
              borderRadius: '50%',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              margin: '0 auto 20px'
            }}>
              <Trash2 style={{ width: '32px', height: '32px', color: '#FBF9E4' }} />
            </div>
            
            <h3 style={{
              fontSize: '24px',
              fontWeight: 'bold',
              color: '#122C4F',
              margin: '0 0 16px'
            }}>
              {t.deleteAccount}
            </h3>
            
            <p style={{
              fontSize: '16px',
              color: '#122C4F',
              margin: '0 0 24px',
              lineHeight: '1.5'
            }}>
              {t.deleteConfirm}
            </p>
            
            <div style={{ display: 'flex', gap: '12px', justifyContent: 'center' }}>
                             <button
                 onClick={() => setShowDeleteConfirm(false)}
                 disabled={isDeletingAccount}
                 style={{
                   padding: '8px 16px',
                   backgroundColor: '#9CA3AF',
                   color: '#FBF9E4',
                   border: 'none',
                   borderRadius: '8px',
                   pointerEvents: isDeletingAccount ? 'none' : 'auto',
                   fontSize: '14px',
                   fontWeight: '500',
                   transition: 'all 0.3s ease'
                 }}
               >
                 {t.no}
               </button>
              
                             <button
                 onClick={handleDeleteAccount}
                 disabled={isDeletingAccount}
                 style={{
                   padding: '8px 16px',
                   backgroundColor: isDeletingAccount ? '#9CA3AF' : '#DC2626',
                   color: '#FBF9E4',
                   border: 'none',
                   borderRadius: '8px',
                   pointerEvents: isDeletingAccount ? 'none' : 'auto',
                   fontSize: '14px',
                   fontWeight: '500',
                   transition: 'all 0.3s ease'
                 }}
               >
                 {isDeletingAccount ? t.deleting : t.deleteAccount}
               </button>
            </div>
          </motion.div>
                 </div>
       )}

               {/* Chat Details Modal */}
        {showChatDetails && selectedChat && (
          <div style={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: 'rgba(0, 0, 0, 0.5)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 1000
          }}>
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              style={{
                backgroundColor: '#FBF9E4',
                padding: '32px',
                borderRadius: '16px',
                maxWidth: '800px',
                width: '90%',
                maxHeight: '80vh',
                overflow: 'hidden',
                display: 'flex',
                flexDirection: 'column',
                border: '2px solid rgba(18, 44, 79, 0.1)'
              }}
            >
              {/* Header */}
              <div style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                marginBottom: '24px',
                borderBottom: '2px solid rgba(18, 44, 79, 0.1)',
                paddingBottom: '16px'
              }}>
                <div>
                  <h3 style={{
                    fontSize: '24px',
                    fontWeight: 'bold',
                    color: '#122C4F',
                    margin: '0 0 4px'
                  }}>
                    {selectedChat.title}
                  </h3>
                  <p style={{
                    fontSize: '14px',
                    color: '#122C4F',
                    opacity: 0.7,
                    margin: 0
                  }}>
                    {new Date(selectedChat.lastUpdated).toLocaleDateString('tr-TR', {
                      day: 'numeric',
                      month: 'long',
                      year: 'numeric',
                      hour: '2-digit',
                      minute: '2-digit'
                    })}
                  </p>
                </div>
                <button
                  onClick={() => setShowChatDetails(false)}
                  style={{
                    background: 'none',
                    border: 'none',
                    color: '#122C4F',
                    padding: '8px',
                    borderRadius: '8px',
                    transition: 'all 0.3s ease'
                  }}
                  onMouseOver={(e) => {
                    e.currentTarget.style.backgroundColor = 'rgba(18, 44, 79, 0.1)'
                  }}
                  onMouseOut={(e) => {
                    e.currentTarget.style.backgroundColor = 'transparent'
                  }}
                >
                  <span style={{ fontSize: '24px' }}>×</span>
                </button>
              </div>

              {/* Chat Messages */}
              <div style={{
                flex: 1,
                overflowY: 'auto',
                paddingRight: '8px'
              }}>
                <div style={{ display: 'grid', gap: '16px' }}>
                  {selectedChat.messages.map((message, index) => (
                    <div key={index}>
                      {/* User Message */}
                      {message.message && (
                        <div style={{
                          backgroundColor: '#122C4F',
                          color: '#FBF9E4',
                          padding: '12px 16px',
                          borderRadius: '12px',
                          marginBottom: '8px',
                          marginLeft: '20%'
                        }}>
                          <p style={{ margin: 0, fontSize: '14px' }}>
                            {message.message}
                          </p>
                          <p style={{
                            margin: '8px 0 0 0',
                            fontSize: '12px',
                            opacity: 0.7
                          }}>
                            {new Date(message.timestamp).toLocaleTimeString('tr-TR', {
                              hour: '2-digit',
                              minute: '2-digit'
                            })}
                          </p>
                        </div>
                      )}
                      
                      {/* AI Response */}
                      {message.response && (
                        <div style={{
                          backgroundColor: 'rgba(18, 44, 79, 0.1)',
                          color: '#122C4F',
                          padding: '12px 16px',
                          borderRadius: '12px',
                          marginRight: '20%'
                        }}>
                          <p style={{ margin: 0, fontSize: '14px', lineHeight: '1.5' }}>
                            {message.response}
                          </p>
                          <p style={{
                            margin: '8px 0 0 0',
                            fontSize: '12px',
                            opacity: 0.7
                          }}>
                            {new Date(message.timestamp).toLocaleTimeString('tr-TR', {
                              hour: '2-digit',
                              minute: '2-digit'
                            })}
                          </p>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            </motion.div>
          </div>
        )}

        {/* Change Password Modal */}
        {showChangePassword && (
         <div style={{
           position: 'fixed',
           top: 0,
           left: 0,
           right: 0,
           bottom: 0,
           backgroundColor: 'rgba(0, 0, 0, 0.5)',
           display: 'flex',
           alignItems: 'center',
           justifyContent: 'center',
           zIndex: 1000
         }}>
           <motion.div
             initial={{ opacity: 0, scale: 0.9 }}
             animate={{ opacity: 1, scale: 1 }}
             style={{
               backgroundColor: '#FBF9E4',
               padding: '32px',
               borderRadius: '16px',
               maxWidth: '400px',
               width: '90%',
               textAlign: 'center',
               border: '2px solid rgba(18, 44, 79, 0.1)'
             }}
           >
             <div style={{
               width: '64px',
               height: '64px',
               backgroundColor: '#122C4F',
               borderRadius: '50%',
               display: 'flex',
               alignItems: 'center',
               justifyContent: 'center',
               margin: '0 auto 20px'
             }}>
               <Lock style={{ width: '32px', height: '32px', color: '#FBF9E4' }} />
             </div>
             
             <h3 style={{
               fontSize: '24px',
               fontWeight: 'bold',
               color: '#122C4F',
               margin: '0 0 16px'
             }}>
               {t.changePassword}
             </h3>
             
             <div style={{ display: 'grid', gap: '16px', marginBottom: '24px' }}>
               <div>
                 <label style={{
                   display: 'block',
                   fontSize: '14px',
                   fontWeight: '500',
                   color: '#122C4F',
                   marginBottom: '8px',
                   textAlign: 'left'
                 }}>
                   {t.currentPassword}
                 </label>
                 <input
                   type="password"
                   name="currentPassword"
                   value={passwordData.currentPassword}
                   onChange={handlePasswordInputChange}
                   style={{
                     width: '100%',
                     padding: '12px 16px',
                     border: '1px solid rgba(18, 44, 79, 0.2)',
                     borderRadius: '8px',
                     fontSize: '16px',
                     backgroundColor: '#FBF9E4',
                     color: '#122C4F',
                     outline: 'none'
                   }}
                   placeholder={`${t.currentPassword} girin`}
                 />
               </div>
               
               <div>
                 <label style={{
                   display: 'block',
                   fontSize: '14px',
                   fontWeight: '500',
                   color: '#122C4F',
                   marginBottom: '8px',
                   textAlign: 'left'
                 }}>
                   {t.newPassword}
                 </label>
                 <input
                   type="password"
                   name="newPassword"
                   value={passwordData.newPassword}
                   onChange={handlePasswordInputChange}
                   style={{
                     width: '100%',
                     padding: '12px 16px',
                     border: '1px solid rgba(18, 44, 79, 0.2)',
                     borderRadius: '8px',
                     fontSize: '16px',
                     backgroundColor: '#FBF9E4',
                     color: '#122C4F',
                     outline: 'none'
                   }}
                   placeholder={`${t.newPassword} girin`}
                 />
               </div>
               
               <div>
                 <label style={{
                   display: 'block',
                   fontSize: '14px',
                   fontWeight: '500',
                   color: '#122C4F',
                   marginBottom: '8px',
                   textAlign: 'left'
                 }}>
                   {t.confirmPassword}
                 </label>
                 <input
                   type="password"
                   name="confirmPassword"
                   value={passwordData.confirmPassword}
                   onChange={handlePasswordInputChange}
                   style={{
                     width: '100%',
                     padding: '12px 16px',
                     border: '1px solid rgba(18, 44, 79, 0.2)',
                     borderRadius: '8px',
                     fontSize: '16px',
                     backgroundColor: '#FBF9E4',
                     color: '#122C4F',
                     outline: 'none'
                   }}
                   placeholder={`${t.confirmPassword} girin`}
                 />
               </div>
             </div>

             {passwordError && (
               <div style={{
                 backgroundColor: 'rgba(229, 62, 62, 0.1)',
                 color: '#E53E3E',
                 padding: '12px',
                 borderRadius: '8px',
                 marginBottom: '16px',
                 fontSize: '14px'
               }}>
                 {passwordError}
               </div>
             )}
             
             <div style={{ display: 'flex', gap: '12px', justifyContent: 'center' }}>
                                <button
                   onClick={() => {
                     setShowChangePassword(false)
                     setPasswordData({
                       currentPassword: '',
                       newPassword: '',
                       confirmPassword: ''
                     })
                     setPasswordError('')
                   }}
                   disabled={isChangingPassword}
                   style={{
                     padding: '12px 20px',
                     backgroundColor: '#9CA3AF',
                     color: '#FBF9E4',
                     border: 'none',
                     borderRadius: '8px',
                     pointerEvents: isChangingPassword ? 'none' : 'auto',
                     fontSize: '14px',
                     fontWeight: '500'
                   }}
                 >
                   {t.cancel}
                 </button>
               
               <button
                 onClick={handleChangePassword}
                 disabled={isChangingPassword}
                 style={{
                   padding: '12px 20px',
                   backgroundColor: isChangingPassword ? '#9CA3AF' : '#122C4F',
                   color: '#FBF9E4',
                   border: 'none',
                   borderRadius: '8px',
                   pointerEvents: isChangingPassword ? 'none' : 'auto',
                   fontSize: '14px',
                   fontWeight: '500'
                 }}
               >
                 {isChangingPassword ? t.changingPassword : t.savePassword}
               </button>
             </div>
           </motion.div>
         </div>
       )}
     </div>
   )
 }

export default AccountPage
