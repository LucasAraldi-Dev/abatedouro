<script setup lang="ts">
import '@/styles/common-headers.css'
import { ref, onMounted, computed } from 'vue'
import { getProdutos, createProduto, updateProduto, deleteProduto, type Produto, type ProdutoCreate, type ProdutoUpdate } from '../services/api'
import BuscaAvancada from './BuscaAvancada.vue'
import ModalAtualizarPreco from './ModalAtualizarPreco.vue'
import ModalHistoricoProduto from './ModalHistoricoProduto.vue'
import { exportToCSV, exportToPDF, formatDate, formatCurrency, formatWeight, type ExportColumn } from '../utils/exportUtils'
import { useToast } from '../composables/useToast'

const { showError } = useToast()

const produtos = ref<Produto[]>([])
const loading = ref(false)
const error = ref('')
const showModal = ref(false)
const editingProduto = ref<Produto | null>(null)
const showDeleteConfirm = ref(false)
const produtoToDelete = ref<Produto | null>(null)
const filtrosBusca = ref<Record<string, any>>({})

// Novos modais
const showModalAtualizarPreco = ref(false)
const showModalHistorico = ref(false)
const produtoSelecionado = ref<Produto | null>(null)

// Configuração dos campos de busca
const camposBusca = [
  {
    key: 'tipo',
    label: 'Tipo',
    type: 'select' as const,
    opcoes: [
      { value: 'Peito', label: 'Peito' },
      { value: 'Coxa', label: 'Coxa' },
      { value: 'Sobrecoxa', label: 'Sobrecoxa' },
      { value: 'Asa', label: 'Asa' },
      { value: 'Carcaça', label: 'Carcaça' },
      { value: 'Miúdos', label: 'Miúdos' },
      { value: 'Outros', label: 'Outros' }
    ]
  },
  {
    key: 'unidade_origem',
    label: 'Unidade de Origem',
    type: 'select' as const,
    opcoes: [
      { value: 'Unidade Belo Jardim', label: 'Unidade Belo Jardim' }
    ]
  },
  {
    key: 'preco_kg',
    label: 'Preço por kg (R$)',
    type: 'number' as const,
    min: 0.01,
    placeholder: 'Preço mínimo'
  }
]

// Filtros
const filtroTipo = ref('')
const filtroUnidade = ref('')
const filtroPrecoMin = ref<number | null>(null)
const filtroPrecoMax = ref<number | null>(null)

// Formulário
const form = ref<ProdutoCreate>({
  nome: '',
  tipo: '',
  preco_kg: 0,
  unidade_origem: ''
})

const formErrors = ref<Record<string, string>>({})

// Computed
const produtosFiltrados = computed(() => {
  // Se não há filtros ativos, retorna todos os produtos
  const temFiltros = filtrosBusca.value.termo || 
                     filtrosBusca.value.tipo || 
                     filtrosBusca.value.unidade_origem || 
                     filtrosBusca.value.preco_kg
  
  if (!temFiltros) {
    return produtos.value
  }
  
  let resultado = [...produtos.value]
  
  // Filtro por termo de busca
  if (filtrosBusca.value.termo && filtrosBusca.value.termo.trim()) {
    const termo = filtrosBusca.value.termo.toLowerCase().trim()
    resultado = resultado.filter(produto => 
      produto.nome.toLowerCase().includes(termo) ||
      produto.tipo.toLowerCase().includes(termo) ||
      produto.unidade_origem.toLowerCase().includes(termo) ||
      produto.preco_kg.toString().includes(termo)
    )
  }
  
  // Filtros específicos
  if (filtrosBusca.value.tipo) {
    resultado = resultado.filter(produto => produto.tipo === filtrosBusca.value.tipo)
  }
  
  if (filtrosBusca.value.unidade_origem) {
    resultado = resultado.filter(produto => produto.unidade_origem === filtrosBusca.value.unidade_origem)
  }
  
  if (filtrosBusca.value.preco_kg) {
    resultado = resultado.filter(produto => produto.preco_kg >= filtrosBusca.value.preco_kg)
  }
  
  return resultado
})

const isEditing = computed(() => editingProduto.value !== null)

const modalTitle = computed(() => isEditing.value ? 'Editar Produto' : 'Novo Produto')

// Métodos
const loadProdutos = async () => {
  try {
    loading.value = true
    error.value = ''
    const response = await getProdutos()
    produtos.value = response
  } catch (err) {
    error.value = 'Erro ao carregar produtos'
    console.error('Erro ao carregar produtos:', err)
  } finally {
    loading.value = false
  }
}

const openModal = (produto?: Produto) => {
  if (produto) {
    editingProduto.value = produto
    form.value = {
      nome: produto.nome,
      tipo: produto.tipo,
      preco_kg: produto.preco_kg,
      unidade_origem: produto.unidade_origem
    }
  } else {
    editingProduto.value = null
    form.value = {
      nome: '',
      tipo: '',
      preco_kg: 0,
      unidade_origem: 'Unidade Belo Jardim'
    }
  }
  formErrors.value = {}
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  editingProduto.value = null
  formErrors.value = {}
}

const validateForm = (): boolean => {
  const errors: Record<string, string> = {}
  
  if (!form.value.nome.trim()) {
    errors.nome = 'Nome é obrigatório'
  }
  
  if (!form.value.tipo.trim()) {
    errors.tipo = 'Tipo é obrigatório'
  }
  
  if (form.value.preco_kg <= 0) {
    errors.preco_kg = 'Preço deve ser maior que zero'
  }
  
  if (!form.value.unidade_origem.trim()) {
    errors.unidade_origem = 'Unidade de origem é obrigatória'
  }
  
  formErrors.value = errors
  return Object.keys(errors).length === 0
}

const saveProduto = async () => {
  if (!validateForm()) {
    return
  }
  
  try {
    loading.value = true
    
    if (isEditing.value && editingProduto.value) {
      const updateData: ProdutoUpdate = { ...form.value }
      await updateProduto(editingProduto.value._id, updateData)
    } else {
      await createProduto(form.value)
    }
    
    await loadProdutos()
    closeModal()
  } catch (err) {
    error.value = isEditing.value ? 'Erro ao atualizar produto' : 'Erro ao criar produto'
    console.error('Erro ao salvar produto:', err)
  } finally {
    loading.value = false
  }
}

const confirmDelete = (produto: Produto) => {
  produtoToDelete.value = produto
  showDeleteConfirm.value = true
}

const cancelDelete = () => {
  produtoToDelete.value = null
  showDeleteConfirm.value = false
}

const deleteProdutoConfirmed = async () => {
  if (!produtoToDelete.value) return
  
  try {
    loading.value = true
    await deleteProduto(produtoToDelete.value._id)
    await loadProdutos()
    cancelDelete()
  } catch (err) {
    error.value = 'Erro ao excluir produto'
    console.error('Erro ao excluir produto:', err)
  } finally {
    loading.value = false
  }
}

const updatePrice = (produto: Produto) => {
  const novoPreco = prompt(`Atualizar preço do produto "${produto.nome}"\nPreço atual: ${formatCurrency(produto.preco_kg)}\n\nNovo preço (R$):`, produto.preco_kg.toFixed(2))
  
  if (novoPreco && !isNaN(parseFloat(novoPreco))) {
    const precoNumerico = parseFloat(parseFloat(novoPreco).toFixed(2))
    if (precoNumerico > 0) {
      updateProdutoPrice(produto._id, precoNumerico)
    } else {
      showError('O preço deve ser maior que zero.')
    }
  }
}

const updateProdutoPrice = async (id: string, novoPreco: number) => {
  try {
    loading.value = true
    const updateData: ProdutoUpdate = { preco_kg: novoPreco }
    await updateProduto(id, updateData)
    await loadProdutos()
  } catch (err) {
    error.value = 'Erro ao atualizar preço do produto'
    console.error('Erro ao atualizar preço:', err)
  } finally {
    loading.value = false
  }
}

const buscarProdutos = () => {
  console.log('Buscando com filtros:', filtrosBusca.value)
}

const limparFiltros = () => {
  filtrosBusca.value = {}
}

const exportarProdutos = (formato: 'csv' | 'pdf') => {
  const columns: ExportColumn[] = [
    { key: 'nome', label: 'Nome' },
    { key: 'tipo', label: 'Tipo' },
    { key: 'preco_kg', label: 'Preço por kg', formatter: (value) => formatCurrency(value) },
    { key: 'unidade_origem', label: 'Unidade de Origem' }
  ]

  const options = {
    filename: 'produtos',
    title: 'Produtos e Cortes',
    subtitle: `${produtosFiltrados.value.length} registros encontrados`,
    columns,
    data: produtosFiltrados.value
  }

  if (formato === 'csv') {
    exportToCSV(options)
  } else {
    exportToPDF(options)
  }
}

const clearFilters = () => {
  filtroTipo.value = ''
  filtroUnidade.value = ''
  filtroPrecoMin.value = null
  filtroPrecoMax.value = null
}

const formatCurrency = (value: number): string => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(value)
}

const formatWeight = (value: number): string => {
  return `${value.toFixed(2)} kg`
}

const convertToUppercase = (event: Event) => {
  const target = event.target as HTMLInputElement
  const value = target.value.toUpperCase()
  form.value.nome = value
}

const formatPrecoInput = () => {
  if (form.value.preco_kg) {
    form.value.preco_kg = parseFloat(form.value.preco_kg.toFixed(2))
  }
}

// Métodos para os novos modais
const abrirModalAtualizarPreco = (produto: Produto) => {
  produtoSelecionado.value = produto
  showModalAtualizarPreco.value = true
}

const fecharModalAtualizarPreco = () => {
  showModalAtualizarPreco.value = false
  produtoSelecionado.value = null
}

const abrirModalHistorico = (produto: Produto) => {
  produtoSelecionado.value = produto
  showModalHistorico.value = true
}

const fecharModalHistorico = () => {
  showModalHistorico.value = false
  produtoSelecionado.value = null
}

const onPrecoAtualizado = async (produtoAtualizado: Produto) => {
  // Atualizar a lista de produtos
  await loadProdutos()
}

// Lifecycle
onMounted(() => {
  loadProdutos()
})
</script>

<template>
  <div class="produtos-container">


    <!-- Busca Avançada -->
    <BuscaAvancada
      v-model="filtrosBusca"
      :campos="camposBusca"
      :loading="loading"
      @search="buscarProdutos"
      @clear="limparFiltros"
    />
    
    <div class="export-actions">
      <button @click="exportarProdutos('csv')" class="btn btn-secondary btn-sm">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
          <polyline points="14,2 14,8 20,8"/>
          <line x1="16" y1="13" x2="8" y2="13"/>
          <line x1="16" y1="17" x2="8" y2="17"/>
          <polyline points="10,9 9,9 8,9"/>
        </svg>
        Exportar CSV
      </button>
      <button @click="exportarProdutos('pdf')" class="btn btn-primary btn-sm">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
          <polyline points="14,2 14,8 20,8"/>
          <line x1="16" y1="13" x2="8" y2="13"/>
          <line x1="16" y1="17" x2="8" y2="17"/>
          <polyline points="10,9 9,9 8,9"/>
        </svg>
        Exportar PDF
      </button>
    </div>

    <!-- Mensagem de erro -->
    <div v-if="error" class="error-message">
      {{ error }}
    </div>

    <!-- Loading -->
    <div v-if="loading" class="loading">
      <img src="../images/logo.png" alt="Carregando produtos" class="loading-logo" />
    </div>

    <!-- Tabela de produtos -->
    <div v-else class="produtos-table-container">
      <div class="table-info">
        <div class="table-header">
          <h3>{{ produtosFiltrados.length }} {{ produtosFiltrados.length === 1 ? 'produto encontrado' : 'produtos encontrados' }}</h3>
        </div>
      </div>
      
      <div class="table-wrapper">
        <table class="produtos-table">
          <thead>
            <tr>
              <th>Nome</th>
              <th>Tipo</th>

              <th>Preço/kg</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="produtosFiltrados.length === 0">
              <td colspan="4" class="no-data">
                {{ produtos.length === 0 ? 'Nenhum produto encontrado.' : 'Nenhum produto corresponde aos filtros aplicados.' }}
              </td>
            </tr>
            <tr v-for="produto in produtosFiltrados" :key="produto._id" class="produto-row">
              <td class="produto-nome">{{ produto.nome }}</td>
              <td>
                <span class="tipo-badge" :class="`tipo-${produto.tipo.toLowerCase()}`">
                  {{ produto.tipo }}
                </span>
              </td>

              <td>{{ formatCurrency(produto.preco_kg) }}</td>
              <td class="actions">
                <button @click="openModal(produto)" class="btn btn-sm btn-outline" title="Editar">
                  ✏️
                </button>
                <button @click="confirmDelete(produto)" class="btn btn-sm btn-danger" title="Excluir">
                  🗑️
                </button>
                <button @click="abrirModalAtualizarPreco(produto)" class="btn btn-sm btn-primary" title="Atualizar Preço">
                  💰
                </button>
                <button @click="abrirModalHistorico(produto)" class="btn btn-sm btn-info" title="Histórico">
                  📋
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal de criação/edição -->
    <div v-if="showModal" class="modal-overlay">
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h3>{{ modalTitle }}</h3>
          <button @click="closeModal" class="modal-close">&times;</button>
        </div>
        
        <form @submit.prevent="saveProduto" class="modal-body">
          <!-- Seção de Cadastro de Produto -->
          <div class="produto-details-section">
            <h4 class="section-title">Cadastro de Produto</h4>
            
            <div class="form-grid">
              <div class="form-group">
                <label for="nome">Nome do Produto *</label>
                <input 
                  id="nome" 
                  v-model="form.nome" 
                  type="text" 
                  class="form-input"
                  :class="{ 'error': formErrors.nome }"
                  placeholder="Ex: PEITO DE FRANGO"
                  @input="convertToUppercase"
                  style="text-transform: uppercase;"
                >
                <span v-if="formErrors.nome" class="error-text">{{ formErrors.nome }}</span>
              </div>
              
              <div class="form-group">
                <label for="tipo">Tipo *</label>
                <select 
                  id="tipo" 
                  v-model="form.tipo" 
                  class="form-select"
                  :class="{ 'error': formErrors.tipo }"
                >
                  <option value="">Selecione o tipo</option>
                  <option value="Peito">Peito</option>
                  <option value="Coxa">Coxa</option>
                  <option value="Sobrecoxa">Sobrecoxa</option>
                  <option value="Asa">Asa</option>
                  <option value="Carcaça">Carcaça</option>
                  <option value="Miúdos">Miúdos</option>
                  <option value="Outros">Outros</option>
                </select>
                <span v-if="formErrors.tipo" class="error-text">{{ formErrors.tipo }}</span>
              </div>
              

              
              <div class="form-group">
                <label for="preco_kg">Preço por kg (R$) *</label>
                <input 
                  id="preco_kg" 
                  v-model.number="form.preco_kg" 
                  type="number" 
                  step="0.01" 
                  min="0.01" 
                  class="form-input"
                  :class="{ 'error': formErrors.preco_kg }"
                  placeholder="0.00"
                  @blur="formatPrecoInput"
                >
                <span v-if="formErrors.preco_kg" class="error-text">{{ formErrors.preco_kg }}</span>
              </div>
              
              <div class="form-group">
                <label for="unidade_origem">Unidade *</label>
                <select 
                  id="unidade_origem" 
                  v-model="form.unidade_origem" 
                  class="form-select"
                  :class="{ 'error': formErrors.unidade_origem }"
                >
                  <option value="">Selecione a unidade</option>
                  <option value="Unidade Belo Jardim">Unidade Belo Jardim</option>
                </select>
                <span v-if="formErrors.unidade_origem" class="error-text">{{ formErrors.unidade_origem }}</span>
              </div>
            </div>
          </div>
          
          <div class="modal-footer">
            <button type="button" @click="closeModal" class="btn btn-secondary">
              Cancelar
            </button>
            <button type="submit" class="btn btn-primary" :disabled="loading">
              {{ loading ? 'Salvando...' : (isEditing ? 'Atualizar' : 'Criar') }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal de confirmação de exclusão -->
    <div v-if="showDeleteConfirm" class="modal-overlay">
      <div class="modal modal-sm" @click.stop>
        <div class="modal-header">
          <h3>Confirmar Exclusão</h3>
        </div>
        
        <div class="modal-body">
          <p>Tem certeza que deseja excluir o produto:</p>
          <p class="delete-item">{{ produtoToDelete?.nome }}</p>
          <p class="warning-text">Esta ação não pode ser desfeita.</p>
        </div>
        
        <div class="modal-footer">
          <button @click="cancelDelete" class="btn btn-secondary">
            Cancelar
          </button>
          <button @click="deleteProdutoConfirmed" class="btn btn-danger" :disabled="loading">
            {{ loading ? 'Excluindo...' : 'Excluir' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Modal de Atualizar Preço -->
    <ModalAtualizarPreco
      :is-visible="showModalAtualizarPreco"
      :produto="produtoSelecionado"
      @close="fecharModalAtualizarPreco"
      @preco-atualizado="onPrecoAtualizado"
    />

    <!-- Modal de Histórico do Produto -->
    <ModalHistoricoProduto
      :is-visible="showModalHistorico"
      :produto="produtoSelecionado"
      @close="fecharModalHistorico"
    />
  </div>
</template>

<style scoped>
@import url('../styles/colors.css');

.produtos-container {
  width: 100%;
  padding: 2rem;
  background: var(--bg-primary);
  min-height: 100vh;
  color: var(--text-primary);
  border-left: 4px solid var(--primary-red);
  border-right: 4px solid var(--primary-red);
}

.export-actions {
  display: flex;
  gap: 0.5rem;
  margin: 1rem 0;
  justify-content: flex-end;
}

/* Estilos do header removidos - usando common-headers.css */

/* Estilos removidos - usando BuscaAvancada */

.table-info {
  padding: 1.25rem 1.5rem;
  background: linear-gradient(135deg, var(--bg-accent) 0%, rgba(220, 38, 38, 0.05) 100%);
  border-bottom: 3px solid var(--primary-red);
  box-shadow: 0 2px 8px rgba(220, 38, 38, 0.15);
}

.table-header h3 {
  margin: 0;
  color: var(--primary-red);
  font-size: 1.1rem;
  font-weight: 700;
  text-shadow: 0 1px 2px rgba(220, 38, 38, 0.3);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.produtos-table-container {
  background: var(--bg-secondary);
  border-radius: 16px;
  overflow: hidden;
  box-shadow: var(--shadow-light);
  border: 2px solid var(--border-light);
  border-top: 4px solid var(--primary-red);
  margin-bottom: 2rem;
}

.table-wrapper {
  overflow-x: auto;
  scrollbar-width: thin;
  scrollbar-color: var(--primary-red) var(--bg-accent);
}

.table-wrapper::-webkit-scrollbar {
  height: 8px;
}

.table-wrapper::-webkit-scrollbar-track {
  background: var(--bg-accent);
  border-radius: 4px;
}

.table-wrapper::-webkit-scrollbar-thumb {
  background: var(--primary-red);
  border-radius: 4px;
}

.produtos-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  min-width: 800px;
}

.produtos-table th {
  background: linear-gradient(135deg, var(--bg-accent) 0%, rgba(220, 38, 38, 0.05) 100%);
  color: var(--text-primary);
  font-weight: 700;
  padding: 1rem 1.25rem;
  text-align: left;
  border-bottom: 3px solid var(--primary-red);
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.75px;
  position: sticky;
  top: 0;
  z-index: 10;
  white-space: nowrap;
}

.produtos-table th:first-child {
  border-top-left-radius: 12px;
}

.produtos-table th:last-child {
  border-top-right-radius: 12px;
}

.produtos-table td {
  padding: 1rem 1.25rem;
  border-bottom: 1px solid var(--border-light);
  color: var(--text-primary);
  vertical-align: middle;
  font-size: 0.9rem;
  line-height: 1.5;
}

.produto-row {
  transition: all 0.3s ease;
}

.produto-row:hover {
  background: linear-gradient(135deg, var(--bg-accent) 0%, rgba(220, 38, 38, 0.02) 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.produto-row:last-child td:first-child {
  border-bottom-left-radius: 12px;
}

.produto-row:last-child td:last-child {
  border-bottom-right-radius: 12px;
}

.produto-nome {
  font-weight: 700;
  color: var(--text-primary);
  font-size: 1rem;
  line-height: 1.4;
}

.tipo-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem 1rem;
  border-radius: 25px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.75px;
  min-width: 80px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.tipo-badge:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.tipo-peito { background: rgba(59, 130, 246, 0.1); color: #3B82F6; }
.tipo-coxa { background: rgba(16, 185, 129, 0.1); color: #10B981; }
.tipo-sobrecoxa { background: rgba(245, 158, 11, 0.1); color: #F59E0B; }
.tipo-asa { background: rgba(139, 92, 246, 0.1); color: #8B5CF6; }
.tipo-carcaça { background: rgba(239, 68, 68, 0.1); color: #EF4444; }
.tipo-miúdos { background: rgba(236, 72, 153, 0.1); color: #EC4899; }
.tipo-outros { background: rgba(107, 114, 128, 0.1); color: #6B7280; }

.valor-total {
  font-weight: 700;
  color: var(--primary-red);
}

.actions {
  display: flex;
  gap: 0.75rem;
  align-items: center;
  justify-content: flex-start;
  flex-wrap: wrap;
}

.actions .btn {
  min-width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  font-size: 1.1rem;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.actions .btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.no-data {
  text-align: center;
  color: var(--text-secondary);
  font-style: italic;
  padding: 4rem 2rem;
  font-size: 1.1rem;
  line-height: 1.6;
  background: linear-gradient(135deg, var(--bg-accent) 0%, rgba(107, 114, 128, 0.05) 100%);
  border-radius: 12px;
  margin: 1rem;
}

/* Botões */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
  justify-content: center;
}

.btn-sm {
  padding: 0.5rem 1rem;
  font-size: 0.75rem;
}

.btn-primary {
  background: var(--gradient-primary);
  color: white;
  border: none;
  box-shadow: var(--shadow-medium);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-heavy);
}

.btn-secondary {
  background: var(--bg-accent);
  color: var(--text-primary);
  border: 1px solid var(--border-light);
}

.btn-secondary:hover {
  background: var(--border-light);
}

.btn-outline {
  background: transparent;
  color: var(--text-secondary);
  border: 1px solid var(--border-light);
}

.btn-outline:hover {
  background: var(--bg-accent);
  color: var(--text-primary);
}

.btn-danger {
  background: #EF4444;
  color: white;
}

.btn-danger:hover {
  background: #DC2626;
}

.btn-info {
  background-color: #06b6d4;
  color: white;
}

.btn-info:hover:not(:disabled) {
  background-color: #0891b2;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.btn-icon {
  font-size: 1.2rem;
  font-weight: 700;
  filter: drop-shadow(0 0 2px rgba(220, 38, 38, 0.5));
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
  animation: fadeIn 0.3s ease;
  padding: 1rem;
}

.modal {
  background: var(--bg-primary);
  border-radius: 16px;
  box-shadow: var(--shadow-heavy);
  border: 1px solid var(--border-light);
  animation: slideUp 0.3s ease;
  width: 100%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-sm {
  max-width: 400px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid var(--border-light);
}

.modal-header h3 {
  margin: 0;
  color: var(--text-primary);
  font-size: 1.25rem;
  font-weight: 700;
}

.modal-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: var(--text-secondary);
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.modal-close:hover {
  background: var(--bg-accent);
  color: var(--text-primary);
}

.modal-body {
  padding: 1.5rem;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding: 1.5rem;
  border-top: 1px solid var(--border-light);
}

/* Seções do formulário de produtos */
.produto-details-section {
  margin-top: 20px;
  padding: 25px;
  background: var(--bg-secondary);
  border-radius: 12px;
  border: 2px solid var(--border-light);
  box-shadow: var(--shadow-light);
}

.section-title {
  color: var(--primary-red);
  font-size: 1.3rem;
  font-weight: 700;
  margin: 0 0 25px 0;
  padding-bottom: 10px;
  border-bottom: 2px solid var(--primary-red);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.subsection-title {
  color: var(--text-primary);
  font-size: 1.1rem;
  font-weight: 600;
  margin: 20px 0 15px 0;
  padding: 10px 15px;
  background: var(--bg-accent);
  border-radius: 8px;
  border-left: 4px solid var(--primary-red);
}

.basic-info-section,
.commercial-section,
.notes-section {
  margin-bottom: 25px;
}

/* Formulário */
.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

.form-group label {
  font-weight: 600;
  color: var(--text-secondary);
  font-size: 0.875rem;
}

.form-input,
.form-select,
.form-textarea {
  padding: 0.75rem;
  border: 1px solid var(--border-light);
  border-radius: 8px;
  background: var(--bg-primary);
  color: var(--text-primary);
  font-size: 0.875rem;
  transition: all 0.3s ease;
}

.form-input:focus,
.form-select:focus,
.form-textarea:focus {
  outline: none;
  border-color: var(--primary-red);
  border-width: 2px;
  box-shadow: 0 0 10px rgba(220, 38, 38, 0.3);
}

.form-input.error,
.form-select.error,
.form-textarea.error {
  border-color: #EF4444;
}

.form-input.calculated {
  background: var(--bg-tertiary) !important;
  color: var(--success) !important;
  font-weight: 600;
  cursor: not-allowed;
}

.calculated-field {
  background: var(--bg-accent);
  border-radius: 8px;
  padding: 15px;
  border: 2px solid var(--success);
}

.form-textarea {
  resize: vertical;
  min-height: 80px;
}

.error-text {
  color: #EF4444;
  font-size: 0.75rem;
  font-weight: 500;
}

.error-message {
  background: rgba(239, 68, 68, 0.1);
  color: #EF4444;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.loading {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  background: #ffffff;
}

.loading-logo {
  width: 140px;
  height: 140px;
  object-fit: contain;
  animation: pulse 1s ease-in-out infinite;
}

@keyframes pulse {
  0% { transform: scale(1); opacity: 0.9; }
  50% { transform: scale(1.05); opacity: 1; }
  100% { transform: scale(1); opacity: 0.9; }
}

.delete-item {
  font-weight: 700;
  color: var(--primary-red);
  margin: 1rem 0;
  padding: 0.5rem;
  background: rgba(220, 38, 38, 0.1);
  border-radius: 4px;
  text-align: center;
}

.warning-text {
  color: var(--text-secondary);
  font-size: 0.875rem;
  text-align: center;
  margin-top: 1rem;
}

/* Responsividade */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from { 
    opacity: 0;
    transform: translateY(30px) scale(0.95);
  }
  to { 
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@media (max-width: 1024px) {
  .form-grid {
    grid-template-columns: 1fr 1fr;
  }
  
  .form-group.full-width {
    grid-column: 1 / -1;
  }
}

@media (max-width: 640px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .form-group.full-width {
    grid-column: 1;
  }
  
  .section-title {
    font-size: 1.1rem;
  }
  
  .subsection-title {
    font-size: 1rem;
    padding: 8px 12px;
  }
}

@media (max-width: 768px) {
  .header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .table-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .table-header h3 {
    font-size: 16px;
  }
  
  .produtos-table th,
  .produtos-table td {
    padding: 0.75rem 0.5rem;
    font-size: 0.75rem;
  }
  
  .modal {
    margin: 1rem;
    max-width: calc(100vw - 2rem);
    max-height: calc(100vh - 2rem);
  }
  
  .modal-body {
    max-height: calc(100vh - 200px);
    overflow-y: auto;
  }
  
  .form-input,
  .form-select {
    padding: 0.875rem;
    font-size: 1rem;
  }
}

@media (max-width: 480px) {
  .produtos-container {
    padding: 1rem;
  }
  
  /* Estilo do título removido - usando common-headers.css */
  
  .actions {
    flex-direction: column;
    gap: 0.25rem;
  }
  
  .btn-sm {
    padding: 0.375rem 0.75rem;
    font-size: 0.7rem;
  }
  
  .modal {
    margin: 0.5rem;
    max-width: calc(100vw - 1rem);
    max-height: calc(100vh - 1rem);
  }
  
  .modal-header {
    padding: 1rem;
  }
  
  .modal-header h3 {
    font-size: 1.25rem;
  }
  
  .form-input,
  .form-select {
    padding: 1rem;
    font-size: 1rem;
    border-radius: 12px;
  }
  
  .modal-footer {
    padding: 1rem;
    gap: 0.75rem;
  }
  
  .modal-footer .btn {
    padding: 0.875rem 1.5rem;
    font-size: 1rem;
    border-radius: 12px;
  }
}

@media (max-width: 320px) {
  .modal {
    margin: 0.25rem;
    max-width: calc(100vw - 0.5rem);
    max-height: calc(100vh - 0.5rem);
  }
  
  .modal-header,
  .modal-footer {
    padding: 0.75rem;
  }
  
  .modal-header h3 {
    font-size: 1.125rem;
  }
  
  .form-grid {
    gap: 0.75rem;
  }
  
  .form-input,
  .form-select {
    padding: 0.875rem;
    font-size: 0.9rem;
  }
  
  .section-title {
    font-size: 1rem;
    margin-bottom: 0.75rem;
  }
  
  .modal-footer .btn {
    padding: 0.75rem 1.25rem;
    font-size: 0.9rem;
  }
  
  .produtos-table {
    font-size: 0.7rem;
  }
  
  .produtos-table th,
  .produtos-table td {
    padding: 0.5rem 0.25rem;
  }
}
</style>