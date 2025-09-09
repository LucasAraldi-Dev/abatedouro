<template>
  <div v-if="isVisible" class="modal-overlay">
    <div class="modal-container" @click.stop>
      <div class="modal-header">
        <h2>Histórico do Produto</h2>
        <button class="close-btn" @click="closeModal">&times;</button>
      </div>
      
      <div class="modal-body">
        <div class="produto-info">
          <h3>{{ produto?.nome }}</h3>
          <p><strong>Tipo:</strong> {{ produto?.tipo }}</p>
          <p><strong>Unidade:</strong> kg</p>
          <p><strong>Preço Atual:</strong> R$ {{ formatCurrency(produto?.preco_kg) }}</p>
        </div>
        
        <div class="historico-section">
          <div class="historico-header" @click="toggleHistorico">
            <h4>Histórico de Alterações</h4>
            <span class="toggle-icon" :class="{ 'expanded': historicoExpanded }">
              {{ historicoExpanded ? '▼' : '▶' }}
            </span>
          </div>
          
          <div v-if="historicoExpanded" class="historico-content">
            <div v-if="isLoading" class="loading">
              <p>Carregando histórico...</p>
            </div>
            
            <div v-else-if="historico.length === 0" class="no-history">
              <p>Nenhuma alteração encontrada para este produto.</p>
            </div>
            
            <div v-else class="historico-list">
              <div 
                v-for="log in historico" 
                :key="log._id" 
                class="historico-item"
              >
                <div class="log-header">
                  <span class="log-tipo">{{ log.tipo_alteracao }}</span>
                  <span class="log-data">{{ formatDate(log.data_alteracao) }}</span>
                </div>
                
                <div class="log-details">
                  <div class="campo-alterado">
                    <strong>Campo:</strong> {{ formatCampo(log.campo_alterado) }}
                  </div>
                  
                  <div class="valores">
                    <div class="valor-anterior">
                      <span class="label">De:</span>
                      <span class="valor">R$ {{ formatCurrency(log.valor_anterior) }}</span>
                    </div>
                    <div class="seta">→</div>
                    <div class="valor-novo">
                      <span class="label">Para:</span>
                      <span class="valor">R$ {{ formatCurrency(log.valor_novo) }}</span>
                    </div>
                  </div>
                  
                  <div v-if="log.observacoes" class="observacoes">
                    <strong>Observações:</strong> {{ log.observacoes }}
                  </div>
                  
                  <div class="usuario">
                    <strong>Usuário:</strong> {{ log.usuario }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="modal-footer">
        <button class="btn btn-secondary" @click="closeModal">Fechar</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { API_BASE_URL } from '../config/env'

export default {
  name: 'ModalHistoricoProduto',
  props: {
    isVisible: {
      type: Boolean,
      default: false
    },
    produto: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      historico: [],
      isLoading: false,
      historicoExpanded: false
    }
  },
  watch: {
    isVisible(newValue) {
      if (newValue && this.produto) {
        this.carregarHistorico()
      }
    }
  },
  methods: {
    closeModal() {
      this.$emit('close')
      this.resetModal()
    },
    
    resetModal() {
      this.historico = []
      this.isLoading = false
      this.historicoExpanded = false
    },
    
    toggleHistorico() {
      this.historicoExpanded = !this.historicoExpanded
      if (this.historicoExpanded && this.historico.length === 0) {
        this.carregarHistorico()
      }
    },
    
    async carregarHistorico() {
      if (!this.produto) return
      
      this.isLoading = true
      
      try {
        const response = await axios.get(
          `${API_BASE_URL}/produto-logs/produto/${this.produto._id}`
        )
        
        this.historico = response.data.sort((a, b) => 
          new Date(b.data_alteracao) - new Date(a.data_alteracao)
        )
      } catch (error) {
        console.error('Erro ao carregar histórico:', error)
        this.historico = []
      } finally {
        this.isLoading = false
      }
    },
    
    formatCurrency(value) {
      if (!value) return '0,00'
      return parseFloat(value).toFixed(2).replace('.', ',')
    },
    
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleString('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    },
    
    formatCampo(campo) {
      const campos = {
        'preco_kg': 'Preço por kg',
        'nome': 'Nome',
        'tipo': 'Tipo',
        'unidade': 'Unidade'
      }
      return campos[campo] || campo
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
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-container {
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 90%;
  max-width: 700px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.modal-header h2 {
  margin: 0;
  color: #1f2937;
  font-size: 1.5rem;
  font-weight: 600;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6b7280;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  color: #374151;
}

.modal-body {
  padding: 1.5rem;
}

.produto-info {
  background-color: #f9fafb;
  padding: 1rem;
  border-radius: 6px;
  margin-bottom: 1.5rem;
}

.produto-info h3 {
  margin: 0 0 0.5rem 0;
  color: #1f2937;
  font-size: 1.25rem;
}

.produto-info p {
  margin: 0.25rem 0;
  color: #6b7280;
}

.historico-section {
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  overflow: hidden;
}

.historico-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background-color: #f3f4f6;
  cursor: pointer;
  transition: background-color 0.2s;
}

.historico-header:hover {
  background-color: #e5e7eb;
}

.historico-header h4 {
  margin: 0;
  color: #374151;
  font-size: 1.1rem;
}

.toggle-icon {
  font-size: 0.9rem;
  color: #6b7280;
  transition: transform 0.2s;
}

.toggle-icon.expanded {
  transform: rotate(0deg);
}

.historico-content {
  padding: 1rem;
  background-color: white;
}

.loading,
.no-history {
  text-align: center;
  padding: 2rem;
  color: #6b7280;
}

.historico-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.historico-item {
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  padding: 1rem;
  background-color: #fafafa;
}

.log-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.log-tipo {
  background-color: #3b82f6;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-size: 0.875rem;
  font-weight: 500;
}

.log-data {
  color: #6b7280;
  font-size: 0.875rem;
}

.log-details {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.campo-alterado {
  color: #374151;
}

.valores {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.valor-anterior,
.valor-novo {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.label {
  font-size: 0.75rem;
  color: #6b7280;
  text-transform: uppercase;
  font-weight: 600;
}

.valor {
  font-weight: 600;
  font-size: 1rem;
}

.valor-anterior .valor {
  color: #dc2626;
}

.valor-novo .valor {
  color: #059669;
}

.seta {
  font-size: 1.25rem;
  color: #6b7280;
  font-weight: bold;
}

.observacoes,
.usuario {
  color: #374151;
  font-size: 0.875rem;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  padding: 1.5rem;
  border-top: 1px solid #e5e7eb;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-secondary {
  background-color: #f3f4f6;
  color: #374151;
}

.btn-secondary:hover {
  background-color: #e5e7eb;
}

/* Responsividade */
@media (max-width: 768px) {
  .modal-container {
    width: 95%;
    margin: 1rem;
  }
  
  .modal-header,
  .modal-body,
  .modal-footer {
    padding: 1rem;
  }
  
  .valores {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .seta {
    transform: rotate(90deg);
  }
}

@media (max-width: 480px) {
  .log-header {
    flex-direction: column;
    gap: 0.5rem;
    align-items: flex-start;
  }
  
  .historico-item {
    padding: 0.75rem;
  }
}
</style>