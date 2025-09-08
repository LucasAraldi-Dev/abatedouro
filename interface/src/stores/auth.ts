import { defineStore } from 'pinia'
import { authLogin, authRegister, authLogout, authMe } from '../services/api'

interface AuthState {
  user: null | { username: string; is_active: boolean; created_at: string }
  loading: boolean
  error: string | null
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    user: null,
    loading: false,
    error: null,
  }),
  actions: {
    clearError() {
      this.error = null
    },
    async initializeAuth() {
      try {
        const res = await authMe()
        if (res.ok && res.data?.username) {
          this.user = {
            username: res.data.username,
            is_active: !!res.data.is_active,
            created_at: res.data.created_at || new Date().toISOString()
          }
        } else {
          this.user = null
        }
      } catch {
        this.user = null
      }
    },
    async login(payload: { username: string; password: string }) {
      this.loading = true
      this.error = null
      try {
        const res = await authLogin(payload)
        if (!res.ok) {
          if (res.status === 403) this.error = 'Conta inativa'
          else if (res.status === 401) this.error = 'Credenciais inválidas'
          else this.error = 'Erro ao realizar login'
          return { success: false }
        }
        // Buscar o usuário autenticado
        const me = await authMe()
        if (me.ok && me.data?.username) {
          this.user = {
            username: me.data.username,
            is_active: !!me.data.is_active,
            created_at: me.data.created_at || new Date().toISOString()
          }
        } else {
          this.user = { username: payload.username, is_active: false, created_at: new Date().toISOString() }
        }
        return { success: true }
      } catch (e) {
        this.error = 'Erro de conexão'
        return { success: false }
      } finally {
        this.loading = false
      }
    },
    async register(payload: { nome_completo: string; email: string; username: string; password: string; confirm_password: string }) {
      this.loading = true
      this.error = null
      try {
        const res = await authRegister(payload)
        if (!res.ok) {
          this.error = res.data?.detail || 'Erro ao registrar'
          return { success: false }
        }
        return { success: true }
      } catch (e) {
        this.error = 'Erro de conexão'
        return { success: false }
      } finally {
        this.loading = false
      }
    },
    async logout() {
      this.loading = true
      try {
        const res = await authLogout()
        if (!res.ok) {
          this.error = 'Falha ao sair'
          return { success: false }
        }
        this.user = null
        return { success: true }
      } catch (e) {
        this.error = 'Erro de conexão'
        return { success: false }
      } finally {
        this.loading = false
      }
    }
  }
})