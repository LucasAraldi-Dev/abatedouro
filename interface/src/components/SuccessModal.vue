<template>
  <div v-if="isVisible" class="modal-overlay" @click="closeModal">
    <div class="modal-container" @click.stop>
      <div class="modal-header">
        <div class="success-icon">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="12" cy="12" r="10" fill="#10B981" />
            <path d="M9 12l2 2 4-4" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
        </div>
        <h2 class="modal-title">Cadastro Realizado com Sucesso!</h2>
      </div>
      
      <div class="modal-body">
        <div class="success-message-container">
          <p class="success-message">Sua conta foi criada e está aguardando aprovação da administração.</p>
        </div>
        
        <div class="content-grid">
          <div class="details-section">
            <div class="detail-item">
              <span class="detail-label">Usuário:</span>
              <span class="detail-value">{{ userData.username }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Email:</span>
              <span class="detail-value">{{ userData.email }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Senha:</span>
              <span class="detail-value">{{ maskPassword(userData.password) }}</span>
            </div>
          </div>
          
          <div class="approval-info">
            <div class="approval-header">
              <i class="fas fa-clock"></i>
              <h4>Aguardando Aprovação</h4>
            </div>
            <p class="approval-text">
              Por questões de <strong>segurança</strong>, todas as novas contas precisam ser aprovadas pela administração antes de serem ativadas.
            </p>
            <div class="approval-steps">
              <div class="step">
                <i class="fas fa-shield-alt"></i>
                <span>Conta criada com segurança</span>
              </div>
              <div class="step">
                <i class="fas fa-user-tie"></i>
                <span>Administração será notificada</span>
              </div>
              <div class="step">
                <i class="fas fa-check-circle"></i>
                <span>Confirmação por email</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="modal-footer">
        <button @click="goToLogin" class="btn-primary">
          <i class="fas fa-arrow-left"></i>
          Voltar ao Login
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SuccessModal',
  props: {
    isVisible: {
      type: Boolean,
      default: false
    },
    userData: {
      type: Object,
      default: () => ({})
    }
  },
  emits: ['close', 'login'],
  setup(props, { emit }) {
    const closeModal = () => {
      emit('close')
    }

    const goToLogin = () => {
      emit('login')
    }

    const maskPassword = (password) => {
      return '*'.repeat(password?.length || 8)
    }

    return {
      closeModal,
      goToLogin,
      maskPassword
    }
  }
}
</script>

<style scoped>
/* Modal Overlay */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}

/* Modal Container */
.modal-container {
  background: var(--bg-primary);
  border-radius: 16px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
  max-width: 500px;
  width: 90%;
  max-height: 90vh;
  overflow: hidden;
  animation: modalSlideIn 0.3s ease-out;
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: translateY(-20px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

/* Modal Header */
.modal-header {
  padding: 2rem 2rem 1rem 2rem;
  text-align: center;
  background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-accent) 100%);
  border-bottom: 1px solid var(--border-light);
}

.modal-title {
  color: var(--text-primary);
  margin: 1rem 0 0 0;
  font-size: 1.5rem;
  font-weight: 600;
}

/* Modal Body */
.modal-body {
  padding: 2rem;
  max-height: 60vh;
  overflow-y: auto;
}

.success-message-container {
  margin-bottom: 2rem;
}

.success-message {
  color: var(--text-secondary);
  margin: 0;
  line-height: 1.6;
  text-align: center;
}

.content-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  align-items: start;
}

/* Success Icon */
.success-icon {
  width: 64px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  filter: drop-shadow(0 4px 12px rgba(16, 185, 129, 0.3));
}

/* Details Section */
.details-section {
  background: var(--bg-accent);
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  border: 1px solid var(--border-light);
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 0;
  border-bottom: 1px solid var(--border-light);
}

.detail-item:last-child {
  border-bottom: none;
}

.detail-label {
  font-weight: 600;
  color: var(--text-primary);
}

.detail-value {
  color: var(--text-secondary);
  font-family: 'Courier New', monospace;
}

@keyframes scaleIn {
  0% {
    transform: scale(0);
  }
  100% {
    transform: scale(1);
  }
}

/* Approval Info */
.approval-info {
  background: var(--bg-accent);
  border-radius: 12px;
  padding: 1.5rem;
  border: 1px solid var(--border-light);
  border-left: 4px solid var(--warning-color);
}

.approval-header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.approval-header i {
  font-size: 1.25rem;
  color: var(--warning-color);
}

.approval-header h4 {
  color: var(--text-primary);
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
}

.approval-text {
  color: var(--text-secondary);
  line-height: 1.6;
  text-align: center;
  margin-bottom: 1.5rem;
}

.approval-text strong {
  color: var(--warning-color);
  font-weight: 600;
}

/* Approval Steps */
.approval-steps {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.step {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  background: var(--bg-primary);
  border-radius: 8px;
  border: 1px solid var(--border-light);
}

.step i {
  font-size: 1rem;
  color: var(--primary-red);
  width: 20px;
  text-align: center;
}

.step span {
  color: var(--text-secondary);
  font-size: 0.875rem;
  line-height: 1.4;
}

/* Modal Footer */
.modal-footer {
  padding: 1.5rem 2rem;
  display: flex;
  justify-content: center;
  gap: 1rem;
  background: var(--bg-accent);
  border-top: 1px solid var(--border-light);
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
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-primary:hover {
  background: #B91C1C;
  transform: translateY(-1px);
}

.btn-primary:active {
  transform: translateY(1px);
}

.btn-primary i {
  font-size: 0.875rem;
}

/* Success Button */
.success-button {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 14px 24px;
  background: var(--button-bg);
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 600;
  transition: all 0.3s ease;
  margin-top: 20px;
  box-shadow: 0 8px 25px rgba(255, 111, 97, 0.3);
}

.success-button:hover {
  background: var(--button-hover);
  transform: translateY(-2px);
  box-shadow: 0 12px 35px rgba(255, 111, 97, 0.4);
}

/* Responsividade */
@media (max-width: 768px) {
  .modal-container {
    width: 95%;
    margin: 1rem;
  }
  
  .modal-header {
    padding: 1.5rem 1.5rem 1rem 1.5rem;
  }
  
  .modal-body {
    padding: 1.5rem;
  }
  
  .modal-footer {
    padding: 1rem 1.5rem;
  }
  
  .modal-title {
    font-size: 1.25rem;
  }
  
  .btn-primary {
    padding: 0.625rem 1.25rem;
    font-size: 0.875rem;
  }
  
  .content-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .approval-info h4 {
    font-size: 18px;
  }
  
  .approval-text {
    font-size: 14px;
  }
  
  .success-button {
    padding: 12px 20px;
    font-size: 14px;
  }
  
  .approval-steps {
    gap: 10px;
  }
  
  .step {
    padding: 8px 12px;
    font-size: 13px;
  }
}

@media (max-width: 480px) {
  .success-modal {
    width: 100%;
    height: auto;
    border-radius: 0;
    padding: 20px 15px;
  }
  
  .success-icon {
    width: 60px;
    height: 60px;
    font-size: 30px;
  }
  
  .approval-icon {
    width: 50px;
    height: 50px;
    font-size: 25px;
  }
  
  .success-modal h3 {
    font-size: 18px;
  }
  
  .approval-info h4 {
    font-size: 16px;
  }
  
  .next-steps h5 {
    font-size: 14px;
  }
  
  .next-steps li {
    font-size: 13px;
  }
}
</style>