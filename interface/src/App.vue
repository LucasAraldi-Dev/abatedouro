<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useThemeStore } from './stores/theme'
import { useAuthStore } from './stores/auth'
import { getHealth } from './services/api'

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
      <div class="logo-container">
         <img 
           src="/logo.png" 
           alt="Logo" 
           class="logo-pulse"
         />
      </div>
      <div class="status-container">
        <transition name="status-fade" mode="out-in">
          <div v-if="serverStatus === 'checking'" class="status-indicator status-checking" key="checking">
            <div class="status-icon">🔍</div>
            <span>Verificando servidor...</span>
          </div>
          <div v-else-if="serverStatus === 'online'" class="status-indicator status-online" key="online">
            <div class="status-icon success-pulse">✅</div>
            <span>Servidor conectado</span>
          </div>
          <div v-else class="status-indicator status-offline" key="offline">
            <div class="status-icon error-shake">❌</div>
            <span>Servidor offline - Tentando reconectar...</span>
          </div>
        </transition>
      </div>
      <div class="loading-progress">
        <div class="progress-bar" :class="{ 
          'error': serverStatus === 'offline',
          'success': serverStatus === 'online'
        }"></div>
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
  background: #ffffff;
  color: #333333;
  padding: 20px;
}

.logo-container {
  margin-bottom: 40px;
}

.logo-pulse {
  width: 120px;
  height: 120px;
  object-fit: contain;
  animation: pulse 2s ease-in-out infinite;
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.3));
}

@keyframes pulse {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.05);
    opacity: 0.8;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

.loading-text {
  text-align: center;
  margin-bottom: 30px;
}

.loading-text p {
  font-size: 18px;
  margin: 0;
  font-weight: 500;
  letter-spacing: 0.5px;
}

.loading-progress {
  width: 200px;
  height: 4px;
  background-color: rgba(0, 0, 0, 0.1);
  border-radius: 2px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background: linear-gradient(90deg, transparent, #ff9800, transparent);
  animation: loading 1.5s ease-in-out infinite;
  border-radius: 2px;
  transition: all 0.3s ease;
}

.progress-bar.success {
  background: linear-gradient(90deg, transparent, #4caf50, transparent);
  animation: success-loading 1s ease-in-out 2;
}

.progress-bar.error {
  background: linear-gradient(90deg, transparent, #f44336, transparent);
  animation: error-pulse 2s ease-in-out infinite;
}

@keyframes loading {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(300%);
  }
}

@keyframes success-loading {
  0% {
    transform: translateX(-100%);
    opacity: 0.8;
  }
  50% {
    opacity: 1;
  }
  100% {
    transform: translateX(300%);
    opacity: 0.8;
  }
}

@keyframes error-pulse {
  0%, 100% {
    opacity: 0.6;
  }
  50% {
    opacity: 1;
  }
}

.status-container {
  margin-bottom: 1.5rem;
  min-height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1rem;
  font-weight: 500;
  padding: 0.75rem 1.5rem;
  border-radius: 25px;
  background: rgba(0, 0, 0, 0.05);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.status-icon {
  font-size: 1.2rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.status-checking {
  color: #ff9800;
  border-color: rgba(255, 152, 0, 0.3);
  background: rgba(255, 152, 0, 0.1);
}

.status-online {
  color: #4caf50;
  border-color: rgba(76, 175, 80, 0.3);
  background: rgba(76, 175, 80, 0.1);
}

.status-offline {
  color: #f44336;
  border-color: rgba(244, 67, 54, 0.3);
  background: rgba(244, 67, 54, 0.1);
}

/* Animações */
.success-pulse {
  animation: successPulse 1.5s ease-in-out 2;
}

.error-shake {
  animation: errorShake 0.5s ease-in-out 2;
}

/* Transições */
.status-fade-enter-active,
.status-fade-leave-active {
  transition: all 0.4s ease;
}

.status-fade-enter-from {
  opacity: 0;
  transform: translateY(-10px) scale(0.95);
}

.status-fade-leave-to {
  opacity: 0;
  transform: translateY(10px) scale(0.95);
}

@keyframes successPulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.2);
  }
}

@keyframes errorShake {
  0%, 100% {
    transform: translateX(0);
  }
  25% {
    transform: translateX(-5px);
  }
  75% {
    transform: translateX(5px);
  }
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>