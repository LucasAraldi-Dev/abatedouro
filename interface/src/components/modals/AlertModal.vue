<template>
  <Teleport to="body">
    <div v-if="isVisible" class="alert-modal-overlay" @click="closeModal">
      <div class="alert-modal-container" @click.stop>
        <div class="alert-header" :class="alertTypeClass">
          <div class="alert-icon">
            <i :class="alertIcon"></i>
          </div>
          <div class="alert-title">
            <h3>{{ alertTitle }}</h3>
          </div>
          <button class="close-alert" @click="closeModal" title="Fechar">
            <i class="fas fa-times"></i>
          </button>
        </div>
        
        <div class="alert-body">
          <div class="alert-message">
            <p>{{ alertMessage }}</p>
          </div>
          
          <!-- Detalhes específicos para erros de validação -->
          <div v-if="alertDetails && alertDetails.length > 0" class="alert-details">
            <div class="details-header">
              <i class="fas fa-list-ul"></i>
              <span>Detalhes do erro:</span>
            </div>
            <ul class="details-list">
              <li v-for="(detail, index) in alertDetails" :key="index"
                  :class="{ 'section-break': detail.startsWith('Erro específico:') }">
                <i v-if="detail.trim()" class="fas fa-exclamation-circle"></i>
                <span v-if="detail.trim()">{{ detail }}</span>
              </li>
            </ul>
          </div>
          
          <!-- Sugestões de solução -->
          <div v-if="alertSuggestions && alertSuggestions.length > 0" class="alert-suggestions">
            <div class="suggestions-header">
              <i class="fas fa-lightbulb"></i>
              <span>Sugestões:</span>
            </div>
            <ul class="suggestions-list">
              <li v-for="(suggestion, index) in alertSuggestions" :key="index">
                <i class="fas fa-check-circle"></i>
                {{ suggestion }}
              </li>
            </ul>
          </div>
        </div>
        
        <div class="alert-footer">
          <button @click="closeModal" class="btn-primary">
            <i class="fas fa-check"></i>
            Entendi
          </button>
          <button v-if="showRetryButton" @click="retryAction" class="btn-secondary">
            <i class="fas fa-redo"></i>
            Tentar Novamente
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script>
import { computed } from 'vue'

export default {
  name: 'AlertModal',
  props: {
    isVisible: {
      type: Boolean,
      default: false
    },
    type: {
      type: String,
      default: 'error', // 'error', 'warning', 'success', 'info'
      validator: (value) => ['error', 'warning', 'success', 'info'].includes(value)
    },
    title: {
      type: String,
      default: ''
    },
    message: {
      type: String,
      default: ''
    },
    details: {
      type: Array,
      default: () => []
    },
    suggestions: {
      type: Array,
      default: () => []
    },
    showRetry: {
      type: Boolean,
      default: false
    }
  },
  emits: ['close', 'retry'],
  setup(props, { emit }) {
    const alertTypeClass = computed(() => {
      return `alert-${props.type}`
    })
    
    const alertIcon = computed(() => {
      const icons = {
        error: 'fas fa-exclamation-triangle',
        warning: 'fas fa-exclamation-circle',
        success: 'fas fa-check-circle',
        info: 'fas fa-info-circle'
      }
      return icons[props.type] || icons.error
    })
    
    const alertTitle = computed(() => {
      if (props.title) return props.title
      
      const defaultTitles = {
        error: 'Erro',
        warning: 'Atenção',
        success: 'Sucesso',
        info: 'Informação'
      }
      return defaultTitles[props.type] || defaultTitles.error
    })
    
    const alertMessage = computed(() => {
      return props.message || 'Ocorreu um problema inesperado.'
    })
    
    const alertDetails = computed(() => {
      return props.details || []
    })
    
    const alertSuggestions = computed(() => {
      return props.suggestions || []
    })
    
    const showRetryButton = computed(() => {
      return props.showRetry && props.type === 'error'
    })
    
    const closeModal = () => {
      emit('close')
    }
    
    const retryAction = () => {
      emit('retry')
    }
    
    return {
      alertTypeClass,
      alertIcon,
      alertTitle,
      alertMessage,
      alertDetails,
      alertSuggestions,
      showRetryButton,
      closeModal,
      retryAction
    }
  }
}
</script>

<style scoped>
/* Modal Overlay */
.alert-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(4px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 3000;
  padding: 1rem;
  animation: fadeIn 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* Modal Container */
.alert-modal-container {
  background: var(--container-bg, #2c2c2c);
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  width: 100%;
  max-width: 500px;
  max-height: 85vh;
  overflow: hidden;
  animation: slideIn 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  border: 1px solid var(--input-border, #555555);
  display: flex;
  flex-direction: column;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-30px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

/* Alert Header */
.alert-header {
  padding: 1.5rem 2rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  border-bottom: 1px solid var(--input-border);
  position: relative;
}

.alert-header.alert-error {
  background: linear-gradient(135deg, var(--error-color, #ff3d71), #ff1744);
  color: white;
}

.alert-header.alert-warning {
  background: linear-gradient(135deg, var(--warning-color, #ff9800), #ff6f00);
  color: white;
}

.alert-header.alert-success {
  background: linear-gradient(135deg, var(--success-color, #00cc66), #00a152);
  color: white;
}

.alert-header.alert-info {
  background: linear-gradient(135deg, var(--primary-color, #ff6f61), var(--secondary-color, #ff3d71));
  color: white;
}

.alert-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.alert-title {
  flex: 1;
}

.alert-title h3 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
}

.close-alert {
  background: none;
  border: none;
  color: currentColor;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 50%;
  transition: all 0.3s ease;
  font-size: 1rem;
  opacity: 0.8;
}

.close-alert:hover {
  opacity: 1;
  background: rgba(255, 255, 255, 0.1);
  transform: scale(1.1);
}

/* Alert Body */
.alert-body {
  padding: 1.5rem 2rem;
  color: var(--text-color, #ffffff);
  overflow-y: auto;
  flex: 1;
}

.alert-message p {
  margin: 0 0 1rem 0;
  font-size: 1rem;
  line-height: 1.5;
}

/* Alert Details */
.alert-details {
  margin-top: 1rem;
  padding: 1rem;
  background: rgba(255, 61, 113, 0.1);
  border-radius: 8px;
  border: 1px solid rgba(255, 61, 113, 0.2);
}

.details-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
  font-weight: 600;
  color: var(--error-color, #ff3d71);
  font-size: 0.9rem;
}

.details-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.details-list li {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  line-height: 1.4;
}

.details-list li:last-child {
  margin-bottom: 0;
}

/* Adiciona espaçamento extra para seções específicas */
.details-list li.section-break {
  margin-top: 1rem;
  font-weight: 600;
  color: var(--error-color, #ff3d71);
}

.details-list li i {
  color: var(--error-color, #ff3d71);
  margin-top: 0.1rem;
  flex-shrink: 0;
}

/* Alert Suggestions */
.alert-suggestions {
  margin-top: 1rem;
  padding: 1rem;
  background: rgba(0, 204, 102, 0.1);
  border-radius: 8px;
  border: 1px solid rgba(0, 204, 102, 0.2);
}

.suggestions-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
  font-weight: 600;
  color: var(--success-color, #00cc66);
  font-size: 0.9rem;
}

.suggestions-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.suggestions-list li {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  line-height: 1.4;
}

.suggestions-list li:last-child {
  margin-bottom: 0;
}

.suggestions-list li i {
  color: var(--success-color, #00cc66);
  margin-top: 0.1rem;
  flex-shrink: 0;
}

/* Alert Footer */
.alert-footer {
  padding: 1rem 2rem 1.5rem;
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  border-top: 1px solid var(--input-border, #555555);
  background: var(--container-bg, #2c2c2c);
}

.btn-primary, .btn-secondary {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.btn-primary {
  background: var(--primary-color, #ff6f61);
  color: white;
  box-shadow: 0 4px 15px rgba(255, 111, 97, 0.3);
}

.btn-primary:hover {
  background: var(--secondary-color, #ff3d71);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 111, 97, 0.4);
}

.btn-secondary {
  background: var(--input-bg, #444444);
  color: var(--text-color, #ffffff);
  border: 1px solid var(--input-border, #555555);
}

.btn-secondary:hover {
  background: var(--input-border, #555555);
  transform: translateY(-1px);
}

/* Responsive Design */
@media (max-width: 768px) {
  .alert-modal-overlay {
    padding: 0.5rem;
  }
  
  .alert-modal-container {
    max-width: 95%;
  }
  
  .alert-header {
    padding: 1rem 1.5rem;
  }
  
  .alert-body {
    padding: 1rem 1.5rem;
  }
  
  .alert-footer {
    padding: 1rem 1.5rem;
    flex-direction: column;
  }
  
  .btn-primary, .btn-secondary {
    width: 100%;
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .alert-modal-overlay {
    padding: 0.25rem;
  }
  
  .alert-header {
    padding: 0.75rem 1rem;
  }
  
  .alert-body {
    padding: 0.75rem 1rem;
  }
  
  .alert-footer {
    padding: 0.75rem 1rem;
  }
  
  .alert-title h3 {
    font-size: 1rem;
  }
  
  .alert-message p {
    font-size: 0.9rem;
  }
}
</style>
