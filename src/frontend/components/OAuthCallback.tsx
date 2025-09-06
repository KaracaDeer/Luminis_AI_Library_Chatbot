import React, { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useAuthStore } from '../stores/authStore';
import { useLanguageStore } from '../stores/languageStore';

const OAuthCallback: React.FC = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { language } = useLanguageStore();
  const { handleOAuthCallback, error, setError } = useAuthStore();
  
  const [isProcessing, setIsProcessing] = useState(true);
  const [status, setStatus] = useState<'processing' | 'success' | 'error'>('processing');

  const isTurkish = language === 'tr';

  useEffect(() => {
    const processOAuthCallback = async () => {
      try {
        // Get provider and code from URL parameters
        const provider = searchParams.get('provider') || 'google';
        const code = searchParams.get('code');
        const error = searchParams.get('error');
        const state = searchParams.get('state');

        if (error) {
          setError(error);
          setStatus('error');
          setIsProcessing(false);
          return;
        }

        if (!code) {
          setError(isTurkish ? 'Yetkilendirme kodu bulunamadı' : 'Authorization code not found');
          setStatus('error');
          setIsProcessing(false);
          return;
        }

        // Handle OAuth callback
        const success = await handleOAuthCallback(provider, code);
        
        if (success) {
          setStatus('success');
          // Redirect to main page after successful authentication
          setTimeout(() => {
            navigate('/');
          }, 2000);
        } else {
          setStatus('error');
        }
      } catch (err) {
        console.error('OAuth callback error:', err);
        setError(isTurkish ? 'OAuth işlemi sırasında hata oluştu' : 'Error occurred during OAuth process');
        setStatus('error');
      } finally {
        setIsProcessing(false);
      }
    };

    processOAuthCallback();
  }, [searchParams, handleOAuthCallback, setError, navigate, isTurkish]);

  if (isProcessing) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="max-w-md w-full bg-white rounded-lg shadow-md p-8 text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <h2 className="text-xl font-semibold text-gray-800 mb-2">
            {isTurkish ? 'Kimlik Doğrulanıyor...' : 'Authenticating...'}
          </h2>
          <p className="text-gray-600">
            {isTurkish 
              ? 'Lütfen bekleyin, hesabınıza giriş yapılıyor...'
              : 'Please wait while we sign you in...'
            }
          </p>
        </div>
      </div>
    );
  }

  if (status === 'success') {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="max-w-md w-full bg-white rounded-lg shadow-md p-8 text-center">
          <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <h2 className="text-xl font-semibold text-gray-800 mb-2">
            {isTurkish ? 'Başarılı!' : 'Success!'}
          </h2>
          <p className="text-gray-600 mb-4">
            {isTurkish 
              ? 'Hesabınıza başarıyla giriş yapıldı. Ana sayfaya yönlendiriliyorsunuz...'
              : 'Successfully signed in to your account. Redirecting to home page...'
            }
          </p>
          <button
            onClick={() => navigate('/')}
            className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
          >
            {isTurkish ? 'Ana Sayfaya Git' : 'Go to Home'}
          </button>
        </div>
      </div>
    );
  }

  if (status === 'error') {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="max-w-md w-full bg-white rounded-lg shadow-md p-8 text-center">
          <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg className="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </div>
          <h2 className="text-xl font-semibold text-gray-800 mb-2">
            {isTurkish ? 'Hata!' : 'Error!'}
          </h2>
          <p className="text-gray-600 mb-4">
            {isTurkish 
              ? 'Kimlik doğrulama sırasında bir hata oluştu. Lütfen tekrar deneyin.'
              : 'An error occurred during authentication. Please try again.'
            }
          </p>
          <div className="space-y-2">
            <button
              onClick={() => navigate('/login')}
              className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 mr-2"
            >
              {isTurkish ? 'Giriş Sayfasına Git' : 'Go to Login'}
            </button>
            <button
              onClick={() => window.location.reload()}
              className="bg-gray-600 text-white px-4 py-2 rounded-md hover:bg-gray-700"
            >
              {isTurkish ? 'Tekrar Dene' : 'Try Again'}
            </button>
          </div>
        </div>
      </div>
    );
  }

  return null;
};

export default OAuthCallback;
