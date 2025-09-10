<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useThemeStore } from '@/stores/theme'
import { useAuthStore } from '@/stores/auth'
import { getHealth } from '@/services/api'
import logoUrl from '@/images/logo.png'

const themeStore = useThemeStore()
const authStore = useAuthStore()
const isAppReady = ref(false)
const serverStatus = ref<'checking' | 'online' | 'offline'>('checking')

const checkServerHealth = async (retries = 3): Promise<boolean> => {
  for (let i = 0; i < retries; i++) {
    try {
      await getHealth()
      return true
    } catch (error) {
      console.warn(`Tentativa ${i + 1} de verificação do servidor falhou:`, error)
      if (i < retries - 1) {
        await new Promise(resolve => setTimeout(resolve, 2000))
      }
    }
  }
  return false
}

onMounted(async () => {
  // Initialize theme
  themeStore.initializeTheme()
  
  // Check server health first
  serverStatus.value = 'checking'
  const isServerOnline = await checkServerHealth()
  
  if (!isServerOnline) {
    serverStatus.value = 'offline'
    // Keep trying to reconnect in background
    const reconnectInterval = setInterval(async () => {
      const reconnected = await checkServerHealth(1)
      if (reconnected) {
        clearInterval(reconnectInterval)
        serverStatus.value = 'online'
        // Small delay for better UX when server comes online
        await new Promise(resolve => setTimeout(resolve, 1200))
        // Initialize auth after server is back online
        await authStore.initializeAuth()
        isAppReady.value = true
      }
    }, 5000)
    return
  }
  
  serverStatus.value = 'online'
  // Small delay for better UX when server is online from start
  await new Promise(resolve => setTimeout(resolve, 800))
  // Initialize auth after server check
  await authStore.initializeAuth()
  isAppReady.value = true
})
</script>

<template>
  <div id="app">
    <div v-if="!isAppReady" class="splash-screen">
      <!-- Logo Principal -->
      <div class="logo-container">
         <img 
            :src="logoUrl" 
            alt="Logo da Aplicação" 
            class="logo-pulse"
         />
      </div>
      
      <!-- Título da Aplicação -->
      <div class="app-title">
        <h1>Sistema de Abatedouro</h1>
        <p class="subtitle">Preparando aplicação...</p>
      </div>
      
      <!-- Status do Servidor -->
      <div class="status-container">
        <transition name="status-fade" mode="out-in">
          <div v-if="serverStatus === 'checking'" class="status-indicator status-checking" key="checking">
            <div class="status-icon">
              <div class="spinner"></div>
            </div>
            <span>Verificando conexão com servidor</span>
          </div>
          <div v-else-if="serverStatus === 'online'" class="status-indicator status-online" key="online">
            <div class="status-icon success-pulse">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="#4caf50" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <span>Servidor conectado com sucesso</span>
          </div>
          <div v-else class="status-indicator status-offline" key="offline">
            <div class="status-icon error-shake">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 9V13M12 17H12.01M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="#f44336" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <span>Servidor offline - Tentando reconectar</span>
          </div>
        </transition>
      </div>
      
      <!-- Barra de Progresso -->
      <div class="loading-progress">
        <div class="progress-bar" :class="{ 
          'error': serverStatus === 'offline',
          'success': serverStatus === 'online',
          'checking': serverStatus === 'checking'
        }"></div>
      </div>
      
      <!-- Informações Adicionais -->
      <div class="loading-info">
        <p v-if="serverStatus === 'checking'">Aguarde enquanto verificamos a disponibilidade do sistema</p>
        <p v-else-if="serverStatus === 'online'">Carregando interface do usuário</p>
        <p v-else>Tentando restabelecer conexão automaticamente</p>
      </div>
    </div>
    <router-view v-else />
  </div>
</template>

<style scoped>
.splash-screen {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  color: #2c3e50;
  padding: 40px 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  position: relative;
  overflow: hidden;
}

.splash-screen::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at 30% 20%, rgba(74, 144, 226, 0.05) 0%, transparent 50%),
              radial-gradient(circle at 70% 80%, rgba(156, 39, 176, 0.05) 0%, transparent 50%);
  pointer-events: none;
}

.logo-container {
  margin-bottom: 32px;
  position: relative;
  z-index: 1;
}

.logo-pulse {
  width: 140px;
  height: 140px;
  object-fit: contain;
  animation: gentlePulse 3s ease-in-out infinite;
  filter: drop-shadow(0 8px 16px rgba(0, 0, 0, 0.15));
  border-radius: 20px;
}

@keyframes gentlePulse {
  0%, 100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.03);
    opacity: 0.9;
  }
}

.app-title {
  text-align: center;
  margin-bottom: 48px;
  position: relative;
  z-index: 1;
}

.app-title h1 {
  font-size: 2.2rem;
  font-weight: 700;
  color: #2c3e50;
  margin: 0 0 12px 0;
  letter-spacing: -0.5px;
  line-height: 1.2;
}

.app-title .subtitle {
  font-size: 1.1rem;
  color: #6c757d;
  margin: 0;
  font-weight: 400;
  letter-spacing: 0.3px;
  animation: fadeInUp 1s ease-out 0.5s both;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.loading-progress {
  width: 280px;
  height: 6px;
  background-color: rgba(0, 0, 0, 0.08);
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 32px;
  position: relative;
  z-index: 1;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
}

.progress-bar {
  height: 100%;
  border-radius: 10px;
  transition: all 0.4s ease;
  position: relative;
}

.progress-bar.checking {
  background: linear-gradient(90deg, transparent, #4a90e2, transparent);
  animation: smoothLoading 2s ease-in-out infinite;
}

.progress-bar.success {
  background: linear-gradient(90deg, transparent, #4caf50, transparent);
  animation: successFlow 1.2s ease-in-out 2;
}

.progress-bar.error {
  background: linear-gradient(90deg, transparent, #e74c3c, transparent);
  animation: errorPulse 2.5s ease-in-out infinite;
}

.loading-info {
  text-align: center;
  margin-top: 24px;
  position: relative;
  z-index: 1;
}

.loading-info p {
  font-size: 0.95rem;
  color: #6c757d;
  margin: 0;
  font-weight: 400;
  letter-spacing: 0.2px;
  line-height: 1.4;
  animation: fadeIn 1s ease-out 1s both;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes smoothLoading {
  0% {
    transform: translateX(-100%);
    opacity: 0.7;
  }
  50% {
    opacity: 1;
  }
  100% {
    transform: translateX(380%);
    opacity: 0.7;
  }
}

@keyframes successFlow {
  0% {
    transform: translateX(-100%);
    opacity: 0.8;
  }
  50% {
    opacity: 1;
    transform: translateX(50%);
  }
  100% {
    transform: translateX(380%);
    opacity: 0.8;
  }
}

@keyframes errorPulse {
  0%, 100% {
    opacity: 0.5;
    transform: translateX(-50%);
  }
  50% {
    opacity: 1;
    transform: translateX(50%);
  }
}

/* Spinner Animation */
.spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(74, 144, 226, 0.2);
  border-top: 2px solid #4a90e2;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.status-container {
  margin-bottom: 40px;
  min-height: 70px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  z-index: 1;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 1rem;
  font-weight: 500;
  padding: 16px 24px;
  border-radius: 30px;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.4s ease;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  min-width: 280px;
  justify-content: center;
}

.status-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
}

.status-checking {
  color: #4a90e2;
  border-color: rgba(74, 144, 226, 0.3);
  background: rgba(74, 144, 226, 0.08);
}

.status-online {
  color: #27ae60;
  border-color: rgba(39, 174, 96, 0.3);
  background: rgba(39, 174, 96, 0.08);
}

.status-offline {
  color: #e74c3c;
  border-color: rgba(231, 76, 60, 0.3);
  background: rgba(231, 76, 60, 0.08);
}

/* Animações dos Ícones */
.success-pulse {
  animation: successPulse 1.8s ease-in-out 2;
}

.error-shake {
  animation: errorShake 0.6s ease-in-out 3;
}

/* Transições de Status */
.status-fade-enter-active,
.status-fade-leave-active {
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.status-fade-enter-from {
  opacity: 0;
  transform: translateY(-15px) scale(0.9);
}

.status-fade-leave-to {
  opacity: 0;
  transform: translateY(15px) scale(0.9);
}

@keyframes successPulse {
  0%, 100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.15);
    opacity: 0.9;
  }
}

@keyframes errorShake {
  0%, 100% {
    transform: translateX(0) rotate(0deg);
  }
  20% {
    transform: translateX(-3px) rotate(-1deg);
  }
  40% {
    transform: translateX(3px) rotate(1deg);
  }
  60% {
    transform: translateX(-2px) rotate(-0.5deg);
  }
  80% {
    transform: translateX(2px) rotate(0.5deg);
  }
}

/* Responsividade */
@media (max-width: 768px) {
  .splash-screen {
    padding: 20px 16px;
  }
  
  .logo-pulse {
    width: 100px;
    height: 100px;
  }
  
  .app-title h1 {
    font-size: 1.8rem;
  }
  
  .app-title .subtitle {
    font-size: 1rem;
  }
  
  .status-indicator {
    min-width: 260px;
    padding: 14px 20px;
    font-size: 0.9rem;
  }
  
  .loading-progress {
    width: 240px;
  }
  
  .loading-info p {
    font-size: 0.85rem;
  }
}

</style>