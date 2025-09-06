import React, { useState } from 'react';
import { useAuthStore } from '../stores/authStore';
import { useLanguageStore } from '../stores/languageStore';

interface AuthModalProps {
  isOpen: boolean;
  onClose: () => void;
  mode: 'login' | 'register';
}

const AuthModal: React.FC<AuthModalProps> = ({ isOpen, onClose, mode }) => {
  const { language } = useLanguageStore();
  const { login, register, loginWithOAuth, isLoading, error, setError } = useAuthStore();
  
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
  });

  const isTurkish = language === 'tr';

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (mode === 'register') {
      if (formData.password !== formData.confirmPassword) {
        setError(isTurkish ? 'Şifreler eşleşmiyor' : 'Passwords do not match');
        return;
      }

      if (formData.password.length < 6) {
        setError(isTurkish ? 'Şifre en az 6 karakter olmalıdır' : 'Password must be at least 6 characters');
        return;
      }

      const success = await register(formData.username, formData.email, formData.password);
      if (success) {
        onClose();
        setFormData({ username: '', email: '', password: '', confirmPassword: '' });
      }
    } else {
      const success = await login(formData.email, formData.password);
      if (success) {
        onClose();
        setFormData({ username: '', email: '', password: '', confirmPassword: '' });
      }
    }
  };

  const handleOAuthLogin = (provider: string) => {
    loginWithOAuth(provider);
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-8 w-full max-w-md mx-4">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold text-gray-800">
            {mode === 'login' 
              ? (isTurkish ? 'Giriş Yap' : 'Login')
              : (isTurkish ? 'Kayıt Ol' : 'Register')
            }
          </h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 text-2xl"
          >
            ×
          </button>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          {mode === 'register' && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                {isTurkish ? 'Kullanıcı Adı' : 'Username'}
              </label>
              <input
                type="text"
                name="username"
                value={formData.username}
                onChange={handleInputChange}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder={isTurkish ? 'Kullanıcı adınızı girin' : 'Enter your username'}
              />
            </div>
          )}

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              {isTurkish ? 'E-posta' : 'Email'}
            </label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleInputChange}
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder={isTurkish ? 'E-posta adresinizi girin' : 'Enter your email'}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              {isTurkish ? 'Şifre' : 'Password'}
            </label>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleInputChange}
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder={isTurkish ? 'Şifrenizi girin' : 'Enter your password'}
            />
          </div>

          {mode === 'register' && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                {isTurkish ? 'Şifre Tekrar' : 'Confirm Password'}
              </label>
              <input
                type="password"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleInputChange}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder={isTurkish ? 'Şifrenizi tekrar girin' : 'Confirm your password'}
              />
            </div>
          )}

          <button
            type="submit"
            disabled={isLoading}
            className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50"
          >
            {isLoading 
              ? (isTurkish ? 'Yükleniyor...' : 'Loading...')
              : (mode === 'login' 
                  ? (isTurkish ? 'Giriş Yap' : 'Login')
                  : (isTurkish ? 'Kayıt Ol' : 'Register')
                )
            }
          </button>
        </form>

        <div className="mt-6">
          <div className="relative">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-gray-300" />
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-2 bg-white text-gray-500">
                {isTurkish ? 'veya' : 'or'}
              </span>
            </div>
          </div>

          <div className="mt-6 grid grid-cols-1 gap-3">
            <button
              onClick={() => handleOAuthLogin('google')}
              className="w-full inline-flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
            >
              <svg className="w-5 h-5" viewBox="0 0 24 24">
                <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
              </svg>
              <span className="ml-2">
                {isTurkish ? 'Google ile devam et' : 'Continue with Google'}
              </span>
            </button>

            <button
              onClick={() => handleOAuthLogin('github')}
              className="w-full inline-flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
            >
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 0C4.477 0 0 4.484 0 10.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0110 4.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.203 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.942.359.31.678.921.678 1.856 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0020 10.017C20 4.484 15.522 0 10 0z" clipRule="evenodd" />
              </svg>
              <span className="ml-2">
                {isTurkish ? 'GitHub ile devam et' : 'Continue with GitHub'}
              </span>
            </button>

            <button
              onClick={() => handleOAuthLogin('microsoft')}
              className="w-full inline-flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
            >
              <svg className="w-5 h-5" viewBox="0 0 23 23">
                <path fill="#f3f3f3" d="M0 0h23v23H0z"/>
                <path fill="#f35325" d="M1 1h10v10H1z"/>
                <path fill="#81bc06" d="M12 1h10v10H12z"/>
                <path fill="#05a6f0" d="M1 12h10v10H1z"/>
                <path fill="#ffc908" d="M12 12h10v10H12z"/>
              </svg>
              <span className="ml-2">
                {isTurkish ? 'Microsoft ile devam et' : 'Continue with Microsoft'}
              </span>
            </button>
          </div>
        </div>

        <div className="mt-6 text-center">
          <p className="text-sm text-gray-600">
            {mode === 'login' ? (
              <>
                {isTurkish ? 'Hesabınız yok mu?' : "Don't have an account?"}{' '}
                <button
                  onClick={() => window.location.reload()}
                  className="text-blue-600 hover:text-blue-500 font-medium"
                >
                  {isTurkish ? 'Kayıt olun' : 'Sign up'}
                </button>
              </>
            ) : (
              <>
                {isTurkish ? 'Zaten hesabınız var mı?' : 'Already have an account?'}{' '}
                <button
                  onClick={() => window.location.reload()}
                  className="text-blue-600 hover:text-blue-500 font-medium"
                >
                  {isTurkish ? 'Giriş yapın' : 'Sign in'}
                </button>
              </>
            )}
          </p>
        </div>
      </div>
    </div>
  );
};

export default AuthModal;
