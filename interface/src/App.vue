<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from './stores/auth'

const auth = useAuthStore()
const isAppReady = ref(false)

// Estado do tema
const currentTheme = ref(localStorage.getItem('theme') || 'light')

// Inicialização
onMounted(async () => {
  // Aplicar tema
  document.documentElement.setAttribute('data-theme', currentTheme.value)
  
  // Inicializar autenticação ANTES de mostrar qualquer conteúdo
  await auth.initializeAuth()
  
  // Marcar app como pronto para renderizar
  isAppReady.value = true
})
</script>

<template>
  <div id="app" :data-theme="currentTheme">
    <!-- Loading inicial enquanto inicializa autenticação -->
    <div v-if="!isAppReady" class="app-loading">
      <div class="loading-spinner"></div>
      <p>Carregando...</p>
    </div>
    
    <!-- Conteúdo principal após inicialização -->
    <template v-else>
      <!-- Router View - AppLogin ou AppHome -->
      <router-view v-slot="{ Component, route }">
        <Transition name="fade" mode="out-in">
          <component :is="Component" :key="route.path" />
        </Transition>
      </router-view>
    </template>
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
}

.app-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  gap: 1rem;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid var(--border-color);
  border-top: 4px solid var(--primary-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}


</style>