<template>
  <div class="etapa-container">
    <div class="etapa-header">
      <h3>Etapa 2: Produtos Processados</h3>
      <p>Adicione os produtos que serão processados no abate</p>
    </div>

    <div class="etapa-content">
      <!-- Busca de Produtos -->
      <div class="search-section">
        <div class="search-container">
          <div class="search-input-group">
            <input
              ref="searchInput"
              v-model="searchTerm"
              type="text"
              class="search-input"
              placeholder="Digite pelo menos 2 caracteres para buscar produtos..."
              @input="onSearchInput"
              @keydown.enter="adicionarPrimeiroProduto"
              @keydown.down="navegarSugestoes(1)"
              @keydown.up="navegarSugestoes(-1)"
              @keydown.escape="limparBusca"
            />
            <button 
              @click="buscarProdutos" 
              class="search-btn"
              :disabled="!searchTerm.trim()"
            >
              🔍
            </button>
          </div>
          
          <!-- Sugestões de Produtos -->
          <div v-if="sugestoesProdutos.length > 0" class="suggestions-dropdown">
            <div 
              v-for="(produto, index) in sugestoesProdutos" 
              :key="produto._id"
              class="suggestion-item"
              :class="{ 'highlighted': index === selectedSuggestion }"
              @click="adicionarProduto(produto)"
              @mouseenter="selectedSuggestion = index"
            >
              <div class="produto-info">
                <span class="produto-nome">{{ produto.nome }}</span>
                <span class="produto-preco">R$ {{ produto.preco_kg?.toFixed(2) || '0.00' }}/kg</span>
              </div>
              <div class="produto-detalhes">
                <span class="produto-tipo">{{ produto.tipo || 'Sem tipo' }}</span>
                <span class="produto-unidade">kg</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Lista de Produtos Adicionados -->
      <div class="produtos-section">
        <div class="section-header">
          <h4>Produtos Selecionados</h4>
          <span class="produtos-count">{{ localFormData.produtos.length }} produto(s)</span>
        </div>

        <div v-if="localFormData.produtos.length === 0" class="empty-state">
          <div class="empty-icon">📦</div>
          <p>Nenhum produto adicionado ainda</p>
          <small>Use a busca acima para adicionar produtos</small>
          <span v-if="validationErrors.produtos" class="error-message">{{ validationErrors.produtos }}</span>
        </div>

        <div v-else class="produtos-tabela">
          <!-- Cabeçalho da Tabela -->
          <div class="tabela-header">
            <div class="header-produto">Produto</div>
            <div class="header-quantidade">Quantidade</div>
            <div class="header-preco">Preço Unit.</div>
            <div class="header-total">Total</div>
            <div class="header-acao">Ação</div>
          </div>
          
          <!-- Linhas dos Produtos -->
          <div 
            v-for="(produto, index) in localFormData.produtos" 
            :key="index"
            class="tabela-linha"
          >
            <div class="coluna-produto">
              <span class="produto-nome">{{ produto.nome }}</span>
              <span class="produto-tipo">{{ produto.tipo || 'Sem tipo' }}</span>
            </div>
            <div class="coluna-quantidade">
              <span class="quantidade-valor">{{ formatNumber(produto.quantidade) }} kg</span>
            </div>
            <div class="coluna-preco">
              <span class="preco-valor">R$ {{ formatCurrency(produto.preco_unitario) }}/kg</span>
            </div>
            <div class="coluna-total">
              <span class="total-valor">R$ {{ formatCurrency((produto.quantidade || 0) * (produto.preco_unitario || 0)) }}</span>
            </div>
            <div class="coluna-acao">
              <button 
                @click="removerProduto(index)"
                class="btn-remover"
                aria-label="Remover produto"
                title="Remover produto"
              >
                🗑️
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Resumo dos Produtos -->
      <div v-if="localFormData.produtos.length > 0" class="resumo-section">
        <h4>Resumo dos Produtos</h4>
        <div class="resumo-grid">
          <div class="resumo-item">
            <span class="label">Total de Produtos:</span>
            <span class="value">{{ localFormData.produtos.length }}</span>
          </div>
          <div class="resumo-item">
            <span class="label">Quantidade Total:</span>
            <span class="value">{{ quantidadeTotalFormatted }}</span>
          </div>
          <div class="resumo-item">
            <span class="label">Valor Total dos Produtos:</span>
            <span class="value">{{ valorTotalProdutosFormatted }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal para Quantidade -->
    <div v-if="showQuantityModal" class="modal-overlay">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h4>Adicionar Produto</h4>
          <button @click="cancelarAdicao" class="close-btn">×</button>
        </div>
        <div class="modal-body">
          <div class="produto-selecionado">
            <h5>{{ produtoSelecionado?.nome }}</h5>
            <p class="produto-tipo">{{ produtoSelecionado?.tipo || 'Sem tipo' }}</p>
            <p class="produto-preco">R$ {{ produtoSelecionado?.preco_kg?.toFixed(2) || '0.00' }}/kg</p>
          </div>
          <div class="form-group">
            <label for="quantidade-input">Quantidade (KG) *</label>
            <input
              ref="quantityInput"
              id="quantidade-input"
              v-model.number="quantidadeTemp"
              type="number"
              class="form-control"
              :class="{ 'error': quantityError }"
              min="0.01"
              step="0.01"
              placeholder="Digite a quantidade em KG"
              @keydown.enter="confirmarAdicao"
              @keydown.escape="cancelarAdicao"
            />
            <span v-if="quantityError" class="error-message">{{ quantityError }}</span>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="cancelarAdicao" class="btn-secondary">Cancelar</button>
          <button @click="confirmarAdicao" class="btn-primary" :disabled="!quantidadeTemp || quantidadeTemp <= 0">Adicionar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { getProdutos } from '../../services/api'
import { useToast } from '../../composables/useToast'

// Toast notifications
const { showWarning } = useToast()

// Props
interface Props {
  formData: any
  isEditing: boolean
}

const props = defineProps<Props>()

// Emits
const emit = defineEmits<{
  'update-form': [data: any]
  'validate': [isValid: boolean]
}>()

// Estado local
const localFormData = ref({ ...props.formData })
const searchTerm = ref('')
const sugestoesProdutos = ref([])
const selectedSuggestion = ref(-1)
const isLoading = ref(false)
const showQuantityModal = ref(false)
const produtoSelecionado = ref(null)
const quantidadeTemp = ref(0)
const quantityError = ref('')
const searchInput = ref(null)
const quantityInput = ref(null)

// Funções de formatação
const formatNumber = (value: number): string => {
  if (!value && value !== 0) return '0'
  return new Intl.NumberFormat('pt-BR').format(value)
}

const formatCurrency = (value: number): string => {
  if (!value && value !== 0) return '0,00'
  return new Intl.NumberFormat('pt-BR', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(value)
}

// Computed values
const quantidadeTotalFormatted = computed(() => {
  const total = localFormData.value.produtos.reduce((sum: number, produto: any) => {
    return sum + (produto.quantidade || 0)
  }, 0)
  return `${formatNumber(total)} kg`
})

const valorTotalProdutosFormatted = computed(() => {
  const total = localFormData.value.produtos.reduce((sum: number, produto: any) => {
    return sum + (produto.total || 0)
  }, 0)
  return `R$ ${formatCurrency(total)}`
})

// Estado de validação
const validationErrors = ref<Record<string, string>>({})

// Validação
const isValid = computed(() => {
  // Limpar erros anteriores
  const errors: Record<string, string> = {}
  
  // Pelo menos um produto deve ser adicionado
  if (localFormData.value.produtos.length === 0) {
    errors.produtos = 'Adicione pelo menos um produto'
    validationErrors.value = errors
    return false
  }
  
  // Validar cada produto
  let hasProductErrors = false
  localFormData.value.produtos.forEach((produto: any, index: number) => {
    if (!produto.quantidade || produto.quantidade <= 0) {
      errors[`produto_${index}_quantidade`] = 'Quantidade deve ser maior que zero'
      hasProductErrors = true
    }
    if (!produto.preco_unitario || produto.preco_unitario <= 0) {
      errors[`produto_${index}_preco`] = 'Preço deve ser maior que zero'
      hasProductErrors = true
    }
    if (produto.quantidade > 150000) {
      errors[`produto_${index}_quantidade`] = 'Quantidade muito alta (máx: 150.000)'
      hasProductErrors = true
    }
    if (produto.preco_unitario > 1000) {
      errors[`produto_${index}_preco`] = 'Preço muito alto (máx: R$ 1.000,00)'
      hasProductErrors = true
    }
  })
  
  validationErrors.value = errors
  return !hasProductErrors
})

// Validar produto específico
const validateProduct = (index: number) => {
  const produto = localFormData.value.produtos[index]
  const errors = { ...validationErrors.value }
  
  // Limpar erros anteriores deste produto
  delete errors[`produto_${index}_quantidade`]
  delete errors[`produto_${index}_preco`]
  
  if (!produto.quantidade || produto.quantidade <= 0) {
    errors[`produto_${index}_quantidade`] = 'Quantidade deve ser maior que zero'
  } else if (produto.quantidade > 150000) {
    errors[`produto_${index}_quantidade`] = 'Quantidade muito alta (máx: 150.000)'
  }
  
  if (!produto.preco_unitario || produto.preco_unitario <= 0) {
    errors[`produto_${index}_preco`] = 'Preço deve ser maior que zero'
  } else if (produto.preco_unitario > 1000) {
    errors[`produto_${index}_preco`] = 'Preço muito alto (máx: R$ 1.000,00)'
  }
  
  validationErrors.value = errors
}

// Funções de busca
const onSearchInput = () => {
  if (searchTerm.value.length >= 2) {
    buscarProdutos()
  } else {
    sugestoesProdutos.value = []
    selectedSuggestion.value = -1
  }
}

const buscarProdutos = async () => {
  if (!searchTerm.value.trim() || searchTerm.value.length < 2) {
    sugestoesProdutos.value = []
    return
  }

  try {
    isLoading.value = true
    const response = await getProdutos({
      search: searchTerm.value,
      limit: 10
    })
    sugestoesProdutos.value = response || []
    selectedSuggestion.value = -1
  } catch (error) {
    console.error('Erro ao buscar produtos:', error)
    sugestoesProdutos.value = []
  } finally {
    isLoading.value = false
  }
}

// Navegação nas sugestões
const navegarSugestoes = (direction: number) => {
  if (sugestoesProdutos.value.length === 0) return
  
  selectedSuggestion.value += direction
  
  if (selectedSuggestion.value < 0) {
    selectedSuggestion.value = sugestoesProdutos.value.length - 1
  } else if (selectedSuggestion.value >= sugestoesProdutos.value.length) {
    selectedSuggestion.value = 0
  }
}

// Adicionar produto
const adicionarPrimeiroProduto = () => {
  if (selectedSuggestion.value >= 0 && sugestoesProdutos.value[selectedSuggestion.value]) {
    abrirModalQuantidade(sugestoesProdutos.value[selectedSuggestion.value])
  } else if (sugestoesProdutos.value.length > 0) {
    abrirModalQuantidade(sugestoesProdutos.value[0])
  }
}

const abrirModalQuantidade = (produto: any) => {
  // Verificar se o produto já foi adicionado
  const jaAdicionado = localFormData.value.produtos.some((p: any) => p._id === produto._id)
  
  if (jaAdicionado) {
    showWarning('Este produto já foi adicionado!')
    return
  }

  produtoSelecionado.value = produto
  quantidadeTemp.value = 0
  quantityError.value = ''
  showQuantityModal.value = true
  
  // Focar no input de quantidade após o modal aparecer
  setTimeout(() => {
    if (quantityInput.value) {
      quantityInput.value.focus()
    }
  }, 100)
}

const confirmarAdicao = () => {
  if (!quantidadeTemp.value || quantidadeTemp.value <= 0) {
    quantityError.value = 'Digite uma quantidade válida'
    return
  }

  if (quantidadeTemp.value > 150000) {
    quantityError.value = 'Quantidade muito alta (máx: 150.000 kg)'
    return
  }

  const novoProduto = {
    _id: produtoSelecionado.value._id,
    nome: produtoSelecionado.value.nome,
    tipo: produtoSelecionado.value.tipo,
      quantidade: quantidadeTemp.value,
      unidade: 'kg',
      preco_unitario: produtoSelecionado.value.preco_kg || 0,
    total: quantidadeTemp.value * (produtoSelecionado.value.preco_kg || 0),
    observacoes: ''
  }

  localFormData.value.produtos.push(novoProduto)
  fecharModal()
  emitUpdate()
}

const cancelarAdicao = () => {
  fecharModal()
}

const fecharModal = () => {
  showQuantityModal.value = false
  produtoSelecionado.value = null
  quantidadeTemp.value = 0
  quantityError.value = ''
  limparBusca()
  
  // Retornar foco para o campo de busca
  setTimeout(() => {
    if (searchInput.value) {
      searchInput.value.focus()
    }
  }, 100)
}

const adicionarProduto = (produto: any) => {
  abrirModalQuantidade(produto)
}

// Remover produto
const removerProduto = (index: number) => {
  localFormData.value.produtos.splice(index, 1)
  emitUpdate()
}

// Calcular total do produto
const calcularTotalProduto = (index: number) => {
  const produto = localFormData.value.produtos[index]
  if (produto) {
    produto.total = (produto.quantidade || 0) * (produto.preco_unitario || 0)
    emitUpdate()
  }
}

// Limpar busca
const limparBusca = () => {
  searchTerm.value = ''
  sugestoesProdutos.value = []
  selectedSuggestion.value = -1
}

// Navegação por teclado
const focusNext = (event: Event) => {
  const target = event.target as HTMLElement
  const container = target.closest('.produto-card') || target.closest('.etapa-container')
  if (!container) return

  const inputs = Array.from(container.querySelectorAll('input, select'))
  const currentIndex = inputs.indexOf(target)
  const nextInput = inputs[currentIndex + 1] as HTMLElement

  if (nextInput) {
    nextInput.focus()
  }
}

// Emitir atualizações
const emitUpdate = () => {
  emit('update-form', localFormData.value)
}

// Watchers
watch(() => props.formData, (newData) => {
  Object.assign(localFormData.value, newData)
}, { deep: true })

watch(localFormData, () => {
  emitUpdate()
}, { deep: true })

watch(isValid, (valid) => {
  emit('validate', valid)
}, { immediate: true })

// Inicialização
onMounted(() => {
  // Focar no campo de busca
  const searchInput = document.querySelector('.search-input') as HTMLElement
  if (searchInput) {
    searchInput.focus()
  }
  
  // Garantir que produtos é um array
  if (!Array.isArray(localFormData.value.produtos)) {
    localFormData.value.produtos = []
  }
})
</script>

<style scoped>
.etapa-container {
  padding: 2rem;
  height: 100%;
  overflow-y: auto;
}

.etapa-header {
  margin-bottom: 2rem;
  text-align: center;
}

.etapa-header h3 {
  color: var(--primary-red);
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0 0 0.5rem 0;
}

.etapa-header p {
  color: var(--text-muted);
  font-size: 1rem;
  margin: 0;
}

.etapa-content {
  max-width: 1200px;
  margin: 0 auto;
}

/* Seção de Busca */
.search-section {
  margin-bottom: 2rem;
}

.search-container {
  position: relative;
  max-width: 500px;
  margin: 0 auto;
}

.search-input-group {
  display: flex;
  gap: 0.5rem;
}

.search-input {
  flex: 1;
  padding: 0.75rem 1rem;
  border: 2px solid var(--border-light);
  border-radius: 8px;
  background: var(--bg-secondary);
  color: var(--text-primary);
  font-size: 1rem;
  transition: all 0.2s ease;
}

.search-input:focus {
  outline: none;
  border-color: var(--primary-red);
  box-shadow: 0 0 0 3px rgba(220, 38, 38, 0.1);
}

.search-btn {
  padding: 0.75rem 1rem;
  background: var(--primary-red);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.2s ease;
}

.search-btn:hover:not(:disabled) {
  background: #B91C1C;
}

.search-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Sugestões */
.suggestions-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: var(--bg-secondary);
  border: 2px solid var(--border-light);
  border-top: none;
  border-radius: 0 0 8px 8px;
  max-height: 300px;
  overflow-y: auto;
  z-index: 100;
  box-shadow: var(--shadow-medium);
}

.suggestion-item {
  padding: 1rem;
  cursor: pointer;
  border-bottom: 1px solid var(--border-light);
  transition: all 0.2s ease;
}

.suggestion-item:hover {
  background: var(--bg-accent);
}

.suggestion-item.highlighted {
  background: #e5e7eb;
  border-left: 3px solid var(--primary-red);
}

.suggestion-item:last-child {
  border-bottom: none;
}

.produto-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.25rem;
}

.produto-nome {
  font-weight: 600;
  color: var(--text-primary);
}

.produto-preco {
  color: var(--primary-red);
  font-weight: 600;
}

.produto-detalhes {
  display: flex;
  justify-content: space-between;
  font-size: 0.875rem;
  color: var(--text-muted);
}

/* Seção de Produtos */
.produtos-section {
  margin-bottom: 2rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.section-header h4 {
  color: var(--text-primary);
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
}

.produtos-count {
  background: var(--primary-red);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 600;
}

/* Estado vazio */
.empty-state {
  text-align: center;
  padding: 3rem 1rem;
  color: var(--text-muted);
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.empty-state p {
  font-size: 1.125rem;
  margin: 0 0 0.5rem 0;
}

.empty-state small {
  font-size: 0.875rem;
}

/* Grid de produtos */
.produtos-grid {
  display: grid;
  gap: 1.5rem;
}

.produto-card {
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  padding: 1.5rem;
  transition: all 0.2s ease;
}

.produto-card:hover {
  border-color: var(--primary-red);
  box-shadow: var(--shadow-medium);
}

.produto-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid var(--primary-red);
}

.produto-header h5 {
  color: var(--primary-red);
  font-size: 1.125rem;
  font-weight: 600;
  margin: 0;
}

.remove-btn {
  background: none;
  border: none;
  color: var(--text-muted);
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.2s ease;
}

.remove-btn:hover {
  background: #EF4444;
  color: white;
}

.produto-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  color: var(--text-primary);
  font-weight: 600;
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
}

.form-control {
  padding: 0.75rem;
  border: 2px solid var(--border-light);
  border-radius: 8px;
  background: var(--bg-secondary);
  color: var(--text-primary);
  font-size: 0.875rem;
  transition: all 0.2s ease;
}

.form-control:focus {
  outline: none;
  border-color: var(--primary-red);
  box-shadow: 0 0 0 3px rgba(220, 38, 38, 0.1);
}

.calculated-value {
  padding: 0.75rem;
  background: var(--bg-accent);
  border: 2px solid var(--border-light);
  border-radius: 8px;
  color: var(--primary-red);
  font-weight: 600;
  font-size: 0.875rem;
}

/* Seção de Resumo */
.resumo-section {
  background: linear-gradient(135deg, var(--bg-accent) 0%, rgba(220, 38, 38, 0.05) 100%);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  padding: 1.5rem;
}

.resumo-section h4 {
  color: var(--primary-red);
  font-size: 1.125rem;
  font-weight: 600;
  margin: 0 0 1rem 0;
}

.resumo-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.resumo-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: 8px;
}

.resumo-item .label {
  color: var(--text-muted);
  font-size: 0.875rem;
  font-weight: 500;
}

.resumo-item .value {
  color: var(--primary-red);
  font-size: 0.875rem;
  font-weight: 700;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
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

.modal-header h4 {
  margin: 0;
  color: var(--primary-red);
  font-size: 1.25rem;
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
  border-radius: 50%;
  transition: all 0.2s;
}

.close-btn:hover {
  background: #f3f4f6;
  color: #374151;
}

.modal-body {
  padding: 1.5rem;
}

.produto-selecionado {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  padding: 1rem;
  margin-bottom: 1.5rem;
}

.produto-selecionado h5 {
  margin: 0 0 0.5rem 0;
  color: #111827;
  font-size: 1.1rem;
  font-weight: 600;
}

.produto-tipo {
  margin: 0 0 0.25rem 0;
  color: #6b7280;
  font-size: 0.875rem;
}

.produto-preco {
  margin: 0;
  color: var(--primary-red);
  font-weight: 600;
  font-size: 1rem;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  padding: 1.5rem;
  border-top: 1px solid #e5e7eb;
}

.btn-secondary {
  background: #f3f4f6;
  color: #374151;
  border: 1px solid #d1d5db;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 500;
  transition: all 0.2s;
}

.btn-secondary:hover {
  background: #e5e7eb;
  border-color: #9ca3af;
}

.btn-primary {
  background: var(--primary-red);
  color: white;
  border: 1px solid var(--primary-red);
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 500;
  transition: all 0.2s;
}

.btn-primary:hover:not(:disabled) {
  background: #dc2626;
  border-color: #dc2626;
}

.btn-primary:disabled {
  background: #d1d5db;
  border-color: #d1d5db;
  cursor: not-allowed;
}

/* Responsividade */
@media (max-width: 768px) {
  .etapa-container {
    padding: 1rem;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .resumo-grid {
    grid-template-columns: 1fr;
  }

  .modal-content {
    width: 95%;
    margin: 1rem;
  }

  .modal-header,
  .modal-body,
  .modal-footer {
    padding: 1rem;
  }

  .modal-footer {
    flex-direction: column;
  }

  .btn-secondary,
  .btn-primary {
    width: 100%;
    padding: 0.75rem;
  }
}

@media (max-width: 480px) {
  .etapa-header h3 {
    font-size: 1.25rem;
  }
  
  .produto-card {
    padding: 1rem;
  }
  
  .resumo-section {
    padding: 1rem;
  }
}

/* Estilos de validação */
.form-control.error {
  border-color: #EF4444;
  background-color: rgba(239, 68, 68, 0.05);
}

.form-control.error:focus {
  border-color: #EF4444;
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
}

.error-message {
  color: #EF4444;
  font-size: 0.75rem;
  font-weight: 500;
  margin-top: 0.25rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.error-message::before {
  content: '⚠';
  font-size: 0.875rem;
}

.form-group:has(.error) label {
  color: #EF4444;
}

.empty-state .error-message {
  margin-top: 1rem;
  justify-content: center;
}

/* Estilos para a tabela de produtos */
.produtos-tabela {
  background: white;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.tabela-header {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr 80px;
  gap: 1rem;
  padding: 1rem;
  background: #f8fafc;
  border-bottom: 2px solid #e5e7eb;
  font-weight: 600;
  color: #374151;
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.025em;
}

.tabela-linha {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr 80px;
  gap: 1rem;
  padding: 1rem;
  border-bottom: 1px solid #f3f4f6;
  transition: background-color 0.2s;
  align-items: center;
}

.tabela-linha:hover {
  background: #f9fafb;
}

.tabela-linha:last-child {
  border-bottom: none;
}

.coluna-produto {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.produto-nome {
  font-weight: 600;
  color: #111827;
  font-size: 0.95rem;
}

.produto-tipo {
  color: #6b7280;
  font-size: 0.8rem;
  text-transform: capitalize;
}

.coluna-quantidade,
.coluna-preco,
.coluna-total {
  display: flex;
  align-items: center;
}

.quantidade-valor,
.preco-valor,
.total-valor {
  font-weight: 600;
  color: #111827;
  font-size: 0.9rem;
}

.total-valor {
  color: var(--primary-red);
  font-weight: 700;
}

.coluna-acao {
  display: flex;
  justify-content: center;
}

.btn-remover {
  background: #fee2e2;
  color: #dc2626;
  border: 1px solid #fecaca;
  width: 36px;
  height: 36px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 1rem;
}

.btn-remover:hover {
  background: #fecaca;
  border-color: #f87171;
  transform: scale(1.05);
}

/* Responsividade para telas menores */
@media (max-width: 768px) {
  .tabela-header {
    grid-template-columns: 1fr;
    gap: 0;
    padding: 0;
    background: transparent;
    border: none;
    display: none; /* Oculta cabeçalho em mobile */
  }
  
  .tabela-linha {
    grid-template-columns: 1fr;
    gap: 0.75rem;
    padding: 1rem;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    margin-bottom: 0.75rem;
    background: #f9fafb;
  }
  
  .tabela-linha:hover {
    background: #f3f4f6;
  }
  
  .coluna-produto,
  .coluna-quantidade,
  .coluna-preco,
  .coluna-total {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem 0;
    border-bottom: 1px solid #e5e7eb;
  }
  
  .coluna-acao {
    padding-top: 0.5rem;
    border-top: 1px solid #e5e7eb;
    margin-top: 0.5rem;
  }
  
  .coluna-produto::before { content: "Produto:"; }
  .coluna-quantidade::before { content: "Quantidade:"; }
  .coluna-preco::before { content: "Preço Unit.:"; }
  .coluna-total::before { content: "Total:"; }
  
  .coluna-produto::before,
  .coluna-quantidade::before,
  .coluna-preco::before,
  .coluna-total::before {
    font-weight: 600;
    color: #6b7280;
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.025em;
  }
}
</style>