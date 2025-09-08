<template>
  <div v-if="isVisible" class="modal-overlay">
    <div class="modal-content terms-modal">
      <div class="modal-header">
        <h3>Termos de Serviço</h3>
        <button @click="closeModal" class="close-button">
          <i class="fas fa-times"></i>
        </button>
      </div>
      
      <div class="modal-body" @scroll="checkScrollPosition" ref="termsContent">
        <div class="terms-content">
          <h4>1. Aceitação dos Termos</h4>
          <p>Ao acessar e usar o Abatedouro Favorito, você concorda em cumprir e estar vinculado a estes Termos de Serviço.</p>
          
          <h4>2. Uso do Sistema</h4>
          <p>O sistema é destinado exclusivamente para o gerenciamento de abates e métricas relacionadas. O usuário compromete-se a:</p>
          <ul>
            <li>Usar o sistema apenas para fins comerciais legítimos</li>
            <li>Manter a confidencialidade de suas credenciais de acesso</li>
            <li>Não compartilhar dados sensíveis com terceiros não autorizados</li>
            <li>Reportar qualquer uso inadequado ou violação de segurança</li>
          </ul>
          
          <h4>3. Responsabilidades do Usuário</h4>
          <p>Você é responsável por:</p>
          <ul>
            <li>Manter suas informações de conta atualizadas e precisas</li>
            <li>Proteger suas credenciais de login</li>
            <li>Usar o sistema de acordo com as políticas da empresa</li>
            <li>Reportar problemas técnicos ou de segurança imediatamente</li>
          </ul>
          
          <h4>4. Privacidade e Proteção de Dados</h4>
          <p>A AraldiTech compromete-se a:</p>
          <ul>
            <li>Proteger seus dados pessoais conforme a LGPD</li>
            <li>Usar informações apenas para fins operacionais</li>
            <li>Manter backups seguros dos dados do sistema</li>
            <li>Não compartilhar informações com terceiros sem autorização</li>
          </ul>
          
          <h4>5. Limitações de Responsabilidade</h4>
          <p>O sistema é fornecido "como está" e a AraldiTech não se responsabiliza por:</p>
          <ul>
            <li>Interrupções temporárias do serviço</li>
            <li>Perda de dados devido a falhas técnicas</li>
            <li>Uso inadequado por parte dos usuários</li>
            <li>Problemas decorrentes de modificações não autorizadas</li>
          </ul>
          
          <h4>6. Modificações dos Termos</h4>
          <p>A AraldiTech reserva-se o direito de modificar estes termos a qualquer momento. Os usuários serão notificados sobre mudanças significativas.</p>
          
          <h4>7. Suporte Técnico</h4>
          <p>Para suporte técnico ou dúvidas sobre o sistema:</p>
          <ul>
            <li>Email: suporte@aralditech.com.br</li>
            <li>Telefone: (11) 9999-9999</li>
            <li>Horário: Segunda a Sexta, 8h às 18h</li>
          </ul>
          
          <h4>8. Vigência</h4>
          <p>Estes termos entram em vigor na data de aceitação e permanecem válidos enquanto você usar o sistema.</p>
          
          <div class="scroll-indicator" v-if="!hasScrolledToEnd">
            <i class="fas fa-arrow-down"></i>
            <span>Role até o final para continuar</span>
          </div>
        </div>
      </div>
      
      <div class="modal-footer">
        <button 
          @click="acceptTerms" 
          class="accept-button" 
          :disabled="!hasScrolledToEnd"
          :class="{ 'disabled': !hasScrolledToEnd }"
        >
          <i class="fas fa-check"></i>
          Li e Concordo
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, nextTick } from 'vue'

export default {
  name: 'TermsModal',
  props: {
    isVisible: {
      type: Boolean,
      default: false
    }
  },
  emits: ['close', 'accept'],
  setup(props, { emit }) {
    const termsContent = ref(null)
    const hasScrolledToEnd = ref(false)

    const closeModal = () => {
      emit('close')
    }

    const acceptTerms = () => {
      if (hasScrolledToEnd.value) {
        emit('accept')
      }
    }

    const checkScrollPosition = () => {
      if (termsContent.value) {
        const { scrollTop, scrollHeight, clientHeight } = termsContent.value
        const scrolledToEnd = scrollTop + clientHeight >= scrollHeight - 10
        hasScrolledToEnd.value = scrolledToEnd
      }
    }

    return {
      termsContent,
      hasScrolledToEnd,
      closeModal,
      acceptTerms,
      checkScrollPosition
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
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(5px);
}

/* Modal Content */
.modal-content {
  background: var(--container-bg);
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  border: 1px solid var(--input-border);
  max-width: 90%;
  max-height: 90%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.terms-modal {
  width: 600px;
  height: 700px;
}

/* Modal Header */
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 25px 30px;
  border-bottom: 1px solid var(--input-border);
  background: var(--container-bg);
}

.modal-header h3 {
  margin: 0;
  font-size: 24px;
  font-weight: 700;
  color: var(--primary-color);
}

.close-button {
  background: none;
  border: none;
  font-size: 20px;
  color: var(--text-color);
  cursor: pointer;
  padding: 8px;
  border-radius: 50%;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
}

.close-button:hover {
  background: rgba(255, 111, 97, 0.1);
  color: var(--primary-color);
  transform: scale(1.1);
}

/* Modal Body */
.modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 0;
  position: relative;
}

/* Scroll customizado */
.modal-body::-webkit-scrollbar {
  width: 8px;
}

.modal-body::-webkit-scrollbar-track {
  background: var(--input-bg);
  border-radius: 4px;
}

.modal-body::-webkit-scrollbar-thumb {
  background: var(--primary-color);
  border-radius: 4px;
  transition: background 0.3s ease;
}

.modal-body::-webkit-scrollbar-thumb:hover {
  background: var(--accent-color);
}

/* Terms Content */
.terms-content {
  padding: 30px;
  line-height: 1.6;
  color: var(--text-color);
}

.terms-content h4 {
  color: var(--primary-color);
  font-size: 18px;
  font-weight: 600;
  margin: 25px 0 15px 0;
  border-left: 4px solid var(--primary-color);
  padding-left: 15px;
}

.terms-content p {
  margin: 15px 0;
  font-size: 14px;
  text-align: justify;
}

.terms-content ul {
  margin: 15px 0;
  padding-left: 20px;
}

.terms-content li {
  margin: 8px 0;
  font-size: 14px;
  color: var(--text-color);
  opacity: 0.9;
}

/* Scroll Indicator */
.scroll-indicator {
  position: sticky;
  bottom: 0;
  background: linear-gradient(transparent, var(--container-bg) 50%);
  padding: 20px 0 10px;
  text-align: center;
  color: var(--primary-color);
  font-size: 14px;
  font-weight: 600;
  animation: pulse 2s infinite;
}

.scroll-indicator i {
  display: block;
  font-size: 20px;
  margin-bottom: 8px;
  animation: bounce 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
  40% { transform: translateY(-10px); }
  60% { transform: translateY(-5px); }
}

/* Modal Footer */
.modal-footer {
  padding: 25px 30px;
  border-top: 1px solid var(--input-border);
  background: var(--container-bg);
  display: flex;
  justify-content: center;
}

.accept-button {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 15px 30px;
  background: #dc2626;
  color: white;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 8px 25px rgba(220, 38, 38, 0.3);
}

.accept-button:hover:not(.disabled) {
  background: #B91C1C;
  transform: translateY(-2px);
  box-shadow: 0 12px 35px rgba(220, 38, 38, 0.4);
}

.accept-button.disabled {
  background: var(--input-border);
  color: var(--text-color);
  opacity: 0.5;
  cursor: not-allowed;
  box-shadow: none;
}

/* Responsividade */
@media (max-width: 768px) {
  .terms-modal {
    width: 95%;
    height: 85%;
    margin: 20px;
  }
  
  .modal-header {
    padding: 20px;
  }
  
  .modal-header h3 {
    font-size: 20px;
  }
  
  .terms-content {
    padding: 20px;
  }
  
  .terms-content h4 {
    font-size: 16px;
  }
  
  .modal-footer {
    padding: 20px;
  }
  
  .accept-button {
    padding: 12px 24px;
    font-size: 14px;
  }
}

@media (max-width: 480px) {
  .terms-modal {
    width: 100%;
    height: 100%;
    border-radius: 0;
  }
  
  .modal-header {
    padding: 15px;
  }
  
  .terms-content {
    padding: 15px;
  }
  
  .modal-footer {
    padding: 15px;
  }
}
</style>