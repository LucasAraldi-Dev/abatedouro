import { defineStore } from 'pinia'
import { authLogin, authRegister, authLogout, authMe } from '../services/api.ts'

interface AuthState {
  user: null | { username: string; is_active: boolean; created_at: string }
  loading: boolean
  error: string | null
  initializing: boolean
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    user: null,
    loading: false,
    error: null,
    initializing: false,
  }),
  getters: {
    isAuthenticated: (state) => !!state.user && state.user.is_active
  },
  actions: {
    clearError() {
      this.error = null
    },
    async initializeAuth() {
      // Evita múltiplas inicializações simultâneas
      if (this.initializing) {
        console.log('🔄 [AUTH STORE DEBUG] Inicialização já em andamento, aguardando...')
        return
      }
      
      // Se já tem usuário, não precisa inicializar novamente
      if (this.user) {
        console.log('🔄 [AUTH STORE DEBUG] Usuário já inicializado:', this.user.username)
        return
      }
      
      this.initializing = true
      console.log('🔄 [AUTH STORE DEBUG] Iniciando initializeAuth...')
      console.log('🔄 [AUTH STORE DEBUG] Estado atual do usuário:', this.user)
      
      try {
        console.log('🔄 [AUTH STORE DEBUG] Chamando authMe()...')
        const res = await authMe()
        console.log('🔄 [AUTH STORE DEBUG] Resposta do authMe:', res)
        
        if (res.ok && res.data?.username) {
          console.log('🔄 [AUTH STORE DEBUG] Usuário autenticado encontrado:', res.data)
          this.user = {
            username: res.data.username,
            is_active: !!res.data.is_active,
            created_at: res.data.created_at || new Date().toISOString()
          }
          console.log('🔄 [AUTH STORE DEBUG] Usuário definido no store:', this.user)
        } else {
          console.log('🔄 [AUTH STORE DEBUG] Nenhum usuário autenticado encontrado')
          this.user = null
        }
      } catch (error) {
        console.log('🔄 [AUTH STORE DEBUG] Erro no initializeAuth:', error)
        this.user = null
      } finally {
        this.initializing = false
      }
      
      console.log('🔄 [AUTH STORE DEBUG] initializeAuth finalizado. isAuthenticated:', this.isAuthenticated)
    },
    async login(payload: { username: string; password: string }) {
      console.log('🔑 [AUTH STORE DEBUG] Iniciando login para:', payload.username)
      
      this.loading = true
      this.error = null
      
      try {
        console.log('🔑 [AUTH STORE DEBUG] Chamando authLogin...')
        const res = await authLogin(payload)
        console.log('🔑 [AUTH STORE DEBUG] Resposta do authLogin:', res)
        
        if (!res.ok) {
          console.log('🔑 [AUTH STORE DEBUG] Login falhou. Status:', res.status)
          if (res.status === 403) this.error = 'Conta inativa'
          else if (res.status === 401) this.error = 'Credenciais inválidas'
          else this.error = 'Erro ao realizar login'
          console.log('🔑 [AUTH STORE DEBUG] Erro definido:', this.error)
          return { 
            success: false, 
            status: res.status, 
            data: res.data, 
            message: this.error 
          }
        }
        
        console.log('🔑 [AUTH STORE DEBUG] Login bem-sucedido! Buscando dados do usuário...')
        // Buscar o usuário autenticado
        const me = await authMe()
        console.log('🔑 [AUTH STORE DEBUG] Resposta do authMe após login:', me)
        
        if (me.ok && me.data?.username) {
          console.log('🔑 [AUTH STORE DEBUG] Dados do usuário obtidos:', me.data)
          this.user = {
            username: me.data.username,
            is_active: !!me.data.is_active,
            created_at: me.data.created_at || new Date().toISOString()
          }
          console.log('🔑 [AUTH STORE DEBUG] Usuário definido no store:', this.user)
        } else {
          console.log('🔑 [AUTH STORE DEBUG] Falha ao obter dados do usuário, usando dados do payload')
          this.user = { username: payload.username, is_active: false, created_at: new Date().toISOString() }
        }
        
        console.log('🔑 [AUTH STORE DEBUG] Login finalizado com sucesso. isAuthenticated:', this.isAuthenticated)
        return { success: true }
      } catch (e) {
        console.log('🔑 [AUTH STORE DEBUG] Erro durante login:', e)
        this.error = 'Erro de conexão'
        return { 
          success: false, 
          status: null, 
          data: null, 
          message: 'Erro de conexão' 
        }
      } finally {
        console.log('🔑 [AUTH STORE DEBUG] Finalizando login. Loading:', false)
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