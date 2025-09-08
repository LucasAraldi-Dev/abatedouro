<template>
  <div v-if="isVisible" class="modal-overlay" @click="closeModal">
    <div class="modal-container" @click.stop>
      <div class="modal-header">
        <div class="mobile-icon">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="5" y="2" width="14" height="20" rx="2" ry="2" fill="#dc2626" stroke="white" stroke-width="2"/>
            <line x1="12" y1="18" x2="12.01" y2="18" stroke="white" stroke-width="2" stroke-linecap="round"/>
          </svg>
        </div>
        <h2 class="modal-title">Cadastro Disponível Apenas no Desktop</h2>
      </div>
      
      <div class="modal-body">
        <p class="info-message">Para uma melhor experiência de cadastro, utilize um computador.</p>
        
        <div class="features-section">
          <div class="feature-item">
            <div class="feature-icon">
              <i class="fas fa-desktop"></i>
            </div>
            <span>Formulário otimizado para telas maiores</span>
          </div>
          <div class="feature-item">
            <div class="feature-icon">
              <i class="fas fa-keyboard"></i>
            </div>
            <span>Digitação mais confortável</span>
          </div>
          <div class="feature-item">
            <div class="feature-icon">
              <i class="fas fa-eye"></i>
            </div>
            <span>Melhor visualização dos campos</span>
          </div>
        </div>
        
        <div class="suggestion-box">
          <div class="suggestion-icon">
            <i class="fas fa-lightbulb"></i>
          </div>
          <div class="suggestion-content">
            <p>
              <strong>Sugestão:</strong> Acesse pelo computador para criar sua conta. 
              Depois você pode fazer login normalmente pelo celular!
            </p>
          </div>
        </div>
      </div>
      
      <div class="modal-footer">
        <button @click="closeModal" class="btn-primary">
          <i class="fas fa-arrow-left"></i>
          Voltar para Login
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MobileMessage',
  props: {
    isVisible: {
      type: Boolean,
      default: false
    }
  },
  emits: ['close'],
  setup(props, { emit }) {
    const closeModal = () => {
      emit('close')
    }

    return {
      closeModal
    }
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-container {
  background: var(--bg-secondary);
  border-radius: 16px;
  box-shadow: var(--shadow-heavy);
  border: 2px solid var(--border-light);
  max-width: 500px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  animation: modalSlideIn 0.3s ease-out;
  display: flex;
  flex-direction: column;
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

.modal-header {
  padding: 1.5rem 2rem;
  text-align: center;
  background: linear-gradient(135deg, var(--bg-accent) 0%, rgba(220, 38, 38, 0.05) 100%);
  border-bottom: 3px solid var(--primary-red);
}

.mobile-icon {
  margin: 0 auto 16px;
  width: 48px;
  height: 48px;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--primary-red);
  margin: 0;
}

.modal-body {
  padding: 1.5rem 2rem;
  background: var(--bg-primary);
}

.info-message {
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 1.5rem;
  text-align: center;
  font-size: 1rem;
}

.features-section {
  background: var(--bg-accent);
  border-radius: 12px;
  padding: 1rem;
  border: 1px solid var(--border-light);
  margin-bottom: 1.5rem;
}
.feature-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 0;
  border-bottom: 1px solid var(--border-light);
}

.feature-item:last-child {
  border-bottom: none;
}

.feature-icon {
  width: 32px;
  height: 32px;
  background: var(--primary-red);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 14px;
  flex-shrink: 0;
}

.feature-item span {
  color: var(--text-primary);
  font-weight: 500;
  font-size: 0.9rem;
}

.suggestion-box {
  background: linear-gradient(135deg, rgba(220, 38, 38, 0.08) 0%, rgba(220, 38, 38, 0.03) 100%);
  border: 1px solid rgba(220, 38, 38, 0.2);
  border-radius: 12px;
  padding: 1rem;
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
}

.suggestion-icon {
  width: 32px;
  height: 32px;
  background: var(--primary-red);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 14px;
  flex-shrink: 0;
}

.suggestion-content p {
  margin: 0;
  font-size: 0.9rem;
  line-height: 1.5;
  color: var(--text-secondary);
}

.suggestion-content strong {
  color: var(--primary-red);
  font-weight: 600;
}

.modal-footer {
  padding: 1rem 2rem 1.5rem;
  display: flex;
  justify-content: center;
  background: var(--bg-accent);
  border-top: 1px solid var(--border-light);
}

.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: var(--primary-red);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 1rem;
}

.btn-primary:hover {
  background: #B91C1C;
  transform: translateY(-1px);
}

.btn-primary:active {
  transform: translateY(1px);
}

/* Responsividade */
@media (max-width: 480px) {
  .modal-container {
    width: 95%;
    margin: 0.5rem;
  }
  
  .modal-header {
    padding: 1rem 1.5rem;
  }
  
  .modal-title {
    font-size: 1.25rem;
  }
  
  .modal-body {
    padding: 1rem 1.5rem;
  }
  
  .info-message {
    font-size: 0.9rem;
  }
  
  .feature-item {
    padding: 0.5rem 0;
  }
  
  .feature-item span {
    font-size: 0.85rem;
  }
  
  .suggestion-box {
    padding: 0.75rem;
  }
  
  .suggestion-content p {
    font-size: 0.85rem;
  }
  
  .modal-footer {
    padding: 0.75rem 1.5rem 1rem;
  }
  
  .btn-primary {
    padding: 0.625rem 1.25rem;
    font-size: 0.9rem;
  }
}
</style>