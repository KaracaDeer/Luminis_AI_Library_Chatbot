import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface User {
  id: number;
  username: string;
  email: string;
  profile_photo?: string;
  is_active: boolean;
  is_verified: boolean;
  auth_provider?: string;
  created_at?: string;
  last_login?: string;
}

interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

interface AuthState {
  user: User | null;
  tokens: AuthTokens | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

interface AuthActions {
  // Authentication actions
  login: (email: string, password: string) => Promise<boolean>;
  register: (username: string, email: string, password: string) => Promise<boolean>;
  logout: () => void;
  refreshToken: () => Promise<boolean>;
  
  // OAuth actions
  loginWithOAuth: (provider: string) => Promise<void>;
  handleOAuthCallback: (provider: string, code: string) => Promise<boolean>;
  
  // Profile actions
  getProfile: () => Promise<void>;
  updateProfile: (updates: Partial<User>) => Promise<boolean>;
  
  // Utility actions
  setUser: (user: User) => void;
  setTokens: (tokens: AuthTokens) => void;
  clearAuth: () => void;
  setError: (error: string | null) => void;
  setLoading: (loading: boolean) => void;
}

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const useAuthStore = create<AuthState & AuthActions>()(
  persist(
    (set, get) => ({
      // Initial state
      user: null,
      tokens: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,

      // Authentication actions
      login: async (email: string, password: string) => {
        try {
          set({ isLoading: true, error: null });
          
          const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password }),
          });

          if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Login failed');
          }

          const data = await response.json();
          
          if (data.success) {
            set({
              user: data.user,
              tokens: {
                access_token: data.access_token,
                refresh_token: data.refresh_token,
                token_type: data.token_type,
              },
              isAuthenticated: true,
              error: null,
            });
            return true;
          } else {
            throw new Error(data.message || 'Login failed');
          }
        } catch (error) {
          const errorMessage = error instanceof Error ? error.message : 'Login failed';
          set({ error: errorMessage });
          return false;
        } finally {
          set({ isLoading: false });
        }
      },

      register: async (username: string, email: string, password: string) => {
        try {
          set({ isLoading: true, error: null });
          
          const response = await fetch(`${API_BASE_URL}/api/auth/register`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, email, password }),
          });

          if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Registration failed');
          }

          const data = await response.json();
          
          if (data.success) {
            set({
              user: data.user,
              tokens: {
                access_token: data.access_token,
                refresh_token: data.refresh_token,
                token_type: data.token_type,
              },
              isAuthenticated: true,
              error: null,
            });
            return true;
          } else {
            throw new Error(data.message || 'Registration failed');
          }
        } catch (error) {
          const errorMessage = error instanceof Error ? error.message : 'Registration failed';
          set({ error: errorMessage });
          return false;
        } finally {
          set({ isLoading: false });
        }
      },

      logout: () => {
        // Call logout endpoint
        const { tokens } = get();
        if (tokens?.access_token) {
          fetch(`${API_BASE_URL}/api/auth/logout`, {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${tokens.access_token}`,
            },
          }).catch(console.error);
        }
        
        // Clear local state
        set({
          user: null,
          tokens: null,
          isAuthenticated: false,
          error: null,
        });
      },

      refreshToken: async () => {
        try {
          const { tokens } = get();
          if (!tokens?.refresh_token) {
            return false;
          }

          const response = await fetch(`${API_BASE_URL}/api/auth/refresh`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ refresh_token: tokens.refresh_token }),
          });

          if (!response.ok) {
            throw new Error('Token refresh failed');
          }

          const data = await response.json();
          
          if (data.success) {
            set({
              tokens: {
                ...tokens,
                access_token: data.access_token,
              },
            });
            return true;
          }
          
          return false;
        } catch (error) {
          console.error('Token refresh failed:', error);
          get().logout();
          return false;
        }
      },

      // OAuth actions
      loginWithOAuth: async (provider: string) => {
        try {
          set({ isLoading: true, error: null });
          
          const response = await fetch(`${API_BASE_URL}/api/auth/oauth/${provider}/url`);
          
          if (!response.ok) {
            throw new Error('Failed to get OAuth URL');
          }

          const data = await response.json();
          
          if (data.success) {
            // Redirect to OAuth provider
            window.location.href = data.oauth_url;
          } else {
            throw new Error('Failed to get OAuth URL');
          }
        } catch (error) {
          const errorMessage = error instanceof Error ? error.message : 'OAuth login failed';
          set({ error: errorMessage });
        } finally {
          set({ isLoading: false });
        }
      },

      handleOAuthCallback: async (provider: string, code: string) => {
        try {
          set({ isLoading: true, error: null });
          
          const response = await fetch(`${API_BASE_URL}/api/auth/oauth/${provider}/callback`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ code }),
          });

          if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'OAuth callback failed');
          }

          const data = await response.json();
          
          if (data.success) {
            set({
              user: data.user,
              tokens: {
                access_token: data.access_token,
                refresh_token: data.refresh_token,
                token_type: data.token_type,
              },
              isAuthenticated: true,
              error: null,
            });
            return true;
          } else {
            throw new Error(data.message || 'OAuth callback failed');
          }
        } catch (error) {
          const errorMessage = error instanceof Error ? error.message : 'OAuth callback failed';
          set({ error: errorMessage });
          return false;
        } finally {
          set({ isLoading: false });
        }
      },

      // Profile actions
      getProfile: async () => {
        try {
          const { tokens } = get();
          if (!tokens?.access_token) {
            return;
          }

          const response = await fetch(`${API_BASE_URL}/api/auth/profile`, {
            headers: {
              'Authorization': `Bearer ${tokens.access_token}`,
            },
          });

          if (!response.ok) {
            if (response.status === 401) {
              // Token expired, try to refresh
              const refreshed = await get().refreshToken();
              if (refreshed) {
                // Retry with new token
                get().getProfile();
              }
            }
            return;
          }

          const data = await response.json();
          
          if (data.success) {
            set({ user: data.user });
          }
        } catch (error) {
          console.error('Failed to get profile:', error);
        }
      },

      updateProfile: async (updates: Partial<User>) => {
        try {
          const { tokens } = get();
          if (!tokens?.access_token) {
            return false;
          }

          const response = await fetch(`${API_BASE_URL}/api/auth/profile`, {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${tokens.access_token}`,
            },
            body: JSON.stringify(updates),
          });

          if (!response.ok) {
            throw new Error('Profile update failed');
          }

          const data = await response.json();
          
          if (data.success) {
            set({ user: data.user });
            return true;
          }
          
          return false;
        } catch (error) {
          const errorMessage = error instanceof Error ? error.message : 'Profile update failed';
          set({ error: errorMessage });
          return false;
        }
      },

      // Utility actions
      setUser: (user: User) => set({ user, isAuthenticated: !!user }),
      setTokens: (tokens: AuthTokens) => set({ tokens, isAuthenticated: !!tokens }),
      clearAuth: () => set({
        user: null,
        tokens: null,
        isAuthenticated: false,
        error: null,
      }),
      setError: (error: string | null) => set({ error }),
      setLoading: (loading: boolean) => set({ isLoading: loading }),
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        user: state.user,
        tokens: state.tokens,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);

// Auto-refresh token when it's about to expire
export const setupTokenRefresh = () => {
  const checkAndRefreshToken = async () => {
    const { tokens, refreshToken } = useAuthStore.getState();
    
    if (tokens?.access_token) {
      try {
        // Decode JWT to check expiration
        const payload = JSON.parse(atob(tokens.access_token.split('.')[1]));
        const exp = payload.exp * 1000; // Convert to milliseconds
        const now = Date.now();
        
        // If token expires in less than 5 minutes, refresh it
        if (exp - now < 5 * 60 * 1000) {
          await refreshToken();
        }
      } catch (error) {
        console.error('Failed to check token expiration:', error);
      }
    }
  };

  // Check every minute
  setInterval(checkAndRefreshToken, 60 * 1000);
  
  // Also check when the app becomes visible
  document.addEventListener('visibilitychange', () => {
    if (!document.hidden) {
      checkAndRefreshToken();
    }
  });
};
