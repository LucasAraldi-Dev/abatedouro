<template>
  <div v-if="isVisible" class="modal-overlay" @click="closeModal">
    <div class="modal-container" @click.stop>
      <div class="modal-header">
        <div class="error-icon">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="12" cy="12" r="10" fill="var(--primary-red)" />
            <path d="M15 9l-6 6m0-6l6 6" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
        </div>
        <h2 class="modal-title">Senha Incorreta</h2>
      </div>
      
      <div class="modal-body">
        <div class="error-message">
          <p class="primary-message">As credenciais informadas não estão corretas.</p>
          <p class="secondary-message">Verifique se digitou corretamente seu usuário e senha.</p>
        </div>
        
        <div class="help-section">
          <div class="help-item">
            <i class="fas fa-info-circle"></i>
            <span>Certifique-se de que o Caps Lock não está ativado</span>
          </div>
          <div class="help-item">
            <i class="fas fa-eye"></i>
            <span>Use o botão de visualizar senha para confirmar</span>
          </div>
          <div class="help-item">
            <i class="fas fa-user-shield"></i>
            <span>Entre em contato com o administrador se esqueceu sua senha</span>
          </div>
        </div>
      </div>
      
      <div class="modal-footer">
        <button @click="closeModal" class="btn-primary">
          <i class="fas fa-arrow-left"></i>
          Tentar Novamente
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ModalErroSenha',
  props: {
    isVisible: {
      type: Boolean,
      default: false
    }
  },
  emits: ['close'],
  methods: {
    closeModal() {
      this.$emit('close')
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
  max-width: 500px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  animation: modalSlideIn 0.3s ease-out;
  border: 1px solid rgba(220, 53, 69, 0.2);
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
  border-bottom: 1px solid rgba(220, 53, 69, 0.1);
}

.error-icon {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #dc3545, #c82333);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
  box-shadow: 0 10px 30px rgba(220, 53, 69, 0.3);
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    box-shadow: 0 10px 30px rgba(220, 53, 69, 0.3);
  }
  50% {
    box-shadow: 0 10px 40px rgba(220, 53, 69, 0.5);
  }
  100% {
    box-shadow: 0 10px 30px rgba(220, 53, 69, 0.3);
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

.help-section {
  background: rgba(220, 53, 69, 0.05);
  border-radius: 12px;
  padding: 20px;
  border-left: 4px solid #dc3545;
}

.help-item {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
  font-size: 14px;
  color: #555;
}

.help-item:last-child {
  margin-bottom: 0;
}

.help-item i {
  color: #dc3545;
  margin-right: 12px;
  width: 16px;
  text-align: center;
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
  box-shadow: 0 4px 15px rgba(220, 53, 69, 0.3);
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
  }
}
</style>