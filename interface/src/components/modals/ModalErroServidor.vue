<template>
  <div v-if="isVisible" class="modal-overlay" @click="closeModal">
    <div class="modal-container" @click.stop>
      <div class="modal-header">
        <div class="error-icon">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="12" cy="12" r="10" fill="var(--primary-red)" />
            <path d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
        </div>
        <h2 class="modal-title">Erro no Servidor</h2>
      </div>
      
      <div class="modal-body">
        <div class="error-message">
          <p class="primary-message">O servidor encontrou um problema temporário.</p>
          <p class="secondary-message">Não foi possível processar sua solicitação no momento.</p>
        </div>
        
        <div class="info-section">
          <div class="info-item">
            <i class="fas fa-clock"></i>
            <span>Tente novamente em alguns instantes</span>
          </div>
          <div class="info-item">
            <i class="fas fa-sync-alt"></i>
            <span>O problema geralmente é temporário</span>
          </div>
          <div class="info-item">
            <i class="fas fa-headset"></i>
            <span>Se persistir, contate o suporte técnico</span>
          </div>
        </div>
        
        <div class="technical-info" v-if="errorDetails">
          <h4>Detalhes Técnicos:</h4>
          <div class="error-details">
            <div class="detail-item" v-if="errorDetails.status">
              <strong>Código:</strong> {{ errorDetails.status }}
            </div>
            <div class="detail-item" v-if="errorDetails.message">
              <strong>Mensagem:</strong> {{ errorDetails.message }}
            </div>
            <div class="detail-item">
              <strong>Horário:</strong> {{ currentTime }}
            </div>
          </div>
        </div>
      </div>
      
      <div class="modal-footer">
        <button @click="retryAction" class="btn-retry" v-if="showRetry">
          <i class="fas fa-redo"></i>
          Tentar Novamente
        </button>
        <button @click="closeModal" class="btn-primary">
          <i class="fas fa-arrow-left"></i>
          Voltar ao Login
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ModalErroServidor',
  props: {
    isVisible: {
      type: Boolean,
      default: false
    },
    errorDetails: {
      type: Object,
      default: () => ({})
    },
    showRetry: {
      type: Boolean,
      default: true
    }
  },
  emits: ['close', 'retry'],
  computed: {
    currentTime() {
      return new Date().toLocaleString('pt-BR')
    }
  },
  methods: {
    closeModal() {
      this.$emit('close')
    },
    retryAction() {
      this.$emit('retry')
    }
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
  backdrop-filter: blur(5px);
}

.modal-container {
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  max-width: 550px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  animation: modalSlideIn 0.3s ease-out;
  border: 1px solid rgba(108, 117, 125, 0.2);
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: translateY(-30px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.modal-header {
  text-align: center;
  padding: 30px 30px 20px;
  border-bottom: 1px solid rgba(108, 117, 125, 0.1);
}

.error-icon {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #6c757d, #5a6268);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
  box-shadow: 0 10px 30px rgba(108, 117, 125, 0.3);
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    box-shadow: 0 10px 30px rgba(108, 117, 125, 0.3);
  }
  50% {
    box-shadow: 0 10px 40px rgba(108, 117, 125, 0.5);
  }
  100% {
    box-shadow: 0 10px 30px rgba(108, 117, 125, 0.3);
  }
}

.error-icon i {
  font-size: 36px;
  color: white;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--primary-red);
  margin: 0;
}

.modal-body {
  padding: 30px;
}

.error-message {
  text-align: center;
  margin-bottom: 30px;
}

.primary-message {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin: 0 0 10px 0;
  line-height: 1.4;
}

.secondary-message {
  font-size: 16px;
  color: #666;
  margin: 0;
  line-height: 1.5;
}

.info-section {
  background: rgba(108, 117, 125, 0.05);
  border-radius: 12px;
  padding: 20px;
  border-left: 4px solid #6c757d;
  margin-bottom: 25px;
}

.info-item {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
  font-size: 14px;
  color: #555;
}

.info-item:last-child {
  margin-bottom: 0;
}

.info-item i {
  color: #6c757d;
  margin-right: 12px;
  width: 16px;
  text-align: center;
}

.technical-info {
  background: rgba(248, 249, 250, 0.8);
  border-radius: 12px;
  padding: 20px;
  border: 1px solid rgba(108, 117, 125, 0.1);
}

.technical-info h4 {
  margin: 0 0 15px 0;
  color: #333;
  font-size: 16px;
  font-weight: 600;
}

.error-details {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.detail-item {
  font-size: 14px;
  color: #555;
  font-family: 'Courier New', monospace;
}

.detail-item strong {
  color: #333;
  margin-right: 8px;
  font-family: inherit;
}

.modal-footer {
  padding: 20px 30px 30px;
  text-align: center;
  display: flex;
  gap: 15px;
  justify-content: center;
  flex-wrap: wrap;
}

.btn-primary, .btn-retry {
  border: none;
  padding: 14px 30px;
  border-radius: 25px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.btn-primary {
  padding: 0.75rem 1.5rem;
  background: var(--primary-red);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-primary:hover {
  background: #B91C1C;
  transform: translateY(-1px);
}

.btn-retry {
  background: linear-gradient(135deg, #28a745, #20c997);
  color: white;
  box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
}

.btn-retry:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(40, 167, 69, 0.4);
  background: linear-gradient(135deg, #20c997, #17a2b8);
}

.btn-primary:active, .btn-retry:active {
  transform: translateY(0);
}

/* Responsividade */
@media (max-width: 768px) {
  .modal-container {
    margin: 20px;
    width: calc(100% - 40px);
  }
  
  .modal-header {
    padding: 20px 20px 15px;
  }
  
  .error-icon {
    width: 60px;
    height: 60px;
    margin-bottom: 15px;
  }
  
  .error-icon i {
    font-size: 28px;
  }
  
  .modal-title {
    font-size: 24px;
  }
  
  .modal-body {
    padding: 20px;
  }
  
  .primary-message {
    font-size: 16px;
  }
  
  .secondary-message {
    font-size: 14px;
  }
  
  .modal-footer {
    padding: 15px 20px 20px;
    flex-direction: column;
  }
  
  .btn-primary, .btn-retry {
    width: 100%;
    justify-content: center;
  }
}
</style>