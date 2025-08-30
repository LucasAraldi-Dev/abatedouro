<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { getLotesAbate, getProdutos, type LoteAbate, type Produto } from '../services/api'

const loading = ref(false)
const error = ref('')
const lotes = ref<LoteAbate[]>([])
const produtos = ref<Produto[]>([])

// Filtros
const filtros = ref({
  dataInicio: '',
  dataFim: '',
  unidade: '',
  tipoRelatorio: 'lotes' // 'lotes', 'produtos', 'resumo'
})

// Opções para filtros
const unidadesDisponiveis = computed(() => {
  const unidades = new Set<string>()
  lotes.value.forEach(lote => unidades.add(lote.unidade))
  produtos.value.forEach(produto => unidades.add(produto.unidade_origem))
  return Array.from(unidades).sort()
})

// Dados filtrados
const lotesFiltrados = computed(() => {
  return lotes.value.filter(lote => {
    // Filtro por data
    if (filtros.value.dataInicio) {
      const dataLote = new Date(lote.data_abate)
      const dataInicio = new Date(filtros.value.dataInicio)
      if (dataLote < dataInicio) return false
    }
    
    if (filtros.value.dataFim) {
      const dataLote = new Date(lote.data_abate)
      const dataFim = new Date(filtros.value.dataFim)
      if (dataLote > dataFim) return false
    }
    
    // Filtro por unidade
    if (filtros.value.unidade && lote.unidade !== filtros.value.unidade) {
      return false
    }
    
    return true
  })
})

const produtosFiltrados = computed(() => {
  return produtos.value.filter(produto => {
    // Filtro por data (usando data_producao)
    if (filtros.value.dataInicio) {
      const dataProduto = new Date(produto.data_producao)
      const dataInicio = new Date(filtros.value.dataInicio)
      if (dataProduto < dataInicio) return false
    }
    
    if (filtros.value.dataFim) {
      const dataProduto = new Date(produto.data_producao)
      const dataFim = new Date(filtros.value.dataFim)
      if (dataProduto > dataFim) return false
    }
    
    // Filtro por unidade
    if (filtros.value.unidade && produto.unidade_origem !== filtros.value.unidade) {
      return false
    }
    
    return true
  })
})

// Relatório de resumo
const relatorioResumo = computed(() => {
  const lotesPorUnidade = new Map<string, {
    totalLotes: number
    totalAves: number
    pesoTotal: number
    produtos: number
    valorProdutos: number
  }>()
  
  // Processar lotes
  lotesFiltrados.value.forEach(lote => {
    if (!lotesPorUnidade.has(lote.unidade)) {
      lotesPorUnidade.set(lote.unidade, {
        totalLotes: 0,
        totalAves: 0,
        pesoTotal: 0,
        produtos: 0,
        valorProdutos: 0
      })
    }
    
    const dados = lotesPorUnidade.get(lote.unidade)!
    dados.totalLotes++
    dados.totalAves += lote.quantidade_aves
    dados.pesoTotal += lote.peso_total_kg
  })
  
  // Processar produtos
  produtosFiltrados.value.forEach(produto => {
    if (!lotesPorUnidade.has(produto.unidade_origem)) {
      lotesPorUnidade.set(produto.unidade_origem, {
        totalLotes: 0,
        totalAves: 0,
        pesoTotal: 0,
        produtos: 0,
        valorProdutos: 0
      })
    }
    
    const dados = lotesPorUnidade.get(produto.unidade_origem)!
    dados.produtos++
    dados.valorProdutos += produto.peso_kg * produto.preco_kg
  })
  
  return Array.from(lotesPorUnidade.entries()).map(([unidade, dados]) => ({
    unidade,
    ...dados,
    mediaAvesPorLote: dados.totalLotes > 0 ? dados.totalAves / dados.totalLotes : 0,
    mediaPesoPorLote: dados.totalLotes > 0 ? dados.pesoTotal / dados.totalLotes : 0,
    valorMedioPorProduto: dados.produtos > 0 ? dados.valorProdutos / dados.produtos : 0
  }))
})

// Totais gerais
const totaisGerais = computed(() => {
  const totalLotes = lotesFiltrados.value.length
  const totalProdutos = produtosFiltrados.value.length
  const totalAves = lotesFiltrados.value.reduce((sum, lote) => sum + lote.quantidade_aves, 0)
  const pesoTotalLotes = lotesFiltrados.value.reduce((sum, lote) => sum + lote.peso_total_kg, 0)
  const pesoTotalProdutos = produtosFiltrados.value.reduce((sum, produto) => sum + produto.peso_kg, 0)
  const valorTotalProdutos = produtosFiltrados.value.reduce((sum, produto) => sum + (produto.peso_kg * produto.preco_kg), 0)
  
  return {
    totalLotes,
    totalProdutos,
    totalAves,
    pesoTotalLotes,
    pesoTotalProdutos,
    valorTotalProdutos,
    mediaAvesPorLote: totalLotes > 0 ? totalAves / totalLotes : 0,
    mediaPesoPorLote: totalLotes > 0 ? pesoTotalLotes / totalLotes : 0,
    precoMedioKg: pesoTotalProdutos > 0 ? valorTotalProdutos / pesoTotalProdutos : 0
  }
})

// Métodos
const loadData = async () => {
  try {
    loading.value = true
    error.value = ''
    
    const [lotesResponse, produtosResponse] = await Promise.all([
      getLotesAbate(),
      getProdutos()
    ])
    
    lotes.value = lotesResponse
    produtos.value = produtosResponse
  } catch (err) {
    error.value = 'Erro ao carregar dados para relatórios'
    console.error('Erro ao carregar dados:', err)
  } finally {
    loading.value = false
  }
}

const limparFiltros = () => {
  filtros.value = {
    dataInicio: '',
    dataFim: '',
    unidade: '',
    tipoRelatorio: 'lotes'
  }
}

const exportarCSV = () => {
  let dados: any[] = []
  let headers: string[] = []
  
  if (filtros.value.tipoRelatorio === 'lotes') {
    headers = ['Data Abate', 'Unidade', 'Tipo Ave', 'Quantidade Aves', 'Peso Total (kg)']
    dados = lotesFiltrados.value.map(lote => [
      formatDate(lote.data_abate),
      lote.unidade,
      lote.tipo_ave || 'N/A',
      lote.quantidade_aves,
      lote.peso_total_kg
    ])
  } else if (filtros.value.tipoRelatorio === 'produtos') {
    headers = ['Nome', 'Tipo', 'Unidade Origem', 'Data Produção', 'Peso (kg)', 'Preço/kg', 'Valor Total']
    dados = produtosFiltrados.value.map(produto => [
      produto.nome,
      produto.tipo,
      produto.unidade_origem,
      formatDate(produto.data_producao),
      produto.peso_kg,
      produto.preco_kg,
      produto.peso_kg * produto.preco_kg
    ])
  } else {
    headers = ['Unidade', 'Total Lotes', 'Total Aves', 'Peso Total (kg)', 'Total Produtos', 'Valor Produtos (R$)']
    dados = relatorioResumo.value.map(item => [
      item.unidade,
      item.totalLotes,
      item.totalAves,
      item.pesoTotal,
      item.produtos,
      item.valorProdutos
    ])
  }
  
  const csvContent = [headers, ...dados]
    .map(row => row.map(cell => `"${cell}"`).join(','))
    .join('\n')
  
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  const url = URL.createObjectURL(blob)
  link.setAttribute('href', url)
  link.setAttribute('download', `relatorio_${filtros.value.tipoRelatorio}_${new Date().toISOString().split('T')[0]}.csv`)
  link.style.visibility = 'hidden'
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

// Formatação
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

// Lifecycle
onMounted(() => {
  loadData()
  
  // Definir datas padrão (último mês)
  const hoje = new Date()
  const umMesAtras = new Date(hoje.getFullYear(), hoje.getMonth() - 1, hoje.getDate())
  
  filtros.value.dataInicio = umMesAtras.toISOString().split('T')[0]
  filtros.value.dataFim = hoje.toISOString().split('T')[0]
})
</script>

<template>
  <div class="relatorios-container">
    <div class="relatorios-header">
      <h2 class="relatorios-title">Relatórios</h2>
      <div class="header-actions">
        <button @click="loadData" class="btn btn-secondary btn-sm" :disabled="loading">
          <span class="btn-icon">🔄</span>
          {{ loading ? 'Atualizando...' : 'Atualizar' }}
        </button>
        <button @click="exportarCSV" class="btn btn-primary btn-sm" :disabled="loading">
          <span class="btn-icon">📊</span>
          Exportar CSV
        </button>
      </div>
    </div>

    <!-- Filtros -->
    <section class="filtros-section">
      <h3 class="section-title">Filtros</h3>
      <div class="filtros-grid">
        <div class="filtro-group">
          <label class="filtro-label">Tipo de Relatório</label>
          <select v-model="filtros.tipoRelatorio" class="filtro-input">
            <option value="lotes">Abates</option>
            <option value="produtos">Produtos/Cortes</option>
            <option value="resumo">Resumo por Unidade</option>
          </select>
        </div>
        
        <div class="filtro-group">
          <label class="filtro-label">Data Início</label>
          <input 
            v-model="filtros.dataInicio" 
            type="date" 
            class="filtro-input"
          />
        </div>
        
        <div class="filtro-group">
          <label class="filtro-label">Data Fim</label>
          <input 
            v-model="filtros.dataFim" 
            type="date" 
            class="filtro-input"
          />
        </div>
        
        <div class="filtro-group">
          <label class="filtro-label">Unidade</label>
          <select v-model="filtros.unidade" class="filtro-input">
            <option value="">Todas as unidades</option>
            <option v-for="unidade in unidadesDisponiveis" :key="unidade" :value="unidade">
              {{ unidade }}
            </option>
          </select>
        </div>
        
        <div class="filtro-actions">
          <button @click="limparFiltros" class="btn btn-outline btn-sm">
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
      Carregando relatórios...
    </div>

    <!-- Conteúdo dos Relatórios -->
    <div v-else class="relatorios-content">
      <!-- Totais Gerais -->
      <section class="totais-section">
        <h3 class="section-title">Totais do Período</h3>
        <div class="totais-grid">
          <div class="total-card">
            <div class="total-icon">📊</div>
            <div class="total-content">
              <div class="total-value">{{ formatNumber(totaisGerais.totalLotes) }}</div>
              <div class="total-label">Lotes</div>
            </div>
          </div>
          
          <div class="total-card">
            <div class="total-icon">🐔</div>
            <div class="total-content">
              <div class="total-value">{{ formatNumber(totaisGerais.totalAves) }}</div>
              <div class="total-label">Aves</div>
            </div>
          </div>
          
          <div class="total-card">
            <div class="total-icon">⚖️</div>
            <div class="total-content">
              <div class="total-value">{{ formatWeight(totaisGerais.pesoTotalLotes) }}</div>
              <div class="total-label">Peso (Lotes)</div>
            </div>
          </div>
          
          <div class="total-card">
            <div class="total-icon">🥩</div>
            <div class="total-content">
              <div class="total-value">{{ formatNumber(totaisGerais.totalProdutos) }}</div>
              <div class="total-label">Produtos</div>
            </div>
          </div>
          
          <div class="total-card">
            <div class="total-icon">💰</div>
            <div class="total-content">
              <div class="total-value">{{ formatCurrency(totaisGerais.valorTotalProdutos) }}</div>
              <div class="total-label">Valor Total</div>
            </div>
          </div>
        </div>
      </section>

      <!-- Relatório de Lotes -->
      <section v-if="filtros.tipoRelatorio === 'lotes'" class="tabela-section">
        <h3 class="section-title">Abates ({{ lotesFiltrados.length }} registros)</h3>
        <div class="tabela-container">
          <table class="tabela">
            <thead>
              <tr>
                <th>Data Abate</th>
                <th>Unidade</th>
                <th>Tipo Ave</th>
                <th>Quantidade Aves</th>
                <th>Peso Total</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="lotesFiltrados.length === 0">
                <td colspan="5" class="no-data">Nenhum lote encontrado para os filtros selecionados</td>
              </tr>
              <tr v-for="lote in lotesFiltrados" :key="lote.id">
                <td>{{ formatDate(lote.data_abate) }}</td>
                <td>{{ lote.unidade }}</td>
                <td>{{ lote.tipo_ave || 'N/A' }}</td>
                <td class="text-right">{{ formatNumber(lote.quantidade_aves) }}</td>
                <td class="text-right">{{ formatWeight(lote.peso_total_kg) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- Relatório de Produtos -->
      <section v-if="filtros.tipoRelatorio === 'produtos'" class="tabela-section">
        <h3 class="section-title">Produtos/Cortes ({{ produtosFiltrados.length }} registros)</h3>
        <div class="tabela-container">
          <table class="tabela">
            <thead>
              <tr>
                <th>Nome</th>
                <th>Tipo</th>
                <th>Unidade Origem</th>
                <th>Data Produção</th>
                <th>Peso</th>
                <th>Preço/kg</th>
                <th>Valor Total</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="produtosFiltrados.length === 0">
                <td colspan="7" class="no-data">Nenhum produto encontrado para os filtros selecionados</td>
              </tr>
              <tr v-for="produto in produtosFiltrados" :key="produto._id">
                <td>{{ produto.nome }}</td>
                <td>{{ produto.tipo }}</td>
                <td>{{ produto.unidade_origem }}</td>
                <td>{{ formatDate(produto.data_producao) }}</td>
                <td class="text-right">{{ formatWeight(produto.peso_kg) }}</td>
                <td class="text-right">{{ formatCurrency(produto.preco_kg) }}</td>
                <td class="text-right primary">{{ formatCurrency(produto.peso_kg * produto.preco_kg) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- Relatório de Resumo -->
      <section v-if="filtros.tipoRelatorio === 'resumo'" class="tabela-section">
        <h3 class="section-title">Resumo por Unidade ({{ relatorioResumo.length }} unidades)</h3>
        <div class="tabela-container">
          <table class="tabela">
            <thead>
              <tr>
                <th>Unidade</th>
                <th>Total Lotes</th>
                <th>Total Aves</th>
                <th>Peso Total (kg)</th>
                <th>Média Aves/Lote</th>
                <th>Média Peso/Lote</th>
                <th>Total Produtos</th>
                <th>Valor Produtos</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="relatorioResumo.length === 0">
                <td colspan="8" class="no-data">Nenhuma unidade encontrada para os filtros selecionados</td>
              </tr>
              <tr v-for="item in relatorioResumo" :key="item.unidade">
                <td class="font-weight-bold">{{ item.unidade }}</td>
                <td class="text-right">{{ formatNumber(item.totalLotes) }}</td>
                <td class="text-right">{{ formatNumber(item.totalAves) }}</td>
                <td class="text-right">{{ formatWeight(item.pesoTotal) }}</td>
                <td class="text-right">{{ formatNumber(item.mediaAvesPorLote) }}</td>
                <td class="text-right">{{ formatWeight(item.mediaPesoPorLote) }}</td>
                <td class="text-right">{{ formatNumber(item.produtos) }}</td>
                <td class="text-right primary">{{ formatCurrency(item.valorProdutos) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </div>
  </div>
</template>

<style scoped>
@import url('../styles/colors.css');

.relatorios-container {
  max-width: 100%;
  margin: 0 auto;
  padding: 0;
.relatorios-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: var(--bg-secondary);
  border-radius: 16px;
  box-shadow: var(--shadow-light);
  border: 1px solid var(--border-light);
} padding-bottom: 1rem;
  border-bottom: 2px solid var(--border-light);
}

.relatorios-title {
  font-size: 2rem;
  font-weight: 700;
  margin: 0;
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.header-actions {
  display: flex;
  gap: 0.75rem;
}

.relatorios-content {
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

/* Filtros */
.filtros-section {
  background: var(--bg-secondary);
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: var(--shadow-light);
}

.filtros-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  align-items: end;
}

.filtro-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filtro-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-primary);
}

.filtro-input {
  padding: 0.75rem;
  border: 1px solid var(--border-light);
  border-radius: 8px;
  background: var(--bg-primary);
  color: var(--text-primary);
  font-size: 0.875rem;
  transition: all 0.3s ease;
}

.filtro-input:focus {
  outline: none;
  border-color: var(--primary-red);
  box-shadow: 0 0 0 3px rgba(220, 38, 38, 0.1);
}

.filtro-actions {
  display: flex;
  align-items: flex-end;
}

/* Totais */
.totais-section {
  background: var(--bg-secondary);
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: var(--shadow-light);
}

.totais-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.total-card {
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

.total-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-medium);
  border-left-color: var(--accent-red);
  border-left-width: 6px;
}

.total-icon {
  font-size: 1.5rem;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  background: var(--bg-accent);
}

.total-content {
  flex: 1;
}

.total-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1;
  margin-bottom: 0.25rem;
}

.total-label {
  font-size: 0.75rem;
  color: var(--text-secondary);
  font-weight: 500;
}

/* Tabelas */
.tabela-section {
  background: var(--bg-secondary);
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: var(--shadow-light);
}

.tabela-container {
  overflow-x: auto;
  border-radius: 8px;
  border: 2px solid var(--border-light);
  border-top: 4px solid var(--primary-red);
}

.tabela {
  width: 100%;
  border-collapse: collapse;
  background: var(--bg-primary);
}

.tabela th {
  background: var(--gradient-primary);
  color: white;
  font-weight: 600;
  padding: 1rem;
  text-align: left;
  border-bottom: 2px solid var(--border-light);
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.tabela td {
  padding: 0.875rem 1rem;
  border-bottom: 1px solid var(--border-light);
  color: var(--text-primary);
  font-size: 0.875rem;
}

.tabela tbody tr:hover {
  background: var(--bg-accent);
}

.text-right {
  text-align: right;
}

.font-weight-bold {
  font-weight: 600;
}

.primary {
  color: var(--primary-red);
  font-weight: 600;
}

.no-data {
  text-align: center;
  color: var(--text-secondary);
  font-style: italic;
  padding: 2rem;
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

/* Responsividade */
@media (max-width: 1024px) {
  .filtros-grid {
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  }
  
  .totais-grid {
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  }
}

@media (max-width: 768px) {
  .relatorios-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .header-actions {
    justify-content: center;
  }
  
  .filtros-grid {
    grid-template-columns: 1fr;
  }
  
  .totais-grid {
    grid-template-columns: 1fr;
  }
  
  .tabela-container {
    font-size: 0.75rem;
  }
  
  .tabela th,
  .tabela td {
    padding: 0.5rem;
  }
}

@media (max-width: 480px) {
  .relatorios-container {
    padding: 0.5rem;
  }
  
  .relatorios-title {
    font-size: 1.5rem;
  }
  
  .total-card {
    padding: 1rem;
  }
  
  .total-icon {
    width: 40px;
    height: 40px;
    font-size: 1.25rem;
  }
  
  .total-value {
    font-size: 1.25rem;
  }
}
</style>