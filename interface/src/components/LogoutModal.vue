<template>
  <div v-if="isVisible" class="logout-modal-overlay" @click="closeModal">
    <div class="logout-modal" @click.stop>
      <div class="modal-header">
        <div class="logout-icon">
          <i class="fas fa-sign-out-alt"></i>
        </div>
        <h3 class="modal-title">Confirmar Saída</h3>
      </div>
      
      <div class="modal-body">
        <p class="logout-message">
          Tem certeza que deseja sair do sistema?
        </p>
        <p class="logout-submessage">
          Você será redirecionado para a página de login.
        </p>
      </div>
      
      <div class="modal-actions">
        <button @click="closeModal" class="cancel-btn">
          <i class="fas fa-times"></i>
          Cancelar
        </button>
        <button @click="confirmLogout" class="confirm-btn">
          <i class="fas fa-sign-out-alt"></i>
          Sair
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  isVisible: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close', 'confirm'])

const closeModal = () => {
  emit('close')
}

const confirmLogout = () => {
  emit('confirm')
}
</script>

<style scoped>
.logout-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: fadeIn 0.2s ease-out;
}

.logout-modal {
  background: var(--bg-color, #ffffff);
  border-radius: 12px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
  max-width: 420px;
  width: 90%;
  padding: 0;
  animation: slideIn 0.3s ease-out;
  border: 1px solid var(--border-color, #e5e7eb);
}

.modal-header {
  padding: 24px 24px 16px;
  text-align: center;
  border-bottom: 1px solid var(--border-color, #e5e7eb);
}

.logout-icon {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #dc2626, #ef4444);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
  box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3);
}

.logout-icon i {
  font-size: 24px;
  color: white;
}

.modal-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-color, #1f2937);
  margin: 0;
}

.modal-body {
  padding: 20px 24px;
  text-align: center;
}

.logout-message {
  font-size: 1rem;
  color: var(--text-color, #374151);
  margin: 0 0 8px;
  font-weight: 500;
}

.logout-submessage {
  font-size: 0.875rem;
  color: var(--text-secondary, #6b7280);
  margin: 0;
}

.modal-actions {
  padding: 16px 24px 24px;
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

.cancel-btn,
.confirm-btn {
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s ease;
  min-width: 100px;
  justify-content: center;
}

.cancel-btn {
  background: var(--bg-secondary, #f3f4f6);
  color: var(--text-color, #374151);
  border: 1px solid var(--border-color, #d1d5db);
}

.cancel-btn:hover {
  background: var(--bg-hover, #e5e7eb);
  transform: translateY(-1px);
}

.confirm-btn {
  background: linear-gradient(135deg, #dc2626, #ef4444);
  color: white;
  box-shadow: 0 2px 8px rgba(220, 38, 38, 0.3);
}

.confirm-btn:hover {
  background: linear-gradient(135deg, #b91c1c, #dc2626);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(220, 38, 38, 0.4);
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-20px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

/* Tema escuro */
[data-theme="dark"] .logout-modal {
  --bg-color: #1f2937;
  --text-color: #f9fafb;
  --text-secondary: #9ca3af;
  --border-color: #374151;
  --bg-secondary: #374151;
  --bg-hover: #4b5563;
}

/* Responsividade */
@media (max-width: 480px) {
  .logout-modal {
    margin: 20px;
    width: calc(100% - 40px);
  }
  
  .modal-actions {
    flex-direction: column;
  }
  
  .cancel-btn,
  .confirm-btn {
    width: 100%;
  }
}
</style>