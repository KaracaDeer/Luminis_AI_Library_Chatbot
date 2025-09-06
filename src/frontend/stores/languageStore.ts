import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface LanguageState {
  language: 'tr' | 'en'
  setLanguage: (language: 'tr' | 'en') => void
}

export const useLanguageStore = create<LanguageState>()(
  persist(
    (set) => ({
      language: 'tr',
      setLanguage: (language) => set({ language }),
    }),
    {
      name: 'luminis-language',
    }
  )
)
