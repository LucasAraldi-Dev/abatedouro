<template>
  <div class="loading-container" :class="{ 'overlay': overlay, 'inline': !overlay }">
    <div class="loading-indicator" :class="sizeClass">
      <div class="spinner">
        <!-- Círculo girando -->
        <div class="spinning-circle"></div>
      </div>
      <!-- Mensagem opcional -->
      <div v-if="message" class="loading-message">{{ message }}</div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoadingIndicator',
  props: {
    /**
     * Mensagem a ser exibida junto com o indicador
     */
    message: {
      type: String,
      default: ''
    },
    /**
     * Se o indicador deve ser exibido como overlay ou inline
     */
    overlay: {
      type: Boolean,
      default: false
    },
    /**
     * Tamanho do indicador: 'small', 'medium' ou 'large'
     */
    size: {
      type: String,
      default: 'medium',
      validator: (value) => ['small', 'medium', 'large'].includes(value)
    }
  },
  computed: {
    /**
     * Classe CSS com base no tamanho
     */
    sizeClass() {
      return `size-${this.size}`;
    }
  }
}
</script>

<style scoped>
.loading-container {
  display: flex;
  align-items: center;
  justify-content: center;
}

.loading-container.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.9);
  z-index: 9999;
  backdrop-filter: blur(0.125rem);
}

.loading-container.inline {
  display: inline-flex;
  margin: 0 0.5rem;
}

.loading-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  border-radius: 0.75rem;
  background: linear-gradient(145deg, #ffffff, #f8f9fa);
  border: 1px solid #e5e7eb;
  box-shadow: 0 10px 30px rgba(220, 38, 38, 0.1);
  transition: all 0.3s ease;
}

.loading-message {
  color: #374151;
  margin-top: 1rem;
  text-align: center;
  font-size: 0.875rem;
  font-weight: 500;
}

/* Spinner */
.spinner {
  display: flex;
  align-items: center;
  justify-content: center;
}

.spinning-circle {
  width: 2rem;
  height: 2rem;
  border: 3px solid #f3f4f6;
  border-top: 3px solid #dc2626;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

/* Tamanhos */
.size-small .spinning-circle {
  width: 1.5rem;
  height: 1.5rem;
  border-width: 2px;
}

.size-small .loading-message {
  font-size: 0.75rem;
}

.size-large .spinning-circle {
  width: 2.5rem;
  height: 2.5rem;
  border-width: 4px;
}

.size-large .loading-message {
  font-size: 1rem;
}

/* Animação de rotação */
@keyframes spin {
  0% { 
    transform: rotate(0deg);
  } 
  100% { 
    transform: rotate(360deg);
  }
}

/* Responsividade */
@media (max-width: 768px) {
  .loading-indicator {
    padding: 0.75rem;
    max-width: 90%;
  }
  
  .loading-message {
    font-size: 0.75rem;
    margin-top: 0.75rem;
  }
}
</style>