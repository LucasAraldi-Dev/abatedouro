<template>
  <div v-if="isVisible" class="modal-overlay">
    <div class="modal-container" @click.stop>
      <div class="modal-header">
        <h2>Atualizar Preço</h2>
        <button class="close-btn" @click="closeModal">&times;</button>
      </div>
      
      <div class="modal-body">
        <div class="produto-info">
          <h3>{{ produto?.nome }}</h3>
          <p><strong>Tipo:</strong> {{ produto?.tipo }}</p>
          <p><strong>Unidade:</strong> {{ produto?.unidade }}</p>
        </div>
        
        <div class="preco-section">
          <div class="preco-atual">
            <label>Preço Atual:</label>
            <span class="preco-valor">R$ {{ formatCurrency(produto?.preco_kg) }}</span>
          </div>
          
          <div class="form-group">
            <label for="novoPreco">Novo Preço por kg:</label>
            <input
              id="novoPreco"
              v-model="novoPreco"
              type="number"
              step="0.01"
              min="0"
              placeholder="0,00"
              class="form-input"
              @blur="formatPrecoInput"
              required
            />
          </div>
        </div>
      </div>
      
      <div class="modal-footer">
        <button class="btn btn-secondary" @click="closeModal">Cancelar</button>
        <button class="btn btn-primary" @click="atualizarPreco" :disabled="!novoPreco || isLoading">
          {{ isLoading ? 'Atualizando...' : 'Atualizar Preço' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { useToast } from '../composables/useToast'

export default {
  name: 'ModalAtualizarPreco',
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
      novoPreco: '',
      isLoading: false
    }
  },
  
  setup() {
    const { showSuccess, showError } = useToast()
    return { showSuccess, showError }
  },
  watch: {
    produto(newProduto) {
      if (newProduto) {
        this.novoPreco = newProduto.preco_kg?.toFixed(2) || ''
      }
    }
  },
  methods: {
    closeModal() {
      this.$emit('close')
      this.resetForm()
    },
    
    resetForm() {
      this.novoPreco = ''
      this.isLoading = false
    },
    
    formatCurrency(value) {
      if (!value) return '0,00'
      return parseFloat(value).toFixed(2).replace('.', ',')
    },
    
    formatPrecoInput() {
      if (this.novoPreco) {
        const numericValue = parseFloat(this.novoPreco)
        if (!isNaN(numericValue)) {
          this.novoPreco = numericValue.toFixed(2)
        }
      }
    },
    
    async atualizarPreco() {
      if (!this.produto || !this.novoPreco) return
      
      const precoNumerico = parseFloat(this.novoPreco)
      if (isNaN(precoNumerico) || precoNumerico < 0) {
        this.showError('Por favor, insira um preço válido.')
        return
      }
      
      if (precoNumerico === this.produto.preco_kg) {
        this.showError('O novo preço deve ser diferente do preço atual.')
        return
      }
      
      this.isLoading = true
      
      try {
        const response = await axios.patch(
          `https://abatedouro-jkax.onrender.com/api/v1/produtos/${this.produto._id}/preco?novo_preco=${precoNumerico}`
        )
        
        this.$emit('preco-atualizado', response.data)
        this.closeModal()
        this.showSuccess('Preço atualizado com sucesso!')
      } catch (error) {
        console.error('Erro ao atualizar preço:', error)
        this.showError('Erro ao atualizar preço. Tente novamente.')
      } finally {
        this.isLoading = false
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
  max-width: 500px;
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

.preco-section {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.preco-atual {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background-color: #f3f4f6;
  border-radius: 6px;
}

.preco-atual label {
  font-weight: 600;
  color: #374151;
}

.preco-valor {
  font-size: 1.25rem;
  font-weight: 700;
  color: #059669;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 500;
  color: #374151;
}

.form-input {
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.2s;
}

.form-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
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

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-secondary {
  background-color: #f3f4f6;
  color: #374151;
}

.btn-secondary:hover:not(:disabled) {
  background-color: #e5e7eb;
}

.btn-primary {
  background-color: #3b82f6;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background-color: #2563eb;
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
  
  .preco-atual {
    flex-direction: column;
    gap: 0.5rem;
    text-align: center;
  }
}

@media (max-width: 480px) {
  .modal-footer {
    flex-direction: column;
  }
  
  .btn {
    width: 100%;
  }
}
</style>