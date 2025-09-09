<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { checkApiHealth } from '../services/api'
import LogoutModal from '../components/LogoutModal.vue'

const router = useRouter()
const auth = useAuthStore()

// Estados da aplicação
const currentTheme = ref(localStorage.getItem('theme') || 'light')
const isOnline = ref(true)
const showLogoutModal = ref(false)

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

// Navegação removida - agora usando router-link diretamente

// Logout
const openLogoutModal = () => {
  showLogoutModal.value = true
}

const closeLogoutModal = () => {
  showLogoutModal.value = false
}

const confirmLogout = async () => {
  try {
    showLogoutModal.value = false
    await auth.logout()
    router.push('/')
  } catch (error) {
    console.error('Erro no logout:', error)
  }
}

// Verificar API periodicamente
setInterval(checkApi, 30000)
checkApi()
</script>

<template>
  <div class="app-home" :data-theme="currentTheme">
    <!-- Header -->
    <header class="app-header">
      <div class="header-content">
        <div class="header-left">
          <div class="logo-container">
            <img src="../images/logo.png" alt="Logo Sistema de Abatedouro" class="app-logo" />
          </div>
          <div class="title-section">
            <h1 class="app-title">Abatedouro Favorito</h1>
            <p class="app-subtitle">Gerenciamento de Abates e Métricas</p>
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
            <button @click="openLogoutModal" class="logout-btn">Sair</button>
          </div>
        </div>
      </div>
    </header>
    
    <!-- Navigation -->
    <nav class="main-nav">
      <router-link 
        to="/home/dashboard" 
        :class="['nav-btn', { active: $route.path === '/home/dashboard' }]"
        :aria-label="'Ir para Dashboard'"
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="3" y="3" width="7" height="7"/>
          <rect x="14" y="3" width="7" height="7"/>
          <rect x="14" y="14" width="7" height="7"/>
          <rect x="3" y="14" width="7" height="7"/>
        </svg>
        Dashboard
      </router-link>
      <router-link 
        to="/home/lotes" 
        :class="['nav-btn', { active: $route.path === '/home/lotes' }]"
        :aria-label="'Ir para Abates'"
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/>
          <rect x="8" y="2" width="8" height="4" rx="1" ry="1"/>
        </svg>
        Abates
      </router-link>
      <router-link 
        to="/home/produtos" 
        :class="['nav-btn', { active: $route.path === '/home/produtos' }]"
        :aria-label="'Ir para Produtos'"
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>
        </svg>
        Produtos
      </router-link>
      <router-link 
        to="/home/relatorios" 
        :class="['nav-btn', { active: $route.path === '/home/relatorios' }]"
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
      </router-link>
      <router-link 
        to="/home/graficos" 
        :class="['nav-btn', { active: $route.path === '/home/graficos' }]"
        :aria-label="'Ir para Gráficos'"
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="18" y1="20" x2="18" y2="10"/>
          <line x1="12" y1="20" x2="12" y2="4"/>
          <line x1="6" y1="20" x2="6" y2="14"/>
        </svg>
        Gráficos
      </router-link>
    </nav>
    
    <!-- Main Content -->
    <main class="main-content">
      <div class="content-wrapper">
        <router-view v-slot="{ Component, route }">
          <Transition name="slide" mode="out-in">
            <keep-alive>
              <component :is="Component" :key="route.path" />
            </keep-alive>
          </Transition>
        </router-view>
      </div>
    </main>
    
    <!-- Modal de Logout -->
    <LogoutModal 
      :isVisible="showLogoutModal" 
      @close="closeLogoutModal" 
      @confirm="confirmLogout" 
    />
  </div>
</template>

<style scoped>
@import url('../styles/colors.css');

.app-home {
  width: 100vw;
  min-height: 100vh;
  background: var(--bg-primary);
  color: var(--text-primary);
  font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  display: flex;
  flex-direction: column;
}

.app-header {
  background: var(--bg-primary);
  border-bottom: 2px solid var(--primary-red);
  padding: 1rem 0;
  width: 100%;
  box-shadow: var(--shadow-md);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  padding: 0 2rem;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-left: 0;
}

.logo-container {
  width: 100px;
  height: 100px;
  border-radius: 12px;
  overflow: hidden;
  background: transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 0.5rem;
}

.app-logo {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.title-section {
  display: flex;
  flex-direction: column;
}

.app-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
  line-height: 1.2;
}

.app-subtitle {
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin: 0;
  font-weight: 400;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.theme-toggle {
  background: var(--bg-tertiary);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 0.5rem;
  cursor: pointer;
  font-size: 1.2rem;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
}

.theme-toggle:hover {
  background: var(--bg-hover);
  transform: translateY(-1px);
}

.status-indicator {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status-indicator.online {
  background: rgba(34, 197, 94, 0.1);
  color: #22c55e;
  border: 1px solid rgba(34, 197, 94, 0.2);
}

.status-indicator.offline {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.user-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.user-label {
  font-weight: 500;
  color: var(--text-primary);
  font-size: 0.875rem;
}

.logout-btn {
  background: var(--primary-red);
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  font-size: 0.875rem;
  transition: all 0.2s ease;
  margin-left: 1rem;
}

.logout-btn:hover {
  background: var(--accent-red);
  transform: translateY(-1px);
}

.main-nav {
  background: var(--bg-secondary);
  border-bottom: 2px solid var(--primary-red);
  padding: 0 2rem;
  display: flex;
  gap: 0.5rem;
  overflow-x: auto;
  width: 100%;
  box-shadow: var(--shadow-sm);
}

.nav-btn {
  background: transparent;
  border: none;
  padding: 1rem 1.5rem;
  cursor: pointer;
  font-weight: 500;
  color: var(--text-secondary);
  border-bottom: 3px solid transparent;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  white-space: nowrap;
  font-size: 0.875rem;
  text-decoration: none;
}

.nav-btn:hover {
  color: var(--text-primary);
  background: rgba(220, 38, 38, 0.1);
  border-bottom-color: var(--primary-red);
}

.nav-btn.active {
  color: var(--primary-red);
  border-bottom-color: var(--primary-red);
  background: rgba(220, 38, 38, 0.1);
  font-weight: 600;
}

.nav-btn svg {
  transition: transform 0.2s ease;
}

.nav-btn:hover svg {
  transform: translateY(-1px);
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
  width: 100%;
}

.content-wrapper {
  flex: 1;
  padding: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
}

.slide-enter-active,
.slide-leave-active {
  transition: opacity 0.15s ease;
}

.slide-enter-from,
.slide-leave-to {
  opacity: 0;
}

@media (max-width: 768px) {
  .header-content {
    padding: 0 1rem;
  }
  
  .header-left {
    gap: 0.5rem;
  }
  
  .app-title {
    font-size: 1.25rem;
  }
  
  .app-subtitle {
    display: none;
  }
  
  .main-nav {
    padding: 0 1rem;
    top: 118px;
  }
  
  .nav-btn {
    padding: 0.75rem 1rem;
    font-size: 0.8rem;
  }
  
  .content-wrapper {
    padding: 1rem;
  }
}
</style>