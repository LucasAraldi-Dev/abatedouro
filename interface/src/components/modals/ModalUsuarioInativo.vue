<template>
  <div v-if="isVisible" class="modal-overlay" @click="closeModal">
    <div class="modal-container" @click.stop>
      <div class="modal-header">
        <div class="error-icon">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="12" cy="12" r="10" fill="var(--primary-red)" />
            <path d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" fill="white" />
            <path d="M15 9l-6 6m0-6l6 6" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
        </div>
        <h2 class="modal-title">Conta Aguardando Aprovação</h2>
      </div>
      
      <div class="modal-body">
        <div class="warning-message">
          <p class="primary-message">Sua conta precisa ser ativada pela administração.</p>
          <p class="secondary-message" v-if="userInfo?.nome">
            Olá {{ userInfo.nome }}! Sua conta foi criada{{ userInfo.data_cadastro ? ` em ${formatDate(userInfo.data_cadastro)}` : '' }}, mas ainda está aguardando aprovação.
          </p>
          <p class="secondary-message" v-else>
            Sua conta foi criada com sucesso, mas ainda está aguardando aprovação da administração.
          </p>
        </div>
        
        <div class="info-section">
          <div class="info-item">
            <i class="fas fa-user-shield"></i>
            <span>Entre em contato com a administração ou gerência</span>
          </div>
          <div class="info-item">
            <i class="fas fa-envelope"></i>
            <span>Solicite a ativação da sua conta</span>
          </div>
          <div class="info-item">
            <i class="fas fa-clock"></i>
            <span>O processo de aprovação pode levar algumas horas</span>
          </div>
        </div>
        
        <div class="status-info" v-if="userInfo">
          <h4>Informações da Conta:</h4>
          <div class="status-details">
            <div class="detail-item" v-if="userInfo.nome">
              <strong>Nome:</strong> {{ userInfo.nome }}
            </div>
            <div class="detail-item" v-if="userInfo.data_cadastro">
              <strong>Data de Cadastro:</strong> {{ formatDate(userInfo.data_cadastro) }}
            </div>
            <div class="detail-item">
              <strong>Status:</strong> <span class="status-pending">Aguardando Aprovação</span>
            </div>
          </div>
        </div>
      </div>
      
      <div class="modal-footer">
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
  name: 'ModalUsuarioInativo',
  props: {
    isVisible: {
      type: Boolean,
      default: false
    },
    userInfo: {
      type: Object,
      default: () => ({})
    }
  },
  emits: ['close'],
  methods: {
    closeModal() {
      this.$emit('close')
    },
    formatDate(dateString) {
      if (!dateString) return ''
      try {
        const date = new Date(dateString)
        return date.toLocaleDateString('pt-BR', {
          day: '2-digit',
          month: '2-digit',
          year: 'numeric'
        })
      } catch (error) {
        return dateString
      }
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
  border: 1px solid rgba(255, 193, 7, 0.2);
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
  border-bottom: 1px solid rgba(255, 193, 7, 0.1);
}

.warning-icon {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #ffc107, #e0a800);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
  box-shadow: 0 10px 30px rgba(255, 193, 7, 0.3);
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    box-shadow: 0 10px 30px rgba(255, 193, 7, 0.3);
  }
  50% {
    box-shadow: 0 10px 40px rgba(255, 193, 7, 0.5);
  }
  100% {
    box-shadow: 0 10px 30px rgba(255, 193, 7, 0.3);
  }
}

.warning-icon i {
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

.warning-message {
  text-align: center;
  margin-bottom: 30px;
}

.primary-message {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin: 0 0 15px 0;
  line-height: 1.4;
}

.secondary-message {
  font-size: 16px;
  color: #666;
  margin: 0 0 10px 0;
  line-height: 1.5;
}

.info-section {
  background: rgba(255, 193, 7, 0.05);
  border-radius: 12px;
  padding: 20px;
  border-left: 4px solid #ffc107;
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
  color: #ffc107;
  margin-right: 12px;
  width: 16px;
  text-align: center;
}

.status-info {
  background: rgba(108, 117, 125, 0.05);
  border-radius: 12px;
  padding: 20px;
  border: 1px solid rgba(108, 117, 125, 0.1);
}

.status-info h4 {
  margin: 0 0 15px 0;
  color: #333;
  font-size: 16px;
  font-weight: 600;
}

.status-details {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.detail-item {
  font-size: 14px;
  color: #555;
}

.detail-item strong {
  color: #333;
  margin-right: 8px;
}

.status-pending {
  color: #ffc107;
  font-weight: 600;
}

.modal-footer {
  padding: 20px 30px 30px;
  text-align: center;
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

.btn-primary:active {
  transform: translateY(0);
  box-shadow: 0 4px 15px rgba(255, 193, 7, 0.3);
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
  
  .warning-icon {
    width: 60px;
    height: 60px;
    margin-bottom: 15px;
  }
  
  .warning-icon i {
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
  }
}
</style>