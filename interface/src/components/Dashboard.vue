<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { getLotesAbate, getProdutos, type LoteAbate, type Produto } from '../services/api'
import { exportToCSV, exportToPDF, formatDate, formatCurrency, formatWeight, type ExportColumn } from '../utils/exportUtils'

const loading = ref(false)
const error = ref('')
const lotes = ref<LoteAbate[]>([])
const produtos = ref<Produto[]>([])

// Filtros de data
const filtros = ref({
  dataInicio: '',
  dataFim: ''
})

// Dados filtrados por data
const dadosFiltrados = computed(() => {
  const lotesFiltrados = lotes.value.filter(lote => {
    if (!filtros.value.dataInicio && !filtros.value.dataFim) return true
    
    const dataLote = new Date(lote.data_abate)
    const dataInicio = filtros.value.dataInicio ? new Date(filtros.value.dataInicio) : null
    const dataFim = filtros.value.dataFim ? new Date(filtros.value.dataFim) : null
    
    if (dataInicio && dataLote < dataInicio) return false
    if (dataFim && dataLote > dataFim) return false
    
    return true
  })
  
  const produtosFiltrados = produtos.value.filter(produto => {
    if (!filtros.value.dataInicio && !filtros.value.dataFim) return true
    
    const dataProduto = new Date(produto.data_producao || produto.created_at)
    const dataInicio = filtros.value.dataInicio ? new Date(filtros.value.dataInicio) : null
    const dataFim = filtros.value.dataFim ? new Date(filtros.value.dataFim) : null
    
    if (dataInicio && dataProduto < dataInicio) return false
    if (dataFim && dataProduto > dataFim) return false
    
    return true
  })
  
  return { lotesFiltrados, produtosFiltrados }
})

// Métricas zeradas para desenvolvimento
const metricas = computed(() => {
  return {
    totalLotes: 0,
    totalProdutos: 0,
    totalAves: 0,
    frangosCorte: 0,
    galinhasPoedeiras: 0,
    pesoTotalLotes: 0,
    pesoTotalProdutos: 0,
    valorTotalProdutos: 0,
    custoTotalAves: 0,
    custoAbatePorKg: 0,
    lucroPorAve: 0,
    lucroTotal: 0,
    rendimentoAbate: 0,
    mediaAvesPorLote: 0,
    mediaPesoPorLote: 0,
    precoMedioKg: 0
  }
})

// Distribuição por unidade removida conforme solicitado

// Distribuição zerada para desenvolvimento
const distribuicaoTiposAve = computed(() => {
  return []
})

// Distribuição zerada para desenvolvimento
const distribuicaoTiposProduto = computed(() => {
  return []
})

// Listas zeradas para desenvolvimento
const lotesRecentes = computed(() => {
  return []
})

const produtosMaisValiosos = computed(() => {
  return []
})

// Métodos - dados zerados para desenvolvimento
const loadData = async () => {
  try {
    loading.value = true
    error.value = ''
    
    // Simular carregamento sem fazer chamadas ao backend
    await new Promise(resolve => setTimeout(resolve, 500))
    
    // Zerar todos os dados
    lotes.value = []
    produtos.value = []
  } catch (err) {
    error.value = 'Erro ao carregar dados do dashboard'
    console.error('Erro ao carregar dados:', err)
  } finally {
    loading.value = false
  }
}

const formatCurrency = (value: number): string => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(value)
}

const formatWeight = (value: number): string => {
  return `${value.toFixed(2)} kg`
}

const formatNumber = (value: number): string => {
  return new Intl.NumberFormat('pt-BR').format(Math.round(value))
}

const formatDate = (dateString: string): string => {
  return new Date(dateString).toLocaleDateString('pt-BR')
}

const formatPercentage = (value: number): string => {
  return `${value.toFixed(1)}%`
}

// Funções de exportação
const exportarDashboard = (formato: 'csv' | 'pdf') => {
  const resumoData = [
    {
      categoria: 'Abates',
      total: metricas.value.totalLotes,
      valor: formatCurrency(metricas.value.valorTotalProdutos),
      detalhes: `${metricas.value.totalAves} aves, ${formatWeight(metricas.value.pesoTotalLotes)}`
    },
    {
      categoria: 'Produtos',
      total: metricas.value.totalProdutos,
      valor: formatCurrency(metricas.value.valorTotalProdutos),
      detalhes: `${formatWeight(metricas.value.pesoTotalProdutos)}`
    }
  ]

  const columns: ExportColumn[] = [
    { key: 'categoria', label: 'Categoria' },
    { key: 'total', label: 'Total' },
    { key: 'valor', label: 'Valor Total' },
    { key: 'detalhes', label: 'Detalhes' }
  ]

  const options = {
    filename: 'dashboard-resumo',
    title: 'Dashboard - Resumo Geral',
    subtitle: `Dados consolidados do sistema em ${formatDate(new Date())}`,
    columns,
    data: resumoData
  }

  if (formato === 'csv') {
    exportToCSV(options)
  } else {
    exportToPDF(options)
  }
}

// Inicializar datas padrão
const inicializarDatas = () => {
  const hoje = new Date()
  filtros.value.dataFim = hoje.toISOString().split('T')[0]
  filtros.value.dataInicio = hoje.toISOString().split('T')[0]
}

// Aplicar filtros de data
const aplicarFiltros = () => {
  loadData()
}

// Limpar filtros
const limparFiltros = () => {
  inicializarDatas()
  loadData()
}

// Lifecycle
onMounted(() => {
  inicializarDatas()
  loadData()
})
</script>

<template>
  <div class="dashboard-container">
    <div class="dashboard-header">
      <div class="header-content">
        <div>
          <h2 class="dashboard-title">Dashboard</h2>
          <p class="dashboard-subtitle">Visão geral do sistema</p>
        </div>
        <div class="header-actions">
          <button @click="loadData" class="btn btn-secondary btn-sm" :disabled="loading">
            <span class="btn-icon">🔄</span>
            {{ loading ? 'Atualizando...' : 'Atualizar' }}
          </button>
          <div class="export-actions">
            <button @click="exportarDashboard('csv')" class="btn btn-secondary btn-sm">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                <polyline points="14,2 14,8 20,8"/>
                <line x1="16" y1="13" x2="8" y2="13"/>
                <line x1="16" y1="17" x2="8" y2="17"/>
                <polyline points="10,9 9,9 8,9"/>
              </svg>
              Exportar CSV
            </button>
            <button @click="exportarDashboard('pdf')" class="btn btn-primary btn-sm">
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
        </div>
      </div>
    </div>

    <!-- Aviso de Desenvolvimento -->
    <div class="development-notice">
      <div class="notice-icon">🚧</div>
      <div class="notice-content">
        <h4 class="notice-title">Funcionalidades em Desenvolvimento</h4>
        <p class="notice-message">
          Esta página está em desenvolvimento. Todos os dados estão temporariamente zerados enquanto implementamos as funcionalidades completas do sistema.
        </p>
      </div>
    </div>

    <!-- Filtros de Data -->
    <section class="filters-section">
      <h3 class="section-title">Filtros por Data</h3>
      <div class="filters-grid">
        <div class="filter-group">
          <label class="filter-label">Data Início</label>
          <input 
            v-model="filtros.dataInicio" 
            type="date" 
            class="filter-input"
            @change="aplicarFiltros"
          />
        </div>
        
        <div class="filter-group">
          <label class="filter-label">Data Fim</label>
          <input 
            v-model="filtros.dataFim" 
            type="date" 
            class="filter-input"
            @change="aplicarFiltros"
          />
        </div>
        
        <div class="filter-actions">
          <button @click="aplicarFiltros" class="btn btn-primary btn-sm">
            <span class="btn-icon">🔍</span>
            Aplicar Filtros
          </button>
          <button @click="limparFiltros" class="btn btn-secondary btn-sm">
            <span class="btn-icon">🗑️</span>
            Limpar
          </button>
        </div>
      </div>
    </section>

    <!-- Mensagem de erro -->
    <div v-if="error" class="error-message">
      {{ error }}
    </div>

    <!-- Loading -->
    <div v-if="loading" class="loading">
      Carregando dados do dashboard...
    </div>

    <!-- Dashboard Content -->
    <div v-else class="dashboard-content">
      <!-- Cards de Métricas Principais -->
      <section class="metrics-section">
        <h3 class="section-title">Métricas do Abatedouro</h3>
        <div class="metrics-grid">
          <div class="metric-card primary">
            <div class="metric-icon">🐔</div>
            <div class="metric-content">
              <div class="metric-value">{{ formatNumber(metricas.frangosCorte) }}</div>
              <div class="metric-label">Frango de Corte</div>
            </div>
          </div>
          
          <div class="metric-card success">
            <div class="metric-icon">🥚</div>
            <div class="metric-content">
              <div class="metric-value">{{ formatNumber(metricas.galinhasPoedeiras) }}</div>
              <div class="metric-label">Galinha Poedeira</div>
            </div>
          </div>
          
          <div class="metric-card warning">
            <div class="metric-icon">💰</div>
            <div class="metric-content">
              <div class="metric-value">{{ formatCurrency(metricas.custoTotalAves) }}</div>
              <div class="metric-label">Custo Total Aves Vivas</div>
            </div>
          </div>
          
          <div class="metric-card info">
            <div class="metric-icon">⚖️</div>
            <div class="metric-content">
              <div class="metric-value">{{ formatCurrency(metricas.custoAbatePorKg) }}</div>
              <div class="metric-label">Custo Abate por Kg</div>
            </div>
          </div>
          
          <div class="metric-card secondary">
            <div class="metric-icon">📈</div>
            <div class="metric-content">
              <div class="metric-value">{{ formatCurrency(metricas.lucroPorAve) }}</div>
              <div class="metric-label">Lucro por Ave</div>
            </div>
          </div>
          
          <div class="metric-card accent">
            <div class="metric-icon">💵</div>
            <div class="metric-content">
              <div class="metric-value">{{ formatCurrency(metricas.lucroTotal) }}</div>
              <div class="metric-label">Lucro Total</div>
            </div>
          </div>
          
          <div class="metric-card primary">
            <div class="metric-icon">📊</div>
            <div class="metric-content">
              <div class="metric-value">{{ formatPercentage(metricas.rendimentoAbate) }}</div>
              <div class="metric-label">Rendimento de Abate</div>
            </div>
          </div>
          
          <div class="metric-card success">
            <div class="metric-icon">⚖️</div>
            <div class="metric-content">
              <div class="metric-value">{{ formatWeight(metricas.pesoTotalProdutos) }}</div>
              <div class="metric-label">Peso Total Produtos</div>
            </div>
          </div>
        </div>
      </section>

      <!-- Custos e Despesas do Abatedouro -->
      <section class="costs-section">
        <h3 class="section-title">Custos e Despesas Operacionais</h3>
        <div class="costs-grid">
          <div class="cost-card">
            <div class="cost-header">
              <span class="cost-icon">🏭</span>
              <span class="cost-title">Mão de Obra</span>
            </div>
            <div class="cost-value">{{ formatCurrency(0.00) }}</div>
            <div class="cost-description">Custos com pessoal</div>
          </div>
          
          <div class="cost-card">
            <div class="cost-header">
              <span class="cost-icon">💧</span>
              <span class="cost-title">Água</span>
            </div>
            <div class="cost-value">{{ formatCurrency(0.00) }}</div>
            <div class="cost-description">Consumo de água</div>
          </div>
          
          <div class="cost-card">
            <div class="cost-header">
              <span class="cost-icon">⚡</span>
              <span class="cost-title">Energia</span>
            </div>
            <div class="cost-value">{{ formatCurrency(0.00) }}</div>
            <div class="cost-description">Energia elétrica</div>
          </div>
          
          <div class="cost-card">
            <div class="cost-header">
              <span class="cost-icon">📦</span>
              <span class="cost-title">Embalagem</span>
            </div>
            <div class="cost-value">{{ formatCurrency(0.00) }}</div>
            <div class="cost-description">Material de embalagem</div>
          </div>
          
          <div class="cost-card">
            <div class="cost-header">
              <span class="cost-icon">🧊</span>
              <span class="cost-title">Gelo</span>
            </div>
            <div class="cost-value">{{ formatCurrency(0.00) }}</div>
            <div class="cost-description">Refrigeração</div>
          </div>
          
          <div class="cost-card">
            <div class="cost-header">
              <span class="cost-icon">🔧</span>
              <span class="cost-title">Manutenção</span>
            </div>
            <div class="cost-value">{{ formatCurrency(0.00) }}</div>
            <div class="cost-description">Manutenção equipamentos</div>
          </div>
        </div>
      </section>

      <!-- Distribuições -->
      <div class="distributions-grid">
        <!-- Card de distribuição por unidade removido conforme solicitado -->

        <!-- Distribuição por Tipo de Ave -->
        <section class="distribution-section">
          <h3 class="section-title">Distribuição por Tipo de Ave</h3>
          <div class="distribution-list">
            <div v-for="tipo in distribuicaoTiposAve" :key="tipo.nome" class="distribution-item">
              <div class="distribution-header">
                <span class="distribution-name">{{ tipo.nome }}</span>
                <span class="distribution-percentage">{{ formatPercentage(tipo.percentualAves) }}</span>
              </div>
              <div class="distribution-bar">
                <div class="distribution-fill success" :style="{ width: tipo.percentualAves + '%' }"></div>
              </div>
              <div class="distribution-details">
                <span>{{ tipo.lotes }} lotes</span>
                <span>{{ formatNumber(tipo.aves) }} aves</span>
              </div>
            </div>
          </div>
        </section>

        <!-- Distribuição por Tipo de Produto -->
        <section class="distribution-section">
          <h3 class="section-title">Distribuição por Tipo de Produto</h3>
          <div class="distribution-list">
            <div v-for="tipo in distribuicaoTiposProduto" :key="tipo.nome" class="distribution-item">
              <div class="distribution-header">
                <span class="distribution-name">{{ tipo.nome }}</span>
                <span class="distribution-percentage">{{ formatPercentage(tipo.percentualValor) }}</span>
              </div>
              <div class="distribution-bar">
                <div class="distribution-fill warning" :style="{ width: tipo.percentualValor + '%' }"></div>
              </div>
              <div class="distribution-details">
                <span>{{ tipo.quantidade }} itens</span>
                <span>{{ formatWeight(tipo.peso) }}</span>
                <span>{{ formatCurrency(tipo.valor) }}</span>
              </div>
            </div>
          </div>
        </section>
      </div>

      <!-- Listas Recentes -->
      <div class="recent-lists-grid">
        <!-- Lotes Recentes -->
        <section class="recent-section">
          <h3 class="section-title">Lotes Recentes</h3>
          <div class="recent-list">
            <div v-if="lotesRecentes.length === 0" class="no-data">
              Nenhum lote encontrado
            </div>
            <div v-for="lote in lotesRecentes" :key="lote.id" class="recent-item">
              <div class="recent-main">
                <div class="recent-title">{{ formatDate(lote.data_abate) }}</div>
                <div class="recent-subtitle">{{ lote.unidade }}</div>
              </div>
              <div class="recent-details">
                <span class="recent-value">{{ formatNumber(lote.quantidade_aves) }} aves</span>
                <span class="recent-value">{{ formatWeight(lote.peso_total_kg) }}</span>
              </div>
            </div>
          </div>
        </section>

        <!-- Produtos Mais Valiosos -->
        <section class="recent-section">
          <h3 class="section-title">Produtos Mais Valiosos</h3>
          <div class="recent-list">
            <div v-if="produtosMaisValiosos.length === 0" class="no-data">
              Nenhum produto encontrado
            </div>
            <div v-for="produto in produtosMaisValiosos" :key="produto._id" class="recent-item">
              <div class="recent-main">
                <div class="recent-title">{{ produto.nome }}</div>
                <div class="recent-subtitle">{{ produto.tipo }} - {{ produto.unidade_origem }}</div>
              </div>
              <div class="recent-details">
                <span class="recent-value">{{ formatWeight(produto.peso_kg) }}</span>
                <span class="recent-value primary">{{ formatCurrency(produto.peso_kg * produto.preco_kg) }}</span>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('../styles/colors.css');

.dashboard-container {
  max-width: 100%;
  margin: 0 auto;
  padding: 0;
}

.dashboard-header {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: var(--bg-secondary);
  border-radius: 16px;
  box-shadow: var(--shadow-light);
  border: 1px solid var(--border-light);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 2rem;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.export-actions {
  display: flex;
  gap: 0.5rem;
}

.dashboard-subtitle {
  color: var(--text-secondary);
  margin: 0.5rem 0 0 0;
  font-size: 0.875rem;
}

.dashboard-title {
  font-size: 2rem;
  font-weight: 700;
  margin: 0;
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.dashboard-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

/* Seções */
.section-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--border-light);
}

/* Métricas */
.metrics-section {
  background: var(--bg-secondary);
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: var(--shadow-light);
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.metric-card {
  background: var(--bg-primary);
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: var(--shadow-light);
  border: 2px solid var(--border-light);
  border-left: 4px solid var(--primary-red);
  transition: all 0.3s ease;
}

.metric-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-medium);
  border-left-color: var(--accent-red);
  border-left-width: 6px;
}

.metric-icon {
  font-size: 2rem;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  background: var(--bg-accent);
}

.metric-card.primary .metric-icon { background: rgba(220, 38, 38, 0.1); }
.metric-card.success .metric-icon { background: rgba(16, 185, 129, 0.1); }
.metric-card.warning .metric-icon { background: rgba(245, 158, 11, 0.1); }
.metric-card.info .metric-icon { background: rgba(59, 130, 246, 0.1); }
.metric-card.secondary .metric-icon { background: rgba(107, 114, 128, 0.1); }
.metric-card.accent .metric-icon { background: rgba(139, 92, 246, 0.1); }

.metric-content {
  flex: 1;
}

.metric-value {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1;
  margin-bottom: 0.25rem;
}

.metric-label {
  font-size: 0.875rem;
  color: var(--text-secondary);
  font-weight: 500;
}

/* Custos e Despesas */
.costs-section {
  background: var(--bg-secondary);
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: var(--shadow-light);
  border: 2px solid var(--border-light);
  border-top: 4px solid var(--primary-red);
}

.costs-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.cost-card {
  background: var(--bg-primary);
  border-radius: 8px;
  padding: 1.25rem;
  border: 1px solid var(--border-light);
  transition: all 0.3s ease;
  border-left: 3px solid var(--primary-red);
}

.cost-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-medium);
  border-left-color: var(--accent-red);
  border-left-width: 4px;
}

.cost-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
}

.cost-icon {
  font-size: 1.5rem;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(220, 38, 38, 0.1);
  border-radius: 8px;
}

.cost-title {
  font-weight: 600;
  color: var(--text-primary);
  font-size: 0.875rem;
}

.cost-value {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--primary-red);
  margin-bottom: 0.25rem;
}

.cost-description {
  font-size: 0.75rem;
  color: var(--text-secondary);
}

/* Distribuições */
.distributions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.distribution-section {
  background: var(--bg-secondary);
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: var(--shadow-light);
  border: 2px solid var(--border-light);
  border-top: 4px solid var(--primary-red);
}

.distribution-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.distribution-item {
  background: var(--bg-primary);
  border-radius: 8px;
  padding: 1rem;
  border: 1px solid var(--border-light);
}

.distribution-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.distribution-name {
  font-weight: 600;
  color: var(--text-primary);
}

.distribution-percentage {
  font-weight: 700;
  color: var(--primary-red);
  font-size: 0.875rem;
}

.distribution-bar {
  height: 6px;
  background: var(--bg-accent);
  border-radius: 3px;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.distribution-fill {
  height: 100%;
  background: var(--primary-red);
  border-radius: 3px;
  transition: width 0.3s ease;
}

.distribution-fill.success { background: #10B981; }
.distribution-fill.warning { background: #F59E0B; }

.distribution-details {
  display: flex;
  gap: 1rem;
  font-size: 0.75rem;
  color: var(--text-secondary);
}

/* Listas Recentes */
.recent-lists-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 1.5rem;
}

.recent-section {
  background: var(--bg-secondary);
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: var(--shadow-light);
}

.recent-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.recent-item {
  background: var(--bg-primary);
  border-radius: 8px;
  padding: 1rem;
  border: 1px solid var(--border-light);
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.3s ease;
}

.recent-item:hover {
  background: var(--bg-accent);
}

.recent-main {
  flex: 1;
}

.recent-title {
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.25rem;
}

.recent-subtitle {
  font-size: 0.75rem;
  color: var(--text-secondary);
}

.recent-details {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.25rem;
}

.recent-value {
  font-size: 0.75rem;
  color: var(--text-secondary);
  font-weight: 500;
}

.recent-value.primary {
  color: var(--primary-red);
  font-weight: 700;
  font-size: 0.875rem;
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

.btn-sm {
  padding: 0.5rem 1rem;
  font-size: 0.75rem;
}

.btn-secondary {
  background: var(--bg-accent);
  color: var(--text-primary);
  border: 1px solid var(--border-light);
}

.btn-secondary:hover {
  background: var(--border-light);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.btn-icon {
  font-size: 1rem;
}

/* Estados */
.error-message {
  background: rgba(239, 68, 68, 0.1);
  color: #EF4444;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.loading {
  text-align: center;
  padding: 3rem;
  color: var(--text-secondary);
  font-size: 1.1rem;
}

.no-data {
  text-align: center;
  color: var(--text-secondary);
  font-style: italic;
  padding: 2rem;
}

/* Responsividade */
@media (max-width: 1024px) {
  .metrics-grid {
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  }
  
  .distributions-grid,
  .recent-lists-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .dashboard-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .metrics-grid {
    grid-template-columns: 1fr;
  }
  
  .metric-card {
    padding: 1rem;
  }
  
  .metric-icon {
    width: 50px;
    height: 50px;
    font-size: 1.5rem;
  }
  
  .metric-value {
    font-size: 1.5rem;
  }
}

@media (max-width: 480px) {
  .dashboard-container {
    padding: 0.5rem;
  }
  
  .dashboard-title {
    font-size: 1.5rem;
  }
  
  .recent-item {
    flex-direction: column;
    align-items: stretch;
    gap: 0.5rem;
  }
  
  .recent-details {
    flex-direction: row;
    justify-content: space-between;
  }
}

/* Filtros */
.filters-section {
  background: var(--bg-secondary);
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  box-shadow: var(--shadow-light);
  border: 2px solid var(--border-light);
}

.filters-grid {
  display: grid;
  grid-template-columns: 1fr 1fr auto;
  gap: 1rem;
  align-items: end;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filter-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-primary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.filter-input {
  padding: 0.75rem;
  border: 2px solid var(--border-medium);
  border-radius: 8px;
  background: var(--bg-primary);
  color: var(--text-primary);
  font-size: 0.875rem;
  transition: all 0.3s ease;
}

.filter-input:focus {
  outline: none;
  border-color: var(--primary-red);
  box-shadow: 0 0 0 3px rgba(220, 38, 38, 0.1);
}

.filter-actions {
  display: flex;
  gap: 0.5rem;
  align-items: flex-end;
}

@media (max-width: 768px) {
  .filters-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .filter-actions {
    justify-content: center;
  }
}

/* Aviso de Desenvolvimento */
.development-notice {
  background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
  border: 2px solid #F59E0B;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.notice-icon {
  font-size: 2rem;
  flex-shrink: 0;
}

.notice-content {
  flex: 1;
}

.notice-title {
  color: #92400E;
  font-size: 1.125rem;
  font-weight: 700;
  margin: 0 0 0.5rem 0;
}

.notice-message {
  color: #78350F;
  font-size: 0.875rem;
  line-height: 1.5;
  margin: 0;
}

@media (max-width: 768px) {
  .development-notice {
    flex-direction: column;
    text-align: center;
    gap: 0.75rem;
  }
  
  .notice-icon {
    font-size: 1.5rem;
  }
}
</style>