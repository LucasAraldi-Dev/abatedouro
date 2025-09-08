<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from './stores/auth'
import { checkApiHealth } from './services/api'

const router = useRouter()
const auth = useAuthStore()

// Estados da aplicação
const currentTheme = ref(localStorage.getItem('theme') || 'light')
const isOnline = ref(true)

// Funções de tema
const toggleTheme = () => {
  currentTheme.value = currentTheme.value === 'light' ? 'dark' : 'light'
  localStorage.setItem('theme', currentTheme.value)
  document.documentElement.setAttribute('data-theme', currentTheme.value)
}

// Verificação da API
const checkApi = async () => {
  try {
    await checkApiHealth()
    isOnline.value = true
  } catch (error) {
    isOnline.value = false
    console.error('API offline:', error)
  }
}

// Navegação
const navigateTo = (route: string) => {
  router.push(route)
}

// Logout
const handleLogout = async () => {
  try {
    await auth.logout()
    router.push('/')
  } catch (error) {
    console.error('Erro no logout:', error)
  }
}

// Inicialização
onMounted(async () => {
  // Aplicar tema
  document.documentElement.setAttribute('data-theme', currentTheme.value)
  
  // Inicializar autenticação
  await auth.initializeAuth()
  
  // Verificar API
  await checkApi()
  
  // Verificar API a cada 30 segundos
  setInterval(checkApi, 30000)
})
</script>

<template>
  <div id="app" :data-theme="currentTheme">
    <!-- Header - apenas para páginas autenticadas -->
    <header v-if="auth.isAuthenticated" class="app-header">
      <div class="header-content">
        <div class="header-left">
          <div class="logo-container">
            <img src="./images/logo.png" alt="Logo Sistema de Abatedouro" class="app-logo" />
          </div>
          <div class="title-section">
            <h1 class="app-title">Sistema de Abatedouro</h1>
            <p class="app-subtitle">Gestão Completa de Produção</p>
          </div>
        </div>
        <div class="header-actions">
          <button @click="toggleTheme" class="theme-toggle" :title="currentTheme === 'light' ? 'Modo Escuro' : 'Modo Claro'">
            <span v-if="currentTheme === 'light'">🌙</span>
            <span v-else>☀️</span>
          </button>
          <span class="status-indicator" :class="{ 'online': isOnline, 'offline': !isOnline }">
            {{ isOnline ? 'Online' : 'Offline' }}
          </span>
          <div class="user-actions">
            <span class="user-label">{{ auth.user?.username }}</span>
            <button @click="handleLogout" class="logout-btn">Sair</button>
          </div>
        </div>
      </div>
    </header>
    
    <!-- Navigation - apenas para páginas autenticadas -->
    <nav v-if="auth.isAuthenticated" class="main-nav">
      <button 
        @click="navigateTo('/dashboard')" 
        :class="['nav-btn', { active: $route.path === '/dashboard' }]"
        :aria-label="'Ir para Dashboard'"
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="3" y="3" width="7" height="7"/>
          <rect x="14" y="3" width="7" height="7"/>
          <rect x="14" y="14" width="7" height="7"/>
          <rect x="3" y="14" width="7" height="7"/>
        </svg>
        Dashboard
      </button>
      <button 
        @click="navigateTo('/lotes')" 
        :class="['nav-btn', { active: $route.path === '/lotes' }]"
        :aria-label="'Ir para Abates'"
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/>
          <rect x="8" y="2" width="8" height="4" rx="1" ry="1"/>
        </svg>
        Abates
      </button>
      <button 
        @click="navigateTo('/produtos')" 
        :class="['nav-btn', { active: $route.path === '/produtos' }]"
        :aria-label="'Ir para Produtos'"
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>
        </svg>
        Produtos
      </button>
      <button 
        @click="navigateTo('/relatorios')" 
        :class="['nav-btn', { active: $route.path === '/relatorios' }]"
        :aria-label="'Ir para Relatórios'"
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
          <polyline points="14,2 14,8 20,8"/>
          <line x1="16" y1="13" x2="8" y2="13"/>
          <line x1="16" y1="17" x2="8" y2="17"/>
          <polyline points="10,9 9,9 8,9"/>
        </svg>
        Relatórios
      </button>
      <button 
        @click="navigateTo('/graficos')" 
        :class="['nav-btn', { active: $route.path === '/graficos' }]"
        :aria-label="'Ir para Gráficos'"
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="18" y1="20" x2="18" y2="10"/>
          <line x1="12" y1="20" x2="12" y2="4"/>
          <line x1="6" y1="20" x2="6" y2="14"/>
        </svg>
        Gráficos
      </button>
    </nav>
    
    <!-- Main Content -->
    <main class="main-content">
      <div class="content-wrapper">
        <router-view v-slot="{ Component }">
          <Transition name="fade" mode="out-in">
            <component :is="Component" />
          </Transition>
        </router-view>
      </div>
    </main>
  </div>
</template>

<style scoped>
@import url('./styles/colors.css');

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  width: 100vw;
  min-height: 100vh;
  background: var(--bg-primary);
  color: var(--text-primary);
  font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  display: flex;
  flex-direction: column;
}

.app-header {
  background: var(--bg-secondary);
  border-bottom: 3px solid var(--primary-red);
  box-shadow: 0 2px 8px rgba(220, 38, 38, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  max-width: 100%;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.logo-container {
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.3s ease;
}

.logo-container:hover {
  transform: scale(1.05);
}

.app-logo {
  width: 60px;
  height: 60px;
  object-fit: contain;
}

.title-section {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.app-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-primary);
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
}

.app-subtitle {
  font-size: 0.875rem;
  color: var(--text-secondary);
  font-weight: 500;
  margin: 0;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.theme-toggle {
  background: var(--bg-accent);
  border: 1px solid var(--border-accent);
  border-radius: 8px;
  padding: 0.5rem;
  cursor: pointer;
  font-size: 1.2rem;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
}

.theme-toggle:hover {
  background: var(--primary-red);
  color: white;
  transform: scale(1.05);
}

.status-indicator {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 600;
  transition: all 0.3s ease;
}

.status-indicator.online {
  background: rgba(16, 185, 129, 0.1);
  color: #10B981;
  border: 2px solid #10B981;
  box-shadow: 0 0 10px rgba(16, 185, 129, 0.3);
}

.status-indicator.offline {
  background: rgba(239, 68, 68, 0.1);
  color: #EF4444;
  border: 2px solid #EF4444;
  box-shadow: 0 0 10px rgba(239, 68, 68, 0.3);
}

.user-actions {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.user-label {
  color: var(--text-secondary);
  font-weight: 600;
}

.logout-btn {
  padding: 0.35rem 0.75rem;
  border-radius: 6px;
  border: 1px solid var(--border-accent);
  background: var(--bg-accent);
  cursor: pointer;
  color: var(--text-primary);
  font-weight: 500;
  transition: all 0.3s ease;
}

.logout-btn:hover {
  background: var(--primary-red);
  color: #fff;
  border-color: var(--primary-red);
}

.main-nav {
  background: var(--bg-secondary);
  border-bottom: 2px solid var(--primary-red);
  padding: 0 2rem;
  display: flex;
  gap: 0;
  box-shadow: 0 2px 4px rgba(220, 38, 38, 0.1);
}

.nav-btn {
  background: none;
  border: none;
  padding: 1.5rem 2rem;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-secondary);
  border-bottom: 3px solid transparent;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.nav-btn svg {
  transition: transform 0.3s ease;
}

.nav-btn:hover {
  color: var(--primary-red);
  background: var(--bg-accent);
  transform: translateY(-2px);
}

.nav-btn:hover svg {
  transform: scale(1.1);
}

.nav-btn.active {
  color: var(--primary-red);
  border-bottom-color: var(--primary-red);
  font-weight: 700;
  background: var(--bg-accent);
}

.main-content {
  flex: 1;
  background: var(--bg-primary);
  overflow-y: auto;
  position: relative;
}

.content-wrapper {
  padding: 0;
  width: 100%;
  margin: 0;
}

/* Transições entre views */
.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.fade-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

/* Responsividade */
@media (max-width: 1200px) {
  .content-wrapper {
    padding: 0;
  }
}

@media (max-width: 1024px) {
  .header-content {
    padding: 1rem 1.5rem;
  }
  
  .content-wrapper {
    padding: 0;
  }
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 1rem;
    padding: 1rem;
  }
  
  .header-left {
    justify-content: center;
  }
  
  .title-section {
    text-align: center;
  }
  
  .app-title {
    font-size: 1.5rem;
  }
  
  .app-subtitle {
    font-size: 0.8rem;
  }
  
  .main-nav {
    flex-wrap: wrap;
    justify-content: center;
    gap: 0.5rem;
    padding: 1rem;
  }
  
  .nav-btn {
    font-size: 0.875rem;
    padding: 0.75rem 1rem;
    min-width: auto;
    flex: 1;
    max-width: 150px;
  }
  
  .nav-btn svg {
    width: 14px;
    height: 14px;
  }
  
  .content-wrapper {
    padding: 0;
  }
}

@media (max-width: 480px) {
  .header-content {
    padding: 0.75rem;
  }
  
  .app-title {
    font-size: 1.25rem;
  }
  
  .nav-btn {
    font-size: 0.8rem;
    padding: 0.625rem 0.75rem;
    gap: 0.25rem;
  }
  
  .nav-btn svg {
    width: 12px;
    height: 12px;
  }
  
  .content-wrapper {
    padding: 0;
  }
}
</style>