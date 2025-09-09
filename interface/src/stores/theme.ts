import { defineStore } from 'pinia'

interface ThemeState {
  currentTheme: 'light' | 'dark'
}

export const useThemeStore = defineStore('theme', {
  state: (): ThemeState => ({
    currentTheme: 'light'
  }),
  
  getters: {
    isDark: (state) => state.currentTheme === 'dark'
  },
  
  actions: {
    initializeTheme() {
      const savedTheme = localStorage.getItem('theme') as 'light' | 'dark' | null
      if (savedTheme) {
        this.currentTheme = savedTheme
      } else {
        this.currentTheme = 'light'
      }
      this.applyTheme()
    },
    
    toggleTheme() {
      this.currentTheme = this.currentTheme === 'light' ? 'dark' : 'light'
      localStorage.setItem('theme', this.currentTheme)
      this.applyTheme()
    },
    
    setTheme(theme: 'light' | 'dark') {
      this.currentTheme = theme
      localStorage.setItem('theme', theme)
      this.applyTheme()
    },
    
    applyTheme() {
      document.documentElement.setAttribute('data-theme', this.currentTheme)
    }
  }
})